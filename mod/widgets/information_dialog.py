#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics General Information Dialog"""

from PySide import QtGui

from mod.gui_tools import h_line_generator
from mod.translation_tools import __

from mod.enums import InformationDetailsMode


class InformationDialog(QtGui.QDialog):
    """ A resizable information report dialog  """

    MINIMUM_WIDTH = 500
    SHOW_DETAILS_TEXT = __("Show details")
    HIDE_DETAILS_TEXT = __("Hide details")

    def __init__(self, title: str, message: str, detailed_text: str = None, details_lang=InformationDetailsMode.PLAIN):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.setWindowTitle(str(title))
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.message_label = QtGui.QLabel(str(message))
        self.message_label.setWordWrap(True)
        self.button_layout = QtGui.QHBoxLayout()
        self.details_widget = QtGui.QWidget()

        self.show_details_button = QtGui.QPushButton(self.SHOW_DETAILS_TEXT)
        self.ok_button = QtGui.QPushButton("OK")

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.show_details_button)
        self.button_layout.addWidget(self.ok_button)

        self.details_textarea = QtGui.QTextEdit()

        if details_lang == InformationDetailsMode.PLAIN:
            self.details_textarea.insertPlainText(str(detailed_text).replace("\\n", "\n"))
        elif details_lang == InformationDetailsMode.HTML:
            self.details_textarea.insertHtml(str(detailed_text).replace("\\n", "\n"))

        self.details_textarea.setReadOnly(True)

        self.details_widget_layout = QtGui.QVBoxLayout()
        self.details_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.details_widget_layout.addWidget(h_line_generator())
        self.details_widget_layout.addWidget(self.details_textarea)
        self.details_widget.setLayout(self.details_widget_layout)
        self.details_widget.setVisible(False)

        self.show_details_button.clicked.connect(self.on_details_button)
        self.ok_button.clicked.connect(self.on_ok_button)

        self.main_layout.addWidget(self.message_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.details_widget)

        if not detailed_text:
            self.show_details_button.setVisible(False)

        self.setLayout(self.main_layout)
        self.exec_()

    def on_details_button(self) -> None:
        """ Reacts to the details button being pressed. """
        self.details_widget.setVisible(not self.details_widget.isVisible())
        self.show_details_button.setText(self.HIDE_DETAILS_TEXT if self.details_widget.isVisible() else self.SHOW_DETAILS_TEXT)
        self.adjustSize()

    def on_ok_button(self) -> None:
        """ Reacts to the ok button being pressed. """
        self.accept()
