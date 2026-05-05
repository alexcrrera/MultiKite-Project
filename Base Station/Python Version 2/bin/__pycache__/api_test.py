import json
import websocket

websocket.enableTrace(True)


def loadTokens():

    with open("config/tokens.json", "r") as f:
        return json.load(f)


def startStream():

    apiKey = loadTokens()["aisStream"]

    socketUrl = "wss://stream.aisstream.io/v0/stream"

    subscription = {
        "APIKey": apiKey,
        "BoundingBoxes": [[[-10, 35], [40, 60]]]
    }

    def onOpen(ws):
        print("OPEN")
        ws.send(json.dumps(subscription))
        print("SUBSCRIPTION SENT")

    def onMessage(ws, message):
        print("MESSAGE RECEIVED")
        print(message[:300])

    def onError(ws, error):
        print("ERROR:", error)

    def onClose(ws, code, msg):
        print("CLOSED", code, msg)

    ws = websocket.WebSocketApp(
        socketUrl,
        on_open=onOpen,
        on_message=onMessage,
        on_error=onError,
        on_close=onClose
    )

    ws.run_forever(ping_interval=30)


if __name__ == "__main__":
    startStream()