from nicegui import ui, app
from right_sidebar import buildRightSidebar
from globalData import GlobalData
from sidebar import buildSidebar
from footer import buildFooter
from header import buildHeader
from settings import buildSettings
from center import buildCenter
from map_utils import update_map  # ADD THIS IMPORT
import asyncio

from css_utils import add_global_css

add_global_css()  # Ensure CSS is added at startup

globalData = GlobalData()

async def backend_loop():
    while True:
        print("Backend tick - monitoring USV...")
        globalData.update_sensors()  # Your existing sensor logic
        
        # ADD THIS LINE: Update map from new sensor data
        if hasattr(globalData, 'map_ref') and globalData.map_ref:
            update_map(globalData)
            
        await asyncio.sleep(1)

app.on_startup(backend_loop)

@ui.page('/')
def main_page():
    buildHeader(globalData)
    buildSidebar(globalData)
    buildRightSidebar(globalData)

    globalData.center_container = ui.column().classes('w-full flex-1 center-container')
    with globalData.center_container:
        buildCenter(globalData)  # Ensure create_map() called here

    buildFooter()

ui.run(title='USV Control Panel', port=8080)
