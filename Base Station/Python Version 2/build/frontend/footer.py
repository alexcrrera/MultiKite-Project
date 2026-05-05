from nicegui import ui


def buildFooter():
    with ui.footer().classes('h-4 bg-gray-900 flex items-center justify-center'):
        ui.label('© 2026 MultiKite Project. All rights reserved.').classes('text-white text-xs')
