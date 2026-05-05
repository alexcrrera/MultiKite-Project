
import time

def getAgeOfDataEntry(globalData, vessel):

    time_vessel  = vessel.get("timestamp")
    #print("Time vessel:", time_vessel)
    current_time = int(time.time())
    dt = current_time - time_vessel if time_vessel else None
    return dt