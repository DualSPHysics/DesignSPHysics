#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics LinkPointLine Edit Dialog """


from PySide2 import QtWidgets

from mod.dataobjects.case import Case
from mod.tools.dialog_tools import error_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class LinkPointlineEdit(QtWidgets.QDialog):
    """ Defines Link pontline window dialog """

    def __init__(self, link_pointline_id, bodies_widgets, parent=None):
        super().__init__(parent=parent)

        self.case = Case.the()
        self.link_pointline_id = link_pointline_id

        # Title
        self.setWindowTitle(__("Link pointline configuration"))
        self.link_pointline_edit_layout = QtWidgets.QVBoxLayout()

        # Find the link pointline for which the button was pressed
        target_link_pointline = None

        for link_pointline in self.case.chrono.link_pointline:
            if link_pointline.id == self.link_pointline_id:
                target_link_pointline = link_pointline

        # This should not happen but if no link pointline is found with reference id, it spawns an error.
        if target_link_pointline is None:
            error_dialog("There was an error opnening the link pointline to edit")
            return

        # Elements that interact
        self.body_layout = QtWidgets.QHBoxLayout()
        self.body_one_label = QtWidgets.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtWidgets.QComboBox()
        if str(target_link_pointline.idbody1) != "":
            self.body_one_line_edit.insertItems(0, ["", str(target_link_pointline.idbody1)])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_pointline.idbody1)])
        for body in bodies_widgets:
            if body.object_check.isChecked() and body.object_name != str(target_link_pointline.idbody1):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addStretch(1)

        self.link_pointline_edit_layout.addLayout(self.body_layout)

        # Vector direction for sliding axis
        self.sliding_vector_layout = QtWidgets.QHBoxLayout()
        self.sliding_vector_label = QtWidgets.QLabel(__("Sliding Vector: "))
        self.sliding_vector_x_label = QtWidgets.QLabel(__("X"))
        self.sliding_vector_x_line_edit = ValueInput(value=target_link_pointline.slidingvector[0])
        self.sliding_vector_y_label = QtWidgets.QLabel(__("Y"))
        self.sliding_vector_y_line_edit = ValueInput(value=target_link_pointline.slidingvector[1])
        self.sliding_vector_z_label = QtWidgets.QLabel(__("Z"))
        self.sliding_vector_z_line_edit = ValueInput(value=target_link_pointline.slidingvector[2])

        self.sliding_vector_layout.addWidget(self.sliding_vector_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.sliding_vector_layout)

        # Point for rotation
        self.rotpoint_layout = QtWidgets.QHBoxLayout()
        self.rotpoint_label = QtWidgets.QLabel(__("Point for rotation: "))
        self.rotpoint_x_label = QtWidgets.QLabel(__("X"))
        self.rotpoint_x_line_edit = SizeInput(value=target_link_pointline.rotpoint[0])
        self.rotpoint_y_label = QtWidgets.QLabel(__("Y"))
        self.rotpoint_y_line_edit = SizeInput(value=target_link_pointline.rotpoint[1])
        self.rotpoint_z_label = QtWidgets.QLabel(__("Z"))
        self.rotpoint_z_line_edit = SizeInput(value=target_link_pointline.rotpoint[2])

        self.rotpoint_layout.addWidget(self.rotpoint_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_y_label)
        self.rotpoint_layout.addWidget(self.rotpoint_y_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_z_label)
        self.rotpoint_layout.addWidget(self.rotpoint_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotpoint_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtWidgets.QHBoxLayout()
        self.rotvector_label = QtWidgets.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtWidgets.QLabel(__("X"))
        self.rotvector_x_line_edit = ValueInput(value=target_link_pointline.rotvector[0])
        self.rotvector_y_label = QtWidgets.QLabel(__("Y"))
        self.rotvector_y_line_edit = ValueInput(value=target_link_pointline.rotvector[1])
        self.rotvector_z_label = QtWidgets.QLabel(__("Z"))
        self.rotvector_z_line_edit = ValueInput(value=target_link_pointline.rotvector[2])

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector_layout)

        # Second vector to avoid rotation
        self.rotvector2_layout = QtWidgets.QHBoxLayout()
        self.rotvector2_label = QtWidgets.QLabel(__("Second vector: "))
        self.rotvector2_x_label = QtWidgets.QLabel(__("X"))
        self.rotvector2_x_line_edit = ValueInput(value=target_link_pointline.rotvector2[0])
        self.rotvector2_y_label = QtWidgets.QLabel(__("Y"))
        self.rotvector2_y_line_edit = ValueInput(value=target_link_pointline.rotvector2[1])
        self.rotvector2_z_label = QtWidgets.QLabel(__("Z"))
        self.rotvector2_z_line_edit = ValueInput(value=target_link_pointline.rotvector2[2])

        self.rotvector2_layout.addWidget(self.rotvector2_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_y_label)
        self.rotvector2_layout.addWidget(self.rotvector2_y_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_z_label)
        self.rotvector2_layout.addWidget(self.rotvector2_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtWidgets.QHBoxLayout()
        self.torsion_damping_layout = QtWidgets.QHBoxLayout()
        self.stiffness_label = QtWidgets.QLabel(__("Stiffness (Nm/rad):"))
        self.stiffness_line_edit = ValueInput(value=target_link_pointline.stiffness)
        self.damping_label = QtWidgets.QLabel(__("Damping (Nms/rad):"))
        self.damping_line_edit = ValueInput(value=target_link_pointline.damping)

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_pointline_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_pointline_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtWidgets.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_pointline_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_pointline_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link pointline edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link pointline save button behaviour"""
        link_pointline = self.case.chrono.get_link_pointline_for_id(self.link_pointline_id)

        link_pointline.idbody1 = str(self.body_one_line_edit.currentText())
        link_pointline.slidingvector = [self.sliding_vector_x_line_edit.value(),self.sliding_vector_y_line_edit.value(),self.sliding_vector_z_line_edit.value()]
        link_pointline.rotpoint = [self.rotpoint_x_line_edit.value(),self.rotpoint_y_line_edit.value(),self.rotpoint_z_line_edit.value()]
        link_pointline.rotvector = [self.rotvector_x_line_edit.value(),self.rotvector_y_line_edit.value(),self.rotvector_z_line_edit.value()]
        link_pointline.rotvector2 = [self.rotvector2_x_line_edit.value(),self.rotvector2_y_line_edit.value(),self.rotvector2_z_line_edit.value()]
        link_pointline.stiffness = self.stiffness_line_edit.value()
        link_pointline.damping = self.damping_line_edit.value()

        if link_pointline.idbody1:
            LinkPointlineEdit.accept(self)
        else:
            error_dialog("You need to select an option for the body to use.")
