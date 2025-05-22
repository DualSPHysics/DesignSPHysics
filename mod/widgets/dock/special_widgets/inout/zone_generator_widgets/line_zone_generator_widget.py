from PySide2 import QtWidgets
from mod.dataobjects.inletoutlet.inlet_outlet_zone_direction import InletOutletZone2DDirection
from mod.dataobjects.inletoutlet.inlet_outlet_zone_line_generator import InletOutletZoneLineGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone2DRotation
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_2d_direction_widget import Zone2DDirectionWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_2d_rotation_widget import Zone2DRotationWidget
from mod.widgets.custom_widgets.size_input import SizeInput


class LineZoneGeneratorWidget(QtWidgets.QWidget):
    """ A widget to show options for the Line zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_label = QtWidgets.QLabel(__("2D Line Inlet"))

        self.direction_widget = Zone2DDirectionWidget()
        self.manual_setting_label = QtWidgets.QLabel("Placement")
        self.manual_setting_layout = QtWidgets.QHBoxLayout()
        self.manual_setting_combo = QtWidgets.QComboBox()
        self.manual_setting_combo.addItems(["Parametric", "Manual"])
        self.manual_setting_layout.addWidget(self.manual_setting_label)
        self.manual_setting_layout.addWidget(self.manual_setting_combo)

        self.point_layout = QtWidgets.QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point 1 [X, Z]"))
        self.point_value_x = SizeInput()
        self.point_value_z = SizeInput()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_z)


        self.point2_layout = QtWidgets.QHBoxLayout()
        self.point2_label = QtWidgets.QLabel(__("Point 2 [X, Z]"))
        self.point2_value_x = SizeInput()
        self.point2_value_z = SizeInput()
        self.point2_layout.addWidget(self.point2_label)
        self.point2_layout.addWidget(self.point2_value_x)
        self.point2_layout.addWidget(self.point2_value_z)

        self.rotation_widget=Zone2DRotationWidget()

        self.main_layout.addWidget(self.main_label)
        self.main_layout.addWidget(self.direction_widget)
        self.main_layout.addLayout(self.manual_setting_layout)
        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.point2_layout)
        self.main_layout.addWidget(self.rotation_widget)

        self.manual_setting_combo.currentIndexChanged.connect(self.on_manual_combo)


    def fill_values(self,io_zone_gen:InletOutletZoneLineGenerator,io_dir:InletOutletZone2DDirection,io_rot:InletOutletZone2DRotation):
        self.manual_setting_combo.setCurrentIndex(1 if io_zone_gen.manual_setting else 0)
        self.point_value_x.setValue(io_zone_gen.point[0])
        self.point_value_z.setValue(io_zone_gen.point[2])

        self.point2_value_x.setValue(io_zone_gen.point2[0])
        self.point2_value_z.setValue(io_zone_gen.point2[2])

        self.direction_widget.fill_values(io_dir)
        self.rotation_widget.fill_values(io_rot)

    def to_dict(self):
        values={}
        values["point"] = [self.point_value_x.value(), 0.0, self.point_value_z.value()]
        values["point2"] = [self.point2_value_x.value(), 0.0,  self.point2_value_z.value()]
        values["direction"] = self.direction_widget.to_dict()
        values["rotation"] = self.rotation_widget.to_dict()
        values["manual_setting"] = self.manual_setting_combo.currentIndex() == 1

        return values

    def on_manual_combo(self):
        index = self.manual_setting_combo.currentIndex()
        if index == 0:
            for x in [self.point_value_x, self.point_value_z, self.point2_value_x, self.point2_value_z,
                      self.rotation_widget]:
                x.setEnabled(True)
        #    self.rotation_widget.rotation_type_combo.setCurrentIndex(
        #        self.rotation_widget)  # Last rotation type
        else:
            for x in [self.point_value_x, self.point_value_z, self.point2_value_x, self.point2_value_z,
                      self.rotation_widget]:
                x.setEnabled(False)
        #    self.rotation_widget.rotation_type_combo.setCurrentIndex(1)  # rotation active