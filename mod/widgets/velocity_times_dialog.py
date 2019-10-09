#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Velocity Times Dialog """

from traceback import print_exc

from PySide import QtGui

from mod.translation_tools import __


class VelocityTimesDialog(QtGui.QDialog):
    """ Dialog with a table to create velocity times. """

    def __init__(self, relaxationzone):
        super(VelocityTimesDialog, self).__init__()
        self.relaxationzone = relaxationzone
        self.velocity_times = relaxationzone.velocity_times

        self.main_layout = QtGui.QVBoxLayout()
        self.table = QtGui.QTableWidget(50, 2)
        self.table.setHorizontalHeaderLabels([__("Time"), __("Value")])

        self.button_layout = QtGui.QHBoxLayout()
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.fill_data()

    def fill_data(self):
        for row, value in enumerate(self.velocity_times):
            self.table.setItem(row, 0, QtGui.QTableWidgetItem(str(value[0])))
            self.table.setItem(row, 1, QtGui.QTableWidgetItem(str(value[1])))

    def on_cancel(self):
        self.reject()

    def on_ok(self):
        self.velocity_times = list()
        for i in range(self.table.rowCount()):
            value_to_insert = []
            try:
                value_to_insert = [float(self.table.item(i, 0).text()), float(self.table.item(i, 0).text())]
            except:
                print_exc()
            if value_to_insert:
                self.velocity_times.append(value_to_insert)
        self.accept()
