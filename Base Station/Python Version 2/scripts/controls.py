from nicegui import ui


def createControls(state, m):

    def zoomIn():

        print("zoom in")
        state.currentZoom += 1
        m.set_zoom(state.currentZoom)

    def zoomOut():
        print("zoom out")

        state.currentZoom -= 1
        m.set_zoom(state.currentZoom)

    def nextVessel():
        print("next vessel")
        if state.vesselIds:
            state.trackedIndex = (state.trackedIndex + 1) % len(state.vesselIds)

    def previousVessel():
        print("previous vessel")
        if state.vesselIds:
            state.trackedIndex = (state.trackedIndex - 1) % len(state.vesselIds)

    ui.separator()

    ui.label('Controls').classes('text-lg')

    with ui.row():
        ui.button('Zoom +', on_click=zoomIn)
        ui.button('Zoom -', on_click=zoomOut)

    #with ui.row():
        ui.button('Previous vessel', on_click=previousVessel)
        ui.button('Next vessel', on_click=nextVessel)