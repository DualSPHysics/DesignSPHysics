from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.flow_gauge import FlowGauge
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_flow_gauge_box
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class FlowGaugeDialog(BaseGaugeDialog):

    def __init__(self, flow_gauge: FlowGauge, parent):
        super().__init__(base_gauge=flow_gauge, parent=parent)

        self.setWindowTitle(__("Flow Gauge"))

        self.flow_layout = QtWidgets.QVBoxLayout()
        self.first_row_layout = QHBoxLayout()
        self.second_row_layout = QHBoxLayout()
        self.third_row_layout = QHBoxLayout()
        self.fourth_row_layout = QHBoxLayout()
        self.fifth_row_layout = QHBoxLayout()
        self.sixth_row_layout = QHBoxLayout()

        self.point_label = QtWidgets.QLabel(__("Point (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        self.dirdat_label = QtWidgets.QLabel(__("Dir Vector (X,Y,Z)"))
        self.dirdat_x_input = ValueInput()
        self.dirdat_y_input = ValueInput()
        self.dirdat_z_input = ValueInput()

        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input,
                  self.dirdat_label, self.dirdat_x_input, self.dirdat_y_input, self.dirdat_z_input]:
            self.first_row_layout.addWidget(x)
        self.vec1_label = QtWidgets.QLabel(__("Vec 1 (X,Y,Z)"))
        self.vec1_x_input = ValueInput()
        self.vec1_y_input = ValueInput()
        self.vec1_z_input = ValueInput()
        self.vec2_label = QtWidgets.QLabel(__("Vec 2 (X,Y,Z)"))
        self.vec2_x_input = ValueInput()
        self.vec2_y_input = ValueInput()
        self.vec2_z_input = ValueInput()

        for x in [self.vec1_label, self.vec1_x_input, self.vec1_y_input, self.vec1_z_input,
                  self.vec2_label, self.vec2_x_input, self.vec2_y_input, self.vec2_z_input,
                  ]:
            self.second_row_layout.addWidget(x)
        self.size1_label = QtWidgets.QLabel(__("Size 1: Length, Point distance"))
        self.size1_length_input = SizeInput()
        self.size1_dp_input = SizeInput()
        self.size2_label = QtWidgets.QLabel(__("Size 2: Length, Point distance"))
        self.size2_length_input = SizeInput()
        self.size2_dp_input = SizeInput()
        for x in [self.size1_label, self.size1_length_input, self.size1_dp_input, self.size2_label,
                  self.size2_length_input, self.size2_dp_input]:
            self.third_row_layout.addWidget(x)
        for x in []:
            self.fourth_row_layout.addWidget(x)

        for x in []:
            self.fifth_row_layout.addWidget(x)
        self.buffersize_label = QtWidgets.QLabel(__("Buffer size"))
        self.buffersize_input = IntValueInput()
        self.kclimit_label = QtWidgets.QLabel(__("Kernel correction limit"))
        self.kclimit_input = ValueInput()
        self.kclimit_enable_checkbox = QtWidgets.QCheckBox(__("Enabled"))

        for x in [self.buffersize_label, self.buffersize_input,self.kclimit_label, self.kclimit_input,
                  self.kclimit_enable_checkbox,]:
            self.sixth_row_layout.addWidget(x)

        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout,
                  self.fifth_row_layout, self.sixth_row_layout]:
            self.flow_layout.addLayout(x)

        self.main_layout.insertLayout(4,self.flow_layout)

        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point_x_input.setValue(self.data.point0[0])
        self.point_y_input.setValue(self.data.point0[1])
        self.point_z_input.setValue(self.data.point0[2])
        self.vec1_x_input.setValue(self.data.vec1[0])
        self.vec1_y_input.setValue(self.data.vec1[1])
        self.vec1_z_input.setValue(self.data.vec1[2])
        self.vec2_x_input.setValue(self.data.vec2[0])
        self.vec2_y_input.setValue(self.data.vec2[1])
        self.vec2_z_input.setValue(self.data.vec2[2])
        self.size1_length_input.setValue(self.data.size1_length)
        self.size2_length_input.setValue(self.data.size2_length)
        self.size1_dp_input.setValue(self.data.size1_distpt)
        self.size2_dp_input.setValue(self.data.size2_distpt)
        self.dirdat_x_input.setValue(self.data.dirdat[0])
        self.dirdat_y_input.setValue(self.data.dirdat[1])
        self.dirdat_z_input.setValue(self.data.dirdat[2])
        self.buffersize_input.setValue(self.data.buffersize)
        self.kclimit_input.setValue(self.data.kclimit)
        self.kclimit_enable_checkbox.setChecked(self.data.kclimit_enable)

    def save_data(self):
        super().save_data()
        self.data.point0 = [self.point_x_input.value(),self.point_y_input.value(),
                           self.point_z_input.value()]
        self.data.vec1 = [self.vec1_x_input.value(),self.vec1_y_input.value(),
                          self.vec1_z_input.value()]
        self.data.vec2 = [self.vec2_x_input.value(),self.vec2_y_input.value(),
                          self.vec2_z_input.value()]
        self.data.size1_length = self.size1_length_input.value()
        self.data.size1_distpt = self.size1_dp_input.value()
        self.data.size2_length = self.size2_length_input.value()
        self.data.size2_distpt = self.size2_dp_input.value()

        self.data.dirdat = [self.dirdat_x_input.value(),self.dirdat_y_input.value(),
                            self.dirdat_z_input.value()]
        self.data.buffersize = self.buffersize_input.value()
        self.data.kclimit = self.kclimit_input.value()
        self.data.kclimit_enable = self.kclimit_enable_checkbox.isChecked()

        if self.data.name:
            update_flow_gauge_box(self.data.fc_object_name, self.data)
            self.accept()
        else:
            warning_dialog("Please name your Gauge")
