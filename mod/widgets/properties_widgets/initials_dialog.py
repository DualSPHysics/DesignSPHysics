#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Initials Dialog """

import FreeCADGui


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.properties.initials_property import InitialsProperty
from mod.tools.dialog_tools import info_dialog
from mod.enums import ObjectType
from mod.functions import make_float
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput


class InitialsDialog(QtWidgets.QDialog):
    """ Defines a window with initials  """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Initials configuration for fluid"))
        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.target= Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name)
        self.target_mk =self.target.obj_mk

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_initials_layout = QtWidgets.QHBoxLayout()
        self.has_initials_label = QtWidgets.QLabel(__("Set initials: "))
        self.has_initials_label.setToolTip(__("Sets the current initial movement vector."))
        self.has_initials_selector = QtWidgets.QComboBox()
        self.has_initials_selector.insertItems(0, ["True", "False"])
        self.has_initials_selector.currentIndexChanged.connect(self.on_initials_change)

        self.initials_type_label = QtWidgets.QLabel(__("Type: "))
        self.initials_type_label.setToolTip(__("Chooses the type of the initial velocity."))
        self.initials_type_selector = QtWidgets.QComboBox()
        self.initials_type_selector.insertItems(0, ['Velocity - Uniform', 'Velocity - Linear', 'Velocity - Parabolic'])
        self.initials_type_selector.currentIndexChanged.connect(self.on_initials_type_change)

        self.has_initials_targetlabel = QtWidgets.QLabel(__("Target MKFluid: ") + str(self.target_mk))

        self.has_initials_layout.addWidget(self.has_initials_label)
        self.has_initials_layout.addWidget(self.has_initials_selector)
        self.has_initials_layout.addWidget(self.initials_type_label)
        self.has_initials_layout.addWidget(self.initials_type_selector)
        self.has_initials_layout.addStretch(1)
        self.has_initials_layout.addWidget(self.has_initials_targetlabel)

        self.initials_props_group = QtWidgets.QGroupBox(__("Initial properties"))
        self.initials_props_layout = QtWidgets.QVBoxLayout()

        self.initials_vector_layout = QtWidgets.QHBoxLayout()
        self.initials_vector_label = QtWidgets.QLabel(__("Direction: "))
        self.initials_vector_label.setToolTip(__("Sets the mk group movement vector."))
        self.initials_vector_label_x = QtWidgets.QLabel("X")
        self.initials_vector_input_x = ValueInput()
        self.initials_vector_label_y = QtWidgets.QLabel("Y")
        self.initials_vector_input_y = ValueInput()
        self.initials_vector_label_z = QtWidgets.QLabel("Z")
        self.initials_vector_input_z = ValueInput()
        self.initials_vector_layout.addWidget(self.initials_vector_label)
        self.initials_vector_layout.addWidget(self.initials_vector_label_x)
        self.initials_vector_layout.addWidget(self.initials_vector_input_x)
        self.initials_vector_layout.addWidget(self.initials_vector_label_y)
        self.initials_vector_layout.addWidget(self.initials_vector_input_y)
        self.initials_vector_layout.addWidget(self.initials_vector_label_z)
        self.initials_vector_layout.addWidget(self.initials_vector_input_z)

        self.initials_velocities_layout = QtWidgets.QVBoxLayout()
        self.initials_velocities_order1_layout = QtWidgets.QHBoxLayout()
        self.initials_velocities_v1_label = QtWidgets.QLabel('V1: ')
        self.initials_velocities_v1_input = VelocityInput()
        self.initials_velocities_z1_label = QtWidgets.QLabel('Z1: ')
        self.initials_velocities_z1_input = SizeInput()
        self.initials_velocities_order1_layout.addWidget(self.initials_velocities_v1_label)
        self.initials_velocities_order1_layout.addWidget(self.initials_velocities_v1_input)
        self.initials_velocities_order1_layout.addWidget(self.initials_velocities_z1_label)
        self.initials_velocities_order1_layout.addWidget(self.initials_velocities_z1_input)

        self.initials_velocities_order2_layout = QtWidgets.QHBoxLayout()
        self.initials_velocities_v2_label = QtWidgets.QLabel('V2: ')
        self.initials_velocities_v2_input = VelocityInput()
        self.initials_velocities_z2_label = QtWidgets.QLabel('Z2: ')
        self.initials_velocities_z2_input = SizeInput()
        self.initials_velocities_order2_layout.addWidget(self.initials_velocities_v2_label)
        self.initials_velocities_order2_layout.addWidget(self.initials_velocities_v2_input)
        self.initials_velocities_order2_layout.addWidget(self.initials_velocities_z2_label)
        self.initials_velocities_order2_layout.addWidget(self.initials_velocities_z2_input)

        self.initials_velocities_order3_layout = QtWidgets.QHBoxLayout()
        self.initials_velocities_v3_label = QtWidgets.QLabel('V3: ')
        self.initials_velocities_v3_input = VelocityInput()
        self.initials_velocities_z3_label = QtWidgets.QLabel('Z3: ')
        self.initials_velocities_z3_input = SizeInput()
        self.initials_velocities_order3_layout.addWidget(self.initials_velocities_v3_label)
        self.initials_velocities_order3_layout.addWidget(self.initials_velocities_v3_input)
        self.initials_velocities_order3_layout.addWidget(self.initials_velocities_z3_label)
        self.initials_velocities_order3_layout.addWidget(self.initials_velocities_z3_input)

        self.initials_velocities_layout.addLayout(self.initials_velocities_order1_layout)
        self.initials_velocities_layout.addLayout(self.initials_velocities_order2_layout)
        self.initials_velocities_layout.addLayout(self.initials_velocities_order3_layout)

        self.initials_props_layout.addLayout(self.initials_vector_layout)
        self.initials_props_layout.addLayout(self.initials_velocities_layout)
        self.initials_props_layout.addStretch(1)
        self.initials_props_group.setLayout(self.initials_props_layout)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.initials_window_layout = QtWidgets.QVBoxLayout()
        self.initials_window_layout.addLayout(self.has_initials_layout)
        self.initials_window_layout.addWidget(self.initials_props_group)
        self.initials_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.initials_window_layout)

        initials_object = Case.the().get_mk_based_properties(self.target.real_mk()).initials
        if initials_object:
            self.has_initials_selector.setCurrentIndex(0)
            self.on_initials_change(0)
            self.initials_props_group.setEnabled(True)
            self.initials_vector_input_x.setValue(initials_object.force[0])
            self.initials_vector_input_y.setValue(initials_object.force[1])
            self.initials_vector_input_z.setValue(initials_object.force[2])
            self.initials_type_selector.setCurrentIndex(initials_object.initials_type)
            self.initials_velocities_v1_input.setValue(initials_object.v1)
            self.initials_velocities_v2_input.setValue(initials_object.v2)
            self.initials_velocities_v3_input.setValue(initials_object.v3)
            self.initials_velocities_z1_input.setValue(initials_object.z1)
            self.initials_velocities_z2_input.setValue(initials_object.z2)
            self.initials_velocities_z3_input.setValue(initials_object.z3)
        else:
            self.has_initials_selector.setCurrentIndex(1)
            self.on_initials_change(1)
            self.initials_props_group.setEnabled(False)
            self.has_initials_selector.setCurrentIndex(1)
            self.initials_type_selector.setCurrentIndex(0)
            self.initials_vector_input_x.setValue(0.0)
            self.initials_vector_input_y.setValue(0.0)
            self.initials_vector_input_z.setValue(0.0)
            self.initials_velocities_v1_input.setValue(0.0)
            self.initials_velocities_v2_input.setValue(0.0)
            self.initials_velocities_v3_input.setValue(0.0)
            self.initials_velocities_z1_input.setValue(0.0)
            self.initials_velocities_z2_input.setValue(0.0)
            self.initials_velocities_z3_input.setValue(0.0)

        self.exec_()

    def on_ok(self):
        """ Saves the dialog settings on the data structure. """
        info_dialog(__("This will apply the initials properties to all objects with mkfluid = ") + str(self.target_mk))
        if self.has_initials_selector.currentIndex() == 1:
            # Initials false
            Case.the().get_mk_based_properties(self.target.real_mk()).initials = None
        else:
            # Initials true
            # Structure: InitialsProperty Object
            force_vector: list = [self.initials_vector_input_x.value(), self.initials_vector_input_y.value(), self.initials_vector_input_z.value()]
            Case.the().get_mk_based_properties(self.target.real_mk()).initials = InitialsProperty(
                mk=self.target_mk,
                force=force_vector,
                initials_type=self.initials_type_selector.currentIndex(),
                v1=self.initials_velocities_v1_input.value(),
                v2=self.initials_velocities_v2_input.value(),
                v3=self.initials_velocities_v3_input.value(),
                z1=self.initials_velocities_z1_input.value(),
                z2=self.initials_velocities_z2_input.value(),
                z3=self.initials_velocities_z3_input.value()
            )
        self.accept()

    def on_cancel(self):
        """ Closes the window and rejects it. """
        self.reject()

    def on_initials_change(self, index):
        """ Reacts to the initials enabled combobox enabling/disabling the properties configuration widget. """
        if index == 0:
            self.initials_props_group.setEnabled(True)
            self.on_initials_type_change(self.initials_type_selector.currentIndex())
        else:
            self.initials_props_group.setEnabled(False)

    def on_initials_type_change(self, index):
        """ Reacts to the initials type combobox enabling/disabling the appropriate properties. """
        if index == 0:
            self.initials_velocities_v1_input.setEnabled(True)
            self.initials_velocities_z1_input.setEnabled(False)
            self.initials_velocities_v2_input.setEnabled(False)
            self.initials_velocities_z2_input.setEnabled(False)
            self.initials_velocities_v3_input.setEnabled(False)
            self.initials_velocities_z3_input.setEnabled(False)
        elif index == 1:
            self.initials_velocities_v1_input.setEnabled(True)
            self.initials_velocities_z1_input.setEnabled(True)
            self.initials_velocities_v2_input.setEnabled(True)
            self.initials_velocities_z2_input.setEnabled(True)
            self.initials_velocities_v3_input.setEnabled(False)
            self.initials_velocities_z3_input.setEnabled(False)
        elif index == 2:
            self.initials_velocities_v1_input.setEnabled(True)
            self.initials_velocities_z1_input.setEnabled(True)
            self.initials_velocities_v2_input.setEnabled(True)
            self.initials_velocities_z2_input.setEnabled(True)
            self.initials_velocities_v3_input.setEnabled(True)
            self.initials_velocities_z3_input.setEnabled(True)
