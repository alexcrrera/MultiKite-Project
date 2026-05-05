import asyncio
import json
import websockets
import socket

vessels = {}
awaitingMessage = True


def loadApiKey():
    with open("config/tokens.json", "r") as f:
        config = json.load(f)
        print("AIS API Key loaded:", config["aisStream"])
    return config["aisStream"]


async def processAisMessage(message):

    global awaitingMessage

    try:
        data = json.loads(message)
    except Exception:
        return

    meta = data.get("MetaData")
    if not meta:
        return

    lat = meta.get("Latitude")
    lon = meta.get("Longitude")
    mmsi = meta.get("MMSI")

    if lat is None or lon is None or mmsi is None:
        return

    name = meta.get("ShipName", "").strip()

    vessels[mmsi] = {
        "name": name,
        "lat": lat,
        "lon": lon
    }

    awaitingMessage = False

    print("VESSEL:", mmsi, lat, lon)


async def aisClient():

    try:

        apiKey = loadApiKey()

        subscription = {
            "APIKey": apiKey,
            "BoundingBoxes": [[[-5.0, 48.0], [55.0, 5.0]]]
        }

        print("DEBUG: connecting to AIS stream")

        async with websockets.connect(
            "wss://stream.aisstream.io/v0/stream",
            family=socket.AF_INET,
            open_timeout=60,
            ping_interval=None
        ) as websocket:

            print("AIS websocket connected")

            await websocket.send(json.dumps(subscription))
            print("AIS subscription sent")

            async for message in websocket:
                print("DEBUG: websocket message received")
                await processAisMessage(message)

    except Exception as e:
        print("AIS CLIENT ERROR:", e)


async def statusLoop():

    global awaitingMessage

    while True:

        if awaitingMessage:
            print("Awaiting AIS message")
        else:
            print("Tracked vessels:", len(vessels))

        await asyncio.sleep(1)


async def main():

    print("AIS backend started")

    asyncio.create_task(aisClient())
    asyncio.create_task(statusLoop())

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())