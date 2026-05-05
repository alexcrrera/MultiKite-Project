class Vessel:

    def __init__(self, vesselId):

        self.id = vesselId

        self.lat = None
        self.lon = None

        self.speed = None
        self.heading = None

        self.timestamp = None
        self.radius1 = 10.0

    def updatePosition(self, lat, lon, timestamp=None):

        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp


    def updateMotion(self, speed=None, heading=None):

        if speed is not None:
            self.speed = speed

        if heading is not None:
            self.heading = heading


    def toDict(self):

        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "speed": self.speed,
            "heading": self.heading,
            "timestamp": self.timestamp
        }


    def __repr__(self):

        return (
            f"Vessel(id={self.id}, "
            f"lat={self.lat}, "
            f"lon={self.lon}, "
            f"speed={self.speed}, "
            f"heading={self.heading})"
        )