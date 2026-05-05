class MapData:
    def __init__(self):
        self.markers = []  # [{'id': str, 'lat': float, 'lng': float, 'label': str, 'color': str}, ...]
        self.moe = {}  # {marker_id: {'radius': float (meters), 'color': str}} or polygons
        self.center_lat = 39.86
        self.center_lng = 2.5
        self.zoom = 10

    def add_marker(self, vessel_id, lat, lng, label='Vessel', color='blue'):
        marker = {'id': vessel_id, 'lat': lat, 'lng': lng, 'label': label, 'color': color}
        if vessel_id not in [m['id'] for m in self.markers]:
            self.markers.append(marker)
        self.update_center()

    def update_moe(self, vessel_id, radius_m=100, color='red'):
        self.moe[vessel_id] = {'radius': radius_m, 'color': color}

    def remove_marker(self, vessel_id):
        self.markers = [m for m in self.markers if m['id'] != vessel_id]
        self.moe.pop(vessel_id, None)

    def update_center(self):
        if self.markers:
            lats = [m['lat'] for m in self.markers]
            lngs = [m['lng'] for m in self.markers]
            self.center_lat = sum(lats) / len(lats)
            self.center_lng = sum(lngs) / len(lngs)

    def to_json(self):
        return {
            'markers': self.markers,
            'moe': self.moe,
            'center': (self.center_lat, self.center_lng),
            'zoom': self.zoom
        }
    

