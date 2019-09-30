#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Object List Table Widget.'''

from PySide import QtGui

from mod.translation_tools import __


class DockObjectListTableWidget(QtGui.QWidget):
    ''' Object List Table Widget. '''

    def __init__(self):
        super().__init__()

        self.setObjectName("DSPH Objects")
        self.objectlist_layout = QtGui.QVBoxLayout()

        self.objectlist_label = QtGui.QLabel("<b>" + __("Object order") + "</b>")
        self.objectlist_label.setWordWrap(True)

        self.objectlist_table = QtGui.QTableWidget(0, 1)
        self.objectlist_table.verticalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.objectlist_layout.addWidget(self.objectlist_label)
        self.objectlist_layout.addWidget(self.objectlist_table)
        self.objectlist_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.objectlist_layout)

    def clear_table_contents(self) -> None:
        ''' Clears the contents of the table within the widget. '''
        self.objectlist_table.clear()

    def set_table_enabled(self, enabled: bool) -> None:
        ''' Sets the enabled state for the table within the widget. '''
        self.objectlist_table.setEnabled(enabled)

    def set_table_row_count(self, count: int) -> None:
        ''' Sets the number of rows for the table within the widget. '''
        self.objectlist_table.setRowCount(count)

    def set_table_cell_widget(self, row: int, column: int, widget: QtGui.QWidget):
        ''' Sets the widget for the specified row and column in the table within the widget. '''
        self.objectlist_table.setCellWidget(row, column, widget)
