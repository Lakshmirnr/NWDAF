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


### **Step 1: Clone the Repository**

```bash
git clone https://github.com/Lakshmirnr/NWDAF.git
cd NWDAF
````

---

### **Step 2: Set Up a Python Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate     # For Linux/Mac
venv\Scripts\activate        # For Windows
```

---

### **Step 3: Install Required Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### **Step 4: Configure Environment Variables**

```bash
cp .env.example .env
nano .env
```

Or set variables directly:

```bash
export NWDAF_DB_URL="mongodb://localhost:27017/nwdaf"
export NWDAF_PORT=8080
```

---

### **Step 5: Initialize Database (If Required)**

Make sure your database service (e.g., MongoDB) is running:

```bash
sudo systemctl start mongod
```

---

### **Step 6: Run NWDAF Service**

```bash
python main.py
```

Or, if a startup script is available:

```bash
./run.sh
```

---

### **Step 7: Verify Installation**

Check if the NWDAF service is active:

```bash
curl http://localhost:8080/nwdaf
```

Expected output:

```bash
{"status": "NWDAF running successfully"}
```


**Usage**

python nwdaf_monitor.py


Real-time monitoring

Reports saved in /reports

Automatic enforcement actions


**References**

Open5GS

3GPP TS 23.501, TS 23.502, TS 33.502

**License**

   Copyright © 2025 Lakshmi R Nair
   
   Copyright © 2025 Preetam Mukherjee
   
   Copyright © 2025 Adithya Anil

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at


       http://www.apache.org/licenses/LICENSE-2.0
