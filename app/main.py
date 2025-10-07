import os, yaml, asyncio, logging, json
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
from app.utils.logging_conf import setup_logging
from app.utils.report_writer import ReportWriter
from app.parsers import ngap_parser, pfcp_parser, http2_parser
from app.algorithms.detectors import run_detectors
from app.algorithms.exposure_engine import ExposureEngine
from app.algorithms.global_metrics import te_signaling_overload, te_session_failure_ratio, ctci, psds, dube
from app.algorithms.composite_exposure import aggregate as aggregate_exposure

TES_PREV = 0.0  # global TES memory

from datetime import datetime

app = FastAPI(title='NWDAF-Secure')
CFG: Dict[str, Any] = {}
WINDOW: Dict[str, List[Dict[str, Any]]] = {'N2': [], 'N4': [], 'SBI': []}
NF_DEFAULT = 'AMF1'  # simplified mapping for demo
REPORTER: ReportWriter = None
ENGINE: ExposureEngine = None
LOG = setup_logging()

def load_cfg():
    global CFG, REPORTER, ENGINE
    with open('config.yaml', 'r') as f:
        CFG = yaml.safe_load(f)
    REPORTER = ReportWriter(CFG['paths']['reports_dir'])
    ENGINE = ExposureEngine(
        weights=CFG['exposure']['weights'],
        clamp_min=CFG['exposure']['clamp_min'],
        clamp_max=CFG['exposure']['clamp_max'],
        entropy_bins=CFG['analysis']['entropy_numeric_bins']
    )
    LOG.info('Configuration loaded.')

@app.on_event('startup')
async def startup():
    load_cfg()
    os.makedirs(CFG['paths']['reports_dir'], exist_ok=True)
    LOG.info('NWDAF-Secure started.')

@app.post('/ingest')
async def ingest(event: Dict[str, Any] = Body(...)):
    iface = event.get('interface')
    payload = event.get('payload', {})
    if iface not in WINDOW:
        return JSONResponse({'error': 'invalid interface'}, status_code=400)
    WINDOW[iface].append(payload)
    # keep a rolling window
    maxw = CFG['analysis']['window_size']
    if len(WINDOW[iface]) > maxw:
        WINDOW[iface] = WINDOW[iface][-maxw:]
    return {'status': 'ok', 'counts': {k: len(v) for k,v in WINDOW.items()}}

@app.post('/analyze')
async def analyze():
    anomalies = run_detectors(WINDOW, CFG)
    exp = ENGINE.compute(NF_DEFAULT, WINDOW, anomalies)
    # simple policy: if exposure > 70, add actions
    actions = []
    if exp['score'] > 85:
        actions.append('BLOCK_SESSIONS')
    elif exp['score'] > 70:
        actions.append('RATE_LIMIT')

    record = {
        'ts': datetime.utcnow().isoformat()+'Z',
        'nf': NF_DEFAULT,
        'interface': 'MULTI',
        'anomalies': anomalies,
        'exposure': exp['score'],
        'actions': actions,
        'context': {'window_counts': {k: len(v) for k,v in WINDOW.items()}, 'entropy': {'cat': exp['ent_cat'], 'num': exp['ent_num']}}
    }
    REPORTER.write(record)
    return record

@app.get('/exposure')
async def exposure():
    anomalies = run_detectors(WINDOW, CFG)
    exp = ENGINE.compute(NF_DEFAULT, WINDOW, anomalies)
    return exp

@app.post('/ingest_files')
async def ingest_files():
    """Ingest all sample trace files from configured data_dir."""
    data_dir = CFG['paths']['data_dir']
    # NGAP
    with open(os.path.join(data_dir, 'n2_ngap.log'), 'r', encoding='utf-8') as f:
        for line in f:
            obj = ngap_parser.parse_line(line.strip())
            if obj: WINDOW['N2'].append(obj)
    # PFCP
    with open(os.path.join(data_dir, 'n4_pfcp.log'), 'r', encoding='utf-8') as f:
        for line in f:
            obj = pfcp_parser.parse_line(line.strip())
            if obj: WINDOW['N4'].append(obj)
    # HTTP2
    with open(os.path.join(data_dir, 'sbi_http2.jsonl'), 'r', encoding='utf-8') as f:
        for line in f:
            obj = http2_parser.parse_line(line.strip())
            if obj: WINDOW['SBI'].append(obj)
    # trim to window size
    maxw = CFG['analysis']['window_size']
    for k in WINDOW:
        WINDOW[k] = WINDOW[k][-maxw:]
    return {'status': 'ok', 'counts': {k: len(v) for k,v in WINDOW.items()}}


@app.post('/analyze_global')
async def analyze_global():
    global TES_PREV
    mcfg = CFG.get('metrics', {})
    # TE_sig
    sig_cfg = mcfg.get('signaling_overload', {})
    te_sig, raw_m = te_signaling_overload(WINDOW, sig_cfg.get('mu',300), sig_cfg.get('sigma',80))
    # TES
    ses_cfg = mcfg.get('session_state', {})
    TES_PREV, fail_ratio = te_session_failure_ratio(WINDOW, ses_cfg.get('lambda',0.8), TES_PREV)
    # CTCI
    tc_cfg = mcfg.get('temporal_correlation', {})
    ct = ctci(WINDOW, tc_cfg.get('pairs', [["N2","SBI"],["N4","SBI"]]), tc_cfg.get('bin_seconds',1))
    # PSDS
    ps = psds(WINDOW, mcfg.get('protocol_semantics', {}).get('grammar', {}))
    # DUBE
    d_dev, H = dube(WINDOW, mcfg.get('entropy_drift', {}).get('baseline', 1.2))
    # Composite
    score = aggregate_exposure(mcfg.get('composite_weights', {}), te_sig, TES_PREV, ct, ps, d_dev)

    thresh = mcfg.get('threshold', {})
    actions = []
    if score >= float(thresh.get('high',85)):
        actions.append('BLOCK_SESSIONS')
    elif score >= float(thresh.get('medium',70)):
        actions.append('RATE_LIMIT')

    record = {
        'ts': datetime.utcnow().isoformat()+'Z',
        'nf': NF_DEFAULT,
        'interface': 'MULTI',
        'metrics': {
            'TE_sig': te_sig, 'TES': TES_PREV, 'fail_ratio': fail_ratio,
            'CTCI': ct, 'PSDS': ps, 'DUBE': d_dev, 'H': H
        },
        'exposure': score,
        'actions': actions,
        'context': {'counts': {k: len(v) for k,v in WINDOW.items()}}
    }
    REPORTER.write(record)
    return record
