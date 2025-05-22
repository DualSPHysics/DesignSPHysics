from PySide2 import QtWidgets
from mod.dataobjects.inletoutlet.inlet_outlet_zone_direction import InletOutletZone3DDirection
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone3DRotation
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_3d_direction_widget import Zone3DDirectionWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_3d_rotation_widget import Zone3DRotationWidget
from mod.widgets.custom_widgets.size_input import SizeInput


class CircleZoneGeneratorWidget(QtWidgets.QWidget):
    """ A widget to show options for the Circle zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_label = QtWidgets.QLabel(__("3D Circle Inlet"))

        self.direction_widget = Zone3DDirectionWidget()

        self.manual_setting_label = QtWidgets.QLabel("Placement")

        self.manual_setting_layout = QtWidgets.QHBoxLayout()
        self.manual_setting_combo = QtWidgets.QComboBox()
        self.manual_setting_combo.addItems(["Parametric", "Manual"])
        self.manual_setting_layout.addWidget(self.manual_setting_label)
        self.manual_setting_layout.addWidget(self.manual_setting_combo)

        self.point_layout = QtWidgets.QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point [X, Y, Z]"))
        self.point_value_x = SizeInput()
        self.point_value_y = SizeInput()
        self.point_value_z = SizeInput()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_y)
        self.point_layout.addWidget(self.point_value_z)

        self.radius_layout = QtWidgets.QHBoxLayout()
        self.radius_label = QtWidgets.QLabel(__("Radius"))
        self.radius_value = SizeInput()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_value)

        self.rotation_widget = Zone3DRotationWidget()

        self.main_layout.addWidget(self.main_label)
        self.main_layout.addWidget(self.direction_widget)
        self.main_layout.addLayout(self.manual_setting_layout)
        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addWidget(self.rotation_widget)
        self.manual_setting_combo.currentIndexChanged.connect(self.on_manual_combo)


    def fill_values(self,io_zone_gen,io_dir:InletOutletZone3DDirection,io_rot:InletOutletZone3DRotation):
        self.manual_setting_combo.setCurrentIndex(1 if io_zone_gen.manual_setting else 0)
        self.point_value_x.setValue(io_zone_gen.point[0])
        self.point_value_y.setValue(io_zone_gen.point[1])
        self.point_value_z.setValue(io_zone_gen.point[2])

        self.radius_value.setValue(io_zone_gen.radius)

        self.direction_widget.fill_values(io_dir)
        self.rotation_widget.fill_values(io_rot)


    def to_dict(self):
        values={}
        values["point"] = [self.point_value_x.value(),
                      self.point_value_y.value(),
                      self.point_value_z.value()]
        values["radius"] = self.radius_value.value()
        values["direction"] = self.direction_widget.to_dict()
        values["rotation"] = self.rotation_widget.to_dict()
        values["manual_setting"] = self.manual_setting_combo.currentIndex() == 1
        return values

    def on_manual_combo(self):
        index = self.manual_setting_combo.currentIndex()
        if index==0:
            for x in [self.point_value_x,self.point_value_y,self.point_value_z,self.radius_value,
                    self.rotation_widget]:
                x.setEnabled(True)
            self.rotation_widget.rotation_combo.setCurrentIndex(self.rotation_widget.rotation_type) #Last rotation type
        else:
            for x in [self.point_value_x,self.point_value_y,self.point_value_z,self.radius_value,
                    self.rotation_widget]:
                x.setEnabled(False)
            self.rotation_widget.rotation_combo.setCurrentIndex(2)   #Adv rotation for showing angles
