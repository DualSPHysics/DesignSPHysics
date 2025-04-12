#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dialog Tools.

Contains general use standard dialogs. """

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __

from mod.widgets.information_dialog import InformationDialog


def warning_dialog(warn_text, detailed_text=None):
    """Spawns a warning dialog with the text and details passed."""
    InformationDialog(__("WARNING"), warn_text, detailed_text)


def error_dialog(error_text, detailed_text=None):
    """Spawns an error dialog with the text and details passed."""
    InformationDialog(__("ERROR"), error_text, detailed_text)


def info_dialog(info_text, detailed_text=None):
    """Spawns an info dialog with the text and details passed."""
    InformationDialog(__("Information"), info_text, detailed_text)


def ok_cancel_dialog(title, text):
    """Spawns an okay/cancel dialog with the title and text passed"""
    open_confirm_dialog = QtWidgets.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok |
                                           QtWidgets.QMessageBox.Cancel)
    open_confirm_dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)
    return open_confirm_dialog.exec_()

def ok_discard_dialog(title, text):
    """Spawns an okay/discard dialog with the title and text passed"""
    open_confirm_dialog = QtWidgets.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok |
                                           QtWidgets.QMessageBox.Discard)
    open_confirm_dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)
    return open_confirm_dialog.exec_()
