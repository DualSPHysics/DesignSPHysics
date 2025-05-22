#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Acceleration Input Dialog."""

from PySide2 import QtCore, QtWidgets
from mod.enums import ObjectType
from mod.tools.stdout_tools import debug

from mod.tools.translation_tools import __

from mod.dataobjects.acceleration_input.acceleration_input_data import AccelerationInputData

from mod.dataobjects.case import Case
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput


class AccelerationInputDialog(QtWidgets.QDialog):
    """ A Dialog which shows the contents of the case AccelerationInput object.
    Shows a list with the AccelerationInputData objects defined for the case and
    its details when clicked.
    Returns: AccelerationInput object"""

    def __init__(self, accinput, parent=None):
        super().__init__(parent=parent)
        self.accinput = accinput
        self.setWindowTitle(__("Acceleration Input List"))

        self.main_layout = QtWidgets.QVBoxLayout()

        self.enabled_check = QtWidgets.QCheckBox(__("Enabled"))

        self.accinput_layout = QtWidgets.QHBoxLayout()
        # LEFT LIST
        self.accinput_list_groupbox = QtWidgets.QGroupBox(__("Acceleration Input list"))
        self.accinput_list_layout = QtWidgets.QVBoxLayout()
        self.accinput_list = QtWidgets.QListWidget()
        self.accinput_list_button_layout = QtWidgets.QHBoxLayout()
        self.accinput_list_add_button = QtWidgets.QPushButton("Add new")
        self.accinput_list_remove_button = QtWidgets.QPushButton("Remove selected")

        self.accinput_list_button_layout.addWidget(self.accinput_list_add_button)
        self.accinput_list_button_layout.addWidget(self.accinput_list_remove_button)

        self.accinput_list_layout.addWidget(self.accinput_list)
        self.accinput_list_layout.addLayout(self.accinput_list_button_layout)
        self.accinput_list_groupbox.setLayout(self.accinput_list_layout)

        # RIGHT FORM
        self.accinput_data_groupbox = QtWidgets.QGroupBox(__("Acceleration Input data"))
        self.accinput_data_layout = QtWidgets.QVBoxLayout()

        self.accinput_label_layout = QtWidgets.QHBoxLayout()
        self.accinput_label_label = QtWidgets.QLabel(__("Label:"))
        self.accinput_label_input = QtWidgets.QLineEdit()
        self.accinput_label_layout.addWidget(self.accinput_label_label)
        self.accinput_label_layout.addWidget(self.accinput_label_input)

        self.accinput_time_layout = QtWidgets.QHBoxLayout()
        self.accinput_time_start_label = QtWidgets.QLabel(__("Time start:"))
        self.accinput_time_start_input = TimeInput()
        self.accinput_time_end_label = QtWidgets.QLabel(__("Time end:"))
        self.accinput_time_end_input = TimeInput()
        for x in [self.accinput_time_start_label, self.accinput_time_start_input, self.accinput_time_end_label,
                  self.accinput_time_end_input]:
            self.accinput_time_layout.addWidget(x)

        self.accinput_mk_layout = QtWidgets.QHBoxLayout()
        self.accinput_type_label = QtWidgets.QLabel(__("Select object type"))
        self.accinput_type_combobox = QtWidgets.QComboBox()
        self.accinput_type_combobox.addItems([__("Bound"),__("Fluid")])
        self.accinput_mkbound_label = QtWidgets.QLabel(__("Mk-bound of selected particles:"))
        self.accinput_mkbound_input = MkSelectInputWithNames(obj_type=ObjectType.BOUND)
        self.accinput_mkfluid_label = QtWidgets.QLabel(__("Mk-fluid of selected particles:"))
        self.accinput_mkfluid_input = MkSelectInputWithNames(obj_type=ObjectType.FLUID)
        for x in [self.accinput_type_label, self.accinput_type_combobox, self.accinput_mkbound_label,
                  self.accinput_mkbound_input, self.accinput_mkfluid_label, self.accinput_mkfluid_input]:
            self.accinput_mk_layout.addWidget(x)

        self.accinput_acccentre_layout = QtWidgets.QHBoxLayout()
        self.accinput_acccentre_label = QtWidgets.QLabel(__("Center of acceleration [X,Y,Z] (m):"))
        self.accinput_acccentre_x = SizeInput()
        self.accinput_acccentre_y = SizeInput()
        self.accinput_acccentre_z = SizeInput()

        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_label)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_x)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_y)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_z)

        self.accinput_globalgravity_layout = QtWidgets.QHBoxLayout()
        self.accinput_globalgravity_check = QtWidgets.QCheckBox(__("Global Gravity"))
        self.accinput_globalgravity_layout.addWidget(self.accinput_globalgravity_check)

        self.accinput_datafile_layout = QtWidgets.QHBoxLayout()
        self.accinput_datafile_label = QtWidgets.QLabel(__("File with acceleration data:"))
        self.accinput_datafile_input = QtWidgets.QLineEdit()
        self.accinput_datafile_button = QtWidgets.QPushButton(__("..."))
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_label)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_input)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_button)

        self.accinput_data_layout.addLayout(self.accinput_label_layout)
        self.accinput_data_layout.addLayout(self.accinput_time_layout)
        self.accinput_data_layout.addLayout(self.accinput_mk_layout)
        self.accinput_data_layout.addLayout(self.accinput_acccentre_layout)
        self.accinput_data_layout.addLayout(self.accinput_globalgravity_layout)
        self.accinput_data_layout.addLayout(self.accinput_datafile_layout)

        self.accinput_data_groupbox.setLayout(self.accinput_data_layout)

        self.accinput_layout.addWidget(self.accinput_list_groupbox)
        self.accinput_layout.addWidget(self.accinput_data_groupbox)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.enabled_check)
        self.main_layout.addLayout(self.accinput_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.accinput_data_groupbox.setEnabled(False)

        self.fill_data()
        self.init_connections()

    def get_result(self):
        """ Returns the AccelerationInput object """
        return self.accinput

    def fill_data(self):
        """ Sets the data for the dialog. """
        self.list_refresh()
        self.on_list_select()
        self.enabled_check.setCheckState(QtCore.Qt.Checked if self.accinput.enabled else QtCore.Qt.Unchecked)
        self.on_enable()
        self.on_change_type()

    def init_connections(self):
        """ Connects widget signals with their corresponding methods. """
        self.ok_button.clicked.connect(self.on_ok)
        self.accinput_datafile_button.clicked.connect(self.on_browse)
        self.accinput_list_add_button.clicked.connect(self.on_add)
        self.accinput_list_remove_button.clicked.connect(self.on_remove)
        self.accinput_list.itemSelectionChanged.connect(self.on_list_select)
        self.enabled_check.stateChanged.connect(self.on_enable)
        self.accinput_label_input.textChanged.connect(self.on_save_data)
        for x in [self.accinput_time_start_input, self.accinput_time_end_input,
                  self.accinput_acccentre_x, self.accinput_acccentre_y, self.accinput_acccentre_z]:
            x.value_changed.connect(self.on_save_data)
        self.accinput_type_combobox.currentIndexChanged.connect(self.on_change_type)

    def on_ok(self):
        """ Defines behaviour on ok button press. """
        self.accept()

    def on_browse(self):
        """ Opens a file dialog to select a file to use. """
        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Select file to use",
                                                           Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(file_name)
        self.accinput_datafile_input.setText(file_name)

    def on_add(self):
        """ Adds the acceleration input thata to the acceleration input list. """
        self.accinput.acclist.append(AccelerationInputData())
        self.list_refresh()

    def on_remove(self):
        """ Removes the acceleration input data from the data structure. """
        if not self.accinput.acclist:
            return
        index = self.accinput_list.currentRow()
        self.accinput.acclist.pop(index)
        self.list_refresh()
        if self.accinput_list.currentRow()==-1:
            self.accinput_data_groupbox.setEnabled(False)

    def on_list_select(self):
        """ Reacts to an acceleration input data being selected. """
        if not self.accinput.acclist:
            return
        index = self.accinput_list.currentRow()
        if index < 0 or index > len(self.accinput.acclist) - 1:
            return
        item: AccelerationInputData = self.accinput.acclist[index]
        self.accinput_data_groupbox.setEnabled(True)
        self.load_item_values(item)

    def load_item_values(self, item):
        self.accinput_label_input.setText(item.label)
        self.accinput_type_combobox.setCurrentIndex(1 if item.is_fluid else 0)
        self.accinput_mkfluid_input.setCurrentIndex(item.mkfluid)
        self.accinput_mkbound_input.setCurrentIndex(item.mkbound)
        self.accinput_time_start_input.setValue(item.time_start)
        self.accinput_time_end_input.setValue(item.time_end)
        self.accinput_acccentre_x.setValue(item.acccentre[0])
        self.accinput_acccentre_y.setValue(item.acccentre[1])
        self.accinput_acccentre_z.setValue(item.acccentre[2])
        self.accinput_globalgravity_check.setChecked(bool(item.globalgravity))
        self.accinput_datafile_input.setText(item.datafile)
        self.on_change_type()

    def list_refresh(self):
        """ Refreshes the acceleration input list. """
        row = self.accinput_list.currentRow()
        self.accinput_list.clear()
        self.accinput_list.insertItems(0, [x.label for x in self.accinput.acclist])
        self.accinput_list.setCurrentRow(row)

    def on_save_data(self):
        """ Saves the data on the window to the acceleration input configuration. """
        if not self.accinput.acclist:
            return
        index = self.accinput_list.currentRow()
        item: AccelerationInputData = self.accinput.acclist[index]

        item.label = str(self.accinput_label_input.text())
        item.time_start = self.accinput_time_start_input.value()
        item.time_end = self.accinput_time_end_input.value()
        item.is_fluid = self.accinput_type_combobox.currentIndex()==1
        item.mkfluid = self.accinput_mkfluid_input.get_mk_value()
        item.mkbound = self.accinput_mkbound_input.get_mk_value()
        item.acccentre = [self.accinput_acccentre_x.value(),
                          self.accinput_acccentre_y.value(),
                          self.accinput_acccentre_z.value()]
        item.globalgravity = bool(self.accinput_globalgravity_check.isChecked())
        item.datafile = str(self.accinput_datafile_input.text())

        self.accinput.acclist[index] = item
        self.list_refresh()

    def on_enable(self):
        """ Enables the widgets on acceleration input enable. """
        self.accinput.enabled = self.enabled_check.isChecked()
        self.accinput_list_groupbox.setEnabled(self.accinput.enabled)
        self.accinput_data_groupbox.setEnabled(self.accinput.enabled and self.accinput_list.currentRow()>-1)#sdfgsdfgdfg

    def on_change_type(self):
        fluid: bool = self.accinput_type_combobox.currentIndex()==1
        if fluid:
            self.accinput_mkfluid_input.setVisible(True)
            self.accinput_mkfluid_label.setVisible(True)
            self.accinput_mkbound_input.setVisible(False)
            self.accinput_mkbound_label.setVisible(False)
        else:
            self.accinput_mkfluid_input.setVisible(False)
            self.accinput_mkfluid_label.setVisible(False)
            self.accinput_mkbound_input.setVisible(True)
            self.accinput_mkbound_label.setVisible(True)
