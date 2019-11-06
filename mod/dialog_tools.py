#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dialog Tools.

Contains general use standard dialogs. """

from PySide import QtGui


def warning_dialog(warn_text, detailed_text=None):
    """Spawns a warning dialog with the text and details passed."""

    warning_messagebox = QtGui.QMessageBox()
    warning_messagebox.setText(str(warn_text))
    warning_messagebox.setIcon(QtGui.QMessageBox.Warning)
    if detailed_text is not None:
        warning_messagebox.setDetailedText(str(detailed_text))
    warning_messagebox.exec_()


def error_dialog(error_text, detailed_text=None):
    """Spawns an error dialog with the text and details passed."""

    error_messagebox = QtGui.QMessageBox()
    error_messagebox.setText(error_text)
    error_messagebox.setIcon(QtGui.QMessageBox.Critical)
    if detailed_text is not None:
        error_messagebox.setDetailedText(str(detailed_text))
    error_messagebox.exec_()


def info_dialog(info_text, detailed_text=None):
    """Spawns an info dialog with the text and details passed."""

    info_messagebox = QtGui.QMessageBox()
    # FIXME: Setting tab characters is a hacky fix to enforce minimum size. However we should subclass a dialog and make a custom MessageBox.
    info_messagebox.setText("{}\t\t\t\t\t".format(info_text.replace("\\n", "\n")))
    info_messagebox.setIcon(QtGui.QMessageBox.Information)
    if detailed_text is not None:
        info_messagebox.setDetailedText(str(detailed_text).replace("\\n", "\n"))
    info_messagebox.exec_()


def ok_cancel_dialog(title, text):
    """Spawns an okay/cancel dialog with the title and text passed"""

    open_confirm_dialog = QtGui.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtGui.QMessageBox.Ok |
                                           QtGui.QMessageBox.Cancel)
    open_confirm_dialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return open_confirm_dialog.exec_()
