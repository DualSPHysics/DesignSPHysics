#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Object List Table Widget."""

from PySide import QtGui

from mod.freecad_tools import get_fc_object
from mod.translation_tools import __

from mod.constants import CASE_LIMITS_OBJ_NAME

from mod.dataobjects.case import Case

from mod.widgets.object_order_widget import ObjectOrderWidget


class DockObjectListTableWidget(QtGui.QWidget):
    """ Object List Table Widget. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

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
        """ Clears the contents of the table within the widget. """
        self.objectlist_table.clear()

    def set_table_enabled(self, enabled: bool) -> None:
        """ Sets the enabled state for the table within the widget. """
        self.objectlist_table.setEnabled(enabled)

    def set_table_row_count(self, count: int) -> None:
        """ Sets the number of rows for the table within the widget. """
        self.objectlist_table.setRowCount(count)

    def set_table_cell_widget(self, row: int, column: int, widget: QtGui.QWidget):
        """ Sets the widget for the specified row and column in the table within the widget. """
        self.objectlist_table.setCellWidget(row, column, widget)

    def refresh(self) -> None:
        """ Deletes everything and refreshes contents with the current simulation objects. """
        self.clear_table_contents()
        num_objects_in_simulation: int = Case.the().number_of_objects_in_simulation()
        self.set_table_row_count(num_objects_in_simulation)

        current_row = 0
        for sim_object in Case.the().objects:
            if sim_object.name == CASE_LIMITS_OBJ_NAME:
                continue
            target_widget = ObjectOrderWidget(index=current_row, object_mk=sim_object.obj_mk, mktype=sim_object.type, object_name=get_fc_object(sim_object.name).Label, parent=self)

            if current_row == 0:
                target_widget.disable_up()
            if current_row == num_objects_in_simulation - 1:
                target_widget.disable_down()

            self.set_table_cell_widget(current_row, 0, target_widget)
            current_row += 1
