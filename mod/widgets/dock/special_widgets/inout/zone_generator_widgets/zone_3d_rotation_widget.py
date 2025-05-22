from PySide2 import QtWidgets
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone3DRotation
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class Zone3DRotationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.pages_widget=QtWidgets.QStackedWidget(None)

        self.rotation_combo_layout=QtWidgets.QHBoxLayout()
        self.rotation_combo_label=QtWidgets.QLabel(__("Rotation: "))
        self.rotation_combo=QtWidgets.QComboBox()
        self.rotation_combo.addItems(["No rotation","Rotate axis","Advanced rotation"])
        self.rotation_combo.currentIndexChanged.connect(self.on_rotation_combo_change)
        self.rotation_combo_layout.addWidget(self.rotation_combo_label)
        self.rotation_combo_layout.addWidget(self.rotation_combo)
        #self.rotation_type=0


        self.rotateaxis_layout=QtWidgets.QVBoxLayout()
        self.rotateaxis_widget = QtWidgets.QWidget()
        self.rotateaxis_widget.setLayout(self.rotateaxis_layout)

        self.rotateaxis_angle_layout = QtWidgets.QHBoxLayout()
        self.rotateaxis_angle_label = QtWidgets.QLabel(__("Rotation angle (degrees)"))
        self.rotateaxis_angle_value = ValueInput()
        self.rotateaxis_angle_layout.addWidget(self.rotateaxis_angle_label)
        self.rotateaxis_angle_layout.addWidget(self.rotateaxis_angle_value)

        self.rotateaxis_point1_layout = QtWidgets.QHBoxLayout()
        self.rotateaxis_point1_label = QtWidgets.QLabel(__("Rotation Point 1 [X, Y, Z]"))
        self.rotateaxis_point1_value_x = SizeInput()
        self.rotateaxis_point1_value_y = SizeInput()
        self.rotateaxis_point1_value_z = SizeInput()
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_label)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_x)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_y)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_z)

        self.rotateaxis_point2_layout = QtWidgets.QHBoxLayout()
        self.rotateaxis_point2_label = QtWidgets.QLabel(__("Rotation point 2 [X, Y, Z]"))
        self.rotateaxis_point2_value_x = SizeInput()
        self.rotateaxis_point2_value_y = SizeInput()
        self.rotateaxis_point2_value_z = SizeInput()
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_label)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_x)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_y)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_z)
        self.rotateaxis_layout.addLayout(self.rotateaxis_angle_layout)
        self.rotateaxis_layout.addLayout(self.rotateaxis_point1_layout)
        self.rotateaxis_layout.addLayout(self.rotateaxis_point2_layout)

        # ROTATEADV (MAY BE HERE OR ON ITS OWN FILE)?
        self.rotateadv_layout = QtWidgets.QVBoxLayout()
        self.rotateadv_widget = QtWidgets.QWidget()
        self.rotateadv_widget.setLayout(self.rotateadv_layout)

        self.rotateadv_angle_layout=QtWidgets.QHBoxLayout()
        self.rotateadv_angle_label = QtWidgets.QLabel(__("Angles"))
        self.rotateadv_angle1_input = ValueInput()
        self.rotateadv_angle2_input = ValueInput()
        self.rotateadv_angle3_input = ValueInput()
        self.rotateadv_axes_label = QtWidgets.QLabel(__("Axes"))
        self.rotateadv_axes_input = QtWidgets.QLineEdit()
        self.rotateadv_instrinsic_checkbox = QtWidgets.QCheckBox(__("Intrinsic"))
        self.rotateadv_center_layout = QtWidgets.QHBoxLayout()
        self.rotateadv_center_label = QtWidgets.QLabel(__("Center [X, Y, Z]"))
        self.rotateadv_center_input_x = SizeInput()
        self.rotateadv_center_input_y = SizeInput()
        self.rotateadv_center_input_z = SizeInput()
        for x in [self.rotateadv_angle_label, self.rotateadv_angle1_input, self.rotateadv_angle2_input, self.rotateadv_angle3_input,
                  #self.rotateadv_axes_label, self.rotateadv_axes_input, self.rotateadv_instrinsic_checkbox,
                  ]:
            self.rotateadv_angle_layout.addWidget(x)
        for x in [ self.rotateadv_center_label, self.rotateadv_center_input_x, self.rotateadv_center_input_y, self.rotateadv_center_input_z]:
            self.rotateadv_center_layout.addWidget(x)
        self.rotateadv_layout.addLayout(self.rotateadv_angle_layout)
        self.rotateadv_layout.addLayout(self.rotateadv_center_layout)

        self.pages_widget.addWidget(QtWidgets.QWidget())
        self.pages_widget.addWidget(self.rotateaxis_widget)
        self.pages_widget.addWidget(self.rotateadv_widget)
        self.pages_widget.addWidget(self.rotateadv_widget)

        #self.pages_widget.setCurrentIndex(0)

        self.main_layout.addLayout(self.rotation_combo_layout)
        self.main_layout.addWidget(self.pages_widget)
        self.on_rotation_combo_change()


    def on_rotation_combo_change(self):
        index=self.rotation_combo.currentIndex()
        self.pages_widget.setCurrentIndex(index)
        enable=True
        '''if index==3:
            enable =False
            self.pages_widget.setCurrentIndex(2)
        for x in [self.rotateadv_angle1_input, self.rotateadv_angle2_input, self.rotateadv_angle3_input,
                   self.rotateadv_center_input_x, self.rotateadv_center_input_y, self.rotateadv_center_input_z]:
            x.setEnabled(enable)'''

    def fill_values(self, io_zone_rotation: InletOutletZone3DRotation):
        self.rotation_type=io_zone_rotation.rotation_type
        self.rotation_combo.setCurrentIndex(io_zone_rotation.rotation_type)
    #if io_zone_rotation.rotation_type ==1:
        self.rotateaxis_angle_value.setValue(io_zone_rotation.rotateaxis_angle)

        self.rotateaxis_point1_value_x.setValue(io_zone_rotation.rotateaxis_point1[0])
        self.rotateaxis_point1_value_y.setValue(io_zone_rotation.rotateaxis_point1[1])
        self.rotateaxis_point1_value_z.setValue(io_zone_rotation.rotateaxis_point1[2])

        self.rotateaxis_point2_value_x.setValue(io_zone_rotation.rotateaxis_point2[0])
        self.rotateaxis_point2_value_y.setValue(io_zone_rotation.rotateaxis_point2[1])
        self.rotateaxis_point2_value_z.setValue(io_zone_rotation.rotateaxis_point2[2])
    # ROTATEADV
    #if io_zone_rotation.rotation_type==2:
        self.rotateadv_angle1_input.setValue(io_zone_rotation.rotateadv_angle[0])
        self.rotateadv_angle2_input.setValue(io_zone_rotation.rotateadv_angle[1])
        self.rotateadv_angle3_input.setValue(io_zone_rotation.rotateadv_angle[2])
        self.rotateadv_axes_input.setText(io_zone_rotation.rotateadv_axes)
        self.rotateadv_axes_input.setEnabled(False)
        self.rotateadv_instrinsic_checkbox.setChecked(io_zone_rotation.rotateadv_intrinsic)
        self.rotateadv_instrinsic_checkbox.setEnabled(False)
        self.rotateadv_center_input_x.setValue(io_zone_rotation.rotateadv_center[0])
        self.rotateadv_center_input_y.setValue(io_zone_rotation.rotateadv_center[1])
        self.rotateadv_center_input_z.setValue(io_zone_rotation.rotateadv_center[2])

        self.on_rotation_combo_change()
    def to_dict(self):
        values = {}
        values["rotation_type"] = self.rotation_combo.currentIndex()
        values["rotateaxis_enabled"] = self.rotation_combo.currentIndex()==1
        values["rotateaxis_angle"] = self.rotateaxis_angle_value.value()
        values["rotateaxis_point1"] = [
            self.rotateaxis_point1_value_x.value(),
            self.rotateaxis_point1_value_y.value(),
            self.rotateaxis_point1_value_z.value()]
        values["rotateaxis_point2"] = [
            self.rotateaxis_point2_value_x.value(),
            self.rotateaxis_point2_value_y.value(),
            self.rotateaxis_point2_value_z.value()]
        # rotateadv
        values["rotateadv_enabled"] = self.rotation_combo.currentIndex()>=2
        values["rotateadv_angle"] = [
            self.rotateadv_angle1_input.value(),
            self.rotateadv_angle2_input.value(),
            self.rotateadv_angle3_input.value()
        ]
        values["rotateadv_axes"] = self.rotateadv_axes_input.text()
        values["rotateadv_intrinsic"] = self.rotateadv_instrinsic_checkbox.isChecked()
        values["rotateadv_center"] = [
            self.rotateadv_center_input_x.value(),
            self.rotateadv_center_input_y.value(),
            self.rotateadv_center_input_z.value()
        ]


        return values