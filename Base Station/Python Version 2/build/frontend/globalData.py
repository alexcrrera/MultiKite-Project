import json
import os
from map import MapData
import os
from path import getPath

json_path = getPath("source", "data.json")

def getDataPath():
    baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(baseDir, "source", "data.json")

class GlobalData:

    def __init__(self):

        self.lastTimestamp = 0

        self.gridLayout = [
            ['left_panel', 'map', 'plot'],
            ['plot', 'plot', 'empty']
        ]

        self.gridRows = 3
        self.gridCols =2

        self.vesselIds = []
        self.trackedIndex = 0
        self.currentZoom = 10
        self.smallSquareMode = 0

        self.base_dir = ""
        self.vessels = []

        self.fps = 50

       

        self.currentZoom = 10

        self.loadData()
        self.loadImages()

        self.latitude = 39.86
        self.longitude = 2.5
        self.mothership_pos = (39.86, 2.5)
        self.mothership_heading = 0

        self.currentTimeUTC = None
        self.app_name = "MULTIKITE CONTROL STATION"
        self.timeZoneOffset = 0
        self.map = MapData()
        self.map.center_lat = self.latitude
        self.map.center_lng = self.longitude
        self.map.zoom = self.currentZoom

        self.map_leaflet = None
     

    def update_sensors(self):
        
        # Placeholder for sensor updates - in real implementation, fetch from hardware or APIs
        self.latitude += 0.01  # Simulate movement
        self.longitude += 0.01
        self.map.center_lat = self.latitude
        self.map.center_lng = self.longitude
        # move marker in map
        print(f"Updated position: {self.latitude}, {self.longitude}")
        for marker in self.map.markers:
            
                marker['lat'] = self.latitude
                marker['lng'] = self.longitude
                #update map
                map = self.map
                map.markers = self.map.markers
  

    def loadData(self):

        json_path = os.path.join("source", "data.json")

        with open(json_path, "r") as file:
            data = json.load(file)

        self.base_dir = os.path.join(os.path.dirname(__file__), data["main_dir"])
        self.mapMode = "osm"
        self.map_tiles = data["map_tiles"]

    def loadImages(self):

        json_path = os.path.join("source", "images.json")

        if os.path.exists(json_path):

            with open(json_path, "r") as file:
                data = json.load(file)

            self.map_image = os.path.join(self.base_dir, data["map"])
            self.camera_feed_image = os.path.join(self.base_dir, data["camera_feed"])
            self.logo_station_image = os.path.join(self.base_dir, data["logo_station"])
            self.logo_image = os.path.join(self.base_dir, data["logo"])

        else:
            print("No images JSON loaded!")

        

    def clickedSquareTab(self):
        self.smallSquareMode = (self.smallSquareMode + 1) % 2
        print(f"Small square mode: {self.smallSquareMode}")