#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics LinkPointLine Edit Dialog '''

from PySide import QtGui
from mod.translation_tools import __
from mod.dialog_tools import error_dialog

# FIXME: Change data references for refactored Case data
class LinkPointlineEdit(QtGui.QDialog):
    ''' Defines Link pontline window dialog '''

    def __init__(self, link_pointline_id):
        super(LinkPointlineEdit, self).__init__()

        self.link_pointline_id = link_pointline_id

        # Title
        self.setWindowTitle(__("Link pointline configuration"))
        self.link_pointline_edit_layout = QtGui.QVBoxLayout()

        # Find the link pointline for which the button was pressed
        target_link_pointline = None

        for link_pointline in self.data['link_pointline']:
            if link_pointline[0] == self.link_pointline_id:
                target_link_pointline = link_pointline

        # This should not happen but if no link pointline is found with reference id, it spawns an error.
        if target_link_pointline is None:
            error_dialog("There was an error opnening the link pointline to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        if str(target_link_pointline[1]) != '':
            self.body_one_line_edit.insertItems(0, ['', str(target_link_pointline[1])])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_pointline[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_pointline[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addStretch(1)

        self.link_pointline_edit_layout.addLayout(self.body_layout)

        # Vector direction for sliding axis
        self.sliding_vector_layout = QtGui.QHBoxLayout()
        self.sliding_vector_label = QtGui.QLabel(__("Sliding Vector: "))
        self.sliding_vector_x_label = QtGui.QLabel(__("X"))
        self.sliding_vector_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][0]))
        self.sliding_vector_y_label = QtGui.QLabel(__("Y"))
        self.sliding_vector_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][1]))
        self.sliding_vector_z_label = QtGui.QLabel(__("Z"))
        self.sliding_vector_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][2]))

        self.sliding_vector_layout.addWidget(self.sliding_vector_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.sliding_vector_layout)

        # Point for rotation
        self.rotpoint_layout = QtGui.QHBoxLayout()
        self.rotpoint_label = QtGui.QLabel(__("Point for rotation: "))
        self.rotpoint_x_label = QtGui.QLabel(__("X"))
        self.rotpoint_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][0]))
        self.rotpoint_y_label = QtGui.QLabel(__("Y"))
        self.rotpoint_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][1]))
        self.rotpoint_z_label = QtGui.QLabel(__("Z"))
        self.rotpoint_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][2]))

        self.rotpoint_layout.addWidget(self.rotpoint_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_y_label)
        self.rotpoint_layout.addWidget(self.rotpoint_y_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_z_label)
        self.rotpoint_layout.addWidget(self.rotpoint_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotpoint_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtGui.QHBoxLayout()
        self.rotvector_label = QtGui.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtGui.QLabel(__("X"))
        self.rotvector_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][0]))
        self.rotvector_y_label = QtGui.QLabel(__("Y"))
        self.rotvector_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][1]))
        self.rotvector_z_label = QtGui.QLabel(__("Z"))
        self.rotvector_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][2]))

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector_layout)

        # Second vector to avoid rotation
        self.rotvector2_layout = QtGui.QHBoxLayout()
        self.rotvector2_label = QtGui.QLabel(__("Second vector: "))
        self.rotvector2_x_label = QtGui.QLabel(__("X"))
        self.rotvector2_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][0]))
        self.rotvector2_y_label = QtGui.QLabel(__("Y"))
        self.rotvector2_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][1]))
        self.rotvector2_z_label = QtGui.QLabel(__("Z"))
        self.rotvector2_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][2]))

        self.rotvector2_layout.addWidget(self.rotvector2_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_y_label)
        self.rotvector2_layout.addWidget(self.rotvector2_y_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_z_label)
        self.rotvector2_layout.addWidget(self.rotvector2_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness"))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_pointline[6]))
        self.damping_label = QtGui.QLabel(__("Damping"))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_pointline[7]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_pointline_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_pointline_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_pointline_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_pointline_edit_layout)
        self.exec_()

    def on_cancel(self):
        ''' Link pointline edit cancel button behaviour.'''
        self.reject()

    def on_save(self):
        ''' Link pointline save button behaviour'''
        count = -1
        for link_pointline_value in self.data['link_pointline']:
            count += 1
            if link_pointline_value[0] == self.link_pointline_id:
                self.data['link_pointline'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_pointline'][count][2] = [float(self.sliding_vector_x_line_edit.text()),
                                                         float(self.sliding_vector_y_line_edit.text()),
                                                         float(self.sliding_vector_z_line_edit.text())]
                self.data['link_pointline'][count][3] = [float(self.rotpoint_x_line_edit.text()),
                                                         float(self.rotpoint_y_line_edit.text()),
                                                         float(self.rotpoint_z_line_edit.text())]
                self.data['link_pointline'][count][4] = [float(self.rotvector_x_line_edit.text()),
                                                         float(self.rotvector_y_line_edit.text()),
                                                         float(self.rotvector_z_line_edit.text())]
                self.data['link_pointline'][count][5] = [float(self.rotvector2_x_line_edit.text()),
                                                         float(self.rotvector2_y_line_edit.text()),
                                                         float(self.rotvector2_z_line_edit.text())]
                self.data['link_pointline'][count][6] = float(self.stiffness_line_edit.text())
                self.data['link_pointline'][count][7] = float(self.damping_line_edit.text())

        if self.data['link_pointline'][count][1] != "":
            LinkPointlineEdit.accept(self)
        else:
            link_pointline_error_dialog = QtGui.QMessageBox()
            link_pointline_error_dialog.setWindowTitle(__("Error!"))
            link_pointline_error_dialog.setText(__("body 1 is necesary!"))
            link_pointline_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_pointline_error_dialog.exec_()
