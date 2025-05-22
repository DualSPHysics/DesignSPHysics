from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterPlane
from mod.tools.dialog_tools import warning_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class PlaneFilterDialog(BaseFilterDialog):

    def __init__(self,plane_filter,parent=None):
        super().__init__(base_filter=plane_filter,parent=parent)
        self.data:FilterPlane=plane_filter
        self.pos_layout = QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point (X,Y,Z)"))
        self.point_x_input = SizeInput()
        self.point_y_input = SizeInput()
        self.point_z_input = SizeInput()
        self.vector_layout=QHBoxLayout()
        self.vector_label = QtWidgets.QLabel(__("Vector (X,Y,Z)"))
        self.vector_x_input = ValueInput()
        self.vector_y_input = ValueInput()
        self.vector_z_input = ValueInput()
        self.distance_layout=QHBoxLayout()
        self.point_distance_label=QtWidgets.QLabel(__("Distance: "))
        self.point_distance_checkbox=QtWidgets.QCheckBox(__("Use"))
        self.distance_input=SizeInput()

        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input]:
            self.pos_layout.addWidget(x)

        for x in [self.vector_label, self.vector_x_input, self.vector_y_input, self.vector_z_input]:
            self.vector_layout.addWidget(x)

        for x in [ self.point_distance_label, self.point_distance_checkbox, self.distance_input]:
            self.distance_layout.addWidget(x)

        self.main_layout.insertLayout(2, self.ftfollow_layout)
        self.main_layout.insertLayout(3, self.pos_layout)
        self.main_layout.insertLayout(4, self.vector_layout)
        self.main_layout.insertLayout(5, self.distance_layout)

        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.point_x_input.setValue(self.data.point[0])
        self.point_y_input.setValue(self.data.point[1])
        self.point_z_input.setValue(self.data.point[2])
        self.vector_x_input.setValue(self.data.vector[0])
        self.vector_y_input.setValue(self.data.vector[1])
        self.vector_z_input.setValue(self.data.vector[2])
        self.point_distance_checkbox.setChecked(self.data.distance_enabled)
        self.distance_input.setValue(self.data.distance)

    def save_data(self):
        super().save_data()
        self.data.point[0] = self.point_x_input.value()
        self.data.point[1] = self.point_y_input.value()
        self.data.point[2] = self.point_z_input.value()
        self.data.vector[0] = self.vector_x_input.value()
        self.data.vector[1] = self.vector_y_input.value()
        self.data.vector[2] = self.vector_z_input.value()
        self.data.distance_enabled = self.point_distance_checkbox.isChecked()
        self.data.distance = self.distance_input.value()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
        #self.data.fc_object_name = create_parts_out_plane(self.data)
