from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

import yaml


class DecisionEngine:
    def __init__(self, cfg: dict, risk_manager: Any) -> None:
        self.cfg = cfg
        self.risk = risk_manager

    @staticmethod
    def _valid_proba(proba):
        if not isinstance(proba, (list, tuple)) or len(proba) != 3:
            return False
        for p in proba:
            if not isinstance(p, (int, float)) or not math.isfinite(p):
                return False
            if p < 0 or p > 1:
                return False
        if abs(sum(proba) - 1.0) > 1e-6:
            return False
        return True

    def decide(self, ensemble_proba, timeframe_signals: dict, risk_inputs: dict, model_version: str | None = None) -> dict:
        ts = datetime.now(timezone.utc).isoformat()
        mv = model_version or self.cfg.get("model_version", "unknown")
        base = {
            "timestamp": ts,
            "model_version": mv,
            "probabilities": list(ensemble_proba) if isinstance(ensemble_proba, (list, tuple)) else None,
            "timeframes_used": list(timeframe_signals.keys()) if timeframe_signals else [],
            "indicators": timeframe_signals or {},
        }

        if not self._valid_proba(ensemble_proba):
            return {**base, "action": "HOLD", "reason": "invalid probabilities", "risk_result": None}

        # data freshness
        if not risk_inputs.get("data_fresh", False) or not risk_inputs.get("enough_data", False):
            return {**base, "action": "HOLD", "reason": "stale or insufficient data", "risk_result": None}

        p_down, p_side, p_up = ensemble_proba[0], ensemble_proba[1], ensemble_proba[2]

        # multi-timeframe conflict detection
        weights = self.cfg.get("timeframe_weights", {})
        weighted_up = 0.0
        weighted_down = 0.0
        total_w = 0.0
        conflicts = 0
        dirs = []
        for tf, sig in (timeframe_signals or {}).items():
            w = weights.get(tf, 0.0)
            d = sig.get("direction", 0) if isinstance(sig, dict) else 0
            dirs.append(d)
            if d > 0:
                weighted_up += w
            elif d < 0:
                weighted_down += w
            total_w += w
        if any(d > 0 for d in dirs) and any(d < 0 for d in dirs):
            conflicts = 1
        penalty = self.cfg.get("conflict_penalty", 0.1) if conflicts else 0.0

        long_thr = self.cfg.get("long_threshold", 0.55)
        short_thr = self.cfg.get("short_threshold", 0.55)
        unc_thr = self.cfg.get("uncertainty_threshold", 0.5)

        if max(ensemble_proba) < unc_thr:
            return {**base, "action": "HOLD", "reason": "high uncertainty", "risk_result": None}

        action = "HOLD"
        reason = "no clear signal"
        if p_up >= long_thr and weighted_up >= weighted_down and conflicts == 0:
            action = "LONG_SIMULATED"
            reason = "bullish ensemble and timeframe agreement"
        elif p_down >= short_thr and weighted_down >= weighted_up and conflicts == 0:
            action = "SHORT_SIMULATED"
            reason = "bearish ensemble and timeframe agreement"
        else:
            if conflicts:
                reason = "timeframe conflict"
            elif p_up >= long_thr or p_down >= short_thr:
                reason = "insufficient timeframe confirmation"

        if action != "HOLD":
            approved, rreason = self.risk.approve(
                list(ensemble_proba),
                risk_inputs.get("volatility", 0.0),
                risk_inputs.get("price", 0.0),
                risk_inputs.get("atr", 0.0),
                risk_inputs.get("data_fresh", False),
                risk_inputs.get("enough_data", False),
            )
            if not approved:
                action = "HOLD"
                reason = f"risk rejected: {rreason}"
            base["risk_result"] = {"approved": approved, "reason": rreason}
        else:
            base["risk_result"] = None

        base["action"] = action
        base["reason"] = reason
        return base
