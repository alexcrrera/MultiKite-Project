from nicegui import ui
from log import buildLog


def buildRightSidebar(globalData):

    with ui.right_drawer().classes('bg-zinc-900 text-white'):

        with ui.column().classes('w-full h-full'):

            ui.label('Menu')
            ui.button('Map')
            ui.button('Telemetry')
            ui.button('Logs')

            ui.space()

            ui.button('Settings')

            ui.space()
            ui.button('Logass')
            buildManualControl(globalData)
            buildJoystick(globalData)
            buildStopButton(globalData)

            buildLog(globalData)


def buildJoystick(globalData):

    with ui.column().classes('w-full items-center'):

        with ui.element('div').classes('flex justify-center w-full'):
            joystick = ui.joystick(
                color='black',
                size=40,
                on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),
                on_end=lambda _: coordinates.set_text('0, 0'),
            ).classes('bg-slate-300')

        coordinates = ui.label('0, 0').classes('text-sm')

def buildManualControl(globalData):
     ui.button('MANUAL CONTROL', color='green', on_click=lambda: print('MANUAL CONTROL')).classes('w-full')
       

def buildStopButton(globalData):
    ui.button('Stop', color='red', on_click=lambda: print('Stop button clicked')).classes('w-full')

   