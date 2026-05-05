from nicegui import ui

class GridManager:
    def __init__(self, globalData):
        self.globalData = globalData
        self.rows = globalData.gridRows
        self.cols = globalData.gridCols

        self.cells = {}          # (r,c) -> container
        self.widgets = {}        # (r,c) -> widget instance
        self.nextIndex = 0       # append pointer (linear)

    def build(self):
        with ui.element('div').classes('w-full h-full').style(f'''
            display:grid;
            grid-template-columns: repeat({self.cols}, minmax(0,1fr));
            grid-template-rows: repeat({self.rows}, 1fr);
        '''):

            for r in range(self.rows):
                for c in range(self.cols):

                    with ui.element('div').style(
                        'min-width:0; min-height:0; border:1px solid #1e3a8a; overflow:hidden;'
                    ):
                        cell = ui.element('div').classes('w-full h-full').style(
                            'min-width:0; min-height:0;'
                        )

                        self.cells[(r, c)] = cell

    def _indexToCoord(self, index):
        r = index // self.cols
        c = index % self.cols
        return (r, c)

    def appendWidget(self, widget):
        if self.nextIndex >= self.rows * self.cols:
            return False  # grid full

        coord = self._indexToCoord(self.nextIndex)
        self.nextIndex += 1

        self.setWidget(coord, widget)
        return True

    def setWidget(self, coord, widget):
        if coord not in self.cells:
            return

        container = self.cells[coord]

        # destroy existing
        if coord in self.widgets:
            self.widgets[coord].destroy()

        container.clear()

        widget.mount(container)
        self.widgets[coord] = widget

    def removeWidget(self, coord):
        if coord in self.widgets:
            self.widgets[coord].destroy()
            del self.widgets[coord]
            self.cells[coord].clear()

    def clear(self):
        for coord in list(self.widgets.keys()):
            self.removeWidget(coord)
        self.nextIndex = 0

    def updateAll(self, data):
        for w in self.widgets.values():
            w.update(data)