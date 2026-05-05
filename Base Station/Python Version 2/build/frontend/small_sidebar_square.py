from nicegui import ui
from map_utils import create_map

class SmallSidebarSquare:
    def __init__(self, globalData):
        self.globalData = globalData
        self.container = None
        self.modeButton = None

    def update(self):
        self.container.clear()
        with self.container:
            if self.globalData.smallSquareMode == 0:
                self.globalData.smallMap = create_map(self.globalData, draw_toolbar=False)
            else:
                ui.image(self.globalData.camera_feed_image).classes('w-full h-full object-contain')

    def toggleMode(self):
        self.globalData.clickedSquareTab()
        icon = 'map' if self.globalData.smallSquareMode == 0 else 'videocam'
        self.modeButton.props(f'icon={icon}')
        self.update()

    def recenterMap(self):
        if hasattr(self.globalData, 'smallMap') and self.globalData.smallMap:
            self.globalData.smallMap.set_center((self.globalData.map.center_lat, self.globalData.map.center_lng))
            self.globalData.smallMap.zoom = self.globalData.map.zoom

    def sync_tiles(self):
        """Safe tile sync - NO rebuild, just tile_layer update."""
        self.update()  # Small map
        
        # Update main map tiles only
        if hasattr(self.globalData, 'map') and self.globalData.map:
            tile_url = self.globalData.map_tiles[self.globalData.mapMode]
            self.globalData.map.tile_layer(url_template=tile_url)
            ui.notify(f'Tiles synced: {self.globalData.mapMode}')

    def build(self):
        with ui.column().classes('w-full'):
            with ui.row().classes('w-full justify-between items-center'):
                self.modeButton = ui.button(icon='videocam', on_click=self.toggleMode
                ).props('flat text-white').tooltip('Toggle').classes('text-white')

                ui.button(icon='my_location', on_click=self.recenterMap
                ).props('flat text-white').tooltip('Recenter').classes('text-white')

                with ui.button(icon='layers').props('flat text-white').tooltip('Sync tiles').classes('text-white'):
                    with ui.menu().props('auto-close'):
                        toggle = ui.toggle(
                            list(self.globalData.map_tiles.keys()),
                            value=self.globalData.mapMode
                        ).props('exclusive')
                        toggle.bind_value(self.globalData, 'mapMode')
                        toggle.on('update:model-value', self.sync_tiles)

            self.container = ui.element('div').classes('w-full aspect-square overflow-hidden')
        self.update()
