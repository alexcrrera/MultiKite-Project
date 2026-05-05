markers = {}
userMarkers = []
lineDots = []
lineSegments = 25

vesselIds = []
trackedIndex = 0
currentZoom = 5

mapMode = 0
mapModes = ["Dark", "Satellite", "OSM"]
markerRemovalThreshold = 0.01
markerTypes = {
    'Red marker': {
        'iconUrl': 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    },
    'Blue marker': {
        'iconUrl': 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    },
    'Green marker': {
        'iconUrl': 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    },
}
markerModeArmed = False

mapCenter = [39.6, 2.8]
