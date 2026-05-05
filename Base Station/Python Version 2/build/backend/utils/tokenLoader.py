from path import getPath
import json

def getTokenData(name):
    tokenPath = getPath("source", "token.json")

    with open(tokenPath, "r") as f:
        return json.load(f)[name]