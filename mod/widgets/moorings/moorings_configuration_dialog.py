#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Moorings Configuration Dialog. """

from copy import deepcopy

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog

from mod.constants import MKFLUID_LIMIT
from mod.enums import MooringsConfigurationMethod, ObjectType

from mod.dataobjects.case import Case
from mod.dataobjects.moorings.moorings_configuration import MooringsConfiguration
from mod.dataobjects.moorings.moordyn.moordyn_body import MoorDynBody
from mod.dataobjects.moorings.moordyn.moordyn_configuration import MoorDynConfiguration

from mod.widgets.moorings.moordyn_parameters_dialog import MoorDynParametersDialog


class MooringsCompatibleFloatingWidget(QtGui.QWidget):
    """ Widget to embed in each element of the floating list for the Moorings Configuration Dialog. """

    def __init__(self, checked: bool, obj_type: ObjectType, mkbound: int):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.root_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.root_layout.setContentsMargins(5, 1, 5, 1)
        self.mkbound = mkbound

        self.use_checkbox: QtGui.QCheckBox = QtGui.QCheckBox()
        self.use_checkbox.setChecked(checked)

        self.mkbound_label: QtGui.QLabel = QtGui.QLabel("{} - <b>{}</b>".format(obj_type.capitalize(), str(self.mkbound)))

        self.root_layout.addWidget(self.use_checkbox)
        self.root_layout.addWidget(self.mkbound_label)
        self.root_layout.addStretch(1)

        self.setLayout(self.root_layout)


