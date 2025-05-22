import os.path

from PySide2.QtCore import Signal

from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_velocity_info import InletOutletVelocityInfo
from mod.dataobjects.inletoutlet.velocities.linear_velocity import LinearVelocity
from mod.dataobjects.inletoutlet.velocities.parabolic_velocity import ParabolicVelocity
from mod.enums import FlowUnits
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput


class VelocityTypeFixedConstantWidget(QtWidgets.QWidget):
    """ A widget to show options for Fixed Constant velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.row = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(__("Constant Velocity:"))
        self.input = ValueInput()
        self.units_label = QtWidgets.QLabel(__("m/s"))
        self.row.addWidget(self.label)
        self.row.addWidget(self.input)
        self.row.addWidget(self.units_label)


        self.main_layout.addLayout(self.row)
        self.setLayout(self.main_layout)

    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        self.input.setValue(velocity_info.fixed_constant_value)

    def to_dict(self):
        values={"fixed_constant_value" : self.input.value()}
        return values

    def set_units_label(self,label):
        self.units_label.setText(label)


class VelocityTypeFixedLinearWidget(QtWidgets.QWidget):
    """ A widget to show options for Fixed Linear velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.v_layout = QtWidgets.QHBoxLayout()
        self.v_label = QtWidgets.QLabel(__("V1:"))
        self.v_input = VelocityInput()
        self.v_layout.addWidget(self.v_label)
        self.v_layout.addWidget(self.v_input)

        self.v2_layout = QtWidgets.QHBoxLayout()
        self.v2_label = QtWidgets.QLabel(__("V2:"))
        self.v2_input = VelocityInput()
        self.v2_layout.addWidget(self.v2_label)
        self.v2_layout.addWidget(self.v2_input)

        self.z_layout = QtWidgets.QHBoxLayout()
        self.z_label = QtWidgets.QLabel(__("Z1:"))
        self.z_input = SizeInput()
        self.z_layout.addWidget(self.z_label)
        self.z_layout.addWidget(self.z_input)

        self.z2_layout = QtWidgets.QHBoxLayout()
        self.z2_label = QtWidgets.QLabel(__("Z2:"))
        self.z2_input = SizeInput()
        self.z2_layout.addWidget(self.z2_label)
        self.z2_layout.addWidget(self.z2_input)

        self.main_layout.addLayout(self.v_layout)
        self.main_layout.addLayout(self.v2_layout)
        self.main_layout.addLayout(self.z_layout)
        self.main_layout.addLayout(self.z2_layout)
        self.setLayout(self.main_layout)
        
    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        self.v_input.setValue(velocity_info.fixed_linear_value.v1)
        self.v2_input.setValue(velocity_info.fixed_linear_value.v2)
        self.z_input.setValue(velocity_info.fixed_linear_value.z1)
        self.z2_input.setValue(velocity_info.fixed_linear_value.z2)

    def to_dict(self):
        values={}
        values["fixed_linear_value.v1"] = self.v_input.value()
        values["fixed_linear_value.v2"] = self.v2_input.value()
        values["fixed_linear_value.z1"] = self.z_input.value()
        values["fixed_linear_value.z2"] = self.z2_input.value()
        return values


