from nicegui import ui
from buildVesselGrid import buildGrid, updateGrid

def buildMiddleLower(globalData):

    with ui.element('div').classes(
        'w-full h-full flex items-center justify-center border-2 border-dashed border-gray-400 grow'
    ):

        
        buildGrid(globalData)
        if not hasattr(globalData, 'addedVesselGrid'):
            #print("Error: vesselGrid not found in globalData after buildGrid.")
            print("Grid init")
            ui.timer(1.0, lambda: updateGrid(globalData))
            globalData.addedVesselGrid = True
    
