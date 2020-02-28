#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Faces Configuration Dialog"""

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import info_dialog
from mod.gui_tools import h_line_generator

from mod.dataobjects.case import Case
from mod.dataobjects.mk_based_properties import MKBasedProperties
from mod.dataobjects.simulation_object import SimulationObject


class MaterialDialog(QtGui.QDialog):
    """ Defines a window with material configuration  """

    NO_MATERIAL_LABEL = __("No material was selected.")

    def __init__(self, selection_name, parent=None):
        super().__init__(parent=parent)

        self.setMinimumSize(400, 240)

        self.setWindowTitle(__("Material configuration"))
        self.ok_button = QtGui.QPushButton(__("OK"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.root_layout = QtGui.QVBoxLayout()

        self.target_object: SimulationObject = Case.the().get_simulation_object(selection_name)
        self.target_mkbasedproperties: MKBasedProperties = Case.the().get_mk_based_properties(self.target_object.type, self.target_object.obj_mk)

        self.selector_layout = QtGui.QHBoxLayout()
        self.material_label = QtGui.QLabel(__("Select a material:"))
        self.material_combo = QtGui.QComboBox()
        self.mk_label = QtGui.QLabel(__("Target MKBound: <b>{}</b>").format(self.target_object.obj_mk))

        self.selector_layout.addWidget(self.material_label)
        self.selector_layout.addWidget(self.material_combo)
        self.selector_layout.addStretch(1)
        self.selector_layout.addWidget(self.mk_label)

        self.material_details_label = QtGui.QLabel(self.NO_MATERIAL_LABEL)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.root_layout.addLayout(self.selector_layout)
        self.root_layout.addWidget(h_line_generator())
        self.root_layout.addWidget(self.material_details_label)
        self.root_layout.addStretch(1)
        self.root_layout.addLayout(self.button_layout)

        self.setLayout(self.root_layout)

        self.material_combo.currentIndexChanged.connect(self._on_material_combo_change)

        self.populate_materials()
        self._on_material_combo_change(self.material_combo.currentIndex())
        self.exec_()

    def populate_materials(self) -> None:
        """ Populates the combobox with the available materials. """
        to_insert = [__("None")]
        for material in Case.the().info.global_materials:
            to_insert.append(material.name)
        self.material_combo.insertItems(0, to_insert)

        combo_value = 0
        if self.target_mkbasedproperties.property:
            if self.target_mkbasedproperties.property in Case.the().info.global_materials:
                combo_value = Case.the().info.global_materials.index(self.target_mkbasedproperties.property) + 1
            else:
                self.target_mkbasedproperties.property = None

        self.material_combo.setCurrentIndex(combo_value)

    def _on_material_combo_change(self, index):
        if index == 0:
            self.material_details_label.setText(self.NO_MATERIAL_LABEL)
        else:
            self.material_details_label.setText(Case.the().info.global_materials[index - 1].html_str())

    def on_ok(self):
        """ Saves the material data and closes the dialog. """
        info_dialog(__("This will apply the motion properties to all objects with mkbound = ") + str(self.target_object.obj_mk))
        self.target_mkbasedproperties.property = None if self.material_combo.currentIndex() == 0 else Case.the().info.global_materials[self.material_combo.currentIndex() - 1]
        self.accept()

    def on_cancel(self):
        """ Closes the dialog and rejects it. """
        self.reject()
