from nicegui import ui
from calculations import getAgeOfDataEntry

def buildGrid(globalData):
    grid = ui.aggrid({
    'columnDefs': [
        {'headerName': 'Vessel', 'field': 'name'},
        {'headerName': 'Latitude', 'field': 'lat'},
        {'headerName': 'Longitude', 'field': 'lon'},
        {'headerName': 'MMSI', 'field': 'mmsi'},
        {'headerName': 'Type', 'field': 'type'},
        {'headerName': 'Last Updated', 'field': 'last_updated'}
    ],
    'rowData': [
  
    ],
    'rowSelection': {'mode': 'multiRow'},
})
    globalData.vesselGrid = grid

def updateGrid(globalData):
    if not hasattr(globalData, 'vesselGrid'):
        print("Vessel grid not initialized yet.")
        return

    grid = globalData.vesselGrid
    vessels = globalData.vessels[-5:]  # last 5
    data = grid.options['rowData']
   # print("data before update:", data)

        
  #  grid.options['rowData'] = []
    grid.options['rowData'] = vessels

    
   # print(vessels)
    #grid.update()
    print(f"Updated vessel grid with {len(vessels)} vessels.")