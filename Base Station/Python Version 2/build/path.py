import os

def getBuildRoot():
    return os.path.abspath(os.path.dirname(__file__))

def getPath(*parts):
    return os.path.join(getBuildRoot(), *parts)