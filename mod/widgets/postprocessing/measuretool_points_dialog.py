#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Points configuration Dialog."""

from PySide import QtGui

from mod.translation_tools import __

from mod.dataobjects.case import Case


class MeasureToolPointsDialog(QtGui.QDialog):
    """ DesignSPHysics ComputeForces Points configuration Dialog. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        measurepoints_tool_dialog = QtGui.QDialog()
        measurepoints_tool_dialog.setModal(False)
        measurepoints_tool_dialog.setWindowTitle(__("MeasureTool Points"))
        measurepoints_tool_layout = QtGui.QVBoxLayout()
        mpoints_table = QtGui.QTableWidget()
        mpoints_table.setRowCount(100)
        mpoints_table.setColumnCount(3)
        mpoints_table.verticalHeader().setVisible(False)
        mpoints_table.setHorizontalHeaderLabels(["X", "Y", "Z"])

        for i, point in enumerate(Case.the().info.measuretool_points):
            mpoints_table.setItem(i, 0, QtGui.QTableWidgetItem(str(point[0])))
            mpoints_table.setItem(i, 1, QtGui.QTableWidgetItem(str(point[1])))
            mpoints_table.setItem(i, 2, QtGui.QTableWidgetItem(str(point[2])))

        def on_mpoints_accept():
            """ MeasureTool points dialog accept button behaviour. """
            Case.the().info.measuretool_points = list()
            for mtool_row in range(0, mpoints_table.rowCount()):
                try:
                    current_point = [
                        float(mpoints_table.item(mtool_row, 0).text()),
                        float(mpoints_table.item(mtool_row, 1).text()),
                        float(mpoints_table.item(mtool_row, 2).text())
                    ]
                    Case.the().info.measuretool_points.append(current_point)
                except (ValueError, AttributeError):
                    pass

            # Deletes the grid points (not compatible together)
            Case.the().info.measuretool_grid = list()
            measurepoints_tool_dialog.accept()

        def on_mpoints_cancel():
            """ MeasureTool points dialog cancel button behaviour. """
            measurepoints_tool_dialog.reject()

        mpoints_bt_layout = QtGui.QHBoxLayout()
        mpoints_cancel = QtGui.QPushButton(__("Cancel"))
        mpoints_accept = QtGui.QPushButton(__("OK"))
        mpoints_accept.clicked.connect(on_mpoints_accept)
        mpoints_cancel.clicked.connect(on_mpoints_cancel)

        mpoints_bt_layout.addWidget(mpoints_accept)
        mpoints_bt_layout.addWidget(mpoints_cancel)

        measurepoints_tool_layout.addWidget(mpoints_table)
        measurepoints_tool_layout.addLayout(mpoints_bt_layout)

        measurepoints_tool_dialog.setLayout(measurepoints_tool_layout)
        measurepoints_tool_dialog.resize(350, 400)
        measurepoints_tool_dialog.exec_()
