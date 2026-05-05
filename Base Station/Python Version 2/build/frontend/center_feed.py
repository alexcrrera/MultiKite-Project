from nicegui import ui, events
from map_utils import create_map, update_map

def buildCenterFeed(globalData):
    globalData.map_leaflet = create_map(globalData, draw_toolbar=True)

    # unify reference
  

    def handle_draw(e: events.GenericEventArguments):
        layer_type = e.args['layerType']
        coords = e.args['layer'].get('_latlng') or e.args['layer'].get('_latlngs')

        ui.notify(f'Drawn {layer_type}: {coords}')

        if coords:
            lat = coords[0] if isinstance(coords, list) else coords['lat']
            lng = coords[1] if isinstance(coords, list) else coords['lng']

            # store separately, do NOT mix with vessel markers
            if not hasattr(globalData, 'drawnMarkers'):
                globalData.drawnMarkers = []

            globalData.drawnMarkers.append({
                'lat': lat,
                'lng': lng,
                'label': layer_type
            })

    globalData.map_leaflet.on('draw:created', handle_draw)
    globalData.map_leaflet.on('draw:edited', lambda e: None)
    globalData.map_leaflet.on('draw:deleted', lambda e: None)

    ui.timer(1.0, lambda: update_map(globalData))