from PySide2 import QtWidgets
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone2DRotation
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class Zone2DRotationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)


        self.rotation_combo_layout = QtWidgets.QHBoxLayout()
        self.rotation_combo_label = QtWidgets.QLabel(__("Rotation: "))
        self.rotation_type_combo = QtWidgets.QComboBox()
        self.rotation_type_combo.addItems(["No rotation","Parametric"])
        self.rotation_type_combo.currentIndexChanged.connect(self.on_rotation_type_change)
        self.rotation_combo_layout.addWidget(self.rotation_combo_label)
        self.rotation_combo_layout.addWidget(self.rotation_type_combo)


        self.rotation_angle_layout = QtWidgets.QHBoxLayout()
        self.rotation_angle_label = QtWidgets.QLabel(__("Rotation angle (degrees)"))
        self.rotation_angle_value = ValueInput()
        self.rotation_angle_layout.addWidget(self.rotation_angle_label)
        self.rotation_angle_layout.addWidget(self.rotation_angle_value)

        self.rotation_center_layout = QtWidgets.QHBoxLayout()
        self.rotation_center_label = QtWidgets.QLabel(__("Rotation Center [X, Z]"))
        self.rotation_center_value_x = SizeInput()
        self.rotation_center_value_z = SizeInput()
        self.rotation_center_layout.addWidget(self.rotation_center_label)
        self.rotation_center_layout.addWidget(self.rotation_center_value_x)
        self.rotation_center_layout.addWidget(self.rotation_center_value_z)


        self.main_layout.addLayout(self.rotation_combo_layout)
        self.main_layout.addLayout(self.rotation_angle_layout)
        self.main_layout.addLayout(self.rotation_center_layout)

    def on_rotation_type_change(self):
        widgets=[self.rotation_angle_label,
            self.rotation_angle_value,
            self.rotation_center_label,
            self.rotation_center_value_x,
            self.rotation_center_value_z]
        if self.rotation_type_combo.currentIndex()==0:
            for w in widgets: w.setVisible(False)
        elif self.rotation_type_combo.currentIndex()==1:
            for w in widgets: w.setVisible(True)
            for w in widgets: w.setEnabled(True)
        elif self.rotation_type_combo.currentIndex()==2:
            for w in widgets: w.setVisible(True)
            for w in widgets: w.setEnabled(False)

    def fill_values(self, io_zone_rotation: InletOutletZone2DRotation):
        self.rotation_angle_value.setValue(io_zone_rotation.rotation_angle)
        self.rotation_center_value_x.setValue(io_zone_rotation.rotation_center[0])
        self.rotation_center_value_z.setValue(io_zone_rotation.rotation_center[1])
        combo_index = 0
        if io_zone_rotation.rotation_enabled:
            combo_index = 1
        if io_zone_rotation.manual_rotation:
            combo_index = 2
        self.rotation_type_combo.setCurrentIndex(combo_index)
        self.on_rotation_type_change()


    def to_dict(self):
        values = {}
        values["manual_rotation"] = self.rotation_type_combo.currentIndex()==2
        values["rotation_enabled"] = self.rotation_type_combo.currentIndex()>0
        values["rotation_angle"] = self.rotation_angle_value.value()
        values["rotation_center"] = [
            self.rotation_center_value_x.value(),
            self.rotation_center_value_z.value()]
        return values
