#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics normals Dialog """

import FreeCADGui

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.dataobjects.properties.bound_normals_property import BoundNormals
from mod.tools.dialog_tools import info_dialog
from mod.enums import BoundNormalsType
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class SetnormalsWidget(QtWidgets.QWidget):
    """ Widget with properties used by the Set type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.normal_layout = QtWidgets.QHBoxLayout()
        self.normal_label = QtWidgets.QLabel(__("Normal: (X,Y,Z) "))
        self.normal_input_x = ValueInput()
        self.normal_input_y = ValueInput()
        self.normal_input_z = ValueInput()
        self.normal_layout.addWidget(self.normal_label)
        self.normal_layout.addWidget(self.normal_input_x)
        self.normal_layout.addWidget(self.normal_input_y)
        self.normal_layout.addWidget(self.normal_input_z)

        self.main_layout.addLayout(self.normal_layout)
        self.setLayout(self.main_layout)


class PlanenormalsWidget(QtWidgets.QWidget):
    """ Widget with properties used by the Plane type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.point_layout = QtWidgets.QHBoxLayout()
        self.point_label = QtWidgets.QLabel(__("Point: (X,Y,Z)"))
        self.point_input_x = SizeInput()
        self.point_input_y = SizeInput()
        self.point_input_z = SizeInput()
        self.point_auto_check = QtWidgets.QCheckBox(__("Auto"))
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_input_x)
        self.point_layout.addWidget(self.point_input_y)
        self.point_layout.addWidget(self.point_input_z)
        self.point_layout.addWidget(self.point_auto_check)

        self.point_auto_check.clicked.connect(self.on_point_auto_check)

        self.normal_layout = QtWidgets.QHBoxLayout()
        self.normal_label = QtWidgets.QLabel(__("Normal: (X,Y,Z) "))
        self.normal_input_x = ValueInput()
        self.normal_input_y = ValueInput()
        self.normal_input_z = ValueInput()
        self.normal_layout.addWidget(self.normal_label)
        self.normal_layout.addWidget(self.normal_input_x)
        self.normal_layout.addWidget(self.normal_input_y)
        self.normal_layout.addWidget(self.normal_input_z)

        self.maxdisth_layout = QtWidgets.QHBoxLayout()
        self.maxdisth_label = QtWidgets.QLabel(__("Max. distance to boundary limit (value*h): "))
        self.maxdisth_input = ValueInput()
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

class SpherenormalsWidget(QtWidgets.QWidget):
    """ Widget with properties used by the Sphere type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.center_layout = QtWidgets.QHBoxLayout()
        self.center_label = QtWidgets.QLabel(__("Center: (X,Y,Z)"))
        self.center_input_x = SizeInput()
        self.center_input_y = SizeInput()
        self.center_input_z = SizeInput()
        self.center_layout.addWidget(self.center_label)
        self.center_layout.addWidget(self.center_input_x)
        self.center_layout.addWidget(self.center_input_y)
        self.center_layout.addWidget(self.center_input_z)

        self.radius_layout = QtWidgets.QHBoxLayout()
        self.radius_label = QtWidgets.QLabel(__("Radius: "))
        self.radius_input = SizeInput()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_input)

        self.inside_layout = QtWidgets.QHBoxLayout()
        self.inside_label = QtWidgets.QLabel(__("Boundary particles inside the sphere:"))
        self.inside_input = QtWidgets.QComboBox()
        self.inside_input.insertItems(0, [__("Yes"), __("No")])
        self.inside_layout.addWidget(self.inside_label)
        self.inside_layout.addWidget(self.inside_input)
        self.inside_layout.addStretch(1)

        self.maxdisth_layout = QtWidgets.QHBoxLayout()
        self.maxdisth_label = QtWidgets.QLabel(__("Max. distance to boundary limit (value*h): "))
        self.maxdisth_input = ValueInput()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.inside_layout)
        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class CylindernormalsWidget(QtWidgets.QWidget):
    """ Widget with properties used by the Cylinder type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.center1_layout = QtWidgets.QHBoxLayout()
        self.center1_label = QtWidgets.QLabel(__("Center 1: (X,Y,Z) "))
        self.center1_input_x = SizeInput()
        self.center1_input_y = SizeInput()
        self.center1_input_z = SizeInput()
        self.center1_layout.addWidget(self.center1_label)
        self.center1_layout.addWidget(self.center1_input_x)
        self.center1_layout.addWidget(self.center1_input_y)
        self.center1_layout.addWidget(self.center1_input_z)

        self.center2_layout = QtWidgets.QHBoxLayout()
        self.center2_label = QtWidgets.QLabel(__("Center 2: (X,Y,Z) "))
        self.center2_input_x = SizeInput()
        self.center2_input_y = SizeInput()
        self.center2_input_z = SizeInput()
        self.center2_layout.addWidget(self.center2_label)
        self.center2_layout.addWidget(self.center2_input_x)
        self.center2_layout.addWidget(self.center2_input_y)
        self.center2_layout.addWidget(self.center2_input_z)

        self.radius_layout = QtWidgets.QHBoxLayout()
        self.radius_label = QtWidgets.QLabel(__("Radius: "))
        self.radius_input = SizeInput()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_input)

        self.inside_layout = QtWidgets.QHBoxLayout()
        self.inside_label = QtWidgets.QLabel(__("Boundary particles inside the cylinder:"))
        self.inside_input = QtWidgets.QComboBox()
        self.inside_input.insertItems(0, [__("Yes"), __("No")])
        self.inside_layout.addWidget(self.inside_label)
        self.inside_layout.addWidget(self.inside_input)
        self.inside_layout.addStretch(1)

        self.maxdisth_layout = QtWidgets.QHBoxLayout()
        self.maxdisth_label = QtWidgets.QLabel(__("Max. distance to boundary limit (value*h): "))
        self.maxdisth_input = ValueInput()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.center1_layout)
        self.main_layout.addLayout(self.center2_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.inside_layout)
        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class PartsnormalsWidget(QtWidgets.QWidget):
    """ Widget with properties used by the Parts type """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.maxdisth_layout = QtWidgets.QHBoxLayout()
        self.maxdisth_label = QtWidgets.QLabel(__("Max. distance to boundary limit (value*h): "))
        self.maxdisth_input = ValueInput()
        self.maxdisth_layout.addWidget(self.maxdisth_label)
        self.maxdisth_layout.addWidget(self.maxdisth_input)

        self.main_layout.addLayout(self.maxdisth_layout)
        self.setLayout(self.main_layout)


