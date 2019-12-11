#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet/Oulet Configuration Dialog """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.freecad_tools import get_fc_main_window

from mod.enums import InletOutletDetermLimit

from mod.widgets.inlet_zone_edit import InletZoneEdit

from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_config import InletOutletConfig
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone


class InletConfigDialog(QtGui.QDialog):
    """ Defines the Inlet/Outlet dialog window.
       Modifies data dictionary passed as parameter. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Reference to the inlet outlet configuration on the case data
        self.inlet_outlet: InletOutletConfig = Case.the().inlet_outlet

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet configuration")
        self.setModal(False)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.main_layout = QtGui.QVBoxLayout()

        # Creates layout for content first options
        self.io_options_layout = QtGui.QHBoxLayout()

        # Creates reuseids option
        self.reuseids_layout = QtGui.QHBoxLayout()
        self.reuseids_option = QtGui.QLabel(__("Reuseids: "))
        self.reuseids_combobox = QtGui.QComboBox()
        self.reuseids_combobox.insertItems(0, [__("False"), __("True")])

        self.reuseids_combobox.setCurrentIndex(1 if self.inlet_outlet.reuseids else 0)

        self.reuseids_layout.addWidget(self.reuseids_option)
        self.reuseids_layout.addWidget(self.reuseids_combobox)

        # Creates resizetime option
        self.resizetime_layout = QtGui.QHBoxLayout()
        self.resizetime_option = QtGui.QLabel(__("Resizetime: "))
        self.resizetime_line_edit = QtGui.QLineEdit(str(self.inlet_outlet.resizetime))

        self.resizetime_layout.addWidget(self.resizetime_option)
        self.resizetime_layout.addWidget(self.resizetime_line_edit)

        # Creates use refilling option
        self.refilling_layout = QtGui.QHBoxLayout()
        self.refilling_option = QtGui.QLabel(__("Refilling: "))
        self.refilling_combobox = QtGui.QComboBox()
        self.refilling_combobox.insertItems(0, [__("False"), __("True")])
        self.refilling_combobox.setCurrentIndex(1 if self.inlet_outlet.userefilling else 0)

        self.refilling_layout.addWidget(self.refilling_option)
        self.refilling_layout.addWidget(self.refilling_combobox)

        # Creates use determlimit option
        self.determlimit_layout = QtGui.QHBoxLayout()
        self.determlimit_option = QtGui.QLabel(__("Determlimit: "))
        self.determlimit_combobox = QtGui.QComboBox()
        self.determlimit_combobox.insertItems(0, [__("1e+3"), __("1e-3")])
        self.determlimit_combobox.setCurrentIndex(0 if self.inlet_outlet.determlimit == InletOutletDetermLimit.ZEROTH_ORDER else 1)

        self.determlimit_layout.addWidget(self.determlimit_option)
        self.determlimit_layout.addWidget(self.determlimit_combobox)

        # Creates 2 main buttons
        self.finish_button = QtGui.QPushButton("Finish")
        self.button_layout = QtGui.QHBoxLayout()

        self.finish_button.clicked.connect(self.on_finish)

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.finish_button)

        # Create the list for zones
        self.zones_groupbox = QtGui.QGroupBox("Inlet/Outlet zones")
        self.zones_groupbox_layout = QtGui.QVBoxLayout()
        self.io_zones_list_layout = QtGui.QVBoxLayout()

        # Add button
        self.add_button_layout = QtGui.QHBoxLayout()
        self.add_zone_button = QtGui.QPushButton("Add Zone")
        self.add_button_layout.addStretch(1)
        self.add_button_layout.addWidget(self.add_zone_button)
        self.add_zone_button.clicked.connect(self.on_add_zone)

        self.zones_groupbox_layout.addLayout(self.add_button_layout)
        self.zones_groupbox_layout.addLayout(self.io_zones_list_layout)

        self.zones_groupbox.setLayout(self.zones_groupbox_layout)

        # Adds options to option layout
        self.io_options_layout.addLayout(self.reuseids_layout)
        self.io_options_layout.addLayout(self.resizetime_layout)
        self.io_options_layout.addLayout(self.refilling_layout)
        self.io_options_layout.addLayout(self.determlimit_layout)

        # Adds options to main
        self.main_layout.addLayout(self.io_options_layout)
        self.main_layout.addWidget(self.zones_groupbox)

        # Adds scroll area
        self.main_layout_dialog = QtGui.QVBoxLayout()
        self.main_layout_scroll = QtGui.QScrollArea()
        self.main_layout_scroll.setMinimumWidth(400)
        self.main_layout_scroll.setWidgetResizable(True)
        self.main_layout_scroll_widget = QtGui.QWidget()
        self.main_layout_scroll_widget.setMinimumWidth(400)

        self.main_layout_scroll_widget.setLayout(self.main_layout)
        self.main_layout_scroll.setWidget(self.main_layout_scroll_widget)
        self.main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout_dialog.addWidget(self.main_layout_scroll)
        self.main_layout_dialog.addLayout(self.button_layout)

        self.setLayout(self.main_layout_dialog)

        self.refresh_zones()

        self.finish_button.setFocus()

        self.exec_()

    def on_add_zone(self):
        """ Adds Inlet/Outlet zone """
        new_io_zone = InletOutletZone()
        self.inlet_outlet.zones.append(new_io_zone)
        self.zone_edit(new_io_zone.id)

    def refresh_zones(self):
        """ Refreshes the zones list """
        while self.io_zones_list_layout.count() > 0:
            target = self.io_zones_list_layout.takeAt(0)
            self.io_zones_list_layout.removeItem(target)
            del target

        count = 0
        for io_object in self.inlet_outlet.zones:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("I/O Zone " + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, io_object=io_object: self.zone_edit(io_object.id))
            to_add_deletebutton.clicked.connect(lambda _=False, io_object=io_object: self.zone_delete(io_object))
            self.io_zones_list_layout.addLayout(to_add_layout)
        self.io_zones_list_layout.addStretch(1)

    def zone_delete(self, io):
        """ Delete one zone from the list """
        self.inlet_outlet.zones.remove(io)
        self.refresh_zones()

    def zone_edit(self, io):
        """ Calls a window for edit zones """
        InletZoneEdit(io, parent=get_fc_main_window())
        self.refresh_zones()

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()

    def on_finish(self):
        """ Save data """

        if not self.inlet_outlet:
            self.inlet_outlet = InletOutletConfig

        self.inlet_outlet.reuseids = self.reuseids_combobox.currentText()
        self.inlet_outlet.resizetime = self.resizetime_line_edit.text()
        self.inlet_outlet.userefilling = self.refilling_combobox.currentText()
        self.inlet_outlet.determlimit = self.determlimit_combobox.currentText()
        InletConfigDialog.accept(self)
