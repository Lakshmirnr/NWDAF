from collections import defaultdict
import time

PacketCapture=[]
FragmentBuffer=defaultdict(list)
FragmentTimer={}
AlertLog=[]
FragmentTimeoutThreshold=5

def send_alert(event,i): print(f"[ALERT] {event}: {i}")

def coordinated_fragmentation_detection():
    for packet in PacketCapture:
        if packet["protocol"]!="PFCP" or not packet["fragmented"]:
            continue
        seid=packet["seid"]
        if seid not in FragmentTimer:
            FragmentTimer[seid]=time.time()
        FragmentBuffer[seid].append(packet)
        if time.time()-FragmentTimer[seid]>FragmentTimeoutThreshold:
            AlertLog.append(("Fragment Arrival Timeout",seid))
    return AlertLog

if __name__=="__main__":
    print(coordinated_fragmentation_detection())
