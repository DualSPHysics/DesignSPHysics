#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics LinkSphere Edit Widget '''

from PySide import QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog

# FIXME: Change data references for refactored Case data
class LinkSphericEdit(QtGui.QDialog):
    ''' Defines Link spheric window dialog '''

    def __init__(self, link_spheric_id):
        super(LinkSphericEdit, self).__init__()

        self.link_spheric_id = link_spheric_id

        # Title
        self.setWindowTitle(__("Link spheric configuration"))
        self.link_spheric_edit_layout = QtGui.QVBoxLayout()

        # Find the link spheric for which the button was pressed
        target_link_spheric = None

        for link_spheric in self.data['link_spheric']:
            if link_spheric[0] == self.link_spheric_id:
                target_link_spheric = link_spheric

        # This should not happen but if no link spheric is found with reference id, it spawns an error.
        if target_link_spheric is None:
            error_dialog("There was an error opnening the link spheric to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        if str(target_link_spheric[1]) != '':
            self.body_one_line_edit.insertItems(0, ['', str(target_link_spheric[1])])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_spheric[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        if str(target_link_spheric[2]) != '':
            self.body_two_line_edit.insertItems(0, ['', str(target_link_spheric[2])])
            self.body_two_line_edit.setCurrentIndex(1)
        else:
            self.body_two_line_edit.insertItems(0, [str(target_link_spheric[2])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric[2]):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_spheric_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact
        self.points_layout = QtGui.QHBoxLayout()
        self.points_label = QtGui.QLabel(__("Points: "))
        self.point_x_label = QtGui.QLabel(__("X"))
        self.point_x_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][0]))
        self.point_y_label = QtGui.QLabel(__("Y"))
        self.point_y_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][1]))
        self.point_z_label = QtGui.QLabel(__("Z"))
        self.point_z_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][2]))

        self.points_layout.addWidget(self.points_label)
        self.points_layout.addWidget(self.point_x_label)
        self.points_layout.addWidget(self.point_x_line_edit)
        self.points_layout.addWidget(self.point_y_label)
        self.points_layout.addWidget(self.point_y_line_edit)
        self.points_layout.addWidget(self.point_z_label)
        self.points_layout.addWidget(self.point_z_line_edit)

        self.link_spheric_edit_layout.addLayout(self.points_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness"))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_spheric[4]))
        self.damping_label = QtGui.QLabel(__("Damping"))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_spheric[5]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_spheric_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_spheric_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_spheric_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_spheric_edit_layout)
        self.exec_()

    def on_cancel(self):
        ''' Link Spheric edit cancel button behaviour.'''
        self.reject()

    def on_save(self):
        ''' Link Spheric save button behaviour'''
        count = -1
        for link_spheric_value in self.data['link_spheric']:
            count += 1
            if link_spheric_value[0] == self.link_spheric_id:
                self.data['link_spheric'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_spheric'][count][2] = str(self.body_two_line_edit.currentText())
                self.data['link_spheric'][count][3] = [float(self.point_x_line_edit.text()),
                                                       float(self.point_y_line_edit.text()),
                                                       float(self.point_z_line_edit.text())]
                self.data['link_spheric'][count][4] = float(self.stiffness_line_edit.text())
                self.data['link_spheric'][count][5] = float(self.damping_line_edit.text())

        if self.data['link_spheric'][count][1] != "":
            LinkSphericEdit.accept(self)
        else:
            link_spheric_error_dialog = QtGui.QMessageBox()
            link_spheric_error_dialog.setWindowTitle(__("Error!"))
            link_spheric_error_dialog.setText(__("body 1 is necessary!"))
            link_spheric_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_spheric_error_dialog.exec_()
