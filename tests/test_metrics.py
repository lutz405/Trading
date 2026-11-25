import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, log_loss

from tradingai.ml.metrics import compute_metrics, expected_calibration_error


def test_roc_auc_binary():
    y = np.array([0,0,1,1])
    proba = np.array([[0.9,0.1],[0.8,0.2],[0.3,0.7],[0.1,0.9]])
    m = compute_metrics(y, proba, labels=[0,1])
    assert abs(m["roc_auc"] - roc_auc_score(y, proba[:,1])) < 1e-9


def test_roc_auc_missing_class():
    y = np.array([0,0,0,0])
    proba = np.array([[0.9,0.1]]*4)
    m = compute_metrics(y, proba, labels=[0,1])
    assert m["roc_auc"] is None


def test_invalid_proba():
    y = np.array([0,1])
    proba = np.array([[0.5,np.nan],[0.5,0.5]])
    m = compute_metrics(y, proba, labels=[0,1])
    assert "error" in m


def test_pr_auc_binary():
    y = np.array([0,0,1,1])
    proba = np.array([[0.9,0.1],[0.8,0.2],[0.3,0.7],[0.1,0.9]])
    m = compute_metrics(y, proba, labels=[0,1])
    assert abs(m["pr_auc"] - average_precision_score(y, proba[:,1])) < 1e-9


def test_brier_binary():
    y = np.array([0,1])
    proba = np.array([[0.8,0.2],[0.3,0.7]])
    m = compute_metrics(y, proba, labels=[0,1])
    expected = (brier_score_loss(y==0, proba[:,0]) + brier_score_loss(y==1, proba[:,1]))/2
    assert abs(m["brier"] - expected) < 1e-9


def test_log_loss_binary():
    y = np.array([0,1])
    proba = np.array([[0.8,0.2],[0.3,0.7]])
    m = compute_metrics(y, proba, labels=[0,1])
    assert abs(m["log_loss"] - log_loss(y, proba, labels=[0,1])) < 1e-9


def test_ece_perfect():
    y = np.array([0,1])
    proba = np.array([[1.0,0.0],[0.0,1.0]])
    ece = expected_calibration_error(y, proba, [0,1])
    assert ece == 0.0


def test_ece_manual():
    y = np.array([0,1])
    proba = np.array([[0.8,0.2],[0.8,0.2]])
    # both predict 0 with conf 0.8; one correct one wrong -> ece = 1*|0.5-0.8|=0.3
    ece = expected_calibration_error(y, proba, [0,1])
    assert abs(ece - 0.3) < 1e-9


def test_evaluate_integration():
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from tradingai.ml.pipeline import evaluate
    X = pd.DataFrame({"a":[1,2,3,4,5,6]})
    y = pd.Series([0,0,1,1,0,1])
    model = RandomForestClassifier(n_estimators=5, random_state=0)
    model.fit(X, y)
    proba = model.predict_proba(X)
    m = evaluate(model, X, y)
    assert "roc_auc" in m
    assert "pr_auc" in m
    assert "brier" in m
    assert "log_loss" in m
    assert "ece" in m
    assert "accuracy" in m
