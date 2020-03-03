#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Logo/Help Widget. """

import webbrowser

from PySide import QtGui

from mod.gui_tools import get_icon
from mod.translation_tools import __

from mod.enums import HelpURL


class DockLogoWidget(QtGui.QWidget):
    """DesignSPHysics Dock Logo/Help Widget. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_label = QtGui.QLabel()
        self.logo_label.setPixmap(get_icon(file_name="logo.png", return_only_path=True))

        self.help_button = QtGui.QPushButton("Help")
        self.help_button.setToolTip(__("Push this button to open a browser with help\non how to use this tool."))
        self.help_button.setIcon(QtGui.QIcon.fromTheme("system-help"))
        self.help_button.clicked.connect(lambda: webbrowser.open(HelpURL.WIKI_HOME))

        self.main_layout.addStretch(0.5)
        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addStretch(0.5)
        self.main_layout.addWidget(self.help_button)

        self.setLayout(self.main_layout)
