"""Machine learning subpackage."""

from .dataset import build_dataset
from .ensemble import ensemble_proba, predict_with_abstention
from .labels import make_labels
from .pipeline import gpu_available, run_training

__all__ = [
    "build_dataset",
    "ensemble_proba",
    "gpu_available",
    "make_labels",
    "predict_with_abstention",
    "run_training",
]
