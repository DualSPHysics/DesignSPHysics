#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Moorings Configuration Dialog. """

from PySide import QtGui

from mod.translation_tools import __


class MooringsConfigurationDialog(QtGui.QDialog):
    """ DesignSPHysics Moorings Configuration Dialog. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(__("Moorings configuration Dialog"))
        self.setMinimumSize(640, 480)

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
        self.floating_selection_label: QtGui.QLabel = QtGui.QLabel(__("Select floatings to use with moorings:"))
        # FIXME: Map rows acoordingly
        self.floating_selection_table: QtGui.QTableWidget = QtGui.QTableWidget(50, 1)
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
        self.xml_file_selection_hlayout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.xml_file_selection_label: QtGui.QLabel = QtGui.QLabel(__("XML File:"))
        self.xml_file_selection_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.xml_file_selection_edit.setPlaceholderText(__("Type a path or select a file"))
        self.xml_file_selection_button: QtGui.QPushButton = QtGui.QPushButton("...")

        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_label)
        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_edit)
        self.xml_file_selection_hlayout.addWidget(self.xml_file_selection_button)

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
        self.root_layout.addLayout(self.xml_file_selection_hlayout)
        self.root_layout.addWidget(self.configure_moordyn_button)
        self.root_layout.addLayout(self.bottom_button_layout)

        self.setLayout(self.root_layout)
        self.exec_()
