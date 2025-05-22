from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.dataobjects.inletoutlet.inlet_outlet_elevation_info import InletOutletElevationInfo
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class ImposezsurfFixedWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()


        self.zsurf_layout = QtWidgets.QHBoxLayout()
        self.zsurf_label = QtWidgets.QLabel(__("Surface"))
        self.zsurf_input = SizeInput()
        self.remove_checkbox = QtWidgets.QCheckBox(__("Remove particles above surface"))
        self.zsurf_layout.addWidget(self.zsurf_label)
        self.zsurf_layout.addWidget(self.zsurf_input)

        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addLayout(self.zsurf_layout)

        self.setLayout(self.main_layout)

    def fill_values(self, elevation_info):
        self.remove_checkbox.setChecked(elevation_info.remove)
        self.zsurf_input.setValue(elevation_info.zsurf)

    def to_dict(self):
        values = {}
        values["remove"] = self.remove_checkbox.isChecked()
        values["zsurf"] = self.zsurf_input.value()
        return values


class ImposezsurfVariableWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.savevtk_checkbox = QtWidgets.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtWidgets.QCheckBox(__("Remove particles above surface"))


        self.zsurf_table = QtWidgets.QTableWidget(60, 2)
        self.zsurf_table.setHorizontalHeaderLabels([__("Time (s)"), __("Surface level (m)")])
        self.zsurf_table.verticalHeader().setVisible(False)
        self.zsurf_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addWidget(self.zsurf_table)

        self.setLayout(self.main_layout)

    def fill_values(self, elevation_info):
        self.savevtk_checkbox.setChecked(elevation_info.savevtk)
        self.remove_checkbox.setChecked(elevation_info.remove)
        currentTableRow = 0
        for time, value in elevation_info.zsurftimes:
            self.zsurf_table.setItem(currentTableRow, 0, QtWidgets.QTableWidgetItem(str(time)))
            self.zsurf_table.setItem(currentTableRow, 1, QtWidgets.QTableWidgetItem(str(value)))
            currentTableRow += 1

    def to_dict(self):
        values = {}
        values["savevtk"] = self.savevtk_checkbox.isChecked()
        values["remove"] = self.remove_checkbox.isChecked()
        values["zsurftimes"] = []
        table = self.zsurf_table
        for i in range(0, table.rowCount()):
            if not table.item(i, 0) or not table.item(i, 1):
                continue
            time_as_string = table.item(i, 0).text()
            value_as_string = table.item(i, 1).text()
            if time_as_string != "" and value_as_string != "":
                values["zsurftimes"].append((float(time_as_string), float(value_as_string)))
        return values


class ImposezsurfVariableFromFileWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.savevtk_checkbox = QtWidgets.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtWidgets.QCheckBox(__("Remove particles above surface"))

        self.zsurf_layout = QtWidgets.QHBoxLayout()
        self.zsurf_label = QtWidgets.QLabel(__("File Path"))
        self.zsurf_input = QtWidgets.QLineEdit()
        self.zsurf_button = QtWidgets.QPushButton(__("Browse..."))
        self.zsurf_layout.addWidget(self.zsurf_label)
        self.zsurf_layout.addWidget(self.zsurf_input)
        self.zsurf_layout.addWidget(self.zsurf_button)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        # self.main_layout.addLayout(self.zbottom_layout)
        self.main_layout.addLayout(self.zsurf_layout)

        self.zsurf_button.clicked.connect(self.on_browse_button)

        self.setLayout(self.main_layout)

    def on_browse_button(self):
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"),
                                                                Case.the().info.last_used_directory,
                                                                "CSV Files (*.csv)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.zsurf_input.setText(file_name_temp)

    def fill_values(self, elevation_info):
        self.savevtk_checkbox.setChecked(elevation_info.savevtk)
        self.remove_checkbox.setChecked(elevation_info.remove)
        self.zsurf_input.setText(elevation_info.zsurffile)

    def to_dict(self):
        values = {}
        values["savevtk"] = self.savevtk_checkbox.isChecked()
        values["remove"] = self.remove_checkbox.isChecked()
        values["zsurffile"] = self.zsurf_input.text()
        return values


class ImposezsurfVariableMeshDataWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.savevtk_checkbox = QtWidgets.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtWidgets.QCheckBox(__("Remove particles above surface"))


        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel(__("File Path"))
        self.file_input = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton(__("Browse..."))
        self.file_layout.addWidget(self.file_label)
        self.file_layout.addWidget(self.file_input)
        self.file_layout.addWidget(self.browse_button)

        self.time_layout = QtWidgets.QHBoxLayout()
        self.initial_time_label = QtWidgets.QLabel(__("Initial time"))
        self.initial_time_input = TimeInput(min_val=0)
        self.timeloop_tbegin_label = QtWidgets.QLabel(__("Timeloop begin"))
        self.timeloop_tbegin_input = TimeInput(min_val=0)
        self.timeloop_tend_label = QtWidgets.QLabel(__("Timeloop end"))
        self.timeloop_tend_input = TimeInput(min_val=0)
        for x in [self.initial_time_label, self.initial_time_input, self.timeloop_tbegin_label,
                  self.timeloop_tbegin_input,
                  self.timeloop_tend_label, self.timeloop_tend_input]:
            self.time_layout.addWidget(x)
        self.setpos_layout = QtWidgets.QHBoxLayout()
        self.setpos_label = QtWidgets.QLabel(__("Position offset (X,Y,Z)"))
        self.setpos_x_input = SizeInput()
        self.setpos_y_input = SizeInput()
        self.setpos_z_input = SizeInput()
        for x in [self.setpos_label, self.setpos_x_input, self.setpos_y_input, self.setpos_z_input]:
            self.setpos_layout.addWidget(x)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        for x in [self.file_layout, self.time_layout, self.setpos_layout]:  # self.zbottom_layout,
            self.main_layout.addLayout(x)

        self.browse_button.clicked.connect(self.on_browse_button)

        self.setLayout(self.main_layout)

    def on_browse_button(self):
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"),
                                                                Case.the().info.last_used_directory,
                                                                "CSV Files (*.csv);;Binary files (*.mbi4)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.file_input.setText(file_name_temp)

    def fill_values(self, elevation_info: InletOutletElevationInfo):
        self.savevtk_checkbox.setChecked(elevation_info.savevtk)
        self.remove_checkbox.setChecked(elevation_info.remove)
        mesh_data = elevation_info.meshdata
        self.file_input.setText(mesh_data.file)
        self.initial_time_input.setValue(mesh_data.initial_time)
        self.timeloop_tbegin_input.setValue(mesh_data.timeloop_tbegin)
        self.timeloop_tend_input.setValue(mesh_data.timeloop_tend)
        self.setpos_x_input.setValue(mesh_data.setpos[0])
        self.setpos_y_input.setValue(mesh_data.setpos[1])
        self.setpos_z_input.setValue(mesh_data.setpos[2])

    def to_dict(self):
        values = {}
        values["savevtk"] = self.savevtk_checkbox.isChecked()
        values["remove"] = self.remove_checkbox.isChecked()
        values["meshdata"] = {}
        values["meshdata"]["file"] = self.file_input.text()
        values["meshdata"]["initial_time"] = self.initial_time_input.value()
        values["meshdata"]["timeloop_tbegin"] = self.timeloop_tbegin_input.value()
        values["meshdata"]["timeloop_tend"] = self.timeloop_tend_input.value()
        values["meshdata"]["setpos"] = [self.setpos_x_input.value(),self.setpos_y_input.value(),
                                        self.setpos_z_input.value()]
        return values


class ImposezsurfCalculatedWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.savevtk_checkbox = QtWidgets.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtWidgets.QCheckBox(__("Remove particles above surface"))

        self.zsurf_layout = QtWidgets.QHBoxLayout()
        self.zsurfmin_label = QtWidgets.QLabel(__("Min surface"))
        self.zsurfmin_input = SizeInput()
        self.zsurffit_label = QtWidgets.QLabel(__("Reduction of zsurf"))
        self.zsurffit_input = ValueInput()

        self.zsurf_layout.addWidget(self.zsurfmin_label)
        self.zsurf_layout.addWidget(self.zsurfmin_input)
        self.zsurf_layout.addWidget(self.zsurffit_label)
        self.zsurf_layout.addWidget(self.zsurffit_input)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addLayout(self.zsurf_layout)

        self.setLayout(self.main_layout)

    def fill_values(self, elevation_info):
        self.savevtk_checkbox.setChecked(elevation_info.savevtk)
        self.remove_checkbox.setChecked(elevation_info.remove)
        self.zsurfmin_input.setValue(elevation_info.zsurfmin)
        self.zsurffit_input.setValue(elevation_info.zsurffit)

    def to_dict(self):
        values = {}
        values["savevtk"] = self.savevtk_checkbox.isChecked()
        values["remove"] = self.remove_checkbox.isChecked()
        values["zsurfmin"] = self.zsurfmin_input.value()
        values["zsurffit"] = self.zsurffit_input.value()
        return values
