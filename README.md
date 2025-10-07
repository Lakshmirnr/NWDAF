# NWDAF-Secure (Prototype)

Proactive, protocol-aware threat detection and exposure assessment for 5G Core control-plane (N1/N2/N4/SBI).

**Key features**
- Real-time parsing of NGAP (N2), PFCP (N4), HTTP/2 (SBI) traces.
- Anomaly features + entropy-based metrics.
- Dynamic exposure scoring per Network Function (AMF/SMF/UPF/PCF/NSSF).
- JSONL security reports with timestamps and enforcement actions (mock SMF/PCF/NSSF).
- FastAPI service for ingestion, analytics, and reporting.

> Note: This is a **research prototype** with mock integrations and sample traces. It is designed for extendability and reproducible experiments.
