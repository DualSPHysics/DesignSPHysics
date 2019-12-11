#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Object Order widget"""

from PySide import QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon

from mod.dataobjects.case import Case


class ObjectOrderWidget(QtGui.QWidget):
    """ A widget representing the object order. """

    def __init__(self, index=999, object_name="No name", object_mk=-1, mktype="bound",
                 up_disabled=False, down_disabled=False, parent=None):
        super().__init__(parent=parent)

        self.index = index
        self.object_name = object_name
        self.parent = parent

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.mk_label = QtGui.QLabel("<b>{}{}</b>".format(mktype[0].upper(), str(object_mk)))
        self.name_label = QtGui.QLabel(str(object_name))
        self.up_button = QtGui.QPushButton(get_icon("up_arrow.png"), None)
        self.up_button.clicked.connect(self.on_up)
        self.down_button = QtGui.QPushButton(get_icon("down_arrow.png"), None)
        self.down_button.clicked.connect(self.on_down)

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.up_button)
        self.main_layout.addWidget(self.down_button)

        self.up_button.setEnabled(not up_disabled)
        self.down_button.setEnabled(not down_disabled)

        self.setLayout(self.main_layout)
        self.setToolTip("MK: {} ({})\n"
                        "Name: {}\n"
                        "{}".format(object_mk, mktype.lower().title(), object_name, __("Press up or down to reorder.")))

    def disable_up(self):
        """ Disables the up button. """
        self.up_button.setEnabled(False)

    def disable_down(self):
        """ Disables the down button. """
        self.down_button.setEnabled(False)

    def on_up(self):
        """ Defines the behaviour on up button press. """
        Case.the().shift_object_up_in_order(self.index)
        if self.parent:
            self.parent.refresh()

    def on_down(self):
        """ Defines the behaviour on down button press. """
        Case.the().shift_object_down_in_order(self.index)
        if self.parent:
            self.parent.refresh()
