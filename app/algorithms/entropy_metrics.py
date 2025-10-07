import numpy as np
from typing import List, Dict, Any

def shannon_entropy(values: List[Any]) -> float:
    if not values:
        return 0.0
    vals, counts = np.unique(values, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)))

def numeric_entropy(values: List[float], bins: int = 10) -> float:
    if not values:
        return 0.0
    hist, _ = np.histogram(values, bins=bins)
    p = hist / hist.sum() if hist.sum() else np.zeros_like(hist, dtype=float)
    nonzero = p[p > 0]
    return float(-np.sum(nonzero * np.log2(nonzero)))
