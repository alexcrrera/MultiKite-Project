from nicegui import ui
from small_sidebar_square import SmallSidebarSquare
from log import buildLog

def buildSidebar(globalData):

    square = SmallSidebarSquare(globalData)

    with ui.left_drawer().classes('bg-zinc-800 text-white'):

        with ui.column().classes('w-full h-full'):

            ui.label('Menu')
            ui.button('Map')
            ui.button('Telemetry')
            ui.button('Logs')

            ui.space()

            ui.button('Settings')

            ui.space()
            ui.button('Logass')

            
    

            with ui.element('div').classes('relative w-full aspect-square'):

                square.build()

            buildLog(globalData)
 
