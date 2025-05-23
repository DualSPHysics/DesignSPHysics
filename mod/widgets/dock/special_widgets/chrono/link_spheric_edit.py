#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics LinkSphere Edit Widget """


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import error_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class LinkSphericEdit(QtWidgets.QDialog):
    """ Defines Link spheric window dialog """

    def __init__(self, link_spheric_id, bodies_widgets, parent=None):
        super().__init__(parent=parent)

        self.case = Case.the()
        self.link_spheric_id = link_spheric_id

        # Title
        self.setWindowTitle(__("Link spheric configuration"))
        self.link_spheric_edit_layout = QtWidgets.QVBoxLayout()

        # Find the link spheric for which the button was pressed
        target_link_spheric = None

        for link_spheric in self.case.chrono.link_spheric:
            if link_spheric.id == self.link_spheric_id:
                target_link_spheric = link_spheric

        # This should not happen but if no link spheric is found with reference id, it spawns an error.
        if target_link_spheric is None:
            error_dialog("There was an error opnening the link spheric to edit")
            return

        # Elements that interact
        self.body_layout = QtWidgets.QHBoxLayout()
        self.body_one_label = QtWidgets.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtWidgets.QComboBox()
        if str(target_link_spheric.idbody1) != "":
            self.body_one_line_edit.insertItems(0, ["", str(target_link_spheric.idbody1)])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_spheric.idbody1)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtWidgets.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtWidgets.QComboBox()
        if str(target_link_spheric.idbody2) != "":
            self.body_two_line_edit.insertItems(0, ["", str(target_link_spheric.idbody2)])
            self.body_two_line_edit.setCurrentIndex(1)
        else:
            self.body_two_line_edit.insertItems(0, [str(target_link_spheric.idbody2)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric.idbody2):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtWidgets.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_spheric_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact
        self.points_layout = QtWidgets.QHBoxLayout()
        self.points_label = QtWidgets.QLabel(__("Points: "))
        self.point_x_label = QtWidgets.QLabel(__("X"))
        self.point_x_line_edit = SizeInput(value=target_link_spheric.rotpoint[0])
        self.point_y_label = QtWidgets.QLabel(__("Y"))
        self.point_y_line_edit = SizeInput(value=target_link_spheric.rotpoint[1])
        self.point_z_label = QtWidgets.QLabel(__("Z"))
        self.point_z_line_edit = SizeInput(value=target_link_spheric.rotpoint[2])

        self.points_layout.addWidget(self.points_label)
        self.points_layout.addWidget(self.point_x_label)
        self.points_layout.addWidget(self.point_x_line_edit)
        self.points_layout.addWidget(self.point_y_label)
        self.points_layout.addWidget(self.point_y_line_edit)
        self.points_layout.addWidget(self.point_z_label)
        self.points_layout.addWidget(self.point_z_line_edit)

        self.link_spheric_edit_layout.addLayout(self.points_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtWidgets.QHBoxLayout()
        self.torsion_damping_layout = QtWidgets.QHBoxLayout()
        self.stiffness_label = QtWidgets.QLabel(__("Stiffness (Nm/rad):"))
        self.stiffness_line_edit = ValueInput(value=target_link_spheric.stiffness)
        self.damping_label = QtWidgets.QLabel(__("Damping (Nms/rad):"))
        self.damping_line_edit = ValueInput(value=target_link_spheric.damping)

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_spheric_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_spheric_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtWidgets.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_spheric_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_spheric_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link Spheric edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link Spheric save button behaviour"""
        link_spheric = self.case.chrono.get_link_spheric_for_id(self.link_spheric_id)

        link_spheric.idbody1 = str(self.body_one_line_edit.currentText())
        link_spheric.idbody2 = str(self.body_two_line_edit.currentText())
        link_spheric.rotpoint = [self.point_x_line_edit.value(),self.point_y_line_edit.value(),self.point_z_line_edit.value()]
        link_spheric.stiffness = self.stiffness_line_edit.value()
        link_spheric.damping = self.damping_line_edit.value()

        if link_spheric.idbody1:
            LinkSphericEdit.accept(self)
        else:
            error_dialog("You need to select an option for the body to use.")
