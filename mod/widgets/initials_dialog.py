#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Initials Dialog '''

import FreeCADGui

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import info_dialog

from mod.dataobjects.initials_property import InitialsProperty

# FIXME: Use new refactored Case structure instead of old data
class InitialsDialog(QtGui.QDialog):
    ''' Defines a window with initials  '''

    def __init__(self):
        super(InitialsDialog, self).__init__()

        self.setWindowTitle(__("Initials configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.target_mk = int(self.data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_initials_layout = QtGui.QHBoxLayout()
        self.has_initials_label = QtGui.QLabel(__("Set initials: "))
        self.has_initials_label.setToolTip(__("Sets the current initial movement vector."))
        self.has_initials_selector = QtGui.QComboBox()
        self.has_initials_selector.insertItems(0, ['True', 'False'])
        self.has_initials_selector.currentIndexChanged.connect(self.on_initials_change)
        self.has_initials_targetlabel = QtGui.QLabel(__("Target MKFluid: ") + str(self.target_mk))
        self.has_initials_layout.addWidget(self.has_initials_label)
        self.has_initials_layout.addWidget(self.has_initials_selector)
        self.has_initials_layout.addStretch(1)
        self.has_initials_layout.addWidget(self.has_initials_targetlabel)

        self.initials_props_group = QtGui.QGroupBox(__("Initial properties"))
        self.initials_props_layout = QtGui.QVBoxLayout()

        self.initials_vector_layout = QtGui.QHBoxLayout()
        self.initials_vector_label = QtGui.QLabel(__("Velocity (m/s): "))
        self.initials_vector_label.setToolTip(__("Sets the mk group movement vector."))
        self.initials_vector_label_x = QtGui.QLabel("X")
        self.initials_vector_input_x = QtGui.QLineEdit()
        self.initials_vector_label_y = QtGui.QLabel("Y")
        self.initials_vector_input_y = QtGui.QLineEdit()
        self.initials_vector_label_z = QtGui.QLabel("Z")
        self.initials_vector_input_z = QtGui.QLineEdit()
        self.initials_vector_layout.addWidget(self.initials_vector_label)
        self.initials_vector_layout.addWidget(self.initials_vector_label_x)
        self.initials_vector_layout.addWidget(self.initials_vector_input_x)
        self.initials_vector_layout.addWidget(self.initials_vector_label_y)
        self.initials_vector_layout.addWidget(self.initials_vector_input_y)
        self.initials_vector_layout.addWidget(self.initials_vector_label_z)
        self.initials_vector_layout.addWidget(self.initials_vector_input_z)

        self.initials_props_layout.addLayout(self.initials_vector_layout)
        self.initials_props_layout.addStretch(1)
        self.initials_props_group.setLayout(self.initials_props_layout)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.initials_window_layout = QtGui.QVBoxLayout()
        self.initials_window_layout.addLayout(self.has_initials_layout)
        self.initials_window_layout.addWidget(self.initials_props_group)
        self.initials_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.initials_window_layout)

        if str(self.target_mk) in self.data['initials_mks'].keys():
            self.has_initials_selector.setCurrentIndex(0)
            self.on_initials_change(0)
            self.initials_props_group.setEnabled(True)
            self.initials_vector_input_x.setText(str(self.data['initials_mks'][str(self.target_mk)].force[0]))
            self.initials_vector_input_y.setText(str(self.data['initials_mks'][str(self.target_mk)].force[1]))
            self.initials_vector_input_z.setText(str(self.data['initials_mks'][str(self.target_mk)].force[2]))
        else:
            self.has_initials_selector.setCurrentIndex(1)
            self.on_initials_change(1)
            self.initials_props_group.setEnabled(False)
            self.has_initials_selector.setCurrentIndex(1)
            self.initials_vector_input_x.setText("0")
            self.initials_vector_input_y.setText("0")
            self.initials_vector_input_z.setText("0")

        self.exec_()

    # Ok button handler
    def on_ok(self):
        info_dialog(__("This will apply the initials properties to all objects with mkfluid = ") + str(self.target_mk))
        if self.has_initials_selector.currentIndex() == 1:
            # Initials false
            if str(self.target_mk) in self.data['initials_mks'].keys():
                self.data['initials_mks'].pop(str(self.target_mk), None)
        else:
            # Initials true
            # Structure: InitialsProperty Object
            self.data['initials_mks'][str(self.target_mk)] = InitialsProperty(
                mk=self.target_mk,
                force=[
                    float(self.initials_vector_input_x.text()),
                    float(self.initials_vector_input_y.text()),
                    float(self.initials_vector_input_z.text())
                ])
        self.accept()

    # Cancel button handler
    def on_cancel(self):
        self.reject()

    # Initials enable/disable dropdown handler
    def on_initials_change(self, index):
        if index == 0:
            self.initials_props_group.setEnabled(True)
        else:
            self.initials_props_group.setEnabled(False)