class VelocityTypeFixedParabolicWidget(QtWidgets.QWidget):
    """ A widget to show options for Fixed Parabolic velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.v_layout = QtWidgets.QHBoxLayout()
        self.v_label = QtWidgets.QLabel(__("V1:"))
        self.v_input = VelocityInput()
        self.v_layout.addWidget(self.v_label)
        self.v_layout.addWidget(self.v_input)

        self.v2_layout = QtWidgets.QHBoxLayout()
        self.v2_label = QtWidgets.QLabel(__("V2:"))
        self.v2_input = VelocityInput()
        self.v2_layout.addWidget(self.v2_label)
        self.v2_layout.addWidget(self.v2_input)

        self.v3_layout = QtWidgets.QHBoxLayout()
        self.v3_label = QtWidgets.QLabel(__("V3:"))
        self.v3_input = VelocityInput()
        self.v3_layout.addWidget(self.v3_label)
        self.v3_layout.addWidget(self.v3_input)

        self.z_layout = QtWidgets.QHBoxLayout()
        self.z_label = QtWidgets.QLabel(__("Z1:"))
        self.z_input = SizeInput()
        self.z_layout.addWidget(self.z_label)
        self.z_layout.addWidget(self.z_input)

        self.z2_layout = QtWidgets.QHBoxLayout()
        self.z2_label = QtWidgets.QLabel(__("Z2:"))
        self.z2_input = SizeInput()
        self.z2_layout.addWidget(self.z2_label)
        self.z2_layout.addWidget(self.z2_input)

        self.z3_layout = QtWidgets.QHBoxLayout()
        self.z3_label = QtWidgets.QLabel(__("Z3:"))
        self.z3_input = SizeInput()
        self.z3_layout.addWidget(self.z3_label)
        self.z3_layout.addWidget(self.z3_input)

        self.main_layout.addLayout(self.v_layout)
        self.main_layout.addLayout(self.v2_layout)
        self.main_layout.addLayout(self.v3_layout)
        self.main_layout.addLayout(self.z_layout)
        self.main_layout.addLayout(self.z2_layout)
        self.main_layout.addLayout(self.z3_layout)
        self.setLayout(self.main_layout)
        
    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        self.v_input.setValue(velocity_info.fixed_parabolic_value.v1)
        self.v2_input.setValue(velocity_info.fixed_parabolic_value.v2)
        self.v3_input.setValue(velocity_info.fixed_parabolic_value.v3)
        self.z_input.setValue(velocity_info.fixed_parabolic_value.z1)
        self.z2_input.setValue(velocity_info.fixed_parabolic_value.z2)
        self.z3_input.setValue(velocity_info.fixed_parabolic_value.z3)

    def to_dict(self):
        values={}
        values["fixed_parabolic_value.v1"] = self.v_input.value()
        values["fixed_parabolic_value.v2"] = self.v2_input.value()
        values["fixed_parabolic_value.v3"] = self.v3_input.value()
        values["fixed_parabolic_value.z1"] = self.z_input.value()
        values["fixed_parabolic_value.z2"] = self.z2_input.value()
        values["fixed_parabolic_value.z3"] = self.z3_input.value()
        return values


class VelocityTypeVariableUniformWidget(QtWidgets.QWidget):
    """ A widget to show options for Variable Uniform velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(60, 2)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("Velocity (m/s)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)
    
    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        currentTableRow = 0
        for time, value in velocity_info.variable_uniform_values:
            self.table.setItem(currentTableRow, 0, QtWidgets.QTableWidgetItem(str(time)))
            self.table.setItem(currentTableRow, 1, QtWidgets.QTableWidgetItem(str(value)))
            currentTableRow += 1

    def to_dict(self):
        values={}
        values["variable_uniform_values"] = []
        table = self.table
        for i in range(0, table.rowCount()):
            if not table.item(i, 0) or not table.item(i, 1):
                continue
            time_as_string = table.item(i, 0).text()
            value_as_string = table.item(i, 1).text()
            if time_as_string != "" and value_as_string != "":
                values["variable_uniform_values"].append((float(time_as_string), float(value_as_string)))
        return values

    def set_units_label(self,label):
        if label=="m/s":
            self.table.setHorizontalHeaderLabels([__("Time (s)"), __("Velocity (m/s)")])
        else:
            self.table.setHorizontalHeaderLabels([__("Time (s)"), __("Flow Velocity") + f"({label})"])

class VelocityTypeVariableLinearWidget(QtWidgets.QWidget):
    """ A widget to show options for Variable Linear velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(60, 5)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("V (m/s)"), __("V2 (m/s)"), __("Z (m)"), __("Z2 (m)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)

    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        currentTableRow = 0
        for time, value in velocity_info.variable_linear_values:
            self.table.setItem(currentTableRow, 0, QtWidgets.QTableWidgetItem(str(time)))
            self.table.setItem(currentTableRow, 1, QtWidgets.QTableWidgetItem(str(value.v1)))
            self.table.setItem(currentTableRow, 2, QtWidgets.QTableWidgetItem(str(value.v2)))
            self.table.setItem(currentTableRow, 3, QtWidgets.QTableWidgetItem(str(value.z1)))
            self.table.setItem(currentTableRow, 4, QtWidgets.QTableWidgetItem(str(value.z2)))
            currentTableRow += 1

    def to_dict(self):
        values={}
        values["variable_linear_values"] = []
        table = self.table
        for i in range(0, table.rowCount()):
            if not table.item(i, 0) or not table.item(i, 1) or not table.item(i, 2) or not table.item(i,
                                                                                                      3) or not table.item(
                i, 4):
                continue
            time_as_string = table.item(i, 0).text()
            v1_as_string = table.item(i, 1).text()
            v2_as_string = table.item(i, 2).text()
            z1_as_string = table.item(i, 3).text()
            z2_as_string = table.item(i, 4).text()
            if time_as_string != "" and v1_as_string != "" and v2_as_string != "" and z1_as_string != "" and z2_as_string != "":
                value = LinearVelocity()
                value.v1 = float(v1_as_string)
                value.v2 = float(v2_as_string)
                value.z1 = float(z1_as_string)
                value.z2 = float(z2_as_string)
                values["variable_linear_values"].append((float(time_as_string), value))
        return values


class VelocityTypeVariableParabolicWidget(QtWidgets.QWidget):
    """ A widget to show options for Variable Parabolic velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget(60, 7)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("V (m/s)"), __("V2 (m/s)"), __("V3 (m/s)"), __("Z (m)"), __("Z2 (m)"), __("Z3 (m)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)
        
    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        currentTableRow = 0
        for time, value in velocity_info.variable_parabolic_values:
            self.table.setItem(currentTableRow, 0, QtWidgets.QTableWidgetItem(str(time)))
            self.table.setItem(currentTableRow, 1, QtWidgets.QTableWidgetItem(str(value.v1)))
            self.table.setItem(currentTableRow, 2, QtWidgets.QTableWidgetItem(str(value.v2)))
            self.table.setItem(currentTableRow, 3, QtWidgets.QTableWidgetItem(str(value.v3)))
            self.table.setItem(currentTableRow, 4, QtWidgets.QTableWidgetItem(str(value.z1)))
            self.table.setItem(currentTableRow, 5, QtWidgets.QTableWidgetItem(str(value.z2)))
            self.table.setItem(currentTableRow, 6, QtWidgets.QTableWidgetItem(str(value.z3)))
            currentTableRow += 1
            
    def to_dict(self):
        values={}
        values["variable_parabolic_values"] = []
        table = self.table
        for i in range(0, table.rowCount()):
            if not table.item(i, 0) or not table.item(i, 1) or not table.item(i, 2) or not table.item(i,
                                                                                                      3) or not table.item(
                i, 4) or not table.item(i, 5) or not table.item(i, 6):
                continue
            time_as_string = table.item(i, 0).text()
            v1_as_string = table.item(i, 1).text()
            v2_as_string = table.item(i, 2).text()
            v3_as_string = table.item(i, 3).text()
            z1_as_string = table.item(i, 4).text()
            z2_as_string = table.item(i, 5).text()
            z3_as_string = table.item(i, 6).text()
            if time_as_string != "" and v1_as_string != "" and v2_as_string != "" and v3_as_string != "" and z1_as_string != "" and z2_as_string != "" and z3_as_string != "":
                value = ParabolicVelocity()
                value.v1 = float(v1_as_string)
                value.v2 = float(v2_as_string)
                value.v3 = float(v3_as_string)
                value.z1 = float(z1_as_string)
                value.z2 = float(z2_as_string)
                value.z3 = float(z3_as_string)
                values["variable_parabolic_values"].append((float(time_as_string), value))
        return values


class VelocityTypeFileWidget(QtWidgets.QWidget):
    """ A widget to show options for File based velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(__("File Path:"))
        self.path_input = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton(__("Browse"))

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.path_input)
        self.main_layout.addWidget(self.button)

        self.button.clicked.connect(self.on_browse_buton)

        self.setLayout(self.main_layout)

    def on_browse_buton(self):
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"), Case.the().info.last_used_directory, "CSV Files (*.csv)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.path_input.setText(file_name_temp)

    def fill_values(self,velocity_info : InletOutletVelocityInfo):
        self.path_input.setText(velocity_info.file_path)

    def to_dict(self):
        values = {"file_path":self.path_input.text()}
        return values

'''
class VelocityTypeInterpolatedWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.firstrow=QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(__("File Path:"))
        self.path_input = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton(__("Browse"))
        self.secondrow=QtWidgets.QHBoxLayout()
        self.gridresetvelz_label = QtWidgets.QLabel(__("Grid Reset Vel Z:"))
        self.gridresetvelz_checkbox=QtWidgets.QCheckBox()
        self.gridposzero_label = QtWidgets.QLabel(__("Grid Pos Zero:"))
        self.gridposzero_x_label = QtWidgets.QLabel(__("X:"))
        self.gridposzero_x_input = ValueInput()
        self.gridposzero_z_label = QtWidgets.QLabel(__("Z"))
        self.gridposzero_z_input = ValueInput()

        for x in [self.label,
        self.path_input,
        self.button]:
            self.firstrow.addWidget(x)
        for x in [self.gridresetvelz_label,
        self.gridresetvelz_checkbox,
        self.gridposzero_label,
        self.gridposzero_x_label,
        self.gridposzero_x_input,
        self.gridposzero_z_label,
        self.gridposzero_z_input]:
            self.secondrow.addWidget(x)
        self.main_layout.addLayout(self.firstrow)
        self.main_layout.addLayout(self.secondrow)

        self.button.clicked.connect(self.on_browse_buton)

        self.setLayout(self.main_layout)

    def on_browse_buton(self):
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"),
                                                                Case.the().info.last_used_directory,
                                                                "CSV Files (*.csv)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.path_input.setText(file_name_temp)

    def fill_values(self, velocity_info: InletOutletVelocityInfo):
        self.path_input.setValue(velocity_info.file_path)
        self.gridresetvelz_checkbox.setChecked(velocity_info.gridresetvelz)
        self.gridposzero_x_input.setValue(velocity_info.gridposzero[0])
        self.gridposzero_z_input.setValue(velocity_info.gridposzero[1])

    def to_dict(self):
        values={}
        values["file_path"] = self.path_input.text()
        values["gridresetvelz"] = self.gridresetvelz_checkbox.isChecked()
        values["gridposzero"] = [self.gridposzero_x_input.value(),self.gridposzero_z_input.value()]
        return values

'''

class FlowVelocityWidget(QtWidgets.QWidget):
    unit_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(__("Flow Velocity:"))
        self.flowvelocity_active_label = QtWidgets.QLabel(__("Active:"))
        self.flowvelocity_active_checkbox=QtWidgets.QCheckBox()
        self.flowvelocity_ratio_label = QtWidgets.QLabel(__("Ratio:"))
        self.flowvelocity_ratio_input = ValueInput()
        self.flowvelocity_units_label = QtWidgets.QLabel(__("Units:"))
        self.flowvelocity_units_combobox = QtWidgets.QComboBox()
        self.flowvelocity_units_combobox.addItem(__("l/s"))
        self.flowvelocity_units_combobox.addItem(__("gal/s"))
        self.flowvelocity_units_combobox.addItem(__("gal/min"))

        for x in [self.label,
        self.flowvelocity_active_label,
        self.flowvelocity_active_checkbox,
        self.flowvelocity_ratio_label,
        self.flowvelocity_ratio_input,
        self.flowvelocity_units_label,
        self.flowvelocity_units_combobox ]:
            self.main_layout.addWidget(x)

        self.flowvelocity_active_checkbox.stateChanged.connect(self.flow_velocity_changed)
        self.flowvelocity_units_combobox.currentIndexChanged.connect(self.flow_velocity_changed)
        self.setLayout(self.main_layout)

    def fill_values(self, velocity_info: InletOutletVelocityInfo):
        self.flowvelocity_active_checkbox.setChecked(velocity_info.flow_velocity_active)

        self.flowvelocity_ratio_input.setValue(velocity_info.flow_velocity_ratio)
        if velocity_info.flow_velocity_units==FlowUnits.LITERSSECOND:
            self.flowvelocity_units_combobox.setCurrentIndex(0)
        if velocity_info.flow_velocity_units == FlowUnits.GALLONSSECOND:
            self.flowvelocity_units_combobox.setCurrentIndex(1)
        if velocity_info.flow_velocity_units==FlowUnits.GALLONSMIN:
            self.flowvelocity_units_combobox.setCurrentIndex(2)


    def to_dict(self):
        values={}
        values["flow_velocity_active"] = self.flowvelocity_active_checkbox.isChecked()
        values["flow_velocity_ratio"] = self.flowvelocity_ratio_input.value()
        values["flow_velocity_units"] = self.flowvelocity_units_combobox.currentText()
        return values

    def flow_velocity_changed(self):
        flow = self.flowvelocity_active_checkbox.isChecked()
        if flow:
            self.unit_changed.emit(self.flowvelocity_units_combobox.currentText())
        else:
            self.unit_changed.emit("m/s")



class VelocityTypeJetCircleWidget(QtWidgets.QWidget):
    """ A widget to show options for Jet Circle velocity. """
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.row = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(__("Jet circle"))
        self.velocity_label = QtWidgets.QLabel(__("Velocity"))
        self.velocity_input = VelocityInput()
        self.distance_label = QtWidgets.QLabel(__("Distance"))
        self.distance_input = SizeInput()
        self.radius_label = QtWidgets.QLabel(__("Radius"))
        self.radius_input = SizeInput()
        for x in [ self.label , self.velocity_label ,self.velocity_input ,self.distance_label ,self.distance_input ,
                   self.radius_label ,self.radius_input]:
            self.row.addWidget(x)
        self.main_layout.addLayout(self.row)
        self.setLayout(self.main_layout)

    def fill_values(self,velocity_info:InletOutletVelocityInfo):
        self.velocity_input.setValue(velocity_info.fixed_jetcircle_value.v)
        self.distance_input.setValue(velocity_info.fixed_jetcircle_value.distance)
        self.radius_input.setValue(velocity_info.fixed_jetcircle_value.radius)

    def to_dict(self):
        values={}
        values["jet_circle.v"]=self.velocity_input.value()
        values["jet_circle.distance"]=self.distance_input.value()
        values["jet_circle.radius"]=self.radius_input.value()
        return values

class VelocityMeshDataWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.firstrow = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel(__("File Path:"))
        self.file_input = QtWidgets.QLineEdit()
        self.file_browse_button = QtWidgets.QPushButton(__("Browse"))
        for x in [self.file_label, self.file_input, self.file_browse_button]:
            self.firstrow.addWidget(x)
        self.secondrow = QtWidgets.QHBoxLayout()
        self.magnitude_checkbox=QtWidgets.QCheckBox(__("Magnitude"))
        self.reverse_checkbox=QtWidgets.QCheckBox(__("Reverse"))
        self.initial_time_label=QtWidgets.QLabel(__("Initial time"))
        self.initial_time_input = TimeInput(min_val=0)
        for x in [self.magnitude_checkbox, self.reverse_checkbox, self.initial_time_label, self.initial_time_input ]:
            self.secondrow.addWidget(x)
        self.thirdrow = QtWidgets.QHBoxLayout()
        self.timeloop_tbegin_label = QtWidgets.QLabel(__("Timeloop begin"))
        self.timeloop_tbegin_input = TimeInput(min_val=0)
        self.timeloop_tend_label = QtWidgets.QLabel(__("Timeloop end"))
        self.timeloop_tend_input = TimeInput(min_val=0)
        for x in [self.timeloop_tbegin_label, self.timeloop_tbegin_input, self.timeloop_tend_label, self.timeloop_tend_input]:
            self.thirdrow.addWidget(x)
        self.fourthrow = QtWidgets.QHBoxLayout()
        self.setpos_label=QtWidgets.QLabel(__("Position offset (X,Y,Z)"))
        self.setpos_x_input = SizeInput()
        self.setpos_y_input = SizeInput()
        self.setpos_z_input = SizeInput()
        for x in [self.setpos_label,  self.setpos_x_input,  self.setpos_y_input, self.setpos_z_input]:
            self.fourthrow.addWidget(x)
        self.fifthrow = QtWidgets.QHBoxLayout()
        self.setvelmul_label = QtWidgets.QLabel(__("Velocity multiplier (X,Y,Z)"))
        self.setvelmul_x_input = ValueInput()
        self.setvelmul_y_input = ValueInput()
        self.setvelmul_z_input = ValueInput()
        for x in [self.setvelmul_label, self.setvelmul_x_input, self.setvelmul_y_input, self.setvelmul_z_input]:
            self.fifthrow.addWidget(x)
        self.sixthrow=QtWidgets.QHBoxLayout()
        self.setveladd_label = QtWidgets.QLabel(__("Velocity offset (X,Y,Z)"))
        self.setveladd_x_input = VelocityInput()
        self.setveladd_y_input = VelocityInput()
        self.setveladd_z_input = VelocityInput()
        for x in [self.setveladd_label, self.setveladd_x_input, self.setveladd_y_input, self.setveladd_z_input]:
            self.sixthrow.addWidget(x)

        self.file_browse_button.clicked.connect(self.on_browse_buton)

        for x in [self.firstrow,self.secondrow,self.thirdrow,self.fourthrow,self.fifthrow,self.sixthrow]:
            self.main_layout.addLayout(x)
        self.setLayout(self.main_layout)

    def on_browse_buton(self):
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"),
                                                                Case.the().info.last_used_directory,
                                                                "CSV Files (*.csv);;Binary files (*.mbi4)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.file_input.setText(file_name_temp)

    def fill_values(self,velocity_info:InletOutletVelocityInfo):
        mesh_data=velocity_info.velocity_mesh_data
        self.file_input.setText(mesh_data.filepath)
        self.magnitude_checkbox.setChecked(mesh_data.magnitude)
        self.reverse_checkbox.setChecked(mesh_data.reverse)
        self.initial_time_input.setValue(mesh_data.initial_time)
        self.timeloop_tbegin_input.setValue(mesh_data.timeloop_tbegin)
        self.timeloop_tend_input.setValue(mesh_data.timeloop_tend)
        self.setpos_x_input.setValue(mesh_data.setpos[0])
        self.setpos_y_input.setValue(mesh_data.setpos[1])
        self.setpos_z_input.setValue(mesh_data.setpos[2])
        self.setvelmul_x_input.setValue(mesh_data.setvelmul[0])
        self.setvelmul_y_input.setValue( mesh_data.setvelmul[1])
        self.setvelmul_z_input.setValue(mesh_data.setvelmul[2])
        self.setveladd_x_input.setValue(mesh_data.setveladd[0])
        self.setveladd_y_input.setValue(mesh_data.setveladd[1])
        self.setveladd_z_input.setValue(mesh_data.setveladd[2])

    def to_dict(self):
        values = {}
        values["filepath"]=self.file_input.text()
        values["magnitude"]=self.magnitude_checkbox.isChecked()
        values["reverse"]=self.reverse_checkbox.isChecked()
        values["initial_time"]=self.initial_time_input.value()
        values["timeloop_tbegin"]=self.timeloop_tbegin_input.value()
        values["timeloop_tend"]=self.timeloop_tend_input.value()
        values["setpos"]=[self.setpos_x_input.value(),self.setpos_y_input.value(),self.setpos_z_input.value()]
        values["setvelmul"]=[self.setvelmul_x_input.value(),self.setvelmul_y_input.value(),self.setvelmul_z_input.value()]
        values["setveladd"]=[self.setveladd_x_input.value(),self.setveladd_y_input.value(),self.setveladd_z_input.value()]
        return values
