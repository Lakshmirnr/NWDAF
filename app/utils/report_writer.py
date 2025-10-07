import os, json
from datetime import datetime

class ReportWriter:
    def __init__(self, reports_dir: str):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)
        self.filepath = os.path.join(self.reports_dir, 'security_reports.jsonl')

    def write(self, record: dict):
        record = dict(record)
        record.setdefault('ts', datetime.utcnow().isoformat()+'Z')
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
