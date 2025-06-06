#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Link Pulley Edit Dialog """


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import error_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class LinkPulleyEdit(QtWidgets.QDialog):
    """ Defines Link pulley window dialog """

    def __init__(self, link_pulley_id, bodies_widgets, parent=None):
        super().__init__(parent=parent)

        self.link_pulley_id = link_pulley_id
        self.case = Case.the()

        # Title
        self.setWindowTitle(__("Link pulley configuration"))
        self.link_pulley_edit_layout = QtWidgets.QVBoxLayout()

        # Find the link pulley for which the button was pressed
        target_link_pulley = None

        for link_pulley in self.case.chrono.link_pulley:
            if link_pulley.id == self.link_pulley_id:
                target_link_pulley = link_pulley

        # This should not happen but if no link pulley is found with reference id, it spawns an error.
        if target_link_pulley is None:
            error_dialog("There was an error opnening the link pulley to edit")
            return

        # Elements that interact
        self.body_layout = QtWidgets.QHBoxLayout()
        self.body_one_label = QtWidgets.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtWidgets.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_pulley.idbody1)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_pulley.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtWidgets.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtWidgets.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_pulley.idbody2)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_pulley.idbody2):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtWidgets.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_pulley_edit_layout.addLayout(self.body_layout)

        # Points for rotation
        self.rotpoints_layout = QtWidgets.QHBoxLayout()
        self.rotpoints_label = QtWidgets.QLabel(__("Points for rotation: "))
        self.rotpoints_x_label = QtWidgets.QLabel(__("X"))
        self.rotpoints_x_line_edit = SizeInput(value=(target_link_pulley.rotpoint[0]))
        self.rotpoints_y_label = QtWidgets.QLabel(__("Y"))
        self.rotpoints_y_line_edit = SizeInput(value=(target_link_pulley.rotpoint[1]))
        self.rotpoints_z_label = QtWidgets.QLabel(__("Z"))
        self.rotpoints_z_line_edit = SizeInput(value=(target_link_pulley.rotpoint[2]))

        self.rotpoints_layout.addWidget(self.rotpoints_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_y_label)
        self.rotpoints_layout.addWidget(self.rotpoints_y_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_z_label)
        self.rotpoints_layout.addWidget(self.rotpoints_z_line_edit)

        self.link_pulley_edit_layout.addLayout(self.rotpoints_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtWidgets.QHBoxLayout()
        self.rotvector_label = QtWidgets.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtWidgets.QLabel(__("X"))
        self.rotvector_x_line_edit = ValueInput(value=(target_link_pulley.rotvector[0]))
        self.rotvector_y_label = QtWidgets.QLabel(__("Y"))
        self.rotvector_y_line_edit = ValueInput(value=(target_link_pulley.rotvector[1]))
        self.rotvector_z_label = QtWidgets.QLabel(__("Z"))
        self.rotvector_z_line_edit = ValueInput(value=(target_link_pulley.rotvector[2]))

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_pulley_edit_layout.addLayout(self.rotvector_layout)

        # Torsion options
        self.torsion_radius_layout = QtWidgets.QHBoxLayout()
        self.torsion_radius2_layout = QtWidgets.QHBoxLayout()
        self.radius_label = QtWidgets.QLabel(__("Radius: "))
        self.radius_line_edit = SizeInput(value=(target_link_pulley.radius))
        self.radius2_label = QtWidgets.QLabel(__("Radius 2: "))
        self.radius2_line_edit = SizeInput(value=(target_link_pulley.radius2))

        self.torsion_radius_layout.addWidget(self.radius_label)
        self.torsion_radius_layout.addWidget(self.radius_line_edit)
        self.torsion_radius2_layout.addWidget(self.radius2_label)
        self.torsion_radius2_layout.addWidget(self.radius2_line_edit)

        self.link_pulley_edit_layout.addLayout(self.torsion_radius_layout)
        self.link_pulley_edit_layout.addLayout(self.torsion_radius2_layout)

        # Buttons
        self.ok_button = QtWidgets.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_pulley_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_pulley_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link pulley edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link pulley save button behaviour"""
        link_pulley = self.case.chrono.get_link_pulley_for_id(self.link_pulley_id)
        link_pulley.idbody1 = str(self.body_one_line_edit.currentText())
        link_pulley.idbody2 = str(self.body_two_line_edit.currentText())
        link_pulley.rotpoint = [self.rotpoints_x_line_edit.value(),self.rotpoints_y_line_edit.value(),self.rotpoints_z_line_edit.value()]
        link_pulley.rotvector = [self.rotvector_x_line_edit.value(),self.rotvector_y_line_edit.value(),self.rotvector_z_line_edit.value()]
        link_pulley.radius = self.radius_line_edit.value()
        link_pulley.radius2 = self.radius2_line_edit.value()

        if link_pulley.idbody1 and link_pulley.idbody2:
            LinkPulleyEdit.accept(self)
        else:
            error_dialog("You need to select an option for each one of the bodies.")
