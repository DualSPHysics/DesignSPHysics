#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Run Dialog'''

from PySide import QtCore, QtGui

from mod.translation_tools import __

class RunDialog(QtGui.QDialog):
    ''' Defines run window dialog '''

    def __init__(self):
        super(RunDialog, self).__init__()

        self.run_watcher = QtCore.QFileSystemWatcher()
        # Title and size
        self.setModal(False)
        self.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
        self.run_dialog_layout = QtGui.QVBoxLayout()

        # Information GroupBox
        self.run_group = QtGui.QGroupBox(__("Simulation Data"))
        self.run_group_layout = QtGui.QVBoxLayout()

        self.run_group_label_case = QtGui.QLabel(__("Case name: "))
        self.run_group_label_proc = QtGui.QLabel(__("Simulation processor: "))
        self.run_group_label_part = QtGui.QLabel(__("Number of particles: "))
        self.run_group_label_partsout = QtGui.QLabel(__("Total particles out: "))
        self.run_group_label_eta = QtGui.QLabel(self)
        self.run_group_label_eta.setText(__("Estimated time to complete simulation: {}").format("Calculating..."))
        self.run_group_label_completed = QtGui.QLabel("<b>{}</b>".format(__("Simulation is complete.")))
        self.run_group_label_completed.setVisible(False)

        self.run_group_layout.addWidget(self.run_group_label_case)
        self.run_group_layout.addWidget(self.run_group_label_proc)
        self.run_group_layout.addWidget(self.run_group_label_part)
        self.run_group_layout.addWidget(self.run_group_label_partsout)
        self.run_group_layout.addWidget(self.run_group_label_eta)
        self.run_group_layout.addWidget(self.run_group_label_completed)
        self.run_group_layout.addStretch(1)

        self.run_group.setLayout(self.run_group_layout)

        # Progress Bar
        self.run_progbar_layout = QtGui.QHBoxLayout()
        self.run_progbar_bar = QtGui.QProgressBar()
        self.run_progbar_bar.setRange(0, 100)
        self.run_progbar_bar.setTextVisible(False)
        self.run_progbar_layout.addWidget(self.run_progbar_bar)

        # Buttons
        self.run_button_layout = QtGui.QHBoxLayout()
        self.run_button_details = QtGui.QPushButton(__("Details"))
        self.run_button_cancel = QtGui.QPushButton(__("Cancel Simulation"))
        self.run_button_layout.addStretch(1)
        self.run_button_layout.addWidget(self.run_button_details)
        self.run_button_layout.addWidget(self.run_button_cancel)

        self.run_dialog_layout.addWidget(self.run_group)
        self.run_dialog_layout.addLayout(self.run_progbar_layout)
        self.run_dialog_layout.addLayout(self.run_button_layout)

        self.setLayout(self.run_dialog_layout)

        # Defines run details
        self.run_details = QtGui.QDialog()
        self.run_details.setMinimumWidth(650)
        self.run_details.setModal(False)
        self.run_details.setWindowTitle(__("Simulation details"))
        self.run_details_layout = QtGui.QVBoxLayout()

        self.run_details_text = QtGui.QTextEdit()
        self.run_details_text.setReadOnly(True)
        self.run_details_layout.addWidget(self.run_details_text)

        self.run_details.setLayout(self.run_details_layout)
