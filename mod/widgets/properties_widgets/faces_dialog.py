#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Faces Configuration Dialog"""

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.properties.faces_property import FacesProperty
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.enums import FreeCADObjectType
from mod.tools.freecad_tools import get_fc_object
from mod.tools.translation_tools import __


class FacesDialog(QtWidgets.QDialog):
    """ Defines a window with faces  """

    def __init__(self, selection_name, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Faces configuration"))
        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.main_layout = QtWidgets.QVBoxLayout()

        self.target_object: SimulationObject = Case.the().get_simulation_object(selection_name)





        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.faces_layout = QtWidgets.QVBoxLayout()

        self.all_faces = QtWidgets.QCheckBox(__("All faces"))
        self.all_faces.setCheckState(QtCore.Qt.Checked)
        self.all_faces.toggled.connect(self.on_faces_checkbox)

        self.front_face = QtWidgets.QCheckBox(__("Front face"))
        self.back_face = QtWidgets.QCheckBox(__("Back face"))
        self.top_face = QtWidgets.QCheckBox(__("Top face"))
        self.bottom_face = QtWidgets.QCheckBox(__("Bottom face"))
        self.left_face = QtWidgets.QCheckBox(__("Left face"))
        self.right_face = QtWidgets.QCheckBox(__("Right face"))

        self.layers_label = QtWidgets.QLabel(__("Layers:"))
        self.layers_input = QtWidgets.QLineEdit()

        if self.target_object.faces_configuration:
            self.all_faces.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.all_faces else QtCore.Qt.Unchecked)
            self.front_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.front_face else QtCore.Qt.Unchecked)
            self.back_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.back_face else QtCore.Qt.Unchecked)
            self.top_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.top_face else QtCore.Qt.Unchecked)
            self.bottom_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.bottom_face else QtCore.Qt.Unchecked)
            self.left_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.left_face else QtCore.Qt.Unchecked)
            self.right_face.setCheckState(QtCore.Qt.Checked if self.target_object.faces_configuration.right_face else QtCore.Qt.Unchecked)
            self.layers_input.setText(self.target_object.faces_configuration.layers)

        self.all_faces.toggled.connect(self.on_faces_checkbox)

        self.faces_options_layout = QtWidgets.QHBoxLayout()
        self.faces_options_col1_layout = QtWidgets.QVBoxLayout()
        self.faces_options_col2_layout = QtWidgets.QVBoxLayout()

        self.faces_options_col1_layout.addWidget(self.front_face)
        self.faces_options_col1_layout.addWidget(self.top_face)
        self.faces_options_col1_layout.addWidget(self.left_face)

        self.faces_options_col2_layout.addWidget(self.back_face)
        self.faces_options_col2_layout.addWidget(self.bottom_face)
        self.faces_options_col2_layout.addWidget(self.right_face)

        self.faces_options_layout.addLayout(self.faces_options_col1_layout)
        self.faces_options_layout.addLayout(self.faces_options_col2_layout)

        self.faces_layout.addWidget(self.all_faces)
        self.faces_layout.addLayout(self.faces_options_layout)

        self.layers_layout = QtWidgets.QVBoxLayout()
        self.layers_layout.addWidget(self.layers_label)
        self.layers_layout.addWidget(self.layers_input)

        if get_fc_object(self.target_object.name).TypeId == FreeCADObjectType.BOX:
            self.main_layout.addLayout(self.faces_layout)
        self.main_layout.addLayout(self.layers_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.on_faces_checkbox()

        self.exec_()

    def on_ok(self):
        """ Composes a FacesProperty object and saves it in the data structure. """
        fp = FacesProperty()

        if self.all_faces.isChecked():
            fp.all_faces = True
        else:
            fp.front_face = self.front_face.isChecked()
            fp.back_face = self.back_face.isChecked()
            fp.top_face = self.top_face.isChecked()
            fp.bottom_face = self.bottom_face.isChecked()
            fp.left_face = self.left_face.isChecked()
            fp.right_face = self.right_face.isChecked()

        fp.build_face_print()
        fp.layers = self.layers_input.text()
        self.target_object.faces_configuration = fp
        self.accept()

    def on_cancel(self):
        """ Closes the dialog and rejects it. """
        self.reject()

    def on_faces_checkbox(self):
        """ Checks the faces state """
        if self.all_faces.isChecked():
            self.front_face.setEnabled(False)
            self.back_face.setEnabled(False)
            self.top_face.setEnabled(False)
            self.bottom_face.setEnabled(False)
            self.left_face.setEnabled(False)
            self.right_face.setEnabled(False)
        else:
            self.front_face.setEnabled(True)
            self.back_face.setEnabled(True)
            self.top_face.setEnabled(True)
            self.bottom_face.setEnabled(True)
            self.left_face.setEnabled(True)
            self.right_face.setEnabled(True)
