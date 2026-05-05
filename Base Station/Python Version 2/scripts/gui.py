from nicegui import ui
import threading
import asyncio
from datetime import datetime
import ais_backend

markers = {}
lineDots = []
lineSegments = 25

vesselIds = []
trackedIndex = 0
currentZoom = 5

mapMode = 0
mapModes = ["Dark", "Satellite", "OSM"]

mapCenter = [39.6, 2.8]

ui.query('body').classes('bg-black m-0 p-0 overflow-hidden')


def centerTrackedVessel():
    global mapCenter

    if not vesselIds:
        return

    v = ais_backend.vessels.get(vesselIds[trackedIndex])

    if v and v.lat is not None and v.lon is not None:
        mapCenter = [v.lat, v.lon]
        m.set_center((v.lat, v.lon))
        m.set_zoom(8)


def toggleMap():
    global mapMode

    mapMode = (mapMode + 1) % len(mapModes)

    darkLayer.run_method("setOpacity", 1 if mapMode == 0 else 0)
    satelliteLayer.run_method("setOpacity", 1 if mapMode == 1 else 0)
    osmLayer.run_method("setOpacity", 1 if mapMode == 2 else 0)

    mapModeLabel.set_text(f"Map: {mapModes[mapMode]}")


def initializeTrackDots():

    for _ in range(lineSegments + 1):

        dot = m.marker(
            latlng=(mapCenter[0], mapCenter[1]),
            options={
                "icon": {
                    "iconUrl": "https://upload.wikimedia.org/wikipedia/commons/3/3c/White_dot.svg",
                    "iconSize": [6, 6],
                    "iconAnchor": [3, 3]
                }
            }
        )

        lineDots.append(dot)


def updateTrackLine(vesselLat, vesselLon):

    cx, cy = mapCenter

    for i in range(lineSegments + 1):

        t = i / lineSegments

        lat = cx + (vesselLat - cx) * t
        lon = cy + (vesselLon - cy) * t

        lineDots[i].move(lat=lat, lng=lon)


with ui.column().classes('w-screen h-screen bg-black text-white overflow-hidden'):

    with ui.row().classes('w-full h-[50px] bg-gray-900 px-4 items-center justify-between shrink-0'):

        timeLabel = ui.label('Time: --')
        vesselCountLabel = ui.label('Vessels: 0')
        lastUpdateLabel = ui.label('Last update: --')
        mapModeLabel = ui.label('Map: Dark')

    with ui.row().classes('w-full flex-nowrap flex-grow overflow-hidden'):

        with ui.column().classes('w-2/3 h-full relative overflow-hidden'):

            m = ui.leaflet(center=(mapCenter[0], mapCenter[1]), zoom=currentZoom).classes('w-full h-full')

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

        with ui.column().classes('w-1/3 h-full bg-gray-900 p-4'):

            ui.label('Telemetry').classes('text-lg')

            vesselPanel = ui.label('Tracked vessels: 0')
            lastVesselPanel = ui.label('Last vessel: ---')

            ui.separator()

            ui.label('Controls').classes('text-lg')

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
                    centerTrackedVessel()

                def nextVessel():
                    global trackedIndex
                    if not vesselIds:
                        return
                    trackedIndex = (trackedIndex + 1) % len(vesselIds)
                    centerTrackedVessel()

                ui.button('Previous', on_click=previousVessel)
                ui.button('Next', on_click=nextVessel)

            ui.button('Center map', on_click=centerTrackedVessel)

            ui.separator()

            ui.button('Change map type', on_click=toggleMap)


def updateMap():

    global vesselIds

    vessels = ais_backend.vessels.copy()
    vesselIds = list(vessels.keys())

    vesselCountLabel.set_text(f"Vessels: {len(vessels)}")
    vesselPanel.set_text(f"Tracked vessels: {len(vessels)}")

    now = datetime.now().strftime("%H:%M:%S")

    timeLabel.set_text(f"Time: {now} UTC")
    lastUpdateLabel.set_text(f"Last update: {now}")

    lastText = "---"

    for vesselId, v in vessels.items():

        if v.lat is None or v.lon is None:
            continue

        lastText = f"{vesselId}  {v.lat:.3f}  {v.lon:.3f}"

        if vesselId not in markers:
            markers[vesselId] = m.marker(latlng=(v.lat, v.lon))
        else:
            markers[vesselId].move(lat=v.lat, lng=v.lon)

    lastVesselPanel.set_text(f"Last vessel: {lastText}")

    if vesselIds:

        trackedId = vesselIds[trackedIndex]
        v = vessels[trackedId]

        vesselInfoLabel.set_text(
            f"Tracked Vessel: {trackedId} | "
            f"Lat: {v.lat:.5f} | "
            f"Lon: {v.lon:.5f}"
        )

        updateTrackLine(v.lat, v.lon)


ui.timer(2, updateMap)


def startAisBackend():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ais_backend.main())


threading.Thread(target=startAisBackend, daemon=True).start()

initializeTrackDots()

ui.run(reload=False)