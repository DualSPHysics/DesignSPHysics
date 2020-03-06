#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Float State configuration dialog. """

import FreeCADGui

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.dialog_tools import info_dialog

from mod.enums import ObjectType

from mod.dataobjects.case import Case
from mod.dataobjects.float_property import FloatProperty


class FloatStateDialog(QtGui.QDialog):
    """ Defines a window with floating  """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Floating configuration"))
        self.ok_button = QtGui.QPushButton(__("OK"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))

        self.target_mk = Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name).obj_mk

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.is_floating_layout = QtGui.QHBoxLayout()
        self.is_floating_label = QtGui.QLabel(__("Set floating: "))
        self.is_floating_label.setToolTip(__("Sets the current MKBound selected as floating."))
        self.is_floating_selector = QtGui.QComboBox()
        self.is_floating_selector.insertItems(0, ["True", "False"])
        self.is_floating_selector.currentIndexChanged.connect(self.on_floating_change)
        self.is_floating_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(self.target_mk))
        self.is_floating_layout.addWidget(self.is_floating_label)
        self.is_floating_layout.addWidget(self.is_floating_selector)
        self.is_floating_layout.addStretch(1)

        self.is_floating_layout.addWidget(self.is_floating_targetlabel)
        self.floating_props_group = QtGui.QGroupBox(__("Floating properties"))
        self.floating_props_layout = QtGui.QVBoxLayout()
        self.floating_props_massrhop_layout = QtGui.QHBoxLayout()
        self.floating_props_massrhop_label = QtGui.QLabel(__("Mass/Density: "))
        self.floating_props_massrhop_label.setToolTip(__("Selects an mass/density calculation method and its value."))
        self.floating_props_massrhop_selector = QtGui.QComboBox()
        self.floating_props_massrhop_selector.insertItems(0, ["massbody (kg)", "rhopbody (kg/m^3)"])
        self.floating_props_massrhop_input = QtGui.QLineEdit()
        self.floating_props_massrhop_selector.currentIndexChanged.connect(self.on_massrhop_change)
        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_label)

        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_selector)
        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_input)
        self.floating_center_layout = QtGui.QHBoxLayout()
        self.floating_center_label = QtGui.QLabel(__("Gravity center (m): "))
        self.floating_center_label.setToolTip(__("Sets the mk group gravity center."))
        self.floating_center_label_x = QtGui.QLabel("X")
        self.floating_center_input_x = QtGui.QLineEdit()
        self.floating_center_label_y = QtGui.QLabel("Y")
        self.floating_center_input_y = QtGui.QLineEdit()
        self.floating_center_label_z = QtGui.QLabel("Z")
        self.floating_center_input_z = QtGui.QLineEdit()
        self.floating_center_auto = QtGui.QCheckBox("Auto ")
        self.floating_center_auto.toggled.connect(self.on_gravity_auto)
        self.floating_center_layout.addWidget(self.floating_center_label)
        self.floating_center_layout.addWidget(self.floating_center_label_x)
        self.floating_center_layout.addWidget(self.floating_center_input_x)
        self.floating_center_layout.addWidget(self.floating_center_label_y)
        self.floating_center_layout.addWidget(self.floating_center_input_y)
        self.floating_center_layout.addWidget(self.floating_center_label_z)
        self.floating_center_layout.addWidget(self.floating_center_input_z)
        self.floating_center_layout.addWidget(self.floating_center_auto)

        self.floating_inertia_layout = QtGui.QHBoxLayout()
        self.floating_inertia_label = QtGui.QLabel(__("Inertia (kg*m<sup>2</sup>): "))
        self.floating_inertia_label.setToolTip(__("Sets the MK group inertia."))
        self.floating_inertia_label_x = QtGui.QLabel("X")
        self.floating_inertia_input_x = QtGui.QLineEdit()
        self.floating_inertia_label_y = QtGui.QLabel("Y")
        self.floating_inertia_input_y = QtGui.QLineEdit()
        self.floating_inertia_label_z = QtGui.QLabel("Z")
        self.floating_inertia_input_z = QtGui.QLineEdit()
        self.floating_inertia_auto = QtGui.QCheckBox("Auto ")
        self.floating_inertia_auto.toggled.connect(self.on_inertia_auto)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_x)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_x)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_y)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_y)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_z)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_z)
        self.floating_inertia_layout.addWidget(self.floating_inertia_auto)

        self.floating_velini_layout = QtGui.QHBoxLayout()
        self.floating_velini_label = QtGui.QLabel(__("Initial linear velocity: "))
        self.floating_velini_label.setToolTip(__("Sets the MK group initial linear velocity"))
        self.floating_velini_label_x = QtGui.QLabel("X")
        self.floating_velini_input_x = QtGui.QLineEdit()
        self.floating_velini_label_y = QtGui.QLabel("Y")
        self.floating_velini_input_y = QtGui.QLineEdit()
        self.floating_velini_label_z = QtGui.QLabel("Z")
        self.floating_velini_input_z = QtGui.QLineEdit()
        self.floating_velini_auto = QtGui.QCheckBox("Auto ")
        self.floating_velini_auto.toggled.connect(self.on_velini_auto)
        self.floating_velini_layout.addWidget(self.floating_velini_label)
        self.floating_velini_layout.addWidget(self.floating_velini_label_x)
        self.floating_velini_layout.addWidget(self.floating_velini_input_x)
        self.floating_velini_layout.addWidget(self.floating_velini_label_y)
        self.floating_velini_layout.addWidget(self.floating_velini_input_y)
        self.floating_velini_layout.addWidget(self.floating_velini_label_z)
        self.floating_velini_layout.addWidget(self.floating_velini_input_z)
        self.floating_velini_layout.addWidget(self.floating_velini_auto)

        self.floating_omegaini_layout = QtGui.QHBoxLayout()
        self.floating_omegaini_label = QtGui.QLabel(__("Initial angular velocity: "))
        self.floating_omegaini_label.setToolTip(__("Sets the MK group initial angular velocity"))
        self.floating_omegaini_label_x = QtGui.QLabel("X")
        self.floating_omegaini_input_x = QtGui.QLineEdit()
        self.floating_omegaini_label_y = QtGui.QLabel("Y")
        self.floating_omegaini_input_y = QtGui.QLineEdit()
        self.floating_omegaini_label_z = QtGui.QLabel("Z")
        self.floating_omegaini_input_z = QtGui.QLineEdit()
        self.floating_omegaini_auto = QtGui.QCheckBox("Auto ")
        self.floating_omegaini_auto.toggled.connect(self.on_omegaini_auto)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_x)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_x)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_y)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_y)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_z)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_z)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_auto)

        self.floating_translation_layout = QtGui.QHBoxLayout()
        self.floating_translation_label = QtGui.QLabel(__("Translation DOF: "))
        self.floating_translation_label.setToolTip(__("Use No for translation restriction in the movement (default=(Yes, Yes, Yes))"))
        self.floating_translation_label_x = QtGui.QLabel("X")
        self.floating_translation_input_x = QtGui.QComboBox()
        self.floating_translation_input_x.insertItems(1, ["No", "Yes"])
        self.floating_translation_label_y = QtGui.QLabel("Y")
        self.floating_translation_input_y = QtGui.QComboBox()
        self.floating_translation_input_y.insertItems(1, ["No", "Yes"])
        self.floating_translation_label_z = QtGui.QLabel("Z")
        self.floating_translation_input_z = QtGui.QComboBox()
        self.floating_translation_input_z.insertItems(1, ["No", "Yes"])
        self.floating_translation_auto = QtGui.QCheckBox("Auto ")
        self.floating_translation_auto.toggled.connect(self.on_translation_auto)
        self.floating_translation_layout.addWidget(self.floating_translation_label)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_x)
        self.floating_translation_layout.addWidget(self.floating_translation_input_x)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_y)
        self.floating_translation_layout.addWidget(self.floating_translation_input_y)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_z)
        self.floating_translation_layout.addWidget(self.floating_translation_input_z)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_auto)

        self.floating_rotation_layout = QtGui.QHBoxLayout()
        self.floating_rotation_label = QtGui.QLabel(__("Rotation DOF: "))
        self.floating_rotation_label.setToolTip(__("Use No for rotation restriction in the movement (default=(Yes , Yes, Yes))"))
        self.floating_rotation_label_x = QtGui.QLabel("X")
        self.floating_rotation_input_x = QtGui.QComboBox()
        self.floating_rotation_input_x.insertItems(1, ["No", "Yes"])
        self.floating_rotation_label_y = QtGui.QLabel("Y")
        self.floating_rotation_input_y = QtGui.QComboBox()
        self.floating_rotation_input_y.insertItems(1, ["No", "Yes"])
        self.floating_rotation_label_z = QtGui.QLabel("Z")
        self.floating_rotation_input_z = QtGui.QComboBox()
        self.floating_rotation_input_z.insertItems(1, ["No", "Yes"])
        self.floating_rotation_auto = QtGui.QCheckBox("Auto ")
        self.floating_rotation_auto.toggled.connect(self.on_rotation_auto)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_x)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_x)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_y)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_y)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_z)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_z)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_auto)

        self.floating_material_layout = QtGui.QHBoxLayout()
        self.floating_material_label = QtGui.QLabel(__("Material: "))
        self.floating_material_line_edit = QtGui.QLineEdit()
        self.floating_material_auto = QtGui.QCheckBox("Auto ")
        self.floating_material_auto.toggled.connect(self.on_material_auto)
        self.floating_material_layout.addWidget(self.floating_material_label)
        self.floating_material_layout.addWidget(self.floating_material_line_edit)
        self.floating_material_layout.addStretch(1)
        self.floating_material_layout.addWidget(self.floating_material_auto)

        self.floating_props_layout.addLayout(self.floating_props_massrhop_layout)
        self.floating_props_layout.addLayout(self.floating_center_layout)
        self.floating_props_layout.addLayout(self.floating_inertia_layout)
        self.floating_props_layout.addLayout(self.floating_velini_layout)
        self.floating_props_layout.addLayout(self.floating_omegaini_layout)
        self.floating_props_layout.addLayout(self.floating_translation_layout)
        self.floating_props_layout.addLayout(self.floating_rotation_layout)
        self.floating_props_layout.addLayout(self.floating_material_layout)
        self.floating_props_layout.addStretch(1)
        self.floating_props_group.setLayout(self.floating_props_layout)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.floatings_window_layout = QtGui.QVBoxLayout()
        self.floatings_window_layout.addLayout(self.is_floating_layout)
        self.floatings_window_layout.addWidget(self.floating_props_group)
        self.floatings_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.floatings_window_layout)

        float_property: FloatProperty = Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).float_property
        if float_property:
            self.is_floating_selector.setCurrentIndex(0)
            self.on_floating_change(0)
            self.floating_props_group.setEnabled(True)
            self.floating_props_massrhop_selector.setCurrentIndex(float_property.mass_density_type)
            self.floating_props_massrhop_input.setText(str(float_property.mass_density_value))
            if not float_property.gravity_center:
                self.floating_center_input_x.setText("0")
                self.floating_center_input_y.setText("0")
                self.floating_center_input_z.setText("0")
            else:
                self.floating_center_input_x.setText(str(float_property.gravity_center[0]))
                self.floating_center_input_y.setText(str(float_property.gravity_center[1]))
                self.floating_center_input_z.setText(str(float_property.gravity_center[2]))

            if not float_property.inertia:
                self.floating_inertia_input_x.setText("0")
                self.floating_inertia_input_y.setText("0")
                self.floating_inertia_input_z.setText("0")
            else:
                self.floating_inertia_input_x.setText(str(float_property.inertia[0]))
                self.floating_inertia_input_y.setText(str(float_property.inertia[1]))
                self.floating_inertia_input_z.setText(str(float_property.inertia[2]))

            if not float_property.initial_linear_velocity:
                self.floating_velini_input_x.setText("0")
                self.floating_velini_input_y.setText("0")
                self.floating_velini_input_z.setText("0")
            else:
                self.floating_velini_input_x.setText(
                    str(float_property.initial_linear_velocity[0]))
                self.floating_velini_input_y.setText(str(float_property.initial_linear_velocity[1]))
                self.floating_velini_input_z.setText(str(float_property.initial_linear_velocity[2]))

            if not float_property.initial_angular_velocity:
                self.floating_omegaini_input_x.setText("0")
                self.floating_omegaini_input_y.setText("0")
                self.floating_omegaini_input_z.setText("0")
            else:
                self.floating_omegaini_input_x.setText(
                    str(float_property.initial_angular_velocity[0]))
                self.floating_omegaini_input_y.setText(str(float_property.initial_angular_velocity[1]))
                self.floating_omegaini_input_z.setText(str(float_property.initial_angular_velocity[2]))

            if not float_property.translation_restriction:
                self.floating_translation_input_x.setCurrentIndex(1)
                self.floating_translation_input_y.setCurrentIndex(1)
                self.floating_translation_input_z.setCurrentIndex(1)
            else:
                self.floating_translation_input_x.setCurrentIndex(float_property.translation_restriction[0])
                self.floating_translation_input_y.setCurrentIndex(float_property.translation_restriction[1])
                self.floating_translation_input_z.setCurrentIndex(float_property.translation_restriction[2])

            if not float_property.rotation_restriction:
                self.floating_rotation_input_x.setCurrentIndex(1)
                self.floating_rotation_input_y.setCurrentIndex(1)
                self.floating_rotation_input_z.setCurrentIndex(1)
            else:
                self.floating_rotation_input_x.setCurrentIndex(float_property.rotation_restriction[0])
                self.floating_rotation_input_y.setCurrentIndex(float_property.rotation_restriction[1])
                self.floating_rotation_input_z.setCurrentIndex(float_property.rotation_restriction[2])

            if not float_property.material:
                self.floating_material_line_edit.setText("")
            else:
                self.floating_material_line_edit.setText(float_property.material)

            self.floating_center_auto.setCheckState(QtCore.Qt.Checked if not float_property.gravity_center else QtCore.Qt.Unchecked)
            self.floating_inertia_auto.setCheckState(QtCore.Qt.Checked if not float_property.inertia else QtCore.Qt.Unchecked)
            self.floating_velini_auto.setCheckState(QtCore.Qt.Checked if not float_property.initial_linear_velocity else QtCore.Qt.Unchecked)
            self.floating_omegaini_auto.setCheckState(QtCore.Qt.Checked if not float_property.initial_angular_velocity else QtCore.Qt.Unchecked)
            self.floating_translation_auto.setCheckState(QtCore.Qt.Checked if not float_property.translation_restriction else QtCore.Qt.Unchecked)
            self.floating_rotation_auto.setCheckState(QtCore.Qt.Checked if not float_property.rotation_restriction else QtCore.Qt.Unchecked)
            self.floating_material_auto.setCheckState(QtCore.Qt.Checked if not float_property.material else QtCore.Qt.Unchecked)
        else:
            self.is_floating_selector.setCurrentIndex(1)
            self.on_floating_change(1)
            self.floating_props_group.setEnabled(False)
            self.is_floating_selector.setCurrentIndex(1)
            self.floating_props_massrhop_selector.setCurrentIndex(1)
            self.floating_props_massrhop_input.setText("1000")
            self.floating_center_input_x.setText("0")
            self.floating_center_input_y.setText("0")
            self.floating_center_input_z.setText("0")
            self.floating_inertia_input_x.setText("0")
            self.floating_inertia_input_y.setText("0")
            self.floating_inertia_input_z.setText("0")
            self.floating_velini_input_x.setText("0")
            self.floating_velini_input_y.setText("0")
            self.floating_velini_input_z.setText("0")
            self.floating_omegaini_input_x.setText("0")
            self.floating_omegaini_input_y.setText("0")
            self.floating_omegaini_input_z.setText("0")
            self.floating_translation_input_x.setCurrentIndex(1)
            self.floating_translation_input_y.setCurrentIndex(1)
            self.floating_translation_input_z.setCurrentIndex(1)
            self.floating_rotation_input_x.setCurrentIndex(1)
            self.floating_rotation_input_y.setCurrentIndex(1)
            self.floating_rotation_input_z.setCurrentIndex(1)
            self.floating_material_line_edit.setText("")

            self.floating_center_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_inertia_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_velini_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_omegaini_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_translation_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_rotation_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_material_auto.setCheckState(QtCore.Qt.Checked)

        self.exec_()

    def on_ok(self):
        """ Composes floating options and saves them into the appropriate data structure. """
        info_dialog(__("This will apply the floating properties to all objects with mkbound = ") + str(self.target_mk))

        if self.is_floating_selector.currentIndex() == 1:
            # Remove Floating
            Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).float_property = None
            self.accept()
            return

        # Floating is true
        fp = FloatProperty()  # FloatProperty to be inserted
        fp.mk = self.target_mk
        fp.mass_density_type = self.floating_props_massrhop_selector.currentIndex()
        fp.mass_density_value = float(self.floating_props_massrhop_input.text())

        fp.gravity_center = list() if self.floating_center_auto.isChecked() else [float(self.floating_center_input_x.text()), float(self.floating_center_input_y.text()), float(self.floating_center_input_z.text())]
        fp.inertia = list() if self.floating_inertia_auto.isChecked() else [float(self.floating_inertia_input_x.text()), float(self.floating_inertia_input_y.text()), float(self.floating_inertia_input_z.text())]
        fp.initial_linear_velocity = list() if self.floating_velini_auto.isChecked() else [float(self.floating_velini_input_x.text()), float(self.floating_velini_input_y.text()), float(self.floating_velini_input_z.text())]
        fp.initial_angular_velocity = list() if self.floating_omegaini_auto.isChecked() else [float(self.floating_omegaini_input_x.text()), float(self.floating_omegaini_input_y.text()), float(self.floating_omegaini_input_z.text())]
        fp.translation_restriction = list() if self.floating_translation_auto.isChecked() else [int(self.floating_translation_input_x.currentIndex()), int(self.floating_translation_input_y.currentIndex()), int(self.floating_translation_input_z.currentIndex())]
        fp.rotation_restriction = list() if self.floating_rotation_auto.isChecked() else [int(self.floating_rotation_input_x.currentIndex()), int(self.floating_rotation_input_y.currentIndex()), int(self.floating_rotation_input_z.currentIndex())]
        fp.material = "" if self.floating_material_auto.isChecked() else str(self.floating_material_line_edit.text())
        Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).float_property = fp

        self.accept()

    def on_cancel(self):
        """ Closes the dialog and rejects. """
        self.reject()

    def on_floating_change(self, index):
        """ Reacts to the floating index changing enabling/disabling the floating properties. """
        self.floating_props_group.setEnabled(index == 0)

    def on_massrhop_change(self, _):
        """ Reacts to the massrhop checkbox change enabling disabling its input. """
        self.floating_props_massrhop_input.setText("0.0")

    def on_gravity_auto(self):
        """ Reacts to the gravity auto check enabling/disabling its inputs. """
        self.floating_center_input_x.setEnabled(not self.floating_center_auto.isChecked())
        self.floating_center_input_y.setEnabled(not self.floating_center_auto.isChecked())
        self.floating_center_input_z.setEnabled(not self.floating_center_auto.isChecked())

    def on_inertia_auto(self):
        """ Reacts to the inertia auto check enabling/disabling its inputs. """
        self.floating_inertia_input_x.setEnabled(not self.floating_inertia_auto.isChecked())
        self.floating_inertia_input_y.setEnabled(not self.floating_inertia_auto.isChecked())
        self.floating_inertia_input_z.setEnabled(not self.floating_inertia_auto.isChecked())

    def on_velini_auto(self):
        """ Reacts to the velini auto check enabling/disabling its inputs. """
        self.floating_velini_input_x.setEnabled(not self.floating_velini_auto.isChecked())
        self.floating_velini_input_y.setEnabled(not self.floating_velini_auto.isChecked())
        self.floating_velini_input_z.setEnabled(not self.floating_velini_auto.isChecked())

    def on_omegaini_auto(self):
        """ Reacts to the omegaini auto check enabling/disabling its inputs. """
        self.floating_omegaini_input_x.setEnabled(not self.floating_omegaini_auto.isChecked())
        self.floating_omegaini_input_y.setEnabled(not self.floating_omegaini_auto.isChecked())
        self.floating_omegaini_input_z.setEnabled(not self.floating_omegaini_auto.isChecked())

    def on_translation_auto(self):
        """ Reacts to the translation auto check enabling disabling its inputs. """
        self.floating_translation_input_x.setEnabled(not self.floating_translation_auto.isChecked())
        self.floating_translation_input_y.setEnabled(not self.floating_translation_auto.isChecked())
        self.floating_translation_input_z.setEnabled(not self.floating_translation_auto.isChecked())

    def on_rotation_auto(self):
        """ Reacts to the rotation checkbox being pressed enabling/disabling its inputs. """
        self.floating_rotation_input_x.setEnabled(not self.floating_rotation_auto.isChecked())
        self.floating_rotation_input_y.setEnabled(not self.floating_rotation_auto.isChecked())
        self.floating_rotation_input_z.setEnabled(not self.floating_rotation_auto.isChecked())

    def on_material_auto(self):
        """ Reacts to the material auto checkbox being pressed enabling/disabling its input. """
        self.floating_material_line_edit.setEnabled(not self.floating_material_auto.isChecked())
