from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class IngestEvent(BaseModel):
    interface: str             # 'N2','N4','SBI'
    payload: Dict[str, Any]

class ExposureScore(BaseModel):
    nf: str
    score: float
    details: Dict[str, Any]

class ReportRecord(BaseModel):
    ts: str
    nf: str
    interface: str
    anomalies: List[str]
    exposure: float
    actions: List[str]
    context: Dict[str, Any] = {}
