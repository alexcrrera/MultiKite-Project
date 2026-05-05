from state import *

def initializeTrackDots(m):

    for _ in range(lineSegments + 1):

        dot = m.marker(
            latlng=(mapCenter[0], mapCenter[1]),
            options={
                "icon": {
                    "iconUrl": "https://upload.wikimedia.org/wikipedia/commons/3/3c/White_dot.svg",
                    "iconSize": [6, 6],
                    "iconAnchor": [3, 3]
                }
            }
        )

        lineDots.append(dot)


def updateTrackLine(vesselLat, vesselLon):

    cx, cy = mapCenter

    for i in range(lineSegments + 1):

        t = i / lineSegments

        lat = cx + (vesselLat - cx) * t
        lon = cy + (vesselLon - cy) * t

        lineDots[i].move(lat=lat, lng=lon)