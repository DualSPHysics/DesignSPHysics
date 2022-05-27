#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Initials Dialog """

import FreeCADGui

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.dialog_tools import info_dialog

from mod.enums import BoundInitialsType, ObjectType

from mod.dataobjects.bound_initials_property import BoundInitialsProperty
from mod.dataobjects.case import Case


class SetInitialsWidget(QtGui.QWidget):
    """ Widget with properties used by the Set type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()

        self.normal_layout = QtGui.QHBoxLayout()
        self.normal_label = QtGui.QLabel(__("Normal: "))
        self.normal_label_x = QtGui.QLabel("X")
        self.normal_input_x = QtGui.QLineEdit()
        self.normal_label_y = QtGui.QLabel("Y")
        self.normal_input_y = QtGui.QLineEdit()
        self.normal_label_z = QtGui.QLabel("Z")
        self.normal_input_z = QtGui.QLineEdit()
        self.normal_layout.addWidget(self.normal_label)
        self.normal_layout.addWidget(self.normal_label_x)
        self.normal_layout.addWidget(self.normal_input_x)
        self.normal_layout.addWidget(self.normal_label_y)
        self.normal_layout.addWidget(self.normal_input_y)
        self.normal_layout.addWidget(self.normal_label_z)
        self.normal_layout.addWidget(self.normal_input_z)

        self.main_layout.addLayout(self.normal_layout)
        self.setLayout(self.main_layout)


class PlaneInitialsWidget(QtGui.QWidget):
    """ Widget with properties used by the Plane type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()

        self.point_layout = QtGui.QHBoxLayout()
        self.point_label = QtGui.QLabel(__("Point: "))
        self.point_label_x = QtGui.QLabel("X")
        self.point_input_x = QtGui.QLineEdit()
        self.point_label_y = QtGui.QLabel("Y")
        self.point_input_y = QtGui.QLineEdit()
        self.point_label_z = QtGui.QLabel("Z")
        self.point_input_z = QtGui.QLineEdit()
        self.point_auto_check = QtGui.QCheckBox(__("Auto"))
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_label_x)
        self.point_layout.addWidget(self.point_input_x)
        self.point_layout.addWidget(self.point_label_y)
        self.point_layout.addWidget(self.point_input_y)
        self.point_layout.addWidget(self.point_label_z)
        self.point_layout.addWidget(self.point_input_z)
        self.point_layout.addWidget(self.point_auto_check)

        self.point_auto_check.clicked.connect(self.on_point_auto_check)

        self.normal_layout = QtGui.QHBoxLayout()
        self.normal_label = QtGui.QLabel(__("Normal: "))
        self.normal_label_x = QtGui.QLabel("X")
        self.normal_input_x = QtGui.QLineEdit()
        self.normal_label_y = QtGui.QLabel("Y")
        self.normal_input_y = QtGui.QLineEdit()
        self.normal_label_z = QtGui.QLabel("Z")
        self.normal_input_z = QtGui.QLineEdit()
        self.normal_layout.addWidget(self.normal_label)
        self.normal_layout.addWidget(self.normal_label_x)
        self.normal_layout.addWidget(self.normal_input_x)
        self.normal_layout.addWidget(self.normal_label_y)
        self.normal_layout.addWidget(self.normal_input_y)
        self.normal_layout.addWidget(self.normal_label_z)
        self.normal_layout.addWidget(self.normal_input_z)

        self.maxdisth_layout = QtGui.QHBoxLayout()
        self.maxdisth_label = QtGui.QLabel(__("Max. distance to boundary limit: "))
        self.maxdisth_input = QtGui.QLineEdit()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.normal_layout)
        self.main_layout.addLayout(self.maxdisth_layout)

        self.setLayout(self.main_layout)

    def on_point_auto_check(self):
        if self.point_auto_check.isChecked():
            self.point_input_x.setEnabled(False)
            self.point_input_y.setEnabled(False)
            self.point_input_z.setEnabled(False)
        else:
            self.point_input_x.setEnabled(True)
            self.point_input_y.setEnabled(True)
            self.point_input_z.setEnabled(True)

