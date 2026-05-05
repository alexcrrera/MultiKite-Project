from nicegui import ui

def createTelemetry():

    vesselCountLabel = ui.label('Vessels: 0')
    lastUpdateLabel = ui.label('Last update: --')
    vesselInfoLabel = ui.label('Tracked vessel: ---')

    return vesselCountLabel, lastUpdateLabel, vesselInfoLabel