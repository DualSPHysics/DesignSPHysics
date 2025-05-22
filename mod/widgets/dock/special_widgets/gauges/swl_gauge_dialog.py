from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.swl_gauge import SWLGauge
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_line
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class SWLGaugeDialog(BaseGaugeDialog):

    def __init__(self, swl_gauge: SWLGauge, parent):
        super().__init__(base_gauge=swl_gauge,parent=parent)
        self.setWindowTitle(__("Surface Water Level Gauge"))
        self.point1_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        self.point2_layout = QHBoxLayout()
        self.point2_label = QtWidgets.QLabel(__("Point 2 (X,Y,Z)"))
        self.point2_x_input = SizeInput()
        self.point2_y_input = SizeInput()
        self.point2_z_input = SizeInput()
        self.conf_layout = QHBoxLayout()
        self.point_dp_label = QtWidgets.QLabel(__("Point dp"))
        self.point_dp_input = SizeInput()
        self.point_dp_coef_dp_checkbox = QtWidgets.QCheckBox(__("Coef DP"))
        self.mass_limit_label = QtWidgets.QLabel(__("Mass limit"))
        self.mass_limit_input = ValueInput() #Value
        self.mass_limit_coef_checkbox = QtWidgets.QCheckBox(__("Coef Mass Limit"))

        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input]:
            self.point1_layout.addWidget(x)
        for x in [self.point2_label, self.point2_x_input, self.point2_y_input, self.point2_z_input ]:
            self.point2_layout.addWidget(x)
        for x in [self.point_dp_label, self.point_dp_input, self.point_dp_coef_dp_checkbox,
                  self.mass_limit_label, self.mass_limit_input, self.mass_limit_coef_checkbox]:
            self.conf_layout.addWidget(x)

        self.point_dp_coef_dp_checkbox.stateChanged.connect(self.on_coef_dp_changed)

        self.main_layout.insertLayout(4,self.point1_layout)
        self.main_layout.insertLayout(5, self.point2_layout)
        self.main_layout.insertLayout(6, self.conf_layout)

        self.fill_values()

    def on_coef_dp_changed(self,enabled):
        if enabled:
            self.point_dp_input.setParent(None)
            self.point_dp_input = ValueInput()
            self.conf_layout.insertWidget(1, self.point_dp_input)
        else:
            self.point_dp_input.setParent(None)
            self.point_dp_input = SizeInput()
            self.conf_layout.insertWidget(1, self.point_dp_input)

    def fill_values(self):
        super().fill_values()

        self.point_x_input.setValue(self.data.point0[0])
        self.point_y_input.setValue(self.data.point0[1])
        self.point_z_input.setValue(self.data.point0[2])
        self.point2_x_input.setValue(self.data.point1[0])
        self.point2_y_input.setValue(self.data.point1[1])
        self.point2_z_input.setValue(self.data.point1[2])
        self.point_dp_coef_dp_checkbox.setChecked(self.data.point_dp_coef_dp)
        #self.on_coef_dp_changed(self.data.point_dp_coef_dp)
        self.point_dp_input.setValue(self.data.point_dp)
        self.mass_limit_input.setValue(self.data.mass_limit)
        self.mass_limit_coef_checkbox.setChecked(self.data.mass_limit_coef)



    def save_data(self):
        super().save_data()
        self.data.point0 = [self.point_x_input.value(),self.point_y_input.value(),
                            self.point_z_input.value()]
        self.data.point1 = [self.point2_x_input.value(),self.point2_y_input.value(),
                            self.point2_z_input.value()]
        self.data.point_dp = self.point_dp_input.value()
        self.data.point_dp_coef_dp = self.point_dp_coef_dp_checkbox.isChecked()
        self.data.mass_limit = self.mass_limit_input.value()
        self.data.mass_limit_coef = self.mass_limit_coef_checkbox.isChecked()
        if self.data.name:
            update_line(fc_object_name=self.data.fc_object_name, point1=self.data.point0, point2=self.data.point1)
            self.accept()
        else:
            warning_dialog("Please name your Gauge")


