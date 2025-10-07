from typing import Dict, Any

# Minimal NGAP line example (CSV-like):
# ts,amf,ran,procedure,outcome,ue_id
# 2025-10-07T10:32:11Z,AMF1,gNB-23,INITIAL_CONTEXT_SETUP,OK,imsi-00101

def parse_line(line: str) -> Dict[str, Any]:
    parts = [p.strip() for p in line.split(',')]
    if len(parts) < 6:
        return {}
    ts, amf, ran, procedure, outcome, ue = parts[:6]
    return {
        'ts': ts, 'amf': amf, 'ran': ran,
        'procedure': procedure, 'outcome': outcome, 'ue': ue
    }
