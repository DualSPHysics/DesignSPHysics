from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog


class GaugeDefaultsDialog(BaseGaugeDialog):

    def __init__(self, base_gauge, parent):
        super().__init__(base_gauge, parent)
        self.setWindowTitle(__("Gauge defaults"))
        self.fill_values()

    def fill_values(self):
        super().fill_values()

    def save_data(self):
        super().save_data()
        self.accept()