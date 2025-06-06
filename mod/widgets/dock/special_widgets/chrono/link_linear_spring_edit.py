#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics LinkLinearSprint Edit Dialog """


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import error_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.value_input import ValueInput


class LinkLinearspringEdit(QtWidgets.QDialog):
    """ Defines Link linearspring window dialog """

    def __init__(self, link_linearspring_id, bodies_widgets, parent=None):
        super().__init__(parent=parent)

        self.case = Case.the()
        self.link_linearspring_id = link_linearspring_id

        # Title
        self.setWindowTitle(__("Link linearspring configuration"))
        self.link_linearspring_edit_layout = QtWidgets.QVBoxLayout()

        # Find the link linearspring for which the button was pressed
        target_link_linearspring = None

        for link_linearspring in self.case.chrono.link_linearspring:
            if link_linearspring.id == self.link_linearspring_id:
                target_link_linearspring = link_linearspring

        # This should not happen but if no link linearspring is found with reference id, it spawns an error.
        if target_link_linearspring is None:
            error_dialog("There was an error opnening the link linearspring to edit")
            return

        # Elements that interact
        self.body_layout = QtWidgets.QHBoxLayout()
        self.body_one_label = QtWidgets.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtWidgets.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_linearspring.idbody1)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtWidgets.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtWidgets.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_linearspring.idbody2)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring.idbody2):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtWidgets.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_linearspring_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact in body 1
        self.points_b1_layout = QtWidgets.QHBoxLayout()
        self.points_b1_label = QtWidgets.QLabel(__("Point in body 1: "))
        self.point_b1_x_label = QtWidgets.QLabel(__("X"))
        self.point_b1_x_line_edit = SizeInput(value=target_link_linearspring.point_fb1[0])
        self.point_b1_y_label = QtWidgets.QLabel(__("Y"))
        self.point_b1_y_line_edit = SizeInput(value=target_link_linearspring.point_fb1[1])
        self.point_b1_z_label = QtWidgets.QLabel(__("Z"))
        self.point_b1_z_line_edit = SizeInput(value=target_link_linearspring.point_fb1[2])

        self.points_b1_layout.addWidget(self.points_b1_label)
        self.points_b1_layout.addWidget(self.point_b1_x_label)
        self.points_b1_layout.addWidget(self.point_b1_x_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_y_label)
        self.points_b1_layout.addWidget(self.point_b1_y_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_z_label)
        self.points_b1_layout.addWidget(self.point_b1_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b1_layout)

        # Points where the elements interact in body 2
        self.points_b2_layout = QtWidgets.QHBoxLayout()
        self.points_b2_label = QtWidgets.QLabel(__("Point in body 2: "))
        self.point_b2_x_label = QtWidgets.QLabel(__("X"))
        self.point_b2_x_line_edit = SizeInput(value=target_link_linearspring.point_fb2[0])
        self.point_b2_y_label = QtWidgets.QLabel(__("Y"))
        self.point_b2_y_line_edit = SizeInput(value=target_link_linearspring.point_fb2[1])
        self.point_b2_z_label = QtWidgets.QLabel(__("Z"))
        self.point_b2_z_line_edit = SizeInput(value=target_link_linearspring.point_fb2[2])

        self.points_b2_layout.addWidget(self.points_b2_label)
        self.points_b2_layout.addWidget(self.point_b2_x_label)
        self.points_b2_layout.addWidget(self.point_b2_x_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_y_label)
        self.points_b2_layout.addWidget(self.point_b2_y_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_z_label)
        self.points_b2_layout.addWidget(self.point_b2_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtWidgets.QHBoxLayout()
        self.torsion_damping_layout = QtWidgets.QHBoxLayout()
        self.stiffness_label = QtWidgets.QLabel(__("Stiffness (N/m):"))
        self.stiffness_line_edit = ValueInput(value=target_link_linearspring.stiffness)
        self.damping_label = QtWidgets.QLabel(__("Damping (Ns/m):"))
        self.damping_line_edit = ValueInput(value=target_link_linearspring.damping)

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_linearspring_edit_layout.addLayout(self.torsion_damping_layout)

        # Spring equilibrium length
        self.rest_layout = QtWidgets.QHBoxLayout()
        self.rest_label = QtWidgets.QLabel(__("Rest length:"))
        self.rest_line_edit = SizeInput(value=target_link_linearspring.rest_length)

        self.rest_layout.addWidget(self.rest_label)
        self.rest_layout.addWidget(self.rest_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.rest_layout)

        # vtk
        self.visualization_options_groupbox = QtWidgets.QGroupBox(__("Visualization Options"))
        self.vtk_layout = QtWidgets.QHBoxLayout()
        self.vtk_nside_label = QtWidgets.QLabel(__("Number of sections: "))
        self.vtk_nside_line_edit = IntValueInput(min_val=1,value=target_link_linearspring.number_of_sections)
        self.vtk_radius_label = QtWidgets.QLabel(__("Spring radius: "))
        self.vtk_radius_line_edit = ValueInput(value=target_link_linearspring.spring_radius)
        self.vtk_length_label = QtWidgets.QLabel(__("Length for revolution: "))
        self.vtk_length_line_edit = ValueInput(value = target_link_linearspring.revolution_length)

        self.vtk_layout.addWidget(self.vtk_nside_label)
        self.vtk_layout.addWidget(self.vtk_nside_line_edit)
        self.vtk_layout.addWidget(self.vtk_radius_label)
        self.vtk_layout.addWidget(self.vtk_radius_line_edit)
        self.vtk_layout.addWidget(self.vtk_length_label)
        self.vtk_layout.addWidget(self.vtk_length_line_edit)

        self.visualization_options_groupbox.setLayout(self.vtk_layout)
        self.link_linearspring_edit_layout.addWidget(self.visualization_options_groupbox)

        # Buttons
        self.ok_button = QtWidgets.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_linearspring_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_linearspring_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link linearspring edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link linearspring save button behaviour"""
        target_linearspring = self.case.chrono.get_link_linearspring_for_id(self.link_linearspring_id)

        target_linearspring.idbody1 = str(self.body_one_line_edit.currentText())
        target_linearspring.idbody2 = str(self.body_two_line_edit.currentText())
        target_linearspring.point_fb1 = [self.point_b1_x_line_edit.value(),self.point_b1_y_line_edit.value(),self.point_b1_z_line_edit.value()]
        target_linearspring.point_fb2 = [self.point_b2_x_line_edit.value(),self.point_b2_y_line_edit.value(),self.point_b2_z_line_edit.value()]
        target_linearspring.stiffness = self.stiffness_line_edit.value()
        target_linearspring.damping = self.damping_line_edit.value()
        target_linearspring.rest_length = self.rest_line_edit.value()
        target_linearspring.number_of_sections = self.vtk_nside_line_edit.value()
        target_linearspring.spring_radius = self.vtk_radius_line_edit.value()
        target_linearspring.revolution_length = self.vtk_length_line_edit.value()

        if target_linearspring.idbody1 and target_linearspring.idbody2:
            LinkLinearspringEdit.accept(self)
        else:
            error_dialog("You need to select an option for each one of the bodies.")
