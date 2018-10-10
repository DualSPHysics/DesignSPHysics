#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
"""

from PySide import QtGui, QtCore


class HoverableLabel(QtGui.QLabel):
    hover = QtCore.Signal(str)
    help_text = ""

    def __init__(self, label_text):
        super(HoverableLabel, self).__init__(label_text)

    def setHelpText(self, help_text):
        self.help_text = help_text

    def enterEvent(self, *args, **kwargs):
        self.hover.emit(self.help_text)
