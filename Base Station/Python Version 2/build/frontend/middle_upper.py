from nicegui import ui

def buildMiddleUpper(globalData):

    with ui.element('div').classes(
        'w-full h-full flex items-center justify-center border-2 border-dashed border-gray-400 grow'
    ):
        ui.label('UPPER AREA')