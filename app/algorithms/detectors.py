from typing import Dict, Any, List
from .anomaly_features import ngap_rules, pfcp_rules, http2_rules

def run_detectors(window: Dict[str, Any], cfg: Dict[str, Any]) -> List[str]:
    anomalies = []
    anomalies += ngap_rules(window.get('N2', []), cfg['analysis']['ngap_abnormal_procedures'])
    anomalies += pfcp_rules(window.get('N4', []), cfg['analysis']['pfcp_rate_threshold_per_min'])
    anomalies += http2_rules(window.get('SBI', []), cfg['analysis']['http2_burst_threshold'])
    return anomalies
