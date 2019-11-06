#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Focusable LineEdit implementation."""

from PySide import QtCore, QtGui


class FocusableLineEdit(QtGui.QLineEdit):
    """ A LineEdit that fires a focus event when focusing it. """
    focus = QtCore.Signal(str)
    help_text = ""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def set_help_text(self, help_text):
        """ Sets the help text for the line edit. """
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        """ Reimplements the QLineEdit focusInEvent and fires the focus signal. """
        QtGui.QLineEdit.focusInEvent(self, *args, **kwargs)
        self.focus.emit(self.help_text)
