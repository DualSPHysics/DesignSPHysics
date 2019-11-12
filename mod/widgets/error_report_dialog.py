#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics General Error Report Dialog"""

import webbrowser
from platform import platform

import FreeCAD
from PySide import QtGui

from mod.gui_tools import h_line_generator

from mod.constants import VERSION
from mod.enums import HelpURL


class ErrorReportDialog(QtGui.QDialog):
    """ Defines an error report dialog  """

    def __init__(self, exception_type, value, traceback_str):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.message_label = QtGui.QLabel("DesignSPHysics encountered an error. Please report the developer the following details.")
        self.button_layout = QtGui.QHBoxLayout()
        self.details_widget = QtGui.QWidget()

        self.report_button = QtGui.QPushButton("Report error")
        self.show_details_button = QtGui.QPushButton("Show details...")
        self.ok_button = QtGui.QPushButton("OK")

        self.button_layout.addWidget(self.report_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.show_details_button)
        self.button_layout.addWidget(self.ok_button)

        self.traceback_textarea = QtGui.QTextEdit("<b>DesignSPHysics version</b>: {}<br/>".format(VERSION) +
                                                  "<b>Platform:</b> {}<br/>".format(platform()) +
                                                  "<b>FreeCAD Version:</b> {}<br/>".format(".".join(FreeCAD.Version()[0:3])) +
                                                  "<b>Exception type:</b> {}<br/>".format(exception_type) +
                                                  "<b>Exception value:</b> {}<br/>".format(value) +
                                                  "<b>Traceback:</b><br/><pre>{}</pre>".format(traceback_str))
        self.traceback_textarea.setReadOnly(True)

        self.details_widget_layout = QtGui.QVBoxLayout()
        self.details_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.details_widget_layout.addWidget(h_line_generator())
        self.details_widget_layout.addWidget(self.traceback_textarea)
        self.details_widget.setLayout(self.details_widget_layout)
        self.details_widget.setVisible(False)

        self.show_details_button.clicked.connect(self.on_details_button)
        self.ok_button.clicked.connect(self.on_ok_button)
        self.report_button.clicked.connect(self.on_report_button)

        self.main_layout.addWidget(self.message_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.details_widget)

        self.setLayout(self.main_layout)
        self.exec_()

    def on_details_button(self) -> None:
        """ Reacts to the details button being pressed. """
        self.details_widget.setVisible(not self.details_widget.isVisible())
        self.adjustSize()

    def on_ok_button(self) -> None:
        """ Reacts to the ok button being pressed. """
        self.accept()

    def on_report_button(self) -> None:
        """ Reacts to the report button being pressed. """
        webbrowser.open(HelpURL.GITHUB_ISSUES, autoraise=True)
