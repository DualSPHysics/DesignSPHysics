from PySide2 import QtWidgets
from mod.enums import InletOutletDirection, ObjectType
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_2d_direction_widget import Zone2DDirectionWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_2d_rotation_widget import Zone2DRotationWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_3d_direction_widget import Zone3DDirectionWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.zone_3d_rotation_widget import Zone3DRotationWidget
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames


class MKZone2DGeneratorWidget(QtWidgets.QWidget):
    """ A widget to show options for the MK zone generator. """
    DIRECTION_MAPPING: dict = {
        0: InletOutletDirection.LEFT,
        1: InletOutletDirection.RIGHT,
        2: InletOutletDirection.TOP,
        3: InletOutletDirection.BOTTOM,
        4: InletOutletDirection.CUSTOM
    }

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.direction_2d_widget = Zone2DDirectionWidget()
        self.rotation_2d_widget = Zone2DRotationWidget()

        self.zone2d3d_mk_label = QtWidgets.QLabel(__("MK fluid: "))
        self.zone2d3d_mk_selector = MkSelectInputWithNames(ObjectType.FLUID)
        self.zone2d3d_mk_selector.setCurrentIndex(0)
        self.zone2d3d_direction_combobox_label = QtWidgets.QLabel(__("Direction: "))
        self.zone2d3d_direction_combobox = QtWidgets.QComboBox()
        self.zone2d3d_direction_combobox.insertItems(0, ["Left", "Right", "Top", "Bottom","Custom"])

        self.main_layout.addWidget(self.zone2d3d_mk_label)
        self.main_layout.addWidget(self.zone2d3d_mk_selector)
        self.main_layout.addWidget(self.zone2d3d_direction_combobox_label)
        self.main_layout.addWidget(self.zone2d3d_direction_combobox)
        self.main_layout.addWidget(self.direction_2d_widget)
        self.main_layout.addWidget(self.rotation_2d_widget)

        self.zone2d3d_direction_combobox.currentIndexChanged.connect(
            self.on_zone2d3d_direction_changed)

    def fill_values(self,zone_gen,zone_direction,zone_rotation):
        self.direction_2d_widget.setVisible(
            self.zone2d3d_direction_combobox.currentIndex() == 6)
        index_to_put = 0
        for index, direction in self.DIRECTION_MAPPING.items():
            if direction == zone_gen.direction:
                index_to_put = index
        self.zone2d3d_direction_combobox.setCurrentIndex(index_to_put)
        self.zone2d3d_mk_selector.update_mk_list()
        self.zone2d3d_mk_selector.set_mk_index(zone_gen.mkfluid)
        self.direction_2d_widget.fill_values(zone_direction)
        self.rotation_2d_widget.fill_values(zone_rotation)


    def to_dict(self):
        values= {"mkfluid": int(self.zone2d3d_mk_selector.get_mk_value()),
                 "direction": self.DIRECTION_MAPPING[
            self.zone2d3d_direction_combobox.currentIndex()],
                 "custom_direction" :self.direction_2d_widget.to_dict(),
                 "rotation" : self.rotation_2d_widget.to_dict()}


        return values

    def on_zone2d3d_direction_changed(self):
        self.direction_2d_widget.setVisible(
                self.zone2d3d_direction_combobox.currentIndex() == 6)



class MKZone3DGeneratorWidget(QtWidgets.QWidget):
    """ A widget to show options for the MK zone generator. """
    DIRECTION_MAPPING: dict = {
        0: InletOutletDirection.LEFT,
        1: InletOutletDirection.RIGHT,
        2: InletOutletDirection.FRONT,
        3: InletOutletDirection.BACK,
        4: InletOutletDirection.TOP,
        5: InletOutletDirection.BOTTOM,
        6: InletOutletDirection.CUSTOM
    }

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.direction_3d_widget = Zone3DDirectionWidget()
        self.rotation_3d_widget = Zone3DRotationWidget()

        self.zone2d3d_mk_label = QtWidgets.QLabel(__("MK fluid: "))
        self.zone2d3d_mk_selector = MkSelectInputWithNames(ObjectType.FLUID)
        self.zone2d3d_mk_selector.setCurrentIndex(0)
        self.zone2d3d_direction_combobox_label = QtWidgets.QLabel(__("Direction: "))
        self.zone2d3d_direction_combobox = QtWidgets.QComboBox()
        self.zone2d3d_direction_combobox.insertItems(0, ["Left", "Right", "Front", "Back", "Top", "Bottom","Custom"])

        self.main_layout.addWidget(self.zone2d3d_mk_label)
        self.main_layout.addWidget(self.zone2d3d_mk_selector)
        self.main_layout.addWidget(self.zone2d3d_direction_combobox_label)
        self.main_layout.addWidget(self.zone2d3d_direction_combobox)
        self.main_layout.addWidget(self.direction_3d_widget)
        self.main_layout.addWidget(self.rotation_3d_widget)

        self.zone2d3d_direction_combobox.currentIndexChanged.connect(
            self.on_zone2d3d_direction_changed)



    def fill_values(self,zone_gen,zone_direction,zone_rotation):
        self.direction_3d_widget.setVisible(
            self.zone2d3d_direction_combobox.currentIndex() == 6)
        index_to_put = 0
        for index, direction in self.DIRECTION_MAPPING.items():
            if direction == zone_gen.direction:
                index_to_put = index
        self.zone2d3d_direction_combobox.setCurrentIndex(index_to_put)
        self.zone2d3d_mk_selector.update_mk_list()
        self.zone2d3d_mk_selector.set_mk_index(zone_gen.mkfluid)
        self.direction_3d_widget.fill_values(zone_direction)
        self.rotation_3d_widget.fill_values(zone_rotation)

    def to_dict(self):
        values= {"mkfluid": int(self.zone2d3d_mk_selector.get_mk_value()),
                 "direction": self.DIRECTION_MAPPING[
            self.zone2d3d_direction_combobox.currentIndex()],
        "custom_direction": self.direction_3d_widget.to_dict(),
        "rotation": self.rotation_3d_widget.to_dict()}
        return values

    def on_zone2d3d_direction_changed(self):
        self.direction_3d_widget.setVisible(
                self.zone2d3d_direction_combobox.currentIndex() == 6)
