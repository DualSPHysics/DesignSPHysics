#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock DP Intro Widget """


from PySide2 import QtWidgets

from mod.tools.translation_tools import __

from mod.dataobjects.case import Case
from mod.tools.freecad_tools import update_dp
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.size_input import SizeInput


class DockDPWidget(QtWidgets.QWidget):
    """ DesignSPHysics Dock DP Intro widget. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.dp_label = QtWidgets.QLabel(__("Inter-particle distance: "))
        self.dp_label.setToolTip(__("Lower DP to have more particles in the case."))

        self.dp_input = SizeInput()
        self.dp_input.setToolTip(__("Lower DP to have more particles in the case."))
        self.dp_input.setValue(Case.the().dp)
        self.dp_input.value_changed.connect(self.on_dp_changed)

        self.main_layout.addWidget(self.dp_label)
        self.main_layout.addWidget(self.dp_input)

        self.setLayout(self.main_layout)

    def on_dp_changed(self):
        """ DP Introduction. Changes the dp at the moment the user changes the text. """
        dp=self.dp_input.value()
        Case.the().dp = dp
        update_dp(dp)

