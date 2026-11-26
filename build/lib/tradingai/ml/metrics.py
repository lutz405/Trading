from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.preprocessing import label_binarize

_METRIC_EXCEPTIONS = (ValueError, TypeError, KeyError, ZeroDivisionError)


def _valid_proba(proba, n_classes):
    if proba is None:
        return False
    arr = np.asarray(proba)
    if arr.ndim != 2:
        return False
    if arr.shape[1] != n_classes:
        return False
    if not np.isfinite(arr).all():
        return False
    return not ((arr < 0).any() or (arr > 1).any())


def compute_metrics(y, proba, labels=None) -> dict:
    y = np.asarray(y)
    proba = np.asarray(proba)
    if labels is None:
        labels = sorted(set(y.tolist()))
    n_classes = proba.shape[1] if proba.ndim == 2 else 0
    out: dict[str, Any] = {}
    if not _valid_proba(proba, n_classes):
        out["error"] = "invalid probabilities"
        return out
    # roc-auc / pr-auc (binary or multiclass ovr)
    try:
        if len(set(y.tolist())) < 2:
            out["roc_auc"] = None
            out["roc_auc_reason"] = "single class present"
        elif n_classes == 2:
            out["roc_auc"] = float(roc_auc_score(y, proba[:, 1]))
        else:
            out["roc_auc"] = float(roc_auc_score(y, proba, multi_class="ovr", average="macro"))
    except _METRIC_EXCEPTIONS as exc:
        out["roc_auc"] = None
        out["roc_auc_reason"] = str(exc)
    try:
        if len(set(y.tolist())) < 2:
            out["pr_auc"] = None
            out["pr_auc_reason"] = "single class present"
        else:
            # macro average precision
            y_bin = label_binarize(y, classes=labels)
            if y_bin.shape[1] == 1 and len(labels) == 2:
                y_bin = np.hstack([1 - y_bin, y_bin])
            aps = []
            for i in range(len(labels)):
                if y_bin[:, i].sum() > 0:
                    aps.append(average_precision_score(y_bin[:, i], proba[:, i]))
            out["pr_auc"] = float(sum(aps) / len(aps)) if aps else None
    except _METRIC_EXCEPTIONS as exc:
        out["pr_auc"] = None
        out["pr_auc_reason"] = str(exc)
    # brier (macro over present classes)
    try:
        y_bin = label_binarize(y, classes=labels)
        if y_bin.shape[1] == 1 and len(labels) == 2:
            y_bin = np.hstack([1 - y_bin, y_bin])
        briers = []
        for i in range(len(labels)):
            if labels[i] in set(y.tolist()):
                briers.append(brier_score_loss(y_bin[:, i], proba[:, i]))
        out["brier"] = float(sum(briers) / len(briers)) if briers else None
    except _METRIC_EXCEPTIONS as exc:
        out["brier"] = None
        out["brier_reason"] = str(exc)
    # log loss
    try:
        out["log_loss"] = float(log_loss(y, proba, labels=labels))
    except _METRIC_EXCEPTIONS as exc:
        out["log_loss"] = None
        out["log_loss_reason"] = str(exc)
    # ECE
    try:
        out["ece"] = float(expected_calibration_error(y, proba, labels))
    except _METRIC_EXCEPTIONS as exc:
        out["ece"] = None
        out["ece_reason"] = str(exc)
    return out


def expected_calibration_error(y, proba, labels, n_bins=10):
    y = np.asarray(y)
    proba = np.asarray(proba)
    confidences = proba.max(axis=1)
    predictions = proba.argmax(axis=1)
    # map labels to indices
    label_to_idx = {lab: i for i, lab in enumerate(labels)}
    y_idx = np.array([label_to_idx[v] for v in y])
    correct = (predictions == y_idx).astype(float)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (confidences > bins[i]) & (confidences <= bins[i + 1])
        if mask.sum() == 0:
            continue
        acc = correct[mask].mean()
        conf = confidences[mask].mean()
        ece += (mask.sum() / len(y)) * abs(acc - conf)
    return float(ece)