class MooringsConfigurationDialog(QtGui.QDialog):
    """ DesignSPHysics Moorings Configuration Dialog. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(__("Moorings configuration Dialog"))
        self.setMinimumSize(640, 480)

        self.moordyn_parameters_data: MoorDynConfiguration = deepcopy(Case.the().moorings.moordyn_configuration)  # Result of the MoorDynParametersDialog

        self.root_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()

        # Composing the top enabled selector layout
        self.enabled_selector_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.enabled_selector_label: QtGui.QLabel = QtGui.QLabel(__("Enabled:"))
        self.enabled_selector_combobox: QtGui.QComboBox = QtGui.QComboBox()
        self.enabled_selector_combobox.addItems([__("No"), __("Yes")])
        self.enabled_selector_layout.addWidget(self.enabled_selector_label)
        self.enabled_selector_layout.addWidget(self.enabled_selector_combobox)
        self.enabled_selector_layout.addStretch(1)

        # Save options layout
        self.save_options_hlayout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.savevtk_label: QtGui.QLabel = QtGui.QLabel(__("Save VTK:"))
        self.savevtk_combo: QtGui.QComboBox = QtGui.QComboBox()
        self.savevtk_combo.addItems([__("Yes"), __("No")])

        self.savepointscsv_label: QtGui.QLabel = QtGui.QLabel(__("Save points (CSV):"))
        self.savepointscsv_combo: QtGui.QComboBox = QtGui.QComboBox()
        self.savepointscsv_combo.addItems([__("Yes"), __("No")])

        self.savepointsvtk_label: QtGui.QLabel = QtGui.QLabel(__("Save points (VTK):"))
        self.savepointsvtk_combo: QtGui.QComboBox = QtGui.QComboBox()
        self.savepointsvtk_combo.addItems([__("Yes"), __("No")])

        self.save_options_hlayout.addWidget(self.savevtk_label)
        self.save_options_hlayout.addWidget(self.savevtk_combo)
        self.save_options_hlayout.addStretch(1)
        self.save_options_hlayout.addWidget(self.savepointscsv_label)
        self.save_options_hlayout.addWidget(self.savepointscsv_combo)
        self.save_options_hlayout.addStretch(1)
        self.save_options_hlayout.addWidget(self.savepointsvtk_label)
        self.save_options_hlayout.addWidget(self.savepointsvtk_combo)

        # Floating selection layout
        self.floating_selection_vlayout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()
        self.floating_selection_label: QtGui.QLabel = QtGui.QLabel(__("Select mks to use with moorings:"))
        self.floating_selection_table: QtGui.QTableWidget = QtGui.QTableWidget(0, 1)
        self.floating_selection_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.floating_selection_table.horizontalHeader().hide()
        self.floating_selection_table.verticalHeader().hide()
        self.floating_selection_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.floating_selection_vlayout.addWidget(self.floating_selection_label)
        self.floating_selection_vlayout.addWidget(self.floating_selection_table)

        # Configuration method selection layout
        self.configuration_method_hlayout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.configuration_method_label: QtGui.QLabel = QtGui.QLabel(__("Configuration method for MoorDyn:"))
        self.configuration_method_combo: QtGui.QComboBox = QtGui.QComboBox()
        self.configuration_method_combo.addItems([__("Embedded"), __("From XML")])
        self.configuration_method_hlayout.addWidget(self.configuration_method_label)
        self.configuration_method_hlayout.addWidget(self.configuration_method_combo)
        self.configuration_method_hlayout.addStretch(1)

        # XML File selection layout
        self.xml_file_selection_widget: QtGui.QWidget = QtGui.QWidget()
        self.xml_file_selection_hlayout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.xml_file_selection_hlayout.setContentsMargins(0, 0, 0, 0)
        self.xml_file_selection_label: QtGui.QLabel = QtGui.QLabel(__("XML File:"))
        self.xml_file_selection_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.xml_file_selection_edit.setPlaceholderText(__("Type a path or select a file"))
        self.xml_file_selection_button: QtGui.QPushButton = QtGui.QPushButton("...")

        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_label)
        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_edit)
        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_button)

        self.xml_file_selection_widget.setLayout(self.xml_file_selection_hlayout)
        self.xml_file_selection_widget.hide()

        # Configure MoorDyn big button
        self.configure_moordyn_button: QtGui.QPushButton = QtGui.QPushButton(__("Configure MoorDyn Parameters"))

        # Composing the bottom button layout (Ok and Cancel buttons)
        self.bottom_button_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ok_button: QtGui.QPushButton = QtGui.QPushButton(__("OK"))
        self.cancel_button: QtGui.QPushButton = QtGui.QPushButton(__("Cancel"))
        self.bottom_button_layout.addStretch(1)
        self.bottom_button_layout.addWidget(self.cancel_button)
        self.bottom_button_layout.addWidget(self.ok_button)

        # Merging all components in the dialog
        self.root_layout.addLayout(self.enabled_selector_layout)
        self.root_layout.addLayout(self.save_options_hlayout)
        self.root_layout.addLayout(self.floating_selection_vlayout)
        self.root_layout.addLayout(self.configuration_method_hlayout)
        self.root_layout.addWidget(self.xml_file_selection_widget)
        self.root_layout.addWidget(self.configure_moordyn_button)
        self.root_layout.addLayout(self.bottom_button_layout)

        # Widget signal connections
        self.enabled_selector_combobox.currentIndexChanged.connect(self._on_enabled_change)
        self.configuration_method_combo.currentIndexChanged.connect(self._on_configuration_method_change)
        self.configure_moordyn_button.clicked.connect(self._on_configure_moordyn_parameters)
        self.ok_button.clicked.connect(self._on_ok)
        self.cancel_button.clicked.connect(self._on_cancel)

        self.setLayout(self.root_layout)

        # Fill data
        self._fill_data()

        # Manual signal trigger
        self._on_enabled_change(self.enabled_selector_combobox.currentIndex())
        self._on_configuration_method_change(self.configuration_method_combo.currentIndex())

        self.exec_()

    def _on_enabled_change(self, index) -> None:
        """ Enables/Disables all the widgets if the enabled combo box is changed. """
        self.savepointscsv_combo.setEnabled(index == 1)
        self.savevtk_combo.setEnabled(index == 1)
        self.savepointsvtk_combo.setEnabled(index == 1)
        self.floating_selection_table.setEnabled(index == 1)
        self.configuration_method_combo.setEnabled(index == 1)
        self.xml_file_selection_widget.setEnabled(index == 1)
        self.configure_moordyn_button.setEnabled(index == 1)

    def _on_configuration_method_change(self, index) -> None:
        """ Hides and shows the appropriate widget based on the configuration selected by the combobox. """
        if index == 0:
            self.xml_file_selection_widget.hide()
            self.configure_moordyn_button.show()
        if index == 1:
            self.xml_file_selection_widget.show()
            self.configure_moordyn_button.hide()

    def _fill_data(self) -> None:
        """ Fills the data passed on the constructor to the different widgets. """
        case = Case.the()
        floating_mkbasedproperties: list = list(filter(lambda mkp: mkp.float_property, case.mkbasedproperties.values()))
        self.enabled_selector_combobox.setCurrentIndex(1 if case.moorings.enabled else 0)
        self.savevtk_combo.setCurrentIndex(0 if case.moorings.saveoptions.savevtk_moorings else 1)
        self.savepointscsv_combo.setCurrentIndex(0 if case.moorings.saveoptions.savecsv_points else 1)
        self.savepointsvtk_combo.setCurrentIndex(0 if case.moorings.saveoptions.savevtk_points else 1)
        self.floating_selection_table.setRowCount(len(floating_mkbasedproperties))
        self.configuration_method_combo.setCurrentIndex({MooringsConfigurationMethod.EMBEDDED: 0, MooringsConfigurationMethod.FROM_XML: 1}[case.moorings.configuration_method])
        self.xml_file_selection_edit.setText(case.moorings.moordyn_xml)

        for index, mkprop in enumerate(floating_mkbasedproperties):
            target_widget: MooringsCompatibleFloatingWidget = MooringsCompatibleFloatingWidget(mkprop.mk - MKFLUID_LIMIT in case.moorings.moored_floatings, ObjectType.BOUND, mkprop.mk - MKFLUID_LIMIT)  # Offset the mk to convert in mkbound
            self.floating_selection_table.setCellWidget(index, 0, target_widget)

    def _on_configure_moordyn_parameters(self) -> None:
        """ Opens up the MoorDyn configuration parameters dialog. """
        new_selected_bodies: list = list()

        for row_num in range(0, self.floating_selection_table.rowCount()):
            target_widget: MooringsCompatibleFloatingWidget = self.floating_selection_table.cellWidget(row_num, 0)
            if target_widget.use_checkbox.isChecked():
                list_of_matching_bodies: list = list(filter(lambda body: body.ref == target_widget.mkbound, self.moordyn_parameters_data.bodies))
                new_body: MoorDynBody = list_of_matching_bodies[0] if list_of_matching_bodies else MoorDynBody(target_widget.mkbound)
                new_selected_bodies.append(new_body)

        self.moordyn_parameters_data.bodies = list(new_selected_bodies)
        if not self.moordyn_parameters_data.bodies:
            error_dialog(__("You must at least select one floating body to configure MoorDyn"))
            return

        MoorDynParametersDialog(self.moordyn_parameters_data)

    def _on_ok(self) -> None:
        """ Reacts to the ok button being pressed. """
        if self.enabled_selector_combobox.currentIndex() == 1:
            Case.the().moorings.enabled = True
            Case.the().moorings.saveoptions.savecsv_points = self.savepointscsv_combo.currentIndex() == 0
            Case.the().moorings.saveoptions.savevtk_moorings = self.savevtk_combo.currentIndex() == 0
            Case.the().moorings.saveoptions.savevtk_points = self.savepointsvtk_combo.currentIndex() == 0
            Case.the().moorings.configuration_method = {0: MooringsConfigurationMethod.EMBEDDED, 1: MooringsConfigurationMethod.FROM_XML}[self.configuration_method_combo.currentIndex()]
            Case.the().moorings.moordyn_xml = self.xml_file_selection_edit.text()
            moored_floatings = Case.the().moorings.moored_floatings
            for row_num in range(0, self.floating_selection_table.rowCount()):
                target_widget: MooringsCompatibleFloatingWidget = self.floating_selection_table.cellWidget(row_num, 0)
                if target_widget.use_checkbox.isChecked() and target_widget.mkbound not in moored_floatings:
                    moored_floatings.append(target_widget.mkbound)
                if not target_widget.use_checkbox.isChecked() and target_widget.mkbound in moored_floatings:
                    moored_floatings.remove(target_widget.mkbound)
            Case.the().moorings.moordyn_configuration = deepcopy(self.moordyn_parameters_data)
        else:
            Case.the().moorings = MooringsConfiguration()
        self.accept()

    def _on_cancel(self) -> None:
        """ Reacts to the cancel button being pressed. """
        self.reject()
