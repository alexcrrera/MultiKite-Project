# center.py
from nicegui import ui
#from plotManager import plotRegistry
from center_feed import buildCenterFeed
from left_drawer_middle_upper import buildLeftDrawerMiddleUpper
from nicegui import ui
from gridManager import GridManager
import json

import os


def getConfigPath(filename):
    baseDir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    return os.path.join(baseDir, "config", filename)
import json

def loadLayout():
    path = getConfigPath("layout.json")
    with open(path, "r") as f:
        return json.load(f)



from labelWidget import LabelWidget


def buildCenter(globalData):

    globalData.gridManager = GridManager(globalData)
    globalData.gridManager.build()

    layoutConfig = loadLayout()
    populateFromConfig(globalData, layoutConfig)



def populateFromConfig(globalData, layoutConfig):
    gm = globalData.gridManager
    gm.clear()

    for widgetConfig in layoutConfig["widgets"]:
        widget = widgetRegistry.create(widgetConfig, globalData)
        if widget:
            gm.appendWidget(widget)



class WidgetRegistry:
    def __init__(self):
        self.registry = {
            "label": LabelWidget,
            "plot": LabelWidget,
        }

    def create(self, config, globalData):
        cls = self.registry.get(config["type"])
        if cls:
            return cls(globalData, config)
        return None

widgetRegistry = WidgetRegistry()