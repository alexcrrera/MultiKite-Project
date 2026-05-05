from nicegui import ui
from state import *
from map_controls import centerTrackedVessel, toggleMap
import json


def createLayout():
    pendingClick = {
        'lat': None,
        'lon': None,
    }

    def extractClickData(args):
        lat = None
        lon = None
        clickX = 24
        clickY = 24

        def search(value):
            nonlocal lat, lon, clickX, clickY

            if isinstance(value, str):
                try:
                    search(json.loads(value))
                except Exception:
                    return
                return

            if isinstance(value, (list, tuple)):
                for item in value:
                    search(item)
                return

            if not isinstance(value, dict):
                return

            if lat is None and 'lat' in value:
                lat = value.get('lat')
            if lon is None and 'lng' in value:
                lon = value.get('lng')
            if lon is None and 'lon' in value:
                lon = value.get('lon')
            if 'x' in value:
                clickX = value.get('x', clickX)
            if 'y' in value:
                clickY = value.get('y', clickY)

            for nestedKey in ('latlng', 'containerPoint', 'layerPoint', 'point', 'detail', 'args'):
                nestedValue = value.get(nestedKey)
                if nestedValue is not None:
                    search(nestedValue)

            for nestedValue in value.values():
                if isinstance(nestedValue, (dict, list, tuple, str)):
                    search(nestedValue)

        search(args)
        return lat, lon, clickX, clickY

    def setMarkerModeArmed(armed):
        global markerModeArmed

        markerModeArmed = armed

        if armed:
            m.classes(add='cursor-crosshair')
            interactionStatus.set_text('Interaction: Marker mode armed | left click to open marker menu')
            return

        m.classes(remove='cursor-crosshair')
        hideMarkerMenu()
        interactionStatus.set_text('Interaction: Navigation | right click to arm marker menu')

    def findClosestUserMarker(lat, lon):
        if not userMarkers:
            return None

        closestMarker = None
        closestDistance = None

        for markerState in userMarkers:
            distance = ((markerState['lat'] - lat) ** 2 + (markerState['lon'] - lon) ** 2) ** 0.5

            if closestDistance is None or distance < closestDistance:
                closestDistance = distance
                closestMarker = markerState

        if closestDistance is None or closestDistance > markerRemovalThreshold:
            return None

        return closestMarker

    def hideMarkerMenu():
        markerMenu.classes(add='hidden')

    def showMarkerMenu(clickX, clickY):
        markerMenu.style(
            f'left: {int(clickX) + 12}px; top: {int(clickY) + 12}px;'
        )
        markerMenu.classes(remove='hidden')

    def removeUserMarker(markerState):
        try:
            markerState['marker'].run_method('remove')
        except Exception:
            markerState['marker'].delete()
        userMarkers.remove(markerState)

    def addUserMarker(lat, lon, markerType):
        markerConfig = markerTypes[markerType]
        marker = m.marker(
            latlng=(lat, lon),
            options={
                'icon': {
                    'iconUrl': markerConfig['iconUrl'],
                    'shadowUrl': 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    'iconSize': [25, 41],
                    'iconAnchor': [12, 41],
                    'popupAnchor': [1, -34],
                    'shadowSize': [41, 41],
                }
            },
        )
        userMarkers.append({'marker': marker, 'lat': lat, 'lon': lon, 'type': markerType})

    def updateMarkerStatus(message):
        markerStatus.set_text(f'User markers: {len(userMarkers)} | {message}')

    def finishMarkerAction(message):
        updateMarkerStatus(message)
        setMarkerModeArmed(False)

    def addMarkerAtPendingClick(markerType):
        lat = pendingClick['lat']
        lon = pendingClick['lon']

        if lat is None or lon is None:
            return

        addUserMarker(lat, lon, markerType)
        finishMarkerAction(f'added {markerType.lower()} at {lat:.5f}, {lon:.5f}')

    def removeNearestMarkerAtPendingClick():
        lat = pendingClick['lat']
        lon = pendingClick['lon']

        if lat is None or lon is None:
            return

        closestMarker = findClosestUserMarker(lat, lon)

        if closestMarker is None:
            finishMarkerAction('no nearby marker to remove')
            return

        removeUserMarker(closestMarker)
        finishMarkerAction('removed nearest marker')

    def toggleMarkerAtPendingClick():
        lat = pendingClick['lat']
        lon = pendingClick['lon']

        if lat is None or lon is None:
            return

        closestMarker = findClosestUserMarker(lat, lon)

        if closestMarker is None:
            addUserMarker(lat, lon, 'Red marker')
            finishMarkerAction(f'toggled on red marker at {lat:.5f}, {lon:.5f}')
            return

        removeUserMarker(closestMarker)
        finishMarkerAction('toggled off nearest marker')

    def cancelMarkerAction():
        setMarkerModeArmed(False)
        updateMarkerStatus('marker action canceled')

    def handleMapContextMenu(_event):
        hideMarkerMenu()
        setMarkerModeArmed(True)
        updateMarkerStatus('marker mode armed')

    def handleMapClick(event):
        if not markerModeArmed:
            hideMarkerMenu()
            return

        args = event.args or {}
        lat, lon, clickX, clickY = extractClickData(args)

        if lat is None or lon is None:
            updateMarkerStatus(f'map click missing coordinates: {str(args)[:120]}')
            return

        pendingClick['lat'] = lat
        pendingClick['lon'] = lon
        showMarkerMenu(clickX, clickY)

    with ui.column().classes('w-screen h-screen bg-black text-white overflow-hidden'):

        with ui.row().classes('w-full h-[50px] bg-gray-900 px-4 items-center justify-between shrink-0'):

            timeLabel = ui.label('Time: --')
            vesselCountLabel = ui.label('Vessels: 0')
            lastUpdateLabel = ui.label('Last update: --')
            mapModeLabel = ui.label('Map: Dark')

        with ui.row().classes('w-full flex-nowrap flex-grow overflow-hidden'):

            with ui.column().classes('w-2/3 h-full relative overflow-hidden'):

                m = ui.leaflet(center=(mapCenter[0], mapCenter[1]), zoom=currentZoom).classes('w-full h-full')
                m.on('click', handleMapClick)
                m.on('contextmenu.prevent', handleMapContextMenu)

                darkLayer = m.tile_layer(
                    url_template='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                    options={'maxZoom': 20, 'opacity': 1}
                )

                satelliteLayer = m.tile_layer(
                    url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    options={'opacity': 0}
                )

                osmLayer = m.tile_layer(
                    url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                    options={'opacity': 0}
                )

                with ui.column().classes(
                    'absolute inset-0 flex items-center justify-center pointer-events-none z-[900]'
                ):
                    ui.label('+').classes('text-white text-3xl')

                with ui.column().classes(
                    'absolute bottom-4 left-4 z-[1000] pointer-events-none'
                ):
                    vesselInfoLabel = ui.label('Tracked Vessel: ---').classes(
                        'bg-black/80 px-4 py-2 rounded text-white text-sm'
                    )

                with ui.column().classes(
                    'absolute z-[1100] hidden min-w-[220px] rounded border border-gray-700 bg-gray-950/95 p-2 shadow-2xl'
                ) as markerMenu:
                    ui.label('Map actions').classes('text-sm font-medium text-white')
                    ui.label('Right click arms marker mode, left click opens this menu').classes('text-xs text-gray-400')
                    ui.button('Add red marker', on_click=lambda: addMarkerAtPendingClick('Red marker')).classes('w-full justify-start')
                    ui.button('Add blue marker', on_click=lambda: addMarkerAtPendingClick('Blue marker')).classes('w-full justify-start')
                    ui.button('Add green marker', on_click=lambda: addMarkerAtPendingClick('Green marker')).classes('w-full justify-start')
                    ui.button('Remove nearest marker', on_click=removeNearestMarkerAtPendingClick).classes('w-full justify-start')
                    ui.button('Toggle nearest marker', on_click=toggleMarkerAtPendingClick).classes('w-full justify-start')
                    ui.button('Cancel', on_click=cancelMarkerAction).classes('w-full justify-start')

            with ui.column().classes('w-1/3 h-full bg-gray-900 p-4'):

                ui.label('Telemetry').classes('text-lg')

                vesselPanel = ui.label('Tracked vessels: 0')
                lastVesselPanel = ui.label('Last vessel: ---')

                ui.separator()

                ui.label('Controls').classes('text-lg')
                interactionStatus = ui.label('Interaction: Navigation | right click to arm marker menu').classes('text-xs text-gray-300')

                ui.separator()

                def clearUserMarkers():
                    while userMarkers:
                        removeUserMarker(userMarkers[-1])

                    setMarkerModeArmed(False)
                    updateMarkerStatus('cleared all user markers')

                ui.button('Clear user markers', on_click=clearUserMarkers)
                markerStatus = ui.label('User markers: 0 | right click the map to arm marker mode').classes('text-xs text-gray-300')

                ui.separator()

                def zoomIn():
                    global currentZoom
                    currentZoom += 1
                    m.set_zoom(currentZoom)

                def zoomOut():
                    global currentZoom
                    currentZoom -= 1
                    m.set_zoom(currentZoom)

                ui.button('Zoom in', on_click=zoomIn)
                ui.button('Zoom out', on_click=zoomOut)

                ui.separator()

                with ui.row():

                    def previousVessel():
                        global trackedIndex
                        if not vesselIds:
                            return
                        trackedIndex = (trackedIndex - 1) % len(vesselIds)
                        centerTrackedVessel(m)

                    def nextVessel():
                        global trackedIndex
                        if not vesselIds:
                            return
                        trackedIndex = (trackedIndex + 1) % len(vesselIds)
                        centerTrackedVessel(m)

                    ui.button('Previous', on_click=previousVessel)
                    ui.button('Next', on_click=nextVessel)

                ui.button('Center map', on_click=lambda: centerTrackedVessel(m))

                ui.separator()

                ui.button(
                    'Change map type',
                    on_click=lambda: toggleMap(
                        darkLayer,
                        satelliteLayer,
                        osmLayer,
                        mapModeLabel
                    )
                )

    setMarkerModeArmed(False)

    return (
        m,
        timeLabel,
        vesselCountLabel,
        lastUpdateLabel,
        vesselPanel,
        lastVesselPanel,
        vesselInfoLabel
    )
