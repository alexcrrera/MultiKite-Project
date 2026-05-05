import sys
import os


# expose build/ as root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from nicegui import ui, app
from right_sidebar import buildRightSidebar
from globalData import GlobalData
from sidebar import buildSidebar
from footer import buildFooter
from header import buildHeader
from settings import buildSettings
from center import buildCenter
from map_utils import update_map
import asyncio

from css_utils import add_global_css

import requests


def startFrontend():
    print("Starting frontend process...")
    add_global_css()

    globalData = GlobalData()

    async def tick():
        while True:
          
           # print(f"Fetched")

            await asyncio.sleep(1 / globalData.fps)
    app.on_startup(tick)

    @ui.page('/')
   
    @ui.page('/')
    def mainPage():

        # TOP LEVEL ONLY
        buildHeader(globalData)
        buildSidebar(globalData)
        buildRightSidebar(globalData)
       # buildFooter()

        # ONLY this goes inside containers
        globalData.center_container = ui.column().classes(
    'w-full'
).style('''
    height: calc(100vh - 110px);

    overflow: hidden;
''')
        with globalData.center_container:
            buildCenter(globalData)

    title = globalData.app_name
    ui.run(title=title, port=8080)


if __name__ in {"__main__", "__mp_main__"}:
    startFrontend()