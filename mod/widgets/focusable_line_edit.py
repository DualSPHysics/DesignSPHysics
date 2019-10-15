#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Focusable LineEdit implementation."""

from PySide import QtCore, QtGui


class FocusableLineEdit(QtGui.QLineEdit):
    focus = QtCore.Signal(str)
    help_text = ""

    def __init__(self,  parent=None):
        super().__init__(parent=parent)

    def set_help_text(self, help_text):
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        QtGui.QLineEdit.focusInEvent(self, *args, **kwargs)
        self.focus.emit(self.help_text)
