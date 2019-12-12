#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Hoverable Label implementation."""

from PySide import QtCore, QtGui


class HoverableLabel(QtGui.QLabel):
    """ A QLabel that emits a signal with a text whenever its hovered by the mouse """

    hover = QtCore.Signal(str)

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.help_text = ""

    def set_help_text(self, help_text):
        """ Sets the help text to emit on hover. """
        self.help_text = help_text

    def enterEvent(self, event: QtGui.QEnterEvent):
        """ Override of the enter event to emit the hover signal. """
        QtGui.QLabel.enterEvent(self, event)
        self.hover.emit(self.help_text)
