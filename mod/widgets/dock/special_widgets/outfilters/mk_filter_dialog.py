from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import FilterMK
from mod.tools.dialog_tools import warning_dialog
from mod.enums import ObjectType
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class MKFilterDialog(BaseFilterDialog):

    def __init__(self, mk_filter, parent=None):
        super().__init__(base_filter=mk_filter, parent=parent)
        self.data: FilterMK = mk_filter
        self.mk_layout = QHBoxLayout()
        self.obj_type_selector = QtWidgets.QComboBox()
        self.obj_type_selector.addItem("MkBound")
        self.obj_type_selector.addItem("MkFluid")
        self.range_checkbox = QtWidgets.QCheckBox(__("Select range"))
        self.mkvalue_label = QtWidgets.QLabel(__("MK Value"))
        self.mkvalue_input = MkSelectInputWithNames(ObjectType.BOUND)
        self.mk_range_layout=QHBoxLayout()
        self.mkvrange_label = QtWidgets.QLabel(__("MK Range"))
        self.mkrange_min_input = MkSelectInputWithNames(ObjectType.BOUND)
        self.mkrange_max_input = MkSelectInputWithNames(ObjectType.BOUND)
        for x in [self.obj_type_selector, self.mkvalue_label, self.mkvalue_input ]:
            self.mk_layout.addWidget(x)
        for x in [self.range_checkbox,self.mkvrange_label, self.mkrange_min_input, self.mkrange_max_input ]:
            self.mk_range_layout.addWidget(x)
        self.main_layout.insertLayout(2, self.mk_layout)
        self.main_layout.insertLayout(3, self.mk_range_layout)
        self.range_checkbox.stateChanged.connect(self.on_check_range)
        self.obj_type_selector.currentIndexChanged.connect(self.on_change_object_type)
        self.fill_values()

    def on_check_range(self, state):
        self.mkvalue_input.setDisabled(state)
        self.mkrange_min_input.setEnabled(state)
        self.mkrange_max_input.setEnabled(state)

    def on_change_object_type(self):
        if self.obj_type_selector.currentIndex() == 0:
            object_type=ObjectType.BOUND
        else:
            object_type = ObjectType.FLUID

        self.mkvalue_input.set_object_type(object_type)
        self.mkrange_min_input.set_object_type(object_type)
        self.mkrange_max_input.set_object_type(object_type)

    def fill_values(self):
        super().fill_values()
        if self.data.obj_type == ObjectType.BOUND:
            self.obj_type_selector.setCurrentIndex(0)
        elif self.data.obj_type == ObjectType.FLUID:
            self.obj_type_selector.setCurrentIndex(1)
        self.range_checkbox.setChecked(self.data.is_range)
        self.on_change_object_type()
        self.mkvalue_input.set_mk_index(self.data.mk_value)
        self.mkrange_min_input.set_mk_index(self.data.range_min)
        self.mkrange_max_input.set_mk_index(self.data.range_max)
        self.on_check_range(self.range_checkbox.isChecked())

    def save_data(self):
        super().save_data()
        if self.obj_type_selector.currentIndex() == 0:
            self.data.obj_type = ObjectType.BOUND
        elif self.obj_type_selector.currentIndex() == 1:
            self.data.obj_type = ObjectType.FLUID
        self.data.is_range=self.range_checkbox.isChecked()
        self.data.mk_value = self.mkvalue_input.get_mk_value()
        self.data.range_min = self.mkrange_min_input.get_mk_value()
        self.data.range_max = self.mkrange_max_input.get_mk_value()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
