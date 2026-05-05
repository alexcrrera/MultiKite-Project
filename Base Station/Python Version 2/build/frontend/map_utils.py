from nicegui import ui
import math

def create_map(globalData, draw_toolbar=False):
    center = [globalData.map.center_lat, globalData.map.center_lng]

    """Creates map + stores ref for backend updates."""
    globalData.map_ref = ui.leaflet(
        center=center,
        zoom=globalData.map.zoom
    ).classes('w-full h-full leaflet-attribution-off')

    # Tiles (static)
    tile_url = globalData.map_tiles[globalData.mapMode]
    globalData.map_ref.tile_layer(url_template=tile_url)

    # Draw toolbar (static)
    if draw_toolbar:
        globalData.map_ref.draw_control = {
            'position': 'topleft',
            'draw': {'marker': True, 'circle': True, 'polygon': True},
            'edit': {'edit': True, 'remove': True}
        }

    # Store layers for updates
    globalData.map_layers = {
        'mothership': None,
        'vessels': [],
        'moe': [],
        'crosshair': None
    }

    _render_layers(globalData)
    return globalData.map_ref



def vesselsToMarkers(globalData):
    markers = []

    for v in globalData.vessels:
        if v["lat"] is None or v["lon"] is None:
            continue

        markers.append({
            "lat": v["lat"],
            "lon": v["lon"],
            "label": f'{v["name"]} ({v["mmsi"]})'
        })

    globalData.map.markers = markers

def _render_layers(globalData):
    """Internal: Clear + re-render all layers."""
    map_ref = globalData.map_ref
    
    # Clear existing layers
    
    for layer in globalData.map_layers['vessels'] + globalData.map_layers['moe']:
        if layer: map_ref.remove_layer(layer)
    
    globalData.map_layers['vessels'] = []
    globalData.map_layers['moe'] = []

    # Mothership arrow
    renderMothership(globalData)
    # Vessels
    for marker_data in globalData.map.markers:
        mk = map_ref.marker(latlng=[marker_data['lat'], marker_data['lng']])
        map_ref.run_layer_method(mk.id, 'bindTooltip', marker_data.get('label', marker_data['id']))
        globalData.map_layers['vessels'].append(mk)

    # MoE circles
    for mid, moe in globalData.map.moe.items():
        pos = next((m for m in globalData.map.markers if m['id'] == mid), None)
        if pos:
            circle = map_ref.circle(center=[pos['lat'], pos['lng']], 
                                  radius=moe['radius']/100, color='red', fill_opacity=0.3)
            globalData.map_layers['moe'].append(circle)

    # Crosshair (pan listener)
    if not globalData.map_layers['crosshair']:
        globalData.map_layers['crosshair'] = map_ref.marker(
            latlng=[globalData.latitude, globalData.longitude])
        map_ref.on('move', lambda e: globalData.map_layers['crosshair'].move(
            lat=e.args['center']['lat'], lng=e.args['center']['lng']))

    # Refresh
   # map_ref.center = [globalData.map.center_lat, globalData.map.center_lng]
    #map_ref.zoom = globalData.map.zoom
    map_ref.update()





def update_map(globalData):
    vessels = globalData.vessels

    markers = []

    for v in vessels:
        if v["lat"] is None or v["lon"] is None:
            continue

        markers.append({
            "id": v["mmsi"],
            "lat": v["lat"],
            "lng": v["lon"],
            "label": f'{v["name"]} ({v["mmsi"]})'
        })

    # update state
    globalData.map.markers = markers

    # update center (optional but keeps behavior consistent)
    if markers:
        lats = [m['lat'] for m in markers]
        lngs = [m['lng'] for m in markers]
        globalData.map.center_lat = sum(lats) / len(lats)
        globalData.map.center_lng = sum(lngs) / len(lngs)

    #print(f"Updated map with {len(markers)} vessel markers.")
    #print("-mu")
    # render
    _render_layers(globalData)

    # --- render ---
    #_render_layers(globalData)

# Usage in main_page():
# create_map(globalData)


def renderMothership(globalData):
    if not hasattr(globalData, 'map_ref'):
        return
    if not hasattr(globalData, 'mothership_pos') or not globalData.mothership_pos:
        return

    mapRef = globalData.map_ref
    lat, lng = globalData.mothership_pos
    heading = getattr(globalData, 'mothership_heading', 0.0)

    # Normalize heading
    heading = float(heading) % 360.0

    # Create once
    if not globalData.map_layers.get('mothership'):
        arrow = mapRef.marker(latlng=[lat, lng])

        svg = f'''
        L.divIcon({{
            html: `
            <svg width="28" height="36" viewBox="0 0 24 32"
                 style="transform: rotate({heading}deg); transform-origin: 50% 50%;">
                <path d="M12 0 L0 24 L6 24 L6 32 L18 32 L18 24 L24 24 Z"
                      fill="#0066cc" stroke="#000"/>
            </svg>`,
            iconSize: [28,36],
            iconAnchor: [14,36]
        }})
        '''

        mapRef.run_layer_method(arrow.id, 'setIcon', svg)
        mapRef.run_layer_method(arrow.id, 'bindTooltip', 'Mothership')

        globalData.map_layers['mothership'] = arrow

    # Update position + rotation
    else:
        arrow = globalData.map_layers['mothership']
        arrow.move(lat=lat, lng=lng)

        svg = f'''
        L.divIcon({{
            html: `
            <svg width="28" height="36" viewBox="0 0 24 32"
                 style="transform: rotate({heading}deg); transform-origin: 50% 50%;">
                <path d="M12 0 L0 24 L6 24 L6 32 L18 32 L18 24 L24 24 Z"
                      fill="#0066cc" stroke="#000"/>
            </svg>`,
            iconSize: [28,36],
            iconAnchor: [14,36]
        }})
        '''

        mapRef.run_layer_method(arrow.id, 'setIcon', svg)