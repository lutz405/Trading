from __future__ import annotations

import math


def compute_metrics(engine) -> dict:
    trades = engine.trades
    equity = engine.equity
    if not equity:
        return {}
    total_return = (equity[-1] - engine.initial_capital) / engine.initial_capital
    # sharpe/sortino on equity returns
    rets = [ (equity[i]-equity[i-1])/equity[i-1] for i in range(1, len(equity)) if equity[i-1] != 0]
    if rets:
        mean = sum(rets)/len(rets)
        var = sum((r-mean)**2 for r in rets)/len(rets)
        std = math.sqrt(var) if var > 0 else 0.0
        sharpe = (mean/std*math.sqrt(252)) if std > 0 else 0.0
        downside = [r for r in rets if r < 0]
        if downside:
            dvar = sum(r*r for r in downside)/len(downside)
            dstd = math.sqrt(dvar)
            sortino = (mean/dstd*math.sqrt(252)) if dstd > 0 else 0.0
        else:
            sortino = float("inf") if mean > 0 else 0.0
    else:
        sharpe = 0.0
        sortino = 0.0
    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    win_rate = len(wins)/len(trades) if trades else 0.0
    gross_profit = sum(t.pnl for t in wins)
    gross_loss = abs(sum(t.pnl for t in losses))
    profit_factor = gross_profit/gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)
    avg_trade = sum(t.pnl for t in trades)/len(trades) if trades else 0.0
    exposure = len(trades) / len(equity) if equity else 0.0
    total_fees = sum(t.fees for t in trades)
    total_slip = sum(t.slippage for t in trades)
    return {
        "net_return": total_return,
        "gross_return": (equity[-1]/engine.initial_capital - 1) + (total_fees/engine.initial_capital),
        "max_drawdown": engine.max_dd,
        "sharpe": sharpe,
        "sortino": sortino,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_trade_return": avg_trade,
        "total_trades": len(trades),
        "exposure": exposure,
        "total_fees": total_fees,
        "total_slippage": total_slip,
    }
