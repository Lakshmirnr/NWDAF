from typing import Dict
def aggregate(weights: Dict[str, float], te_sig: float, tes: float, ctci: float, psds: float, dube: float) -> float:
    w1 = float(weights.get("w1", 0.25))
    w2 = float(weights.get("w2", 0.20))
    w3 = float(weights.get("w3", 0.20))
    w4 = float(weights.get("w4", 0.20))
    w5 = float(weights.get("w5", 0.15))
    score = 100.0 * (w1*min(1.0, te_sig) + w2*min(1.0, tes) + w3*min(1.0, ctci) + w4*min(1.0, psds) + w5*min(1.0, dube))
    return max(0.0, min(100.0, float(score)))
