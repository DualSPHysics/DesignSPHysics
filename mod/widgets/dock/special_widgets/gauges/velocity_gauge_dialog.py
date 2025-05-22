from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.velocity_gauge import VelocityGauge
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_sphere
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.size_input import SizeInput


class VelocityGaugeDialog(BaseGaugeDialog):

    def __init__(self, velocity_gauge: VelocityGauge, parent):
        super().__init__(base_gauge=velocity_gauge, parent=parent)

        self.setWindowTitle(__("Velocity Gauge"))

        self.velocity_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input]:
            self.velocity_layout.addWidget(x)

        self.main_layout.insertLayout(4, self.velocity_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point_x_input.setValue(self.data.point0[0])
        self.point_y_input.setValue(self.data.point0[1])
        self.point_z_input.setValue(self.data.point0[2])

    def save_data(self):
        super().save_data()
        self.data.point0 = [self.point_x_input.value(), self.point_y_input.value(),
                            self.point_z_input.value()]
        if self.data.name:
            update_sphere(fc_object_name=self.data.fc_object_name, center=self.data.point0, radius=0.01)
            self.accept()
        else:
            warning_dialog("Please name your Gauge")

