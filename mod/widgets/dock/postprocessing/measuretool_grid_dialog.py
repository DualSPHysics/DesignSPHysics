#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MeasureTool Grid Dialog """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import warning_dialog
from mod.tools.translation_tools import __


class MeasureToolGridDialog(QtWidgets.QDialog):
    """ Defines grid point button behaviour."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.grid_size=1
        if Case.the().post_processing_settings.measuretool_grid:
            self.grid_size=len(Case.the().post_processing_settings.measuretool_grid)

        self.current_grid = []

        self.setWindowTitle(__("MeasureTool Points"))
        self.measuregrid_tool_layout = QtWidgets.QVBoxLayout()
        self.mgrid_table = QtWidgets.QTableWidget()
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


        for i, grid in enumerate(Case.the().post_processing_settings.measuretool_grid):
            for j in range(0, self.mgrid_table.columnCount()):
                self.mgrid_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(grid[j])))
                if j > 8:
                    #self.mgrid_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(grid[j])))
                    self.mgrid_table.setItem(i, j, QtWidgets.QTableWidgetItem("HOLA"))
                    self.mgrid_table.item(i, j).setBackground(QtWidgets.QColor(210, 255, 255))
                    self.mgrid_table.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


        if Case.the().post_processing_settings.measuretool_grid == list():
            for self.mgrid_row in range(0, self.grid_size):
                self.mgrid_table.setItem(self.mgrid_row, 0, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 1, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 2, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 3, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 4, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 5, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 6, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 7, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 8, QtWidgets.QTableWidgetItem("0"))
                self.mgrid_table.setItem(self.mgrid_row, 9, QtWidgets.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtWidgets.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtWidgets.QTableWidgetItem(""))

                self.mgrid_table.item(self.mgrid_row, 9).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # Compute possible final points
        if self.mgrid_table.item(0, 0):
            self.on_mgrid_change(0, 0)

        self.mgrid_bt_layout = QtWidgets.QHBoxLayout()
        self.mgrid_cancel = QtWidgets.QPushButton(__("Cancel"))
        self.mgrid_accept = QtWidgets.QPushButton(__("OK"))
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
            empty_row=True
            for i in range(0,8):
                if self.mgrid_table.item(self.mgrid_row, i):
                    empty_row=False
            if empty_row:
                self.grid_size=self.mgrid_row
                return
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


                # Make the operations to calculate final points
                self.mgrid_table.setItem(self.mgrid_row, 9, QtWidgets.QTableWidgetItem(str(
                    float(self.current_grid[0]) +
                    float(self.current_grid[6] - 1) *
                    float(self.current_grid[3])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtWidgets.QTableWidgetItem(str(
                    float(self.current_grid[1]) +
                    float(self.current_grid[7] - 1) *
                    float(self.current_grid[4])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtWidgets.QTableWidgetItem(str(
                    float(self.current_grid[2]) +
                    float(self.current_grid[8] - 1) *
                    float(self.current_grid[5])
                )))

                if self.current_grid[6] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 9, QtWidgets.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[7] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 10, QtWidgets.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[8] == 0:
                    self.mgrid_table.setItem(self.mgrid_row, 11, QtWidgets.QTableWidgetItem(str(
                        "0"
                    )))

                self.mgrid_table.item(self.mgrid_row, 9).setBackground(QtWidgets.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 10).setBackground(QtWidgets.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 11).setBackground(QtWidgets.QColor(210, 255, 255))
                # Those should not be used
                self.mgrid_table.item(self.mgrid_row, 9).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            except (ValueError, AttributeError):
                self.grid_size = self.mgrid_row+1
                return

    def on_mgrid_accept(self):
        """ MeasureTool point grid accept button behaviour."""
        Case.the().post_processing_settings.measuretool_grid = list()
        for self.mgrid_row in range(0, self.grid_size):
            try:
                self.current_grid = [
                    float(self.mgrid_table.item(self.mgrid_row, 0).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 1).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 2).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 3).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 4).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 5).text().replace(',','.')),
                    int(self.mgrid_table.item(self.mgrid_row, 6).text().replace(',','.')),
                    int(self.mgrid_table.item(self.mgrid_row, 7).text().replace(',','.')),
                    int(self.mgrid_table.item(self.mgrid_row, 8).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 9).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 10).text().replace(',','.')),
                    float(self.mgrid_table.item(self.mgrid_row, 11).text().replace(',','.'))
                ]
                Case.the().post_processing_settings.measuretool_grid.append(self.current_grid)
            except (ValueError, AttributeError):
                warning_dialog(f"Please insert only numbers")
                return

        # Deletes the list of points (not compatible together) CHECK
        Case.the().post_processing_settings.measuretool_points = list()
        self.accept()

    def on_mgrid_cancel(self):
        """ MeasureTool point grid cancel button behaviour"""
        self.reject()
