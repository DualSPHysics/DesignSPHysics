#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Execution Progress Dialog."""

from PySide import QtGui, QtCore

from mod.translation_tools import __


class ExportProgressDialog(QtGui.QDialog):
    """ Export Progress Dialog. """

    on_cancel = QtCore.Signal()

    def __init__(self, minimum: int, maximum: int, parent=None):
        super().__init__(parent=parent)

        self.minimum = minimum
        self.maximum = maximum

        self.setModal(False)
        self.setMinimumSize(400, 100)
        self.setWindowTitle(__("Exporting: {}%").format("0"))
        self.export_dialog_layout = QtGui.QVBoxLayout()

        self.export_progbar_layout = QtGui.QHBoxLayout()
        self.export_progbar_bar = QtGui.QProgressBar()
        self.export_progbar_bar.setRange(0, 100)
        self.export_progbar_bar.setTextVisible(False)
        self.export_progbar_layout.addWidget(self.export_progbar_bar)

        self.export_button_layout = QtGui.QHBoxLayout()
        self.export_button_cancel = QtGui.QPushButton(__("Cancel Exporting"))
        self.export_button_layout.addStretch(1)
        self.export_button_layout.addWidget(self.export_button_cancel)

        self.export_dialog_layout.addLayout(self.export_progbar_layout)
        self.export_dialog_layout.addStretch(1)
        self.export_dialog_layout.addLayout(self.export_button_layout)

        self.export_button_cancel.clicked.connect(self.on_cancel.emit)

        self.setLayout(self.export_dialog_layout)

        self.set_range(self.minimum, self.maximum)
        self.set_value(self.minimum)

    def set_range(self, minimum: int, maximum: int) -> None:
        """ Sets the range of the progress bar within the dialog. """
        self.export_progbar_bar.setRange(minimum, maximum)

    def set_value(self, value: int) -> None:
        """ Sets the value of the progress bar within the dialog. """
        self.export_progbar_bar.setValue(value)

    def get_value(self) -> int:
        """ Returns the current progress bar value. """
        return self.export_progbar_bar.value()

    def update_data(self, current) -> None:
        """ Updates the dialog with new data. """
        self.set_value(current)
        self.setWindowTitle("{export_text} {current}/{total}".format(export_text=__("Exporting:"), current=current, total=self.maximum))
