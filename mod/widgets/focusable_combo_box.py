#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Focusable ComboBox implementation.'''

from PySide import QtCore, QtGui


class FocusableComboBox(QtGui.QComboBox):
    focus = QtCore.Signal(str)
    help_text = ""

    def set_help_text(self, help_text):
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        QtGui.QComboBox.focusInEvent(self, *args, **kwargs).__init__()
        self.focus.emit(self.help_text)
