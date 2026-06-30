from collections import defaultdict

PacketCapture=[]
SessionStateDB={}
DeletionRequestCount=defaultdict(int)
TEIDTargetRate=defaultdict(int)
AlertLog=[]
DeletionThreshold=5
TEIDRateThreshold=10

def send_alert(event,i): print(f"[ALERT] {event}: {i}")

def abrupt_teid_reassignment(seid,teid):
    return seid in SessionStateDB and SessionStateDB[seid]!=teid

def session_hijacking_detection():
    for packet in PacketCapture:
        if packet["protocol"]!="PFCP": continue
        t=packet["message_type"]; seid=packet["seid"]; teid=packet["teid"]
        if t=="PFCP Session Establishment":
            SessionStateDB[seid]=teid
        elif t=="PFCP Session Deletion Request":
            if seid not in SessionStateDB:
                AlertLog.append(("Deletion Request for Unknown Session",seid))
            elif teid!=SessionStateDB[seid]:
                AlertLog.append(("SEID-TEID Association Mismatch",seid))
            DeletionRequestCount[seid]+=1
            if abrupt_teid_reassignment(seid,teid):
                AlertLog.append(("Abrupt TEID Reassignment",seid))
            TEIDTargetRate[teid]+=1
    return AlertLog

if __name__=="__main__":
    print(session_hijacking_detection())
