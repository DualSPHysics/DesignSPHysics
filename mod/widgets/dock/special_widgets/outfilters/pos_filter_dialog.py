from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterPos
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_box
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class PosFilterDialog(BaseFilterDialog):

    def __init__(self, pos_filter, parent=None):
        super().__init__(base_filter=pos_filter, parent=parent)
        self.data: FilterPos = pos_filter
        self.point1_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point Min(X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_x_checkbox = QtWidgets.QCheckBox()
        self.point_y_input = SizeInput()
        self.point_y_checkbox = QtWidgets.QCheckBox()
        self.point_z_input = SizeInput()
        self.point_z_checkbox = QtWidgets.QCheckBox()

        for x in [self.point_label, self.point_x_input, self.point_x_checkbox, self.point_y_input,
                  self.point_y_checkbox,
                  self.point_z_input, self.point_z_checkbox]:
            self.point1_layout.addWidget(x)

        self.point2_layout = QHBoxLayout()
        self.point2_label = QtWidgets.QLabel(__("Point Max(X,Y,Z)"))
        self.point2_x_input = SizeInput()
        self.point2_x_checkbox = QtWidgets.QCheckBox()
        self.point2_y_input = SizeInput()
        self.point2_y_checkbox = QtWidgets.QCheckBox()
        self.point2_z_input = SizeInput()
        self.point2_z_checkbox = QtWidgets.QCheckBox()


        for x in [self.point2_label, self.point2_x_input, self.point2_x_checkbox, self.point2_y_input,
                  self.point2_y_checkbox, self.point2_z_input, self.point2_z_checkbox]:
            self.point2_layout.addWidget(x)

        self.main_layout.insertLayout(2, self.ftfollow_layout)
        self.main_layout.insertLayout(3, self.point1_layout)
        self.main_layout.insertLayout(4, self.point2_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point_x_input.setValue(self.data.pos_min[0])
        self.point_x_checkbox.setChecked(self.data.enable_pos_min[0])
        self.point_y_input.setValue(self.data.pos_min[1])
        self.point_y_checkbox.setChecked(self.data.enable_pos_min[1])
        self.point_z_input.setValue(self.data.pos_min[2])
        self.point_z_checkbox.setChecked(self.data.enable_pos_min[2])
        self.point2_x_input.setValue(self.data.pos_max[0])
        self.point2_x_checkbox.setChecked(self.data.enable_pos_max[0])
        self.point2_y_input.setValue(self.data.pos_max[1])
        self.point2_y_checkbox.setChecked(self.data.enable_pos_max[1])
        self.point2_z_input.setValue(self.data.pos_max[2])
        self.point2_z_checkbox.setChecked(self.data.enable_pos_max[2])

    def save_data(self):
        super().save_data()
        self.data.pos_min[0] = self.point_x_input.value()
        self.data.pos_min[1] = self.point_y_input.value()
        self.data.pos_min[2] = self.point_z_input.value()
        self.data.enable_pos_min[0] = self.point_x_checkbox.isChecked()
        self.data.enable_pos_min[1] = self.point_y_checkbox.isChecked()
        self.data.enable_pos_min[2] = self.point_z_checkbox.isChecked()
        self.data.pos_max[0] = self.point2_x_input.value()
        self.data.pos_max[1] = self.point2_y_input.value()
        self.data.pos_max[2] = self.point2_z_input.value()
        self.data.enable_pos_max[0] = self.point2_x_checkbox.isChecked()
        self.data.enable_pos_max[1] = self.point2_y_checkbox.isChecked()
        self.data.enable_pos_max[2] = self.point2_z_checkbox.isChecked()

        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
        #update_pos_filter
        size=[self.data.pos_max[0]-self.data.pos_min[0],self.data.pos_max[1]-self.data.pos_min[1],self.data.pos_max[2]-self.data.pos_min[2]]
        update_box(self.data.fc_object_name,self.data.pos_min,size)



