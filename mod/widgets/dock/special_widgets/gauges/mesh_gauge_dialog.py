from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.gauges.mesh_gauge import MeshGauge
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_mesh_gauge_box
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.gauges.base_gauge_dialog import BaseGaugeDialog
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class MeshGaugeDialog(BaseGaugeDialog):

    def __init__(self, mesh_gauge: MeshGauge, parent):
        super().__init__(base_gauge=mesh_gauge, parent=parent)

        self.setWindowTitle(__("Mesh Gauge"))

        self.mesh_layout = QtWidgets.QVBoxLayout()
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
        self.vec1_label = QtWidgets.QLabel(__("Vec 1 (X,Y,Z)"))
        self.vec1_x_input = ValueInput()
        self.vec1_y_input = ValueInput()
        self.vec1_z_input = ValueInput()
        for x in [self.point_label, self.point_x_input, self.point_y_input, self.point_z_input, self.vec1_label,
                  self.vec1_x_input, self.vec1_y_input, self.vec1_z_input]:
            self.first_row_layout.addWidget(x)
        self.vec2_label = QtWidgets.QLabel(__("Vec 2 (X,Y,Z)"))
        self.vec2_x_input = ValueInput()
        self.vec2_y_input = ValueInput()
        self.vec2_z_input = ValueInput()
        self.vec3_label = QtWidgets.QLabel(__("Vec 3 (X,Y,Z)"))
        self.vec3_x_input = ValueInput()
        self.vec3_y_input = ValueInput()
        self.vec3_z_input = ValueInput()
        for x in [self.vec2_label, self.vec2_x_input, self.vec2_y_input, self.vec2_z_input, self.vec3_label,
                  self.vec3_x_input, self.vec3_y_input, self.vec3_z_input]:
            self.second_row_layout.addWidget(x)
        self.size1_label = QtWidgets.QLabel(__("Size 1: Length, Point distance"))
        self.size1_length_input = SizeInput()
        self.size1_dp_input = SizeInput()
        self.size2_label = QtWidgets.QLabel(__("Size 2: Length, Point distance"))
        self.size2_length_input = SizeInput()
        self.size2_dp_input = SizeInput()
        self.size3_label = QtWidgets.QLabel(__("Size 3: Length, Point distance"))
        self.size3_length_input = SizeInput()
        self.size3_dp_input = SizeInput()
        for x in [self.size1_label, self.size1_length_input, self.size1_dp_input, self.size2_label,
                  self.size2_length_input, self.size2_dp_input, self.size3_label, self.size3_length_input,
                  self.size3_dp_input]:
            self.third_row_layout.addWidget(x)
        self.dirdat_label = QtWidgets.QLabel("Direction Vector")
        self.dirdat_x_input = ValueInput()
        self.dirdat_y_input = ValueInput()
        self.dirdat_z_input = ValueInput()
        self.mass_limit_label = QtWidgets.QLabel(__("Mass limit"))
        self.mass_limit_input = ValueInput()
        self.mass_limit_coef_checkbox = QtWidgets.QCheckBox(__("Coef Mass Limit"))
        for x in [self.dirdat_label, self.dirdat_x_input, self.dirdat_y_input, self.dirdat_z_input,
                  self.mass_limit_label, self.mass_limit_input, self.mass_limit_coef_checkbox]:
            self.fourth_row_layout.addWidget(x)
        self.output_data_label = QtWidgets.QLabel(__("Output data"))
        self.output_data_vel_checkbox = QtWidgets.QCheckBox(__("Velocity"))
        self.output_data_vel_dir_checkbox = QtWidgets.QCheckBox(__("Velocity Direction"))
        self.output_data_rhop_checkbox = QtWidgets.QCheckBox(__("Density"))
        self.output_data_zsurf_checkbox = QtWidgets.QCheckBox(__("Water height"))
        self.output_fmt_label = QtWidgets.QLabel(__("Output format"))
        self.output_fmt_bin_checkbox = QtWidgets.QCheckBox(__(".bin"))
        self.output_fmt_csv_checkbox = QtWidgets.QCheckBox(__(".csv"))
        for x in [self.output_data_label, self.output_data_vel_checkbox, self.output_data_vel_dir_checkbox,
                  self.output_data_rhop_checkbox, self.output_data_zsurf_checkbox, self.output_fmt_label,
                  self.output_fmt_bin_checkbox, self.output_fmt_csv_checkbox]:
            self.fifth_row_layout.addWidget(x)
        self.buffersize_label = QtWidgets.QLabel(__("Buffer size"))
        self.buffersize_input = IntValueInput()
        self.kclimit_label = QtWidgets.QLabel(__("Kernel correction limit"))
        self.kclimit_input = ValueInput()
        self.kclimit_enable_checkbox = QtWidgets.QCheckBox(__("Enabled"))
        self.kc_dummy_label = QtWidgets.QLabel(__("Kernel correction dummy value"))
        self.kc_dummy_input = ValueInput()
        self.kc_dummy_enable_checkbox = QtWidgets.QCheckBox(__("Enabled"))

        for x in [self.buffersize_label, self.buffersize_input, self.kclimit_label, self.kclimit_input,
                  self.kclimit_enable_checkbox, self.kc_dummy_label, self.kc_dummy_input,
                  self.kc_dummy_enable_checkbox]:
            self.sixth_row_layout.addWidget(x)

        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout,
                  self.fifth_row_layout, self.sixth_row_layout]:
            self.mesh_layout.addLayout(x)

        self.main_layout.insertLayout(4,self.mesh_layout)

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
        self.vec3_x_input.setValue(self.data.vec3[0])
        self.vec3_y_input.setValue(self.data.vec3[1])
        self.vec3_z_input.setValue(self.data.vec3[2])
        self.size1_length_input.setValue(self.data.size1_length)
        self.size2_length_input.setValue(self.data.size2_length)
        self.size3_length_input.setValue(self.data.size3_length)
        self.size1_dp_input.setValue(self.data.size1_distpt)
        self.size2_dp_input.setValue(self.data.size2_distpt)
        self.size3_dp_input.setValue(self.data.size3_distpt)
        self.dirdat_x_input.setValue(self.data.dirdat[0])
        self.dirdat_y_input.setValue(self.data.dirdat[1])
        self.dirdat_z_input.setValue(self.data.dirdat[2])
        self.mass_limit_input.setValue(self.data.mass_limit)
        self.mass_limit_coef_checkbox.setChecked(self.data.mass_limit_coef)
        self.output_data_vel_checkbox.setChecked(self.data.output_data_vel)
        self.output_data_vel_dir_checkbox.setChecked(self.data.output_data_veldir)
        self.output_data_rhop_checkbox.setChecked(self.data.output_data_rhop)
        self.output_data_zsurf_checkbox.setChecked(self.data.output_data_zsurf)
        self.output_fmt_bin_checkbox.setChecked(self.data.output_fmt_bin)
        self.output_fmt_csv_checkbox.setChecked(self.data.output_fmt_csv)
        self.buffersize_input.setValue(self.data.buffersize)
        self.kclimit_input.setValue(self.data.kclimit)
        self.kclimit_enable_checkbox.setChecked(self.data.kclimit_enable)
        self.kc_dummy_input.setValue(self.data.kc_dummy)
        self.kc_dummy_enable_checkbox.setChecked(self.data.kc_dummy_enable)

    def save_data(self):
        super().save_data()
        self.data.point0 = [self.point_x_input.value(),self.point_y_input.value(),
                           self.point_z_input.value()]
        self.data.vec1 = [self.vec1_x_input.value(),self.vec1_y_input.value(),
                          self.vec1_z_input.value()]
        self.data.vec2 = [self.vec2_x_input.value(),self.vec2_y_input.value(),
                          self.vec2_z_input.value()]
        self.data.vec3 = [self.vec3_x_input.value(),self.vec3_y_input.value(),
                          self.vec3_z_input.value()]
        self.data.size1_length = self.size1_length_input.value()
        self.data.size1_distpt = self.size1_dp_input.value()
        self.data.size2_length = self.size2_length_input.value()
        self.data.size2_distpt = self.size2_dp_input.value()
        self.data.size3_length = self.size3_length_input.value()
        self.data.size3_distpt = self.size3_dp_input.value()

        self.data.dirdat = [self.dirdat_x_input.value(),self.dirdat_y_input.value(),
                            self.dirdat_z_input.value()]
        self.data.mass_limit = self.mass_limit_input.value()
        self.data.mass_limit_coef = self.mass_limit_coef_checkbox.isChecked()
        self.data.output_data_vel = self.output_data_vel_checkbox.isChecked()
        self.data.output_data_veldir = self.output_data_vel_dir_checkbox.isChecked()
        self.data.output_data_rhop = self.output_data_rhop_checkbox.isChecked()
        self.data.output_data_zsurf = self.output_data_zsurf_checkbox.isChecked()
        self.data.output_data=""
        if self.data.output_data_vel:
            self.data.output_data = self.data.output_data + "vel,"
        if self.data.output_data_veldir:
            self.data.output_data = self.data.output_data + "veldir,"
        if self.data.output_data_rhop:
            self.data.output_data = self.data.output_data + "rhop,"
        if self.data.output_data_zsurf:
            self.data.output_data = self.data.output_data + "zsurf,"

        self.data.output_fmt_bin = self.output_fmt_bin_checkbox.isChecked()
        self.data.output_fmt_csv = self.output_fmt_csv_checkbox.isChecked()
        self.data.output_fmt=""
        if self.data.output_fmt_csv:
            self.data.output_fmt = self.data.output_fmt + "csv,"
        if self.data.output_fmt_bin:
            self.data.output_fmt = self.data.output_fmt + "bin"
        self.data.buffersize = self.buffersize_input.value()
        self.data.kclimit = self.kclimit_input.value()
        self.data.kclimit_enable = self.kclimit_enable_checkbox.isChecked()
        self.data.kc_dummy = self.kc_dummy_input.value()
        self.data.kc_dummy_enable = self.kc_dummy_enable_checkbox.isChecked()
        if self.data.name:
            update_mesh_gauge_box(self.data.fc_object_name, self.data)
            self.accept()
        else:
            warning_dialog("Please name your Gauge")
