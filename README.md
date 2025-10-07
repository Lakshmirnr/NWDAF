**5G Control-Plane Security Monitoring Framework**

**Description**

A real-time security monitoring framework for 5G Core networks, built on Open5GS. It analyzes key control-plane interfaces (N1, N2, N4, and SBI) using custom parsers for NGAP, PFCP, and HTTP/2, detecting session manipulation, signaling misuse, and other anomalies.

**Features**

Monitors N1 (NAS), N2 (NGAP), N4 (PFCP), and SBI (HTTP/2) interfaces in real time

Modular security exposure evaluation architecture with dynamic threat scoring

Generates structured, timestamped security reports

Automatic mitigation via SMF, PCF, and NSSF interfaces

Supports temporal threat analysis and enhanced network-wide monitoring

**Requirements**

Open5GS 5G Core

Python 3.8+

UERANSIM

**Installation**

git clone https://github.com/username/5g-nwdaf-security-monitor.git
cd 5g-nwdaf-security-monitor
pip install -r requirements.txt


**Usage**

python nwdaf_monitor.py


Real-time monitoring

Reports saved in /reports

Automatic enforcement actions


**References**

Open5GS

3GPP TS 23.501, TS 23.502, TS 33.502
