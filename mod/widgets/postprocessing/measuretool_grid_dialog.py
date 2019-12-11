#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MeasureTool Grid Dialog """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import debug

from mod.dataobjects.case import Case


class MeasureToolGridDialog(QtGui.QDialog):
    """ Defines grid point button behaviour."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.current_grid = []

        self.setWindowTitle(__("MeasureTool Points"))
        self.measuregrid_tool_layout = QtGui.QVBoxLayout()
        self.mgrid_table = QtGui.QTableWidget()
        self.mgrid_table.setRowCount(100)
        self.mgrid_table.setColumnCount(12)
        self.mgrid_table.verticalHeader().setVisible(False)
        self.mgrid_table.setHorizontalHeaderLabels([
            "BeginX",
            "BeginY",
            "BeginZ",
            "StepX",
            "StepY",
            "StepZ",
            "CountX",
            "CountY",
            "CountZ",
            "FinalX",
            "FinalY",
            "FinalZ"
        ])

        for i, grid in enumerate(Case.the().info.measuretool_grid):
            for j in range(0, self.mgrid_table.columnCount()):
                self.mgrid_table.setItem(i, j, QtGui.QTableWidgetItem(str(grid[j])))
                if j > 8:
                    self.mgrid_table.setItem(i, j, QtGui.QTableWidgetItem(str(grid[j])))
                    self.mgrid_table.item(i, j).setBackground(QtGui.QColor(210, 255, 255))
                    self.mgrid_table.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        if Case.the().info.measuretool_grid == list():
            for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
                self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(""))
                self.mgrid_table.item(self.mgrid_row, 9).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # Compute possible final points
        self.on_mgrid_change(0, 0)

        self.mgrid_bt_layout = QtGui.QHBoxLayout()
        self.mgrid_cancel = QtGui.QPushButton(__("Cancel"))
        self.mgrid_accept = QtGui.QPushButton(__("OK"))
        self.mgrid_accept.clicked.connect(self.on_mgrid_accept)
        self.mgrid_cancel.clicked.connect(self.on_mgrid_cancel)

        self.mgrid_bt_layout.addWidget(self.mgrid_accept)
        self.mgrid_bt_layout.addWidget(self.mgrid_cancel)

        self.mgrid_table.cellChanged.connect(self.on_mgrid_change)

        self.measuregrid_tool_layout.addWidget(self.mgrid_table)
        self.measuregrid_tool_layout.addLayout(self.mgrid_bt_layout)

        self.setLayout(self.measuregrid_tool_layout)
        self.resize(1250, 400)
        self.setModal(False)
        self.exec_()

    def on_mgrid_change(self, _, column):
        """ Defines what happens when a field changes on the table"""
        if column > 8:
            return
        for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
            try:
                self.current_grid = [
                    float(self.mgrid_table.item(self.mgrid_row, 0).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 1).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 2).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 3).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 4).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 5).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 6).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 7).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 8).text())
                ]

                debug(self.current_grid)

                # Make the operations to calculate final points
                self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[0]) +
                    float(self.current_grid[6] - 1) *
                    float(self.current_grid[3])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[1]) +
                    float(self.current_grid[7] - 1) *
                    float(self.current_grid[4])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[2]) +
                    float(self.current_grid[8] - 1) *
                    float(self.current_grid[5])
                )))

                if self.current_grid[6] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[7] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[8] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(str(
                        "0"
                    )))

                self.mgrid_table.item(self.mgrid_row, 9).setBackground(QtGui.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 10).setBackground(QtGui.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 11).setBackground(QtGui.QColor(210, 255, 255))
                # Those should not be used
                self.mgrid_table.item(self.mgrid_row, 9).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            except (ValueError, AttributeError):
                pass

    def on_mgrid_accept(self):
        """ MeasureTool point grid accept button behaviour."""
        Case.the().info.measuretool_grid = list()
        for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
            try:
                self.current_grid = [
                    float(self.mgrid_table.item(self.mgrid_row, 0).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 1).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 2).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 3).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 4).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 5).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 6).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 7).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 8).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 9).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 10).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 11).text())
                ]
                Case.the().info.measuretool_grid.append(self.current_grid)
            except (ValueError, AttributeError):
                pass

        # Deletes the list of points (not compatible together)
        Case.the().info.measuretool_points = list()
        self.accept()

    def on_mgrid_cancel(self):
        """ MeasureTool point grid cancel button behaviour"""
        self.reject()
