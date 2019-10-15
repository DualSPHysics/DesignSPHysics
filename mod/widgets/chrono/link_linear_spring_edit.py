#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics LinkLinearSprint Edit Dialog """

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog

from mod.dataobjects.case import Case


class LinkLinearspringEdit(QtGui.QDialog):
    """ Defines Link linearspring window dialog """

    def __init__(self, link_linearspring_id, parent=None):
        super(LinkLinearspringEdit, self).__init__(parent=parent)

        self.link_linearspring_id = link_linearspring_id

        # Title
        self.setWindowTitle(__("Link linearspring configuration"))
        self.link_linearspring_edit_layout = QtGui.QVBoxLayout()

        # Find the link linearspring for which the button was pressed
        target_link_linearspring = None

        for link_linearspring in Case.instance().chrono.link_linearspring:
            if link_linearspring.id == self.link_linearspring_id:
                target_link_linearspring = link_linearspring

        # This should not happen but if no link linearspring is found with reference id, it spawns an error.
        if target_link_linearspring is None:
            error_dialog("There was an error opnening the link linearspring to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_linearspring.idbody1)])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_linearspring.idbody2)])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring.idbody2):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_linearspring_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact in body 1
        self.points_b1_layout = QtGui.QHBoxLayout()
        self.points_b1_label = QtGui.QLabel(__("Points in body 1: "))
        self.point_b1_x_label = QtGui.QLabel(__("X"))
        self.point_b1_x_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb1[0]))
        self.point_b1_y_label = QtGui.QLabel(__("Y"))
        self.point_b1_y_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb1[1]))
        self.point_b1_z_label = QtGui.QLabel(__("Z"))
        self.point_b1_z_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb1[2]))

        self.points_b1_layout.addWidget(self.points_b1_label)
        self.points_b1_layout.addWidget(self.point_b1_x_label)
        self.points_b1_layout.addWidget(self.point_b1_x_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_y_label)
        self.points_b1_layout.addWidget(self.point_b1_y_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_z_label)
        self.points_b1_layout.addWidget(self.point_b1_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b1_layout)

        # Points where the elements interact in body 2
        self.points_b2_layout = QtGui.QHBoxLayout()
        self.points_b2_label = QtGui.QLabel(__("Points in body 2: "))
        self.point_b2_x_label = QtGui.QLabel(__("X"))
        self.point_b2_x_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb2[0]))
        self.point_b2_y_label = QtGui.QLabel(__("Y"))
        self.point_b2_y_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb2[1]))
        self.point_b2_z_label = QtGui.QLabel(__("Z"))
        self.point_b2_z_line_edit = QtGui.QLineEdit(str(target_link_linearspring.point_fb2[2]))

        self.points_b2_layout.addWidget(self.points_b2_label)
        self.points_b2_layout.addWidget(self.point_b2_x_label)
        self.points_b2_layout.addWidget(self.point_b2_x_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_y_label)
        self.points_b2_layout.addWidget(self.point_b2_y_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_z_label)
        self.points_b2_layout.addWidget(self.point_b2_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness: "))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_linearspring.stiffness))
        self.damping_label = QtGui.QLabel(__("Damping: "))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_linearspring.damping))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_linearspring_edit_layout.addLayout(self.torsion_damping_layout)

        # Spring equilibrium length
        self.rest_layout = QtGui.QHBoxLayout()
        self.rest_label = QtGui.QLabel(__("Rest length: "))
        self.rest_line_edit = QtGui.QLineEdit(str(target_link_linearspring.rest_length))

        self.rest_layout.addWidget(self.rest_label)
        self.rest_layout.addWidget(self.rest_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.rest_layout)

        # vtk
        self.vtk_layout = QtGui.QHBoxLayout()
        self.vtk_nside_label = QtGui.QLabel(__("Number of sections: "))
        self.vtk_nside_line_edit = QtGui.QLineEdit(str(target_link_linearspring.number_of_sections))
        self.vtk_radius_label = QtGui.QLabel(__("Spring radius: "))
        self.vtk_radius_line_edit = QtGui.QLineEdit(str(target_link_linearspring.sprint_radius))
        self.vtk_length_label = QtGui.QLabel(__("Length for revolution: "))
        self.vtk_length_line_edit = QtGui.QLineEdit(str(target_link_linearspring.revolution_length))

        self.vtk_layout.addWidget(self.vtk_nside_label)
        self.vtk_layout.addWidget(self.vtk_nside_line_edit)
        self.vtk_layout.addWidget(self.vtk_radius_label)
        self.vtk_layout.addWidget(self.vtk_radius_line_edit)
        self.vtk_layout.addWidget(self.vtk_length_label)
        self.vtk_layout.addWidget(self.vtk_length_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.vtk_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
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
        count = -1
        for link_linearspring_value in Case.instance().chrono.link_linearspring:
            count += 1
            if link_linearspring_value[0] == self.link_linearspring_id:
                Case.instance().chrono.link_linearspring[count].idbody1 = str(self.body_one_line_edit.currentText())
                Case.instance().chrono.link_linearspring[count].idbody2 = str(self.body_two_line_edit.currentText())
                Case.instance().chrono.link_linearspring[count].point_fb1 = [float(self.point_b1_x_line_edit.text()),
                                                                             float(self.point_b1_y_line_edit.text()),
                                                                             float(self.point_b1_z_line_edit.text())]
                Case.instance().chrono.link_linearspring[count].point_fb2 = [float(self.point_b2_x_line_edit.text()),
                                                                             float(self.point_b2_y_line_edit.text()),
                                                                             float(self.point_b2_z_line_edit.text())]
                Case.instance().chrono.link_linearspring[count].stiffness = float(self.stiffness_line_edit.text())
                Case.instance().chrono.link_linearspring[count].damping = float(self.damping_line_edit.text())
                Case.instance().chrono.link_linearspring[count].rest_length = float(self.rest_line_edit.text())
                Case.instance().chrono.link_linearspring[count].number_of_sections = float(self.vtk_nside_line_edit.text())
                Case.instance().chrono.link_linearspring[count].spring_radius = float(self.vtk_radius_line_edit.text())
                Case.instance().chrono.link_linearspring[count].revolution_length = float(self.vtk_length_line_edit.text())

        if Case.instance().chrono.link_linearspring[count].idbody1 and Case.instance().chrono.link_linearspring[count].idbody2:
            LinkLinearspringEdit.accept(self)
        else:
            link_linearspring_error_dialog = QtGui.QMessageBox()
            link_linearspring_error_dialog.setWindowTitle(__("Error!"))
            link_linearspring_error_dialog.setText(__("bodies are necessary!"))
            link_linearspring_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_linearspring_error_dialog.exec_()
