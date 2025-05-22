from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.force_gauge import ForceGauge
from mod.tools.dialog_tools import warning_dialog
from mod.enums import ObjectType
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames


class ForceGaugeDialog(BaseGaugeDialog):

    def __init__(self, force_gauge: ForceGauge, parent):
        super().__init__(base_gauge=force_gauge,parent=parent)

        self.setWindowTitle(__("Force Gauge"))

        self.force_layout = QHBoxLayout()
        self.target_label = QtWidgets.QLabel(__("Target MK"))
        self.target_mk_input = MkSelectInputWithNames(ObjectType.BOUND)
        for x in [self.target_label,self.target_mk_input]:
            self.force_layout.addWidget(x)

        self.main_layout.insertLayout(4,self.force_layout)

        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.target_mk_input.set_mk_index(self.data.target)

    def save_data(self):
        super().save_data()
        self.data.target=self.target_mk_input.get_mk_value()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Gauge")