class SphereInitialsWidget(QtGui.QWidget):
    """ Widget with properties used by the Sphere type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()

        self.center_layout = QtGui.QHBoxLayout()
        self.center_label = QtGui.QLabel(__("Center: "))
        self.center_label_x = QtGui.QLabel("X")
        self.center_input_x = QtGui.QLineEdit()
        self.center_label_y = QtGui.QLabel("Y")
        self.center_input_y = QtGui.QLineEdit()
        self.center_label_z = QtGui.QLabel("Z")
        self.center_input_z = QtGui.QLineEdit()
        self.center_layout.addWidget(self.center_label)
        self.center_layout.addWidget(self.center_label_x)
        self.center_layout.addWidget(self.center_input_x)
        self.center_layout.addWidget(self.center_label_y)
        self.center_layout.addWidget(self.center_input_y)
        self.center_layout.addWidget(self.center_label_z)
        self.center_layout.addWidget(self.center_input_z)

        self.radius_layout = QtGui.QHBoxLayout()
        self.radius_label = QtGui.QLabel(__("Radius: "))
        self.radius_input = QtGui.QLineEdit()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_input)

        self.inside_layout = QtGui.QHBoxLayout()
        self.inside_label = QtGui.QLabel(__("Boundary particles inside the sphere:"))
        self.inside_input = QtGui.QComboBox()
        self.inside_input.insertItems(0, [__("Yes"), __("No")])
        self.inside_layout.addWidget(self.inside_label)
        self.inside_layout.addWidget(self.inside_input)
        self.inside_layout.addStretch(1)

        self.maxdisth_layout = QtGui.QHBoxLayout()
        self.maxdisth_label = QtGui.QLabel(__("Max. distance to boundary limit: "))
        self.maxdisth_input = QtGui.QLineEdit()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.inside_layout)
        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class CylinderInitialsWidget(QtGui.QWidget):
    """ Widget with properties used by the Cylinder type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()

        self.center1_layout = QtGui.QHBoxLayout()
        self.center1_label = QtGui.QLabel(__("Center 1: "))
        self.center1_label_x = QtGui.QLabel("X")
        self.center1_input_x = QtGui.QLineEdit()
        self.center1_label_y = QtGui.QLabel("Y")
        self.center1_input_y = QtGui.QLineEdit()
        self.center1_label_z = QtGui.QLabel("Z")
        self.center1_input_z = QtGui.QLineEdit()
        self.center1_layout.addWidget(self.center1_label)
        self.center1_layout.addWidget(self.center1_label_x)
        self.center1_layout.addWidget(self.center1_input_x)
        self.center1_layout.addWidget(self.center1_label_y)
        self.center1_layout.addWidget(self.center1_input_y)
        self.center1_layout.addWidget(self.center1_label_z)
        self.center1_layout.addWidget(self.center1_input_z)

        self.center2_layout = QtGui.QHBoxLayout()
        self.center2_label = QtGui.QLabel(__("Center 2: "))
        self.center2_label_x = QtGui.QLabel("X")
        self.center2_input_x = QtGui.QLineEdit()
        self.center2_label_y = QtGui.QLabel("Y")
        self.center2_input_y = QtGui.QLineEdit()
        self.center2_label_z = QtGui.QLabel("Z")
        self.center2_input_z = QtGui.QLineEdit()
        self.center2_layout.addWidget(self.center2_label)
        self.center2_layout.addWidget(self.center2_label_x)
        self.center2_layout.addWidget(self.center2_input_x)
        self.center2_layout.addWidget(self.center2_label_y)
        self.center2_layout.addWidget(self.center2_input_y)
        self.center2_layout.addWidget(self.center2_label_z)
        self.center2_layout.addWidget(self.center2_input_z)

        self.radius_layout = QtGui.QHBoxLayout()
        self.radius_label = QtGui.QLabel(__("Radius: "))
        self.radius_input = QtGui.QLineEdit()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_input)

        self.inside_layout = QtGui.QHBoxLayout()
        self.inside_label = QtGui.QLabel(__("Boundary particles inside the cylinder:"))
        self.inside_input = QtGui.QComboBox()
        self.inside_input.insertItems(0, [__("Yes"), __("No")])
        self.inside_layout.addWidget(self.inside_label)
        self.inside_layout.addWidget(self.inside_input)
        self.inside_layout.addStretch(1)

        self.maxdisth_layout = QtGui.QHBoxLayout()
        self.maxdisth_label = QtGui.QLabel(__("Max. distance to boundary limit: "))
        self.maxdisth_input = QtGui.QLineEdit()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.center1_layout)
        self.main_layout.addLayout(self.center2_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.inside_layout)
        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class PartsInitialsWidget(QtGui.QWidget):
    """ Widget with properties used by the Parts type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtGui.QVBoxLayout()

        self.maxdisth_layout = QtGui.QHBoxLayout()
        self.maxdisth_label = QtGui.QLabel(__("Max. distance to boundary limit: "))
        self.maxdisth_input = QtGui.QLineEdit()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class BoundInitialsDialog(QtGui.QDialog):
    """ Defines a window with initials  """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Initials configuration for boundary"))
        self.ok_button = QtGui.QPushButton(__("OK"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.target_mk = Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name).obj_mk

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_initials_layout = QtGui.QHBoxLayout()
        self.has_initials_label = QtGui.QLabel(__("Set initials: "))
        self.has_initials_label.setToolTip(__("Sets the current initial movement vector."))
        self.has_initials_selector = QtGui.QComboBox()
        self.has_initials_selector.insertItems(0, ["True", "False"])
        self.has_initials_selector.currentIndexChanged.connect(self.on_initials_change)

        self.initials_type_label = QtGui.QLabel(__("Type: "))
        self.initials_type_label.setToolTip(__("Chooses the type of the initial velocity."))
        self.initials_type_selector = QtGui.QComboBox()
        self.initials_type_selector.insertItems(0, ['Normals - Set', 'Normals - Plane', 'Normals - Sphere', 'Normals - Cylinder', 'Normals - Parts'])
        self.initials_type_selector.currentIndexChanged.connect(self.on_initials_type_change)

        self.has_initials_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(self.target_mk))

        self.has_initials_layout.addWidget(self.has_initials_label)
        self.has_initials_layout.addWidget(self.has_initials_selector)
        self.has_initials_layout.addWidget(self.initials_type_label)
        self.has_initials_layout.addWidget(self.initials_type_selector)
        self.has_initials_layout.addStretch(1)
        self.has_initials_layout.addWidget(self.has_initials_targetlabel)

        self.initials_props_group = QtGui.QGroupBox(__("Initial properties"))
        self.initials_props_layout = QtGui.QVBoxLayout()

        self.set_initials_widget = SetInitialsWidget()
        self.plane_initials_widget = PlaneInitialsWidget()
        self.sphere_initials_widget = SphereInitialsWidget()
        self.cylinder_initials_widget = CylinderInitialsWidget()
        self.parts_initials_widget = PartsInitialsWidget()

        self.initials_props_layout.addWidget(self.set_initials_widget)
        self.initials_props_layout.addWidget(self.plane_initials_widget)
        self.initials_props_layout.addWidget(self.sphere_initials_widget)
        self.initials_props_layout.addWidget(self.cylinder_initials_widget)
        self.initials_props_layout.addWidget(self.parts_initials_widget)
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

        self.set_initials_widget.setVisible(True)
        self.plane_initials_widget.setVisible(False)
        self.sphere_initials_widget.setVisible(False)
        self.cylinder_initials_widget.setVisible(False)
        self.parts_initials_widget.setVisible(False)

        initials_object = Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).bound_initials
        if initials_object:
            self.has_initials_selector.setCurrentIndex(0)
            self.on_initials_change(0)
            self.initials_props_group.setEnabled(True)
            self.initials_type_selector.setCurrentIndex(initials_object.initials_type)
            self.set_initials_widget.normal_input_x.setText(str(initials_object.normal[0]))
            self.set_initials_widget.normal_input_y.setText(str(initials_object.normal[1]))
            self.set_initials_widget.normal_input_z.setText(str(initials_object.normal[2]))
            self.plane_initials_widget.point_input_x.setText(str(initials_object.point[0]))
            self.plane_initials_widget.point_input_y.setText(str(initials_object.point[1]))
            self.plane_initials_widget.point_input_z.setText(str(initials_object.point[2]))
            self.plane_initials_widget.point_auto_check.setCheckState(QtCore.Qt.Checked if initials_object.point_auto else QtCore.Qt.Unchecked)
            self.plane_initials_widget.normal_input_x.setText(str(initials_object.normal[0]))
            self.plane_initials_widget.normal_input_y.setText(str(initials_object.normal[1]))
            self.plane_initials_widget.normal_input_z.setText(str(initials_object.normal[2]))
            self.plane_initials_widget.maxdisth_input.setText(str(initials_object.maxdisth))
            self.sphere_initials_widget.center_input_x.setText(str(initials_object.center[0]))
            self.sphere_initials_widget.center_input_y.setText(str(initials_object.center[1]))
            self.sphere_initials_widget.center_input_z.setText(str(initials_object.center[2]))
            self.sphere_initials_widget.radius_input.setText(str(initials_object.radius))
            self.sphere_initials_widget.inside_input.setCurrentIndex(0 if initials_object.inside else 1)
            self.sphere_initials_widget.maxdisth_input.setText(str(initials_object.maxdisth))
            self.cylinder_initials_widget.center1_input_x.setText(str(initials_object.center1[0]))
            self.cylinder_initials_widget.center1_input_y.setText(str(initials_object.center1[1]))
            self.cylinder_initials_widget.center1_input_z.setText(str(initials_object.center1[2]))
            self.cylinder_initials_widget.center2_input_x.setText(str(initials_object.center2[0]))
            self.cylinder_initials_widget.center2_input_y.setText(str(initials_object.center2[1]))
            self.cylinder_initials_widget.center2_input_z.setText(str(initials_object.center2[2]))
            self.cylinder_initials_widget.radius_input.setText(str(initials_object.radius))
            self.cylinder_initials_widget.inside_input.setCurrentIndex(0 if initials_object.inside else 1)
            self.cylinder_initials_widget.maxdisth_input.setText(str(initials_object.maxdisth))
            self.parts_initials_widget.maxdisth_input.setText(str(initials_object.maxdisth))

            if initials_object.point_auto:
                self.plane_initials_widget.on_point_auto_check()

            self.on_initials_type_change(initials_object.initials_type)
        else:
            self.has_initials_selector.setCurrentIndex(1)
            self.on_initials_change(1)
            self.initials_props_group.setEnabled(False)
            self.has_initials_selector.setCurrentIndex(1)
            self.initials_type_selector.setCurrentIndex(0)
            self.set_initials_widget.normal_input_x.setText("1.0")
            self.set_initials_widget.normal_input_y.setText("0.0")
            self.set_initials_widget.normal_input_z.setText("0.0")
            self.plane_initials_widget.point_input_x.setText("1.0")
            self.plane_initials_widget.point_input_y.setText("0.0")
            self.plane_initials_widget.point_input_z.setText("0.0")
            self.plane_initials_widget.normal_input_x.setText("1.0")
            self.plane_initials_widget.normal_input_y.setText("0.0")
            self.plane_initials_widget.normal_input_z.setText("0.0")
            self.plane_initials_widget.maxdisth_input.setText("2.0")
            self.sphere_initials_widget.center_input_x.setText("1.0")
            self.sphere_initials_widget.center_input_y.setText("0.0")
            self.sphere_initials_widget.center_input_z.setText("0.0")
            self.sphere_initials_widget.radius_input.setText("1.0")
            self.sphere_initials_widget.inside_input.setCurrentIndex(0)
            self.sphere_initials_widget.maxdisth_input.setText("2.0")
            self.cylinder_initials_widget.center1_input_x.setText("1.0")
            self.cylinder_initials_widget.center1_input_y.setText("0.0")
            self.cylinder_initials_widget.center1_input_z.setText("0.0")
            self.cylinder_initials_widget.center2_input_x.setText("1.0")
            self.cylinder_initials_widget.center2_input_y.setText("0.0")
            self.cylinder_initials_widget.center2_input_z.setText("0.0")
            self.cylinder_initials_widget.radius_input.setText("1.0")
            self.cylinder_initials_widget.inside_input.setCurrentIndex(0)
            self.cylinder_initials_widget.maxdisth_input.setText("2.0")
            self.parts_initials_widget.maxdisth_input.setText("2.0")

        self.exec_()

    def on_ok(self):
        """ Saves the dialog settings on the data structure. """
        info_dialog(__("This will apply the initials properties to all objects with mkbound = ") + str(self.target_mk))
        if self.has_initials_selector.currentIndex() == 1:
            # Initials false
            Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).bound_initials = None
        else:
            # Initials true
            # Structure: BoundInitialsProperty Object
            bound_initials = BoundInitialsProperty()
            bound_initials.mk = self.target_mk
            bound_initials.initials_type = self.initials_type_selector.currentIndex()
            if bound_initials.initials_type == BoundInitialsType.SET:
                bound_initials.normal = [float(self.set_initials_widget.normal_input_x.text()), float(self.set_initials_widget.normal_input_y.text()), float(self.set_initials_widget.normal_input_z.text())]
            elif bound_initials.initials_type == BoundInitialsType.PLANE:
                bound_initials.point_auto = self.plane_initials_widget.point_auto_check.isChecked()
                bound_initials.normal = [float(self.plane_initials_widget.normal_input_x.text()), float(self.plane_initials_widget.normal_input_y.text()), float(self.plane_initials_widget.normal_input_z.text())]
                bound_initials.point = [float(self.plane_initials_widget.point_input_x.text()), float(self.plane_initials_widget.point_input_y.text()), float(self.plane_initials_widget.point_input_z.text())]
                bound_initials.maxdisth = float(self.plane_initials_widget.maxdisth_input.text())
            elif bound_initials.initials_type == BoundInitialsType.SPHERE:
                bound_initials.center = [float(self.sphere_initials_widget.center_input_x.text()), float(self.sphere_initials_widget.center_input_y.text()), float(self.sphere_initials_widget.center_input_z.text())]
                bound_initials.radius = float(self.sphere_initials_widget.radius_input.text())
                bound_initials.maxdisth = float(self.sphere_initials_widget.maxdisth_input.text())
                bound_initials.inside = self.sphere_initials_widget.inside_input.currentIndex() == 0
            elif bound_initials.initials_type == BoundInitialsType.CYLINDER:
                bound_initials.center1 = [float(self.cylinder_initials_widget.center1_input_x.text()), float(self.cylinder_initials_widget.center1_input_y.text()), float(self.cylinder_initials_widget.center1_input_z.text())]
                bound_initials.center2 = [float(self.cylinder_initials_widget.center2_input_x.text()), float(self.cylinder_initials_widget.center2_input_y.text()), float(self.cylinder_initials_widget.center2_input_z.text())]
                bound_initials.radius = float(self.cylinder_initials_widget.radius_input.text())
                bound_initials.maxdisth = float(self.cylinder_initials_widget.maxdisth_input.text())
                bound_initials.inside = self.cylinder_initials_widget.inside_input.currentIndex() == 0
            elif bound_initials.initials_type == BoundInitialsType.PARTS:
                bound_initials.maxdisth = float(self.parts_initials_widget.maxdisth_input.text())

            Case.the().get_mk_based_properties(ObjectType.BOUND, self.target_mk).bound_initials = bound_initials
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
        self.set_initials_widget.setVisible(False)
        self.plane_initials_widget.setVisible(False)
        self.sphere_initials_widget.setVisible(False)
        self.cylinder_initials_widget.setVisible(False)
        self.parts_initials_widget.setVisible(False)
        self.adjustSize()
        if index == 0:
            self.set_initials_widget.setVisible(True)
        elif index == 1:
            self.plane_initials_widget.setVisible(True)
        elif index == 2:
            self.sphere_initials_widget.setVisible(True)
        elif index == 3:
            self.cylinder_initials_widget.setVisible(True)
        elif index == 4:
            self.parts_initials_widget.setVisible(True)
