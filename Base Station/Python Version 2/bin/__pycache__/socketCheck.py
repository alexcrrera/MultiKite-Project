import asyncio
import websockets
import socket
import time
async def test():
    print("connecting")
    timeconnect = time.time()

    ws = await websockets.connect(
        "wss://stream.aisstream.io/v0/stream",
        family=socket.AF_INET,
        open_timeout=50
    )

    print("connected")
    timeconnected = time.time()
    print("Connection time:", timeconnected - timeconnect)

asyncio.run(test())