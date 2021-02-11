#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Link Hinge Edit Dialog """

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog

from mod.dataobjects.case import Case


class LinkHingeEdit(QtGui.QDialog):
    """ Defines Link hinge window dialog """

    def __init__(self, link_hinge_id, bodies_widgets, parent=None):
        super().__init__(parent=parent)

        self.link_hinge_id = link_hinge_id
        self.case = Case.the()

        # Title
        self.setWindowTitle(__("Link hinge configuration"))
        self.link_hinge_edit_layout = QtGui.QVBoxLayout()

        # Find the link hinge for which the button was pressed
        target_link_hinge = None

        for link_hinge in self.case.chrono.link_hinge:
            if link_hinge.id == self.link_hinge_id:
                target_link_hinge = link_hinge

        # This should not happen but if no link hinge is found with reference id, it spawns an error.
        if target_link_hinge is None:
            error_dialog("There was an error opnening the link hinge to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_hinge.idbody1)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_hinge.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_hinge.idbody2)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_hinge.idbody2):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_hinge_edit_layout.addLayout(self.body_layout)

        # Points for rotation
        self.rotpoints_layout = QtGui.QHBoxLayout()
        self.rotpoints_label = QtGui.QLabel(__("Points for rotation: "))
        self.rotpoints_x_label = QtGui.QLabel(__("X"))
        self.rotpoints_x_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotpoint[0]))
        self.rotpoints_y_label = QtGui.QLabel(__("Y"))
        self.rotpoints_y_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotpoint[1]))
        self.rotpoints_z_label = QtGui.QLabel(__("Z"))
        self.rotpoints_z_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotpoint[2]))

        self.rotpoints_layout.addWidget(self.rotpoints_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_y_label)
        self.rotpoints_layout.addWidget(self.rotpoints_y_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_z_label)
        self.rotpoints_layout.addWidget(self.rotpoints_z_line_edit)

        self.link_hinge_edit_layout.addLayout(self.rotpoints_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtGui.QHBoxLayout()
        self.rotvector_label = QtGui.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtGui.QLabel(__("X"))
        self.rotvector_x_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotvector[0]))
        self.rotvector_y_label = QtGui.QLabel(__("Y"))
        self.rotvector_y_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotvector[1]))
        self.rotvector_z_label = QtGui.QLabel(__("Z"))
        self.rotvector_z_line_edit = QtGui.QLineEdit(str(target_link_hinge.rotvector[2]))

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_hinge_edit_layout.addLayout(self.rotvector_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness (Nm/rad):"))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_hinge.stiffness))
        self.damping_label = QtGui.QLabel(__("Damping (Nms/rad):"))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_hinge.damping))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_hinge_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_hinge_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_hinge_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_hinge_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link hinge edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link hinge save button behaviour"""
        link_hinge = self.case.chrono.get_link_hinge_for_id(self.link_hinge_id)
        link_hinge.idbody1 = str(self.body_one_line_edit.currentText())
        link_hinge.idbody2 = str(self.body_two_line_edit.currentText())
        link_hinge.rotpoint = [float(self.rotpoints_x_line_edit.text()), float(self.rotpoints_y_line_edit.text()), float(self.rotpoints_z_line_edit.text())]
        link_hinge.rotvector = [float(self.rotvector_x_line_edit.text()), float(self.rotvector_y_line_edit.text()), float(self.rotvector_z_line_edit.text())]
        link_hinge.stiffness = float(self.stiffness_line_edit.text())
        link_hinge.damping = float(self.damping_line_edit.text())

        if link_hinge.idbody1 and link_hinge.idbody2:
            LinkHingeEdit.accept(self)
        else:
            error_dialog("You need to select an option for each one of the bodies.")
