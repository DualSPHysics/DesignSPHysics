from PySide2 import QtWidgets
from mod.dataobjects.inletoutlet.inlet_outlet_zone_direction import InletOutletZone2DDirection
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput


class Zone2DDirectionWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.direction_layout = QtWidgets.QHBoxLayout()
        self.direction_label = QtWidgets.QLabel(__("Direction Vector [X, Z]"))
        self.direction_value_x = ValueInput()
        self.direction_value_z = ValueInput()
        self.direction_layout.addWidget(self.direction_label)
        self.direction_layout.addWidget(self.direction_value_x)
        self.direction_layout.addWidget(self.direction_value_z)
        self.main_layout.addLayout(self.direction_layout)

    def fill_values(self,zone_direction:InletOutletZone2DDirection):
        self.direction_value_x.setValue(zone_direction.direction[0])
        self.direction_value_z.setValue(zone_direction.direction[1])

    def to_dict(self):
        values = {}
        values["direction"] = [self.direction_value_x.value(),
                               self.direction_value_z.value()]
        return values