class BoundNormalsDialog(QtWidgets.QDialog):
    """ Defines a window with normals  """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Normals configuration for boundary"))
        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.target = Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name)
        self.target_mk = self.target.obj_mk

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_normals_layout = QtWidgets.QHBoxLayout()
        self.has_normals_label = QtWidgets.QLabel(__("Set normals: "))
        self.has_normals_label.setToolTip(__("Enables normal generation"))
        self.has_normals_selector = QtWidgets.QComboBox()
        self.has_normals_selector.insertItems(0, ["True", "False"])
        self.has_normals_selector.currentIndexChanged.connect(self.on_normals_change)

        self.normals_type_label = QtWidgets.QLabel(__("Type: "))
        self.normals_type_label.setToolTip(__("Chooses the type of the normals."))
        self.normals_type_selector = QtWidgets.QComboBox()
        self.normals_type_selector.insertItems(0, ['Normals - Set', 'Normals - Plane', 'Normals - Sphere', 'Normals - Cylinder', 'Normals - Parts'])
        self.normals_type_selector.currentIndexChanged.connect(self.on_normals_type_change)

        self.has_normals_targetlabel = QtWidgets.QLabel(__("Target MKBound: ") + str(self.target_mk))

        self.has_normals_layout.addWidget(self.has_normals_label)
        self.has_normals_layout.addWidget(self.has_normals_selector)
        self.has_normals_layout.addWidget(self.normals_type_label)
        self.has_normals_layout.addWidget(self.normals_type_selector)
        self.has_normals_layout.addStretch(1)
        self.has_normals_layout.addWidget(self.has_normals_targetlabel)

        self.normals_props_group = QtWidgets.QGroupBox(__("Normals properties"))
        self.normals_props_layout = QtWidgets.QVBoxLayout()

        self.set_normals_widget = SetnormalsWidget()
        self.plane_normals_widget = PlanenormalsWidget()
        self.sphere_normals_widget = SpherenormalsWidget()
        self.cylinder_normals_widget = CylindernormalsWidget()
        self.parts_normals_widget = PartsnormalsWidget()

        self.normals_props_layout.addWidget(self.set_normals_widget)
        self.normals_props_layout.addWidget(self.plane_normals_widget)
        self.normals_props_layout.addWidget(self.sphere_normals_widget)
        self.normals_props_layout.addWidget(self.cylinder_normals_widget)
        self.normals_props_layout.addWidget(self.parts_normals_widget)
        self.normals_props_layout.addStretch(1)
        self.normals_props_group.setLayout(self.normals_props_layout)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.normals_window_layout = QtWidgets.QVBoxLayout()
        self.normals_window_layout.addLayout(self.has_normals_layout)
        self.normals_window_layout.addWidget(self.normals_props_group)
        self.normals_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.normals_window_layout)

        self.set_normals_widget.setVisible(True)
        self.plane_normals_widget.setVisible(False)
        self.sphere_normals_widget.setVisible(False)
        self.cylinder_normals_widget.setVisible(False)
        self.parts_normals_widget.setVisible(False)

        normals_object = Case.the().get_mk_based_properties(self.target.real_mk()).bound_normals
        if normals_object:
            self.has_normals_selector.setCurrentIndex(0)
            self.on_normals_change(0)
            self.normals_props_group.setEnabled(True)
            self.normals_type_selector.setCurrentIndex(normals_object.normals_type)
            self.set_normals_widget.normal_input_x.setValue(normals_object.normal[0])
            self.set_normals_widget.normal_input_y.setValue(normals_object.normal[1])
            self.set_normals_widget.normal_input_z.setValue(normals_object.normal[2])
            self.plane_normals_widget.point_input_x.setValue(normals_object.point[0])
            self.plane_normals_widget.point_input_y.setValue(normals_object.point[1])
            self.plane_normals_widget.point_input_z.setValue(normals_object.point[2])
            self.plane_normals_widget.point_auto_check.setCheckState(QtCore.Qt.Checked if normals_object.point_auto else QtCore.Qt.Unchecked)
            self.plane_normals_widget.normal_input_x.setValue(normals_object.normal[0])
            self.plane_normals_widget.normal_input_y.setValue(normals_object.normal[1])
            self.plane_normals_widget.normal_input_z.setValue(normals_object.normal[2])
            self.plane_normals_widget.maxdisth_input.setValue(normals_object.maxdisth)
            self.sphere_normals_widget.center_input_x.setValue(normals_object.center[0])
            self.sphere_normals_widget.center_input_y.setValue(normals_object.center[1])
            self.sphere_normals_widget.center_input_z.setValue(normals_object.center[2])
            self.sphere_normals_widget.radius_input.setValue(normals_object.radius)
            self.sphere_normals_widget.inside_input.setCurrentIndex(0 if normals_object.inside else 1)
            self.sphere_normals_widget.maxdisth_input.setValue(normals_object.maxdisth)
            self.cylinder_normals_widget.center1_input_x.setValue(normals_object.center1[0])
            self.cylinder_normals_widget.center1_input_y.setValue(normals_object.center1[1])
            self.cylinder_normals_widget.center1_input_z.setValue(normals_object.center1[2])
            self.cylinder_normals_widget.center2_input_x.setValue(normals_object.center2[0])
            self.cylinder_normals_widget.center2_input_y.setValue(normals_object.center2[1])
            self.cylinder_normals_widget.center2_input_z.setValue(normals_object.center2[2])
            self.cylinder_normals_widget.radius_input.setValue(normals_object.radius)
            self.cylinder_normals_widget.inside_input.setCurrentIndex(0 if normals_object.inside else 1)
            self.cylinder_normals_widget.maxdisth_input.setValue(normals_object.maxdisth)
            self.parts_normals_widget.maxdisth_input.setValue(normals_object.maxdisth)

            if normals_object.point_auto:
                self.plane_normals_widget.on_point_auto_check()

            self.on_normals_type_change(normals_object.normals_type)
        else:
            self.has_normals_selector.setCurrentIndex(1)
            self.on_normals_change(1)
            self.normals_props_group.setEnabled(False)
            self.has_normals_selector.setCurrentIndex(1)
            self.normals_type_selector.setCurrentIndex(0)
            self.set_normals_widget.normal_input_x.setValue(1.0)
            self.set_normals_widget.normal_input_y.setValue(0.0)
            self.set_normals_widget.normal_input_z.setValue(0.0)
            self.plane_normals_widget.point_input_x.setValue(1.0)
            self.plane_normals_widget.point_input_y.setValue(0.0)
            self.plane_normals_widget.point_input_z.setValue(0.0)
            self.plane_normals_widget.normal_input_x.setValue(1.0)
            self.plane_normals_widget.normal_input_y.setValue(0.0)
            self.plane_normals_widget.normal_input_z.setValue(0.0)
            self.plane_normals_widget.maxdisth_input.setValue(2.0)
            self.sphere_normals_widget.center_input_x.setValue(1.0)
            self.sphere_normals_widget.center_input_y.setValue(0.0)
            self.sphere_normals_widget.center_input_z.setValue(0.0)
            self.sphere_normals_widget.radius_input.setValue(1.0)
            self.sphere_normals_widget.inside_input.setCurrentIndex(0)
            self.sphere_normals_widget.maxdisth_input.setValue(2.0)
            self.cylinder_normals_widget.center1_input_x.setValue(1.0)
            self.cylinder_normals_widget.center1_input_y.setValue(0.0)
            self.cylinder_normals_widget.center1_input_z.setValue(0.0)
            self.cylinder_normals_widget.center2_input_x.setValue(1.0)
            self.cylinder_normals_widget.center2_input_y.setValue(0.0)
            self.cylinder_normals_widget.center2_input_z.setValue(0.0)
            self.cylinder_normals_widget.radius_input.setValue(1.0)
            self.cylinder_normals_widget.inside_input.setCurrentIndex(0)
            self.cylinder_normals_widget.maxdisth_input.setValue(2.0)
            self.parts_normals_widget.maxdisth_input.setValue(2.0)

        self.exec_()

    def on_ok(self):
        """ Saves the dialog settings on the data structure. """
        info_dialog(__("This will apply the normals properties to all objects with mkbound = ") + str(self.target_mk))
        if self.has_normals_selector.currentIndex() == 1:
            # normals false
            Case.the().get_mk_based_properties(self.target.real_mk()).bound_normals = None
        else:
            # normals true
            # Structure: BoundNormalsType Object
            bound_normals = BoundNormals()
            bound_normals.mk = self.target_mk
            bound_normals.normals_type = self.normals_type_selector.currentIndex()
            if bound_normals.normals_type == BoundNormalsType.SET:
                bound_normals.normal = [self.set_normals_widget.normal_input_x.value(),self.set_normals_widget.normal_input_y.value(),self.set_normals_widget.normal_input_z.value()]
            elif bound_normals.normals_type == BoundNormalsType.PLANE:
                bound_normals.point_auto = self.plane_normals_widget.point_auto_check.isChecked()
                bound_normals.normal = [self.plane_normals_widget.normal_input_x.value(),self.plane_normals_widget.normal_input_y.value(),self.plane_normals_widget.normal_input_z.value()]
                bound_normals.point = [self.plane_normals_widget.point_input_x.value(),self.plane_normals_widget.point_input_y.value(),self.plane_normals_widget.point_input_z.value()]
                bound_normals.maxdisth = self.plane_normals_widget.maxdisth_input.value()
            elif bound_normals.normals_type == BoundNormalsType.SPHERE:
                bound_normals.center = [self.sphere_normals_widget.center_input_x.value(),self.sphere_normals_widget.center_input_y.value(),self.sphere_normals_widget.center_input_z.value()]
                bound_normals.radius = self.sphere_normals_widget.radius_input.value()
                bound_normals.maxdisth = self.sphere_normals_widget.maxdisth_input.value()
                bound_normals.inside = self.sphere_normals_widget.inside_input.currentIndex() == 0
            elif bound_normals.normals_type == BoundNormalsType.CYLINDER:
                bound_normals.center1 = [self.cylinder_normals_widget.center1_input_x.value(),self.cylinder_normals_widget.center1_input_y.value(),self.cylinder_normals_widget.center1_input_z.value()]
                bound_normals.center2 = [self.cylinder_normals_widget.center2_input_x.value(),self.cylinder_normals_widget.center2_input_y.value(),self.cylinder_normals_widget.center2_input_z.value()]
                bound_normals.radius = self.cylinder_normals_widget.radius_input.value()
                bound_normals.maxdisth = self.cylinder_normals_widget.maxdisth_input.value()
                bound_normals.inside = self.cylinder_normals_widget.inside_input.currentIndex() == 0
            elif bound_normals.normals_type == BoundNormalsType.PARTS:
                bound_normals.maxdisth = self.parts_normals_widget.maxdisth_input.value()

            Case.the().get_mk_based_properties(self.target.real_mk()).bound_normals = bound_normals
        self.accept()

    def on_cancel(self):
        """ Closes the window and rejects it. """
        self.reject()

    def on_normals_change(self, index):
        """ Reacts to the normals enabled combobox enabling/disabling the properties configuration widget. """
        if index == 0:
            self.normals_props_group.setEnabled(True)
            self.normals_type_selector.setEnabled(True)
            self.on_normals_type_change(self.normals_type_selector.currentIndex())
        else:
            self.normals_props_group.setEnabled(False)
            self.normals_type_selector.setEnabled(False)

    def on_normals_type_change(self, index):
        """ Reacts to the normals type combobox enabling/disabling the appropriate properties. """
        self.set_normals_widget.setVisible(False)
        self.plane_normals_widget.setVisible(False)
        self.sphere_normals_widget.setVisible(False)
        self.cylinder_normals_widget.setVisible(False)
        self.parts_normals_widget.setVisible(False)
        self.adjustSize()
        if index == 0:
            self.set_normals_widget.setVisible(True)
        elif index == 1:
            self.plane_normals_widget.setVisible(True)
        elif index == 2:
            self.sphere_normals_widget.setVisible(True)
        elif index == 3:
            self.cylinder_normals_widget.setVisible(True)
        elif index == 4:
            self.parts_normals_widget.setVisible(True)
