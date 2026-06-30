from collections import defaultdict
import time

PacketCapture=[]
FragmentBuffer=defaultdict(list)
FragmentTimer={}
ReassemblyFailureCount=defaultdict(int)
AlertLog=[]
FragmentTimeoutThreshold=5

def delayed_fragmentation_detection():
    for packet in PacketCapture:
        if packet["protocol"]!="PFCP" or not packet["fragmented"]:
            continue
        seid=packet["seid"]
        if seid not in FragmentTimer:
            FragmentTimer[seid]=time.time()
        FragmentBuffer[seid].append(packet)
        if time.time()-FragmentTimer[seid]>FragmentTimeoutThreshold:
            AlertLog.append(("Delayed Fragment Arrival",seid))
    return AlertLog

if __name__=="__main__":
    print(delayed_fragmentation_detection())
