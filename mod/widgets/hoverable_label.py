#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Hoverable Label implementation.'''

from PySide import QtCore, QtGui


class HoverableLabel(QtGui.QLabel):
    hover = QtCore.Signal(str)
    help_text = ""

    def setHelpText(self, help_text):
        self.help_text = help_text

    # FIXME: Avoid to define non-used parameters or call super() method.
    def enterEvent(self, *args, **kwargs):
        self.hover.emit(self.help_text)
