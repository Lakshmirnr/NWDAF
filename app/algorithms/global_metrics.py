from typing import Dict, Any, List, Tuple
from collections import Counter
import numpy as np

def _count_messages(window: Dict[str, List[dict]]) -> int:
    return sum(len(v) for v in window.values())

def te_signaling_overload(window: Dict[str, List[dict]], mu: float, sigma: float) -> Tuple[float, float]:
    # Compute global signaling overload exposure (z-like, clamped at 0) and raw count
    m = _count_messages(window)
    if sigma <= 0:
        return 0.0, float(m)
    z = (m - mu) / sigma
    return float(max(0.0, z)), float(m)

def te_session_failure_ratio(window: Dict[str, List[dict]], lam: float, prev_tes: float) -> Tuple[float, float]:
    # Use SBI HTTP status codes as failure proxy: (>=500 or 429) => fail
    sbi = window.get("SBI", [])
    if not sbi:
        return prev_tes, 0.0
    total = len(sbi)
    fails = sum(1 for e in sbi if isinstance(e.get("status"), int) and (e["status"] >= 500 or e["status"] == 429))
    ratio = fails / total if total else 0.0
    tes = lam * prev_tes + (1.0 - lam) * ratio
    return float(tes), float(ratio)

def _bin_times(events: List[dict], bin_sec: int):
    # Bin timestamps into counts per bin
    if not events:
        return np.array([]), np.array([])
    import datetime
    def parse(ts: str) -> float:
        try:
            return datetime.datetime.fromisoformat(ts.replace("Z","")).timestamp()
        except Exception:
            return 0.0
    times = np.array([parse(e.get("ts","0")) for e in events], dtype=float)
    t0 = float(times[0]) if len(times) else 0.0
    idx = np.floor((times - t0) / max(1, bin_sec)).astype(int)
    if len(idx)==0: 
        return np.array([]), np.array([])
    max_idx = int(idx.max())
    series = np.zeros(max_idx+1, dtype=float)
    for i in idx:
        if 0 <= i < len(series):
            series[i] += 1.0
    return np.arange(len(series)), series

def ctci(window: Dict[str, List[dict]], pairs: List[Tuple[str,str]], bin_seconds: int = 1) -> float:
    # Average Pearson correlation across interface pairs over binned counts
    vals = []
    for a,b in pairs:
        ea, eb = window.get(a, []), window.get(b, [])
        _, sa = _bin_times(ea, bin_seconds)
        _, sb = _bin_times(eb, bin_seconds)
        if len(sa)==0 or len(sb)==0:
            vals.append(0.0)
            continue
        L = min(len(sa), len(sb))
        sa, sb = sa[:L], sb[:L]
        if np.std(sa)==0 or np.std(sb)==0:
            vals.append(0.0)
            continue
        corr = float(np.corrcoef(sa, sb)[0,1])
        vals.append(max(0.0, corr))
    return float(np.mean(vals)) if vals else 0.0

def psds(window: Dict[str, List[dict]], grammar: Dict[str, List[str]]) -> float:
    # Protocol Semantic Deviation Score using set-difference ratios
    n2 = window.get("N2", [])
    seen_proc = {e.get("procedure") for e in n2 if e.get("procedure")}
    g_proc = set(grammar.get("N2_procedures", []))
    dev_proc = len([p for p in seen_proc if p not in g_proc])
    denom_proc = max(1, len(g_proc))
    r_proc = dev_proc/denom_proc

    sbi = window.get("SBI", [])
    seen_paths = {e.get("path") for e in sbi if e.get("path")}
    g_paths = set(grammar.get("SBI_paths", []))
    dev_paths = len([p for p in seen_paths if p not in g_paths])
    denom_paths = max(1, len(g_paths))
    r_paths = dev_paths/denom_paths
    return float((r_proc + r_paths)/2.0)

def dube(window: Dict[str, List[dict]], baseline: float):
    # Deviation of Behavioral Entropy vs baseline (bits)
    labels = []
    for e in window.get("N2", []):
        if e.get("procedure"): labels.append(("N2", e["procedure"]))
    for e in window.get("N4", []):
        if e.get("msg_type"): labels.append(("N4", e["msg_type"]))
    for e in window.get("SBI", []):
        if e.get("path"): labels.append(("SBI", e["path"]))
    if not labels:
        return 0.0, 0.0
    cnt = Counter(labels)
    total = sum(cnt.values())
    ps = [c/total for c in cnt.values()]
    import math
    H = -sum(p*math.log(p,2) for p in ps if p>0)
    dev = abs(H - baseline)
    return float(dev), float(H)
