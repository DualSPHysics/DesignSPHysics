#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Points configuration Dialog."""


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import warning_dialog
from mod.tools.stdout_tools import debug
from mod.tools.translation_tools import __


class MeasureToolPointsDialog(QtWidgets.QDialog):
    """ DesignSPHysics ComputeForces Points configuration Dialog. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        measurepoints_tool_dialog = QtWidgets.QDialog()
        measurepoints_tool_dialog.setModal(False)
        measurepoints_tool_dialog.setWindowTitle(__("MeasureTool Points"))
        measurepoints_tool_layout = QtWidgets.QVBoxLayout()
        mpoints_table = QtWidgets.QTableWidget()
        mpoints_table.setRowCount(100)
        mpoints_table.setColumnCount(3)
        mpoints_table.verticalHeader().setVisible(False)
        mpoints_table.setHorizontalHeaderLabels(["X", "Y", "Z"])

        for i, point in enumerate(Case.the().post_processing_settings.measuretool_points):
            mpoints_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(point[0])))
            mpoints_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(point[1])))
            mpoints_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(point[2])))

        def on_mpoints_accept():
            """ MeasureTool points dialog accept button behaviour. """
            Case.the().post_processing_settings.measuretool_points = list()
            for mtool_row in range(0, mpoints_table.rowCount()):
                if mpoints_table.item(mtool_row, 0) and mpoints_table.item(mtool_row, 0).text().strip():
                    try:
                        current_point = [
                            float(mpoints_table.item(mtool_row, 0).text().replace(',','.')),
                            float(mpoints_table.item(mtool_row, 1).text().replace(',','.')),
                            float(mpoints_table.item(mtool_row, 2).text().replace(',','.'))
                        ]
                        Case.the().post_processing_settings.measuretool_points.append(current_point)
                    except (ValueError, AttributeError):
                        warning_dialog("Please insert only valid numbers")
                        return

            # Deletes the grid points (not compatible together)
            Case.the().post_processing_settings.measuretool_grid = list()
            measurepoints_tool_dialog.accept()

        def on_mpoints_cancel():
            """ MeasureTool points dialog cancel button behaviour. """
            measurepoints_tool_dialog.reject()

        mpoints_bt_layout = QtWidgets.QHBoxLayout()
        mpoints_cancel = QtWidgets.QPushButton(__("Cancel"))
        mpoints_accept = QtWidgets.QPushButton(__("OK"))
        mpoints_accept.clicked.connect(on_mpoints_accept)
        mpoints_cancel.clicked.connect(on_mpoints_cancel)

        mpoints_bt_layout.addWidget(mpoints_accept)
        mpoints_bt_layout.addWidget(mpoints_cancel)

        measurepoints_tool_layout.addWidget(mpoints_table)
        measurepoints_tool_layout.addLayout(mpoints_bt_layout)

        measurepoints_tool_dialog.setLayout(measurepoints_tool_layout)
        measurepoints_tool_dialog.resize(350, 400)
        measurepoints_tool_dialog.exec_()
