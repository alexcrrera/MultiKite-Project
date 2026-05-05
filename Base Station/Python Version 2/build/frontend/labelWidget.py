from nicegui import ui
from baseWidget import BaseWidget


class LabelWidget(BaseWidget):
    def build(self):
        title = self.config.get("title", "")
        self.label = ui.label(f"{title}: --")

    def process(self, values):
        if values:
            self.label.set_text(f"{self.config.get('title','')}: {values[0]}")