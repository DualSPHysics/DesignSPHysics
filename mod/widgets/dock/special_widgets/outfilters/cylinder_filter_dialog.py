from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterCylinder
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_cylinder
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class CylinderFilterDialog(BaseFilterDialog):

    def __init__(self,cylinder_filter,parent=None):
        super().__init__(base_filter=cylinder_filter,parent=parent)
        self.data:FilterCylinder=cylinder_filter
        self.point1_layout = QHBoxLayout()
        self.point1_label = QtWidgets.QLabel(__("Point 1 (X,Y,Z)"))
        self.point1_x_input = SizeInput()
        self.point1_y_input = SizeInput()
        self.point1_z_input = SizeInput()
        self.point2_layout=QHBoxLayout()
        self.point2_label = QtWidgets.QLabel(__("Point 2 (X,Y,Z)"))
        self.point2_x_input = SizeInput()
        self.point2_y_input = SizeInput()
        self.point2_z_input = SizeInput()
        self.radius_layout = QHBoxLayout()
        self.radius_label=QtWidgets.QLabel(__("Radius: "))
        self.radius_input=SizeInput()

        for x in [self.point1_label, self.point1_x_input, self.point1_y_input, self.point1_z_input]:
            self.point1_layout.addWidget(x)

        for x in [self.point2_label,self.point2_x_input, self.point2_y_input, self.point2_z_input]:
            self.point2_layout.addWidget(x)

        for x in [self.radius_label, self.radius_input]:
            self.radius_layout.addWidget(x)

        self.main_layout.insertLayout(2, self.ftfollow_layout)
        self.main_layout.insertLayout(3,self.point1_layout)
        self.main_layout.insertLayout(4, self.point2_layout)
        self.main_layout.insertLayout(5, self.radius_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point1_x_input.setValue(self.data.point1[0])
        self.point1_y_input.setValue(self.data.point1[1])
        self.point1_z_input.setValue(self.data.point1[2])
        self.point2_x_input.setValue(self.data.point2[0])
        self.point2_y_input.setValue(self.data.point2[1])
        self.point2_z_input.setValue(self.data.point2[2])
        self.radius_input.setValue(self.data.radius)

    def save_data(self):
        super().save_data()
        self.data.point1[0] = self.point1_x_input.value()
        self.data.point1[1] = self.point1_y_input.value()
        self.data.point1[2] = self.point1_z_input.value()
        self.data.point2[0] = self.point2_x_input.value()
        self.data.point2[1] = self.point2_y_input.value()
        self.data.point2[2] = self.point2_z_input.value()
        self.data.radius = self.radius_input.value()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
        update_cylinder(self.data.fc_object_name,self.data.point1,self.data.point2,self.data.radius)
