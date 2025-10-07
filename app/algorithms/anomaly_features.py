from typing import List, Dict, Any

def ngap_rules(evts: List[Dict[str, Any]], abnormal_proc: List[str]) -> List[str]:
    anomalies = []
    for e in evts:
        if e.get('procedure') in abnormal_proc or e.get('outcome') == 'FAIL':
            anomalies.append(f"NGAP:{e.get('procedure')}:{e.get('outcome')}")
    return anomalies

def pfcp_rules(evts: List[Dict, Any], rate_threshold: int) -> List[str]:
    # Simple rate-based detection
    count = len(evts)
    return [f'PFCP_HIGH_RATE:{count}'] if count > rate_threshold else []

def http2_rules(evts: List[Dict[str, Any]], burst_threshold: int) -> List[str]:
    # Simple burst detection by count in window
    count = len(evts)
    return [f'HTTP2_BURST:{count}'] if count > burst_threshold else []
