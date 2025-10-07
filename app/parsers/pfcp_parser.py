from typing import Dict, Any

# Minimal PFCP line example:
# ts,smf,upf,msg_type,seid,teid
# 2025-10-07T10:32:12Z,SMF1,UPF-A,SESSION_ESTABLISHMENT,0x9a,0x10

def parse_line(line: str) -> Dict[str, Any]:
    parts = [p.strip() for p in line.split(',')]
    if len(parts) < 6:
        return {}
    ts, smf, upf, msg_type, seid, teid = parts[:6]
    return {
        'ts': ts, 'smf': smf, 'upf': upf, 'msg_type': msg_type,
        'seid': seid, 'teid': teid
    }
