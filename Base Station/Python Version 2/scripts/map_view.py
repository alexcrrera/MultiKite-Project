from nicegui import ui

def createMap(state):

    m = ui.leaflet(center=tuple(state.mapCenter), zoom=state.currentZoom).classes(
        'w-full h-full'
    )

    darkLayer = m.tile_layer(
        url_template='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    )

    satelliteLayer = m.tile_layer(
        url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        options={'opacity': 0}
    )

    osmLayer = m.tile_layer(
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        options={'opacity': 0}
    )

    return m, darkLayer, satelliteLayer, osmLayer