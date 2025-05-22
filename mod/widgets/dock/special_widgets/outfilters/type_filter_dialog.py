from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import TypeFilter
from mod.tools.dialog_tools import warning_dialog
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.outfilters.base_dialog import BaseFilterDialog


class TypeFilterDialog(BaseFilterDialog):

    def __init__(self, type_filter, parent=None):
        super().__init__(base_filter=type_filter, parent=parent)
        self.data:TypeFilter = type_filter
        self.type_layout = QHBoxLayout()
        self.bound_checkbox = QtWidgets.QCheckBox(__("Bound"))
        self.fixed_checkbox = QtWidgets.QCheckBox(__("Fixed"))
        self.moving_checkbox = QtWidgets.QCheckBox(__("Moving"))
        self.floating_checkbox = QtWidgets.QCheckBox(__("Floating"))
        self.fluid_checkbox = QtWidgets.QCheckBox(__("Fluid"))

        for x in [self.bound_checkbox, self.fixed_checkbox, self.moving_checkbox, self.floating_checkbox,
                  self.fluid_checkbox]:
            self.type_layout.addWidget(x)

        self.main_layout.insertLayout(2, self.type_layout)
        self.fill_values()

    def fill_values(self):
        super().fill_values()
        self.bound_checkbox.setChecked(self.data.bound)
        self.fixed_checkbox.setChecked(self.data.fixed)
        self.moving_checkbox.setChecked(self.data.moving)
        self.floating_checkbox.setChecked(self.data.floating)
        self.fluid_checkbox.setChecked(self.data.fluid)

    def save_data(self):
        super().save_data()
        self.data.bound = self.bound_checkbox.isChecked()
        self.data.fixed = self.fixed_checkbox.isChecked()
        self.data.moving = self.moving_checkbox.isChecked()
        self.data.floating = self.floating_checkbox.isChecked()
        self.data.fluid = self.fluid_checkbox.isChecked()
        if self.data.name:
            self.accept()
        else:
            warning_dialog("Please name your Filter")
