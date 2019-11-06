#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Focusable ComboBox implementation. """

from PySide import QtCore, QtGui


class FocusableComboBox(QtGui.QComboBox):
    """ A ComboBox that emits the focus signal with a help text as a parameter when focusing it on the GUI. """
    focus = QtCore.Signal(str)
    help_text = ""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def set_help_text(self, help_text):
        """ Sets the help text for the combobox. """
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        """ Redefines the focusInEvent from QtGui.QComboBox adding a focus signal fire. """
        QtGui.QComboBox.focusInEvent(self, *args, **kwargs)
        self.focus.emit(self.help_text)
