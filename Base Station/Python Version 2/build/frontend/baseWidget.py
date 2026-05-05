class BaseWidget:
    def __init__(self, globalData, config):
        self.globalData = globalData
        self.config = config
        self.inputs = config.get("inputs", [])
        self.container = None

    def mount(self, parent):
        self.container = parent
        with self.container:
            self.build()

    def build(self):
        raise NotImplementedError

    def update(self, data):
        # extract only relevant indices
        values = [data[i] for i in self.inputs if i < len(data)]
        self.process(values)

    def process(self, values):
        pass

    def destroy(self):
        if self.container:
            self.container.clear()