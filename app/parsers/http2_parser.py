import json
from typing import Dict, Any

# Minimal HTTP/2 SBI record example as JSON per line:
# {"ts":"2025-10-07T10:32:13Z","src_nf":"AMF1","dst_nf":"PCF1","path":"/nudm-sdm/v2","method":"GET","status":200,"lat_ms":22}

def parse_line(line: str) -> Dict[str, Any]:
    try:
        obj = json.loads(line)
        return obj
    except Exception:
        return {}
