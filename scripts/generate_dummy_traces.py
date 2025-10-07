from datetime import datetime, timedelta
import json, random

now = datetime.utcnow()
with open('app/data/sample_traces/n2_ngap.log','w') as f:
    for i in range(300):
        ts = (now + timedelta(seconds=i)).isoformat()+'Z'
        proc = random.choice(['INITIAL_CONTEXT_SETUP','HANDOVER_PREP','HANDOVER_FAILURE','AUTH','AUTH_FAILURE'])
        outcome = 'FAIL' if 'FAIL' in proc else 'OK'
        f.write(f"{ts},AMF1,gNB-23,{proc},{outcome},imsi-00101\n")


with open('app/data/sample_traces/n4_pfcp.log','w') as f:
    for i in range(450):
        ts = (now + timedelta(seconds=i)).isoformat()+'Z'
        msg = random.choice(['SESSION_ESTABLISHMENT','SESSION_MODIFICATION','HEARTBEAT','SESSION_DELETION'])
        f.write(f"{ts},SMF1,UPF-A,{msg},0x9a,0x10\n")


with open('app/data/sample_traces/sbi_http2.jsonl','w') as f:
    for i in range(500):
        ts = (now + timedelta(milliseconds=200*i)).isoformat()+'Z'
        obj = {
            "ts": ts, "src_nf": "AMF1", "dst_nf": random.choice(["PCF1","UDM1","NSSF1"]),
            "path": random.choice(["/nudm-sdm/v2","/npcf-policyauth/v1","/nnssf-nsselection/v1"]),
            "method": random.choice(["GET","POST"]),
            "status": random.choice([200,200,200,429,500]),
            "lat_ms": random.randint(10, 120)
        }
        f.write(json.dumps(obj) + "\n")
print("Dummy traces generated under app/data/sample_traces/")
