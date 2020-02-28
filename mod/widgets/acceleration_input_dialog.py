#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Acceleration Input Dialog."""

from PySide import QtCore, QtGui

from mod.translation_tools import __

from mod.dataobjects.acceleration_input_data import AccelerationInputData

from mod.dataobjects.case import Case


class AccelerationInputDialog(QtGui.QDialog):
    """ A Dialog which shows the contents of the case AccelerationInput object.
    Shows a list with the AccelerationInputData objects defined for the case and
    its details when clicked.
    Returns: AccelerationInput object"""

    def __init__(self, accinput, parent=None):
        super().__init__(parent=parent)
        self.accinput = accinput
        self.setWindowTitle(__("Acceleration Input List"))

        self.main_layout = QtGui.QVBoxLayout()

        self.enabled_check = QtGui.QCheckBox(__("Enabled"))

        self.accinput_layout = QtGui.QHBoxLayout()

        self.accinput_list_groupbox = QtGui.QGroupBox(__("Acceleration Input list"))
        self.accinput_list_layout = QtGui.QVBoxLayout()
        self.accinput_list = QtGui.QListWidget()
        self.accinput_list_button_layout = QtGui.QHBoxLayout()
        self.accinput_list_add_button = QtGui.QPushButton("Add new")
        self.accinput_list_remove_button = QtGui.QPushButton("Remove selected")

        self.accinput_list_button_layout.addWidget(self.accinput_list_add_button)
        self.accinput_list_button_layout.addWidget(self.accinput_list_remove_button)

        self.accinput_list_layout.addWidget(self.accinput_list)
        self.accinput_list_layout.addLayout(self.accinput_list_button_layout)
        self.accinput_list_groupbox.setLayout(self.accinput_list_layout)

        self.accinput_data_groupbox = QtGui.QGroupBox(__("Acceleration Input data"))
        self.accinput_data_layout = QtGui.QVBoxLayout()

        self.accinput_label_layout = QtGui.QHBoxLayout()
        self.accinput_label_label = QtGui.QLabel(__("Label:"))
        self.accinput_label_input = QtGui.QLineEdit()
        self.accinput_label_layout.addWidget(self.accinput_label_label)
        self.accinput_label_layout.addWidget(self.accinput_label_input)

        self.accinput_mkfluid_layout = QtGui.QHBoxLayout()
        self.accinput_mkfluid_label = QtGui.QLabel(__("Mk-fluid of selected particles:"))
        self.accinput_mkfluid_input = QtGui.QLineEdit()
        self.accinput_mkfluid_layout.addWidget(self.accinput_mkfluid_label)
        self.accinput_mkfluid_layout.addWidget(self.accinput_mkfluid_input)

        self.accinput_acccentre_layout = QtGui.QHBoxLayout()
        self.accinput_acccentre_label = QtGui.QLabel(__("Center of acceleration [X,Y,Z] (m):"))
        self.accinput_acccentre_x = QtGui.QLineEdit()
        self.accinput_acccentre_y = QtGui.QLineEdit()
        self.accinput_acccentre_z = QtGui.QLineEdit()

        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_label)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_x)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_y)
        self.accinput_acccentre_layout.addWidget(self.accinput_acccentre_z)

        self.accinput_globalgravity_layout = QtGui.QHBoxLayout()
        self.accinput_globalgravity_check = QtGui.QCheckBox(__("Global Gravity"))
        self.accinput_globalgravity_layout.addWidget(self.accinput_globalgravity_check)

        self.accinput_datafile_layout = QtGui.QHBoxLayout()
        self.accinput_datafile_label = QtGui.QLabel(__("File with acceleration data:"))
        self.accinput_datafile_input = QtGui.QLineEdit()
        self.accinput_datafile_button = QtGui.QPushButton(__("..."))
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_label)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_input)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_button)

        self.accinput_save_layout = QtGui.QHBoxLayout()
        self.accinput_save_button = QtGui.QPushButton(__("Save Data"))
        self.accinput_save_layout.addStretch(1)
        self.accinput_save_layout.addWidget(self.accinput_save_button)

        self.accinput_data_layout.addLayout(self.accinput_label_layout)
        self.accinput_data_layout.addLayout(self.accinput_mkfluid_layout)
        self.accinput_data_layout.addLayout(self.accinput_acccentre_layout)
        self.accinput_data_layout.addLayout(self.accinput_globalgravity_layout)
        self.accinput_data_layout.addLayout(self.accinput_datafile_layout)
        self.accinput_data_layout.addLayout(self.accinput_save_layout)

        self.accinput_data_groupbox.setLayout(self.accinput_data_layout)

        self.accinput_layout.addWidget(self.accinput_list_groupbox)
        self.accinput_layout.addWidget(self.accinput_data_groupbox)

        self.button_layout = QtGui.QHBoxLayout()
        self.ok_button = QtGui.QPushButton(__("OK"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.enabled_check)
        self.main_layout.addLayout(self.accinput_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

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

    def init_connections(self):
        """ Connects widget signals with their corresponding methods. """
        self.ok_button.clicked.connect(self.on_ok)
        self.accinput_datafile_button.clicked.connect(self.on_browse)
        self.accinput_list_add_button.clicked.connect(self.on_add)
        self.accinput_list_remove_button.clicked.connect(self.on_remove)
        self.accinput_list.itemSelectionChanged.connect(self.on_list_select)
        self.accinput_save_button.clicked.connect(self.on_save_data)
        self.enabled_check.stateChanged.connect(self.on_enable)

    def on_ok(self):
        """ Defines behaviour on ok button press. """
        self.accept()

    def on_browse(self):
        """ Opens a file dialog to select a file to use. """
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self, "Select file to use", Case.the().info.last_used_directory)
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

    def on_list_select(self):
        """ Reacts to an acceleration input data being selected. """
        if not self.accinput.acclist:
            return
        index = self.accinput_list.currentRow()
        if index < 0 or index > len(self.accinput.acclist) - 1:
            return
        item = self.accinput.acclist[index]
        self.accinput_label_input.setText(item.label)
        self.accinput_mkfluid_input.setText(str(item.mkfluid))
        self.accinput_acccentre_x.setText(str(item.acccentre[0]))
        self.accinput_acccentre_y.setText(str(item.acccentre[1]))
        self.accinput_acccentre_z.setText(str(item.acccentre[2]))
        self.accinput_globalgravity_check.setChecked(bool(item.globalgravity))
        self.accinput_datafile_input.setText(item.datafile)

    def list_refresh(self):
        """ Refreshes the acceleration input list. """
        self.accinput_list.clear()
        self.accinput_list.insertItems(0, [x.label for x in self.accinput.acclist])
        self.accinput_list.setCurrentRow(0)

    def on_save_data(self):
        """ Saves the data on the window to the acceleration input configuration. """
        if not self.accinput.acclist:
            return
        index = self.accinput_list.currentRow()
        item = self.accinput.acclist[index]

        item.label = str(self.accinput_label_input.text())
        item.mkfluid = int(self.accinput_mkfluid_input.text())
        item.acccentre = [float(self.accinput_acccentre_x.text()),
                          float(self.accinput_acccentre_y.text()),
                          float(self.accinput_acccentre_z.text())]
        item.globalgravity = bool(self.accinput_globalgravity_check.isChecked())
        item.datafile = str(self.accinput_datafile_input.text())

        self.accinput.acclist[index] = item
        self.list_refresh()

    def on_enable(self):
        """ Enables the widgets on acceleration input enable. """
        self.accinput.enabled = self.enabled_check.isChecked()
        self.accinput_list_groupbox.setEnabled(self.accinput.enabled)
        self.accinput_data_groupbox.setEnabled(self.accinput.enabled)
