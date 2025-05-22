from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.max_z_gauge import MaxZGauge
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_line
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.size_input import SizeInput


class MaxZGaugeDialog(BaseGaugeDialog):

    def __init__(self, max_z_gauge: MaxZGauge, parent):
        super().__init__(base_gauge=max_z_gauge,parent=parent)

        self.setWindowTitle(__("Max Z Gauge"))

        self.max_z_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point0 (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input]:
            self.max_z_layout.addWidget(x)
        self.max_z_height_layout=QHBoxLayout()
        self.height_label = QtWidgets.QLabel(__("Height"))
        self.height_input = SizeInput()
        self.dist_limit_label = QtWidgets.QLabel(__("Limit distance"))
        self.dist_limit_input = SizeInput()
        for x in [self.height_label,  self.height_input, self.dist_limit_label, self.dist_limit_input]:
            self.max_z_height_layout.addWidget(x)

        self.main_layout.insertLayout(4,self.max_z_layout)
        self.main_layout.insertLayout(5, self.max_z_height_layout)

        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point_x_input.setValue(self.data.point0[0])
        self.point_y_input.setValue(self.data.point0[1])
        self.point_z_input.setValue(self.data.point0[2])
        self.height_input.setValue(self.data.height)
        self.dist_limit_input.setValue(self.data.dist_limit)
        #Create gauge object


    def save_data(self):
        super().save_data()
        self.data.point0 = [self.point_x_input.value(),self.point_y_input.value(),
                            self.point_z_input.value()]
        self.data.height = self.height_input.value()
        self.data.dist_limit = self.dist_limit_input.value()

        if self.data.name:
            update_line(fc_object_name=self.data.fc_object_name, point1=self.data.point0, point2=[self.data.point0[0],
                                                                                                  self.data.point0[1],
                                                                                                  self.data.point0[
                                                                                                      2] + self.data.height])
            self.accept()
        else:
            warning_dialog("Please name your Gauge")



