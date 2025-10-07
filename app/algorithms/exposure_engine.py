from typing import Dict, Any, List
from .entropy_metrics import shannon_entropy, numeric_entropy

class ExposureEngine:
    def __init__(self, weights: Dict[str, float], clamp_min: float, clamp_max: float, entropy_bins: int):
        self.weights = weights
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max
        self.entropy_bins = entropy_bins

    def compute(self, nf: str, window: Dict[str, Any], anomalies: List[str]) -> Dict[str, Any]:
        # Entropy of categorical procedures and HTTP paths; latency numeric entropy
        ngap_proc = [e.get('procedure') for e in window.get('N2', []) if e.get('procedure')]
        http_paths = [e.get('path') for e in window.get('SBI', []) if e.get('path')]
        lat_vals  = [e.get('lat_ms') for e in window.get('SBI', []) if isinstance(e.get('lat_ms'), (int,float))]

        ent_cat = (shannon_entropy(ngap_proc) + shannon_entropy(http_paths)) / 2.0
        ent_num = numeric_entropy(lat_vals, bins=self.entropy_bins)
        ent = (ent_cat + ent_num) / 2.0

        # Normalize rough anomaly strength
        anom_strength = min(len(anomalies)/10.0, 1.0)

        score = self.weights.get('anomalies', 0.6) * (anom_strength*100.0) + \                self.weights.get('entropy', 0.4) * (min(ent,1.0)*100.0)

        score = max(self.clamp_min, min(self.clamp_max, score))
        return {'nf': nf, 'score': score, 'ent_cat': ent_cat, 'ent_num': ent_num, 'anom_count': len(anomalies)}
