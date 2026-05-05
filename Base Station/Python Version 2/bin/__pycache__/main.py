import json
import asyncio
import threading
from websocket import WebSocketApp
import websockets


class Vessel:

    def __init__(self, mmsi):

        self.mmsi = mmsi
        self.name = None
        self.lat = None
        self.lon = None
        self.sog = None
        self.cog = None
        self.lastUpdate = None

    def updateFromAis(self, data):
        print("Updating vessel", self.mmsi)

        meta = data.get("MetaData", {})
        msg = data.get("Message", {})

        self.name = meta.get("ShipName", self.name)
        self.lat = meta.get("latitude", self.lat)
        self.lon = meta.get("longitude", self.lon)
        self.lastUpdate = meta.get("time_utc", self.lastUpdate)

        if "PositionReport" in msg:
            pr = msg["PositionReport"]
        elif "StandardClassBPositionReport" in msg:
            pr = msg["StandardClassBPositionReport"]
        else:
            pr = None

        if pr:
            self.sog = pr.get("Sog", self.sog)
            self.cog = pr.get("Cog", self.cog)

    def toDict(self):

        return {
            "mmsi": self.mmsi,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "sog": self.sog,
            "cog": self.cog,
            "lastUpdate": self.lastUpdate
        }


vessels = {}
clients = set()


def loadTokens():

    with open("config/tokens.json", "r") as f:
        return json.load(f)


async def broadcastVessel(vessel):

    if vessel.lat is None or vessel.lon is None:
        return

    payload = json.dumps(vessel.toDict())

    dead = []

    for ws in clients:
        try:
            await ws.send(payload)
        except:
            dead.append(ws)

    for ws in dead:
        clients.remove(ws)


async def wsHandler(websocket):

    clients.add(websocket)

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        clients.remove(websocket)


def startAis(loop):

    apiKey = loadTokens()["aisStream"]

    subscription = {
        "APIKey": apiKey,
        "BoundingBoxes": [[[-180,-90],[180,90]]],
        "FilterMessageTypes": [
            "PositionReport",
            "StandardClassBPositionReport"
        ]
    }

    def on_open(ws):

        print("AIS websocket connected")

        ws.send(json.dumps(subscription))

        print("AIS subscription sent")

    def on_message(ws, message):

        data = json.loads(message)

        meta = data.get("MetaData", {})
        mmsi = meta.get("MMSI")

        if mmsi is None:
            return

        if mmsi not in vessels:
            vessels[mmsi] = Vessel(mmsi)

        vessel = vessels[mmsi]
        vessel.updateFromAis(data)

        loop.call_soon_threadsafe(
            asyncio.create_task,
            broadcastVessel(vessel)
        )

    def on_error(ws, error):
        print("AIS error:", error)

    def on_close(ws, code, msg):
        print("AIS connection closed")

    ws = WebSocketApp(
        "wss://stream.aisstream.io/v0/stream",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever(ping_interval=20)


async def main():

    loop = asyncio.get_running_loop()

    threading.Thread(
        target=startAis,
        args=(loop,),
        daemon=True
    ).start()

    server = await websockets.serve(
        wsHandler,
        "localhost",
        8765
    )

    print("WebSocket server running on ws://localhost:8765")

    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())