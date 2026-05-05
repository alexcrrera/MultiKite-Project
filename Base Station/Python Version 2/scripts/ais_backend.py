import asyncio
import requests
from vessel import Vessel

vessels = {}


def fetchTargets():

    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

    r = requests.get(url, timeout=5)

    if r.status_code != 200:
        print("AIS backend: HTTP error", r.status_code)
        return []

    data = r.json()

    targets = []

    for f in data["features"]:

        coords = f["geometry"]["coordinates"]

        lon = coords[0]
        lat = coords[1]

        targets.append({
            "id": f["id"],
            "lat": lat,
            "lon": lon
        })


    return targets


def updateVessels(targets):

    for t in targets:

        vid = t["id"]
        lat = t["lat"]
        lon = t["lon"]

        if vid not in vessels:
            vessels[vid] = Vessel(vid)

        vessels[vid].updatePosition(lat, lon)

    print("AIS backend: vessels:", len(vessels))


async def pollLoop():

    while True:

        try:

            targets = fetchTargets()
            updateVessels(targets)

        except Exception as e:

            print("AIS backend error:", e)

        await asyncio.sleep(10)


async def main():

    print("AIS backend started")

    await pollLoop()