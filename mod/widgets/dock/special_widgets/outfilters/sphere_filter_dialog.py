from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterSphere
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_sphere
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class SphereFilterDialog(BaseFilterDialog):

    def __init__(self,sphere_filter,parent=None):
        super().__init__(base_filter=sphere_filter,parent=parent)
        self.data:FilterSphere=sphere_filter
        self.pos_layout = QHBoxLayout()
        self.center_label = QtWidgets.QLabel(__("Center (X,Y,Z)"))
        self.center_x_input = SizeInput()
        self.center_y_input = SizeInput()
        self.center_z_input = SizeInput()
        self.radius_layout=QHBoxLayout()
        self.radius_label=QtWidgets.QLabel(__("Radius: "))
        self.radius_input=SizeInput()

        for x in [self.center_label, self.center_x_input, self.center_y_input, self.center_z_input ]:
            self.pos_layout.addWidget(x)

        for x in [self.radius_label, self.radius_input]:
            self.radius_layout.addWidget(x)

        self.main_layout.insertLayout(2, self.ftfollow_layout)
        self.main_layout.insertLayout(3 ,self.pos_layout)
        self.main_layout.insertLayout(4, self.radius_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.center_x_input.setValue(self.data.center[0])
        self.center_y_input.setValue(self.data.center[1])
        self.center_z_input.setValue(self.data.center[2])
        self.radius_input.setValue(self.data.radius)

    def save_data(self):
        super().save_data()
        self.data.center[0] = self.center_x_input.value()
        self.data.center[1] = self.center_y_input.value()
        self.data.center[2] = self.center_z_input.value()
        self.data.radius = self.radius_input.value()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
        #update sphere filter self.data.fc_object_name = create_parts_out_sphere(self.data)
        update_sphere(self.data.fc_object_name,self.data.center,self.data.radius)

