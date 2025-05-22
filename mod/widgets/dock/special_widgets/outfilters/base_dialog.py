from PySide2.QtWidgets import QHBoxLayout

from PySide2 import QtWidgets
from mod.dataobjects.outparts_filter.filters import BaseFilter
from mod.enums import FilterOperations, ObjectType
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames


class BaseFilterDialog(QtWidgets.QDialog):


    def __init__(self, base_filter, parent):
        super().__init__(parent=parent)
        self.data:BaseFilter = base_filter

        self.main_layout = QtWidgets.QVBoxLayout()

        self.name_layout = QHBoxLayout()
        self.name_label = QtWidgets.QLabel(__("Filter name"))
        self.name_input = QtWidgets.QLineEdit()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)

        self.base = QHBoxLayout()
        self.operation_label = QtWidgets.QLabel(__("Operation"))
        self.operation_combobox = QtWidgets.QComboBox()
        self.operation_combobox.addItem("add")
        self.operation_combobox.addItem("del")
        self.operation_combobox.addItem("confirm")
        self.inverse_checkbox = QtWidgets.QCheckBox(text=__("Inverse"))
        for x in [self.operation_label, self.operation_combobox, self.inverse_checkbox,]:
            self.base.addWidget(x)
        self.ftfollow_layout = QHBoxLayout()
        self.ftfollow_checkbox= QtWidgets.QCheckBox(text=__("Follow MK:"))
        self.ftfollow_mk_label = QtWidgets.QLabel(__("MK"))
        self.ftfollow_mk_select = MkSelectInputWithNames(obj_type=ObjectType.BOUND)
        for x in [self.ftfollow_checkbox,  self.ftfollow_mk_label, self.ftfollow_mk_select]:
            self.ftfollow_layout.addWidget(x)

        self.buttons_layout = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(text=__("OK"))
        self.ok_button.clicked.connect(self.save_data)
        self.buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(self.name_layout)
        self.main_layout.addLayout(self.base)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def fill_values(self):
        if self.data.name != "":
            self.name_input.setText(self.data.name)
            self.name_input.setEnabled(False)

        self.operation_combobox.setCurrentIndex(FilterOperations.pos[self.data.operation])
        self.inverse_checkbox.setChecked(self.data.inverse)
        self.ftfollow_checkbox.setChecked(self.data.ftfollow_active)
        self.ftfollow_mk_select.set_mk_index(self.data.ftfollow_mk)

    def save_data(self):
        self.data.name = self.name_input.text()
        self.data.operation=FilterOperations.operation[self.operation_combobox.currentText()]
        self.data.inverse=self.inverse_checkbox.isChecked()
        self.data.ftfollow_active=self.ftfollow_checkbox.isChecked()
        self.data.ftfollow_mk=self.ftfollow_mk_select.get_mk_value()


