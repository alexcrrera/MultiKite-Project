

from calculations import getAgeOfDataEntry


def handleVesselData(globalData, vesselData)->None:
    """vesselData contains all the vessels received from the backend. We want to add a timestamp to each vessel and then store it in globalData."""

   # print("Received vessel data:", vesselData)


    for vessel in vesselData:
        vessel['last_updated'] = getAgeOfDataEntry(globalData, vessel)
        
    
    globalData.vessels = vesselData
    return