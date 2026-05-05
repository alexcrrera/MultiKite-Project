import asyncio
import websockets
import json
from datetime import datetime, timezone


def getTokenData(name):
    with open("build/token.json", "r") as f:
        data = json.load(f)
    return data[name]



async def connect_ais_stream(token, endpoint):

    async with websockets.connect(endpoint) as websocket:
        subscribe_message = {
            "APIKey": token,  # Required
            "BoundingBoxes": [[[ -90, -180], [90, 180]]],  # Required
            "FiltersShipMMSI": ["368207620", "367719770", "211476060"],  # Optional!
            "FilterMessageTypes": ["PositionReport"]  # Optional!
        }

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            print(f"Received message: {message}")
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                # the message parameter contains a key of the message type which contains the message itself
                ais_message = message["Message"]["PositionReport"]

                print(
                    f"[{datetime.now(timezone.utc)}] "
                    f"ShipId: {ais_message['UserID']} "
                    f"Latitude: {ais_message['Latitude']} "
                    f"Longitude: {ais_message['Longitude']}"
                )



if __name__ == "__main__":
    token = getTokenData("aisstream")
    endpoint = token[0]["endpoint"]
    asyncio.run(connect_ais_stream(token[0]["key"], endpoint))