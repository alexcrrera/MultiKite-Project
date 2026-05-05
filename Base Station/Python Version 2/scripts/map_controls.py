import ais_backend
from state import *

def centerTrackedVessel(m):

    global mapCenter

    if not vesselIds:
        return

    v = ais_backend.vessels.get(vesselIds[trackedIndex])

    if v and v.lat is not None and v.lon is not None:
        mapCenter = [v.lat, v.lon]
        m.set_center((v.lat, v.lon))
        m.set_zoom(8)


def toggleMap(darkLayer, satelliteLayer, osmLayer, mapModeLabel):

    global mapMode

    mapMode = (mapMode + 1) % len(mapModes)

    darkLayer.run_method("setOpacity", 1 if mapMode == 0 else 0)
    satelliteLayer.run_method("setOpacity", 1 if mapMode == 1 else 0)
    osmLayer.run_method("setOpacity", 1 if mapMode == 2 else 0)

    mapModeLabel.set_text(f"Map: {mapModes[mapMode]}")