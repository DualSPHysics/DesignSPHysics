#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Setup Plugin Dialog """

from PySide import QtGui

from mod.stdout_tools import debug
from mod.translation_tools import __
from mod.template_tools import get_template_text
from mod.executable_tools import get_executable_info_flag

from mod.dataobjects.executable_paths import ExecutablePaths


class FeatureSupportDialog(QtGui.QDialog):
    """ Dialog that displays the currently supportede features of the currently configured executables. """

    TEMPLATE_PATH = "/templates/feature_support_report.html"
    MIN_WIDTH = 620
    MIN_HEIGHT = 440

    def __init__(self, executable_paths: ExecutablePaths):
        super().__init__()
        self._executable_paths = executable_paths

        self.setWindowTitle(__("DualSPHysics Suite Feature Report"))

        self.root_layout = QtGui.QVBoxLayout()

        self.report_text = QtGui.QTextEdit()
        self.report_text.setReadOnly(True)

        self.button_layout = QtGui.QHBoxLayout()
        self.ok_button = QtGui.QPushButton(__("OK"))

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        self.root_layout.addWidget(self.report_text)
        self.root_layout.addLayout(self.button_layout)

        self.fill_report()

        self.setLayout(self.root_layout)
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMinimumHeight(self.MIN_HEIGHT)

        self.ok_button.clicked.connect(self.on_ok)

        debug("Executable paths are: ")
        debug(executable_paths)

    def on_ok(self):
        """ Defines the behaviour when the user presses the OK button. """
        self.accept()

    def fill_report(self):
        """ Fills the report QTextEdit with data. """
        template_text = get_template_text(self.TEMPLATE_PATH)

        gencase_info = get_executable_info_flag(self._executable_paths.gencase)
        gencase_features = "\n".join(["<li><b>{}</b>: {}</li>".format(x, gencase_info["Features"][x]) for x in gencase_info["Features"].keys()])
        dsph_info = get_executable_info_flag(self._executable_paths.dsphysics)
        dsph_features = "\n".join(["<li><b>{}</b>: {}</li>".format(x, str(dsph_info["Features"][x]).replace("True", __("Supported")).replace("False", __("Not supported"))) for x in dsph_info["Features"].keys()])

        formatter = {
            "gencase_fullname": gencase_info["FullName"],
            "gencase_features": gencase_features,
            "dsph_fullname": dsph_info["FullName"],
            "dsph_features": dsph_features
        }
        template_text = template_text.format(**formatter)
        self.report_text.setHtml(template_text)
