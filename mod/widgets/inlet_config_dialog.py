#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet/Oulet Configuration Dialog """

import uuid
from traceback import print_exc

from PySide import QtCore, QtGui

from mod.translation_tools import __

from mod.widgets.inlet_zone_edit import InletZoneEdit

from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_config import InletOutletConfig
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone


class InletConfigDialog(QtGui.QDialog):
    """ Defines the Inlet/Outlet dialog window.
       Modifies data dictionary passed as parameter. """

    def __init__(self, parent=None):
        super(InletConfigDialog, self).__init__(parent=parent)

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet configuration")
        self.setModal(False)
        self.setMinimumWidth(520)
        self.setMinimumHeight(200)
        self.main_layout = QtGui.QVBoxLayout()

        # Creates layout for content first options
        self.option_layout = QtGui.QHBoxLayout()

        # Creates reuseids option
        self.reuseids_layout = QtGui.QHBoxLayout()
        self.reuseids_option = QtGui.QLabel(__("Reuseids: "))
        self.reuseids_combobox = QtGui.QComboBox()
        self.reuseids_combobox.insertItems(0, [__("False"), __("True")])

        try:
            if not Case.instance().inlet_outlet.reuseids:
                self.reuseids_combobox.setCurrentIndex(0)
            else:
                self.reuseids_combobox.setCurrentIndex(1)
        except:
            print_exc()
            self.reuseids_combobox.setCurrentIndex(0)

        self.reuseids_layout.addWidget(self.reuseids_option)
        self.reuseids_layout.addWidget(self.reuseids_combobox)
        self.reuseids_layout.addStretch(1)

        # Creates resizetime option
        self.resizetime_layout = QtGui.QHBoxLayout()
        self.resizetime_option = QtGui.QLabel(__("Resizetime: "))
        try:
            self.resizetime_line_edit = QtGui.QLineEdit(str(Case.instance().inlet_outlet.resizetime))
        except:
            print_exc()
            self.resizetime_line_edit = QtGui.QLineEdit("0.5")

        self.resizetime_layout.addWidget(self.resizetime_option)
        self.resizetime_layout.addWidget(self.resizetime_line_edit)
        self.resizetime_layout.addStretch(1)

        # Creates use refilling option
        self.refilling_layout = QtGui.QHBoxLayout()
        self.refilling_option = QtGui.QLabel(__("Refilling: "))
        self.refilling_combobox = QtGui.QComboBox()
        self.refilling_combobox.insertItems(0, [__("False"), __("True")])

        try:
            if str(Case.instance().inlet_outlet.userefilling) == "False":
                self.refilling_combobox.setCurrentIndex(0)
            else:
                self.refilling_combobox.setCurrentIndex(1)
        except:
            print_exc()
            self.refilling_combobox.setCurrentIndex(0)

        self.refilling_layout.addWidget(self.refilling_option)
        self.refilling_layout.addWidget(self.refilling_combobox)
        self.refilling_layout.addStretch(1)

        # Creates use determlimit option
        self.determlimit_layout = QtGui.QHBoxLayout()
        self.determlimit_option = QtGui.QLabel(__("Determlimit: "))
        self.determlimit_combobox = QtGui.QComboBox()
        self.determlimit_combobox.insertItems(0, [__("1e+3"), __("1e-3")])

        try:
            if str(Case.instance().inlet_outlet.determlimit) == "1e+3":
                self.determlimit_combobox.setCurrentIndex(0)
            else:
                self.determlimit_combobox.setCurrentIndex(1)
        except:
            print_exc()
            self.determlimit_combobox.setCurrentIndex(0)

        self.determlimit_layout.addWidget(self.determlimit_option)
        self.determlimit_layout.addWidget(self.determlimit_combobox)
        self.determlimit_layout.addStretch(1)

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        # Create the list for zones
        self.main_zones = QtGui.QGroupBox("Inlet/Outlet zones")
        self.main_zones.setMaximumWidth(500)
        self.zones_layout = QtGui.QVBoxLayout()
        self.zones_layout_list = QtGui.QVBoxLayout()

        # Add button
        self.inlet_button_layout = QtGui.QHBoxLayout()
        self.button_link_inlet = QtGui.QPushButton("Add Zone")
        self.inlet_button_layout.addStretch(1)
        self.inlet_button_layout.addWidget(self.button_link_inlet)
        self.button_link_inlet.clicked.connect(self.on_add_zone)

        self.zones_layout.addLayout(self.inlet_button_layout)
        self.zones_layout.addLayout(self.zones_layout_list)

        self.main_zones.setLayout(self.zones_layout)

        self.refresh_zones()

        # Adds options to option layout
        self.option_layout.addLayout(self.reuseids_layout)
        self.option_layout.addLayout(self.resizetime_layout)
        self.option_layout.addLayout(self.refilling_layout)
        self.option_layout.addLayout(self.determlimit_layout)

        # Adds options to main
        self.main_layout.addLayout(self.option_layout)
        self.main_layout.addWidget(self.main_zones)
        self.main_layout.addStretch(1)

        # Adds scroll area
        self.main_layout_dialog = QtGui.QVBoxLayout()
        self.main_layout_scroll = QtGui.QScrollArea()
        self.main_layout_scroll.setMinimumWidth(400)
        self.main_layout_scroll.setMaximumWidth(500)
        self.main_layout_scroll.setWidgetResizable(True)
        self.main_layout_scroll_widget = QtGui.QWidget()
        self.main_layout_scroll_widget.setMinimumWidth(400)
        self.main_layout_scroll_widget.setMaximumWidth(500)

        self.main_layout_scroll_widget.setLayout(self.main_layout)
        self.main_layout_scroll.setWidget(self.main_layout_scroll_widget)
        self.main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout_dialog.addWidget(self.main_layout_scroll)
        self.main_layout_dialog.addLayout(self.button_layout)

        self.setLayout(self.main_layout_dialog)

        self.exec_()

    def on_add_zone(self):
        """ Adds Inlet/Outlet zone """
        uid_temp = uuid.uuid4()
        Case.instance().inlet_outlet.zones.append(InletOutletZone())
        self.zone_edit(str(uid_temp))

    def refresh_zones(self):
        """ Refreshes the zones list """
        count = 0
        while self.zones_layout_list.count() > 0:
            target = self.zones_layout_list.takeAt(0)
            target.setParent(None)

        for inletObject in Case.instance().inlet_outlet.zones:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_layout2 = QtGui.QHBoxLayout()
            to_add_label2 = QtGui.QLabel(" ")
            to_add_layout2.addWidget(to_add_label2)
            to_add_label = QtGui.QLabel("I/O Zone " + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda io=inletObject.id: self.zone_edit(io))
            to_add_deletebutton.clicked.connect(lambda io=inletObject: self.zone_delete(io))
            self.zones_layout_list.addLayout(to_add_layout2)
            self.zones_layout_list.addLayout(to_add_layout)

    def zone_delete(self, io):
        """ Delete one zone from the list """
        Case.instance().inlet_outlet.zones.remove(io)
        self.refresh_zones()

    def zone_edit(self, io):
        """ Calls a window for edit zones """
        InletZoneEdit(io, parent=self)
        self.refresh_zones()

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()

    def on_ok(self):
        """ Save data """

        if not Case.instance().inlet_outlet:
            Case.instance().inlet_outlet = InletOutletConfig

        Case.instance().inlet_outlet.reuseids = self.reuseids_combobox.currentText()
        Case.instance().inlet_outlet.resizetime = self.resizetime_line_edit.text()
        Case.instance().inlet_outlet.userefilling = self.refilling_combobox.currentText()
        Case.instance().inlet_outlet.determlimit = self.determlimit_combobox.currentText()
        InletConfigDialog.accept(self)
