from collections import defaultdict

PacketCapture=[]
SEID_MessageCount=defaultdict(int)
MalformedPacketCount=defaultdict(int)
AlertLog=[]
PFCP_FloodingThreshold=100

def send_alert(event,identifier):
    print(f"[ALERT] {event}: {identifier}")

def is_valid_seid(packet): return True
def is_valid_checksum(packet): return True
def is_valid_message_type(packet): return True
def is_valid_sequence_number(packet): return True

def attack_detection():
    for packet in PacketCapture:
        if packet["protocol"]!="PFCP":
            continue
        seid=packet["seid"]
        SEID_MessageCount[seid]+=1
        if SEID_MessageCount[seid]>PFCP_FloodingThreshold:
            AlertLog.append(("PFCP Flooding Detected",seid))
            send_alert("PFCP Flooding Detected",seid)
        malformed=False
        if not is_valid_seid(packet): malformed=True
        if not is_valid_checksum(packet): malformed=True
        if not is_valid_message_type(packet): malformed=True
        if not is_valid_sequence_number(packet): malformed=True
        if malformed:
            MalformedPacketCount[seid]+=1
            if MalformedPacketCount[seid]>5:
                AlertLog.append(("Multiple Malformed Packets",seid))
                send_alert("Multiple Malformed Packets",seid)
    return AlertLog

if __name__=="__main__":
    print(attack_detection())
