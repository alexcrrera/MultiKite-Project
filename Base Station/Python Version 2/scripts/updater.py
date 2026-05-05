from datetime import datetime
import ais_backend
from state import *
from track_line import updateTrackLine

def updateMap(
    m,
    vesselCountLabel,
    vesselPanel,
    lastUpdateLabel,
    timeLabel,
    lastVesselPanel,
    vesselInfoLabel
):

    global vesselIds

    vessels = ais_backend.vessels.copy()
    vesselIds = list(vessels.keys())

    vesselCountLabel.set_text(f"Vessels: {len(vessels)}")
    vesselPanel.set_text(f"Tracked vessels: {len(vessels)}")

    now = datetime.now().strftime("%H:%M:%S")

    timeLabel.set_text(f"Time: {now} UTC")
    lastUpdateLabel.set_text(f"Last update: {now}")

    lastText = "---"

    for vesselId, v in vessels.items():

        if v.lat is None or v.lon is None:
            continue

        lastText = f"{vesselId}  {v.lat:.3f}  {v.lon:.3f}"

        if vesselId not in markers:
            markers[vesselId] = m.marker(latlng=(v.lat, v.lon))
        else:
            markers[vesselId].move(lat=v.lat, lng=v.lon)

    lastVesselPanel.set_text(f"Last vessel: {lastText}")

    if vesselIds:

        trackedId = vesselIds[trackedIndex]
        v = vessels[trackedId]

        vesselInfoLabel.set_text(
            f"Tracked Vessel: {trackedId} | "
            f"Lat: {v.lat:.5f} | "
            f"Lon: {v.lon:.5f}"
        )

        updateTrackLine(v.lat, v.lon)