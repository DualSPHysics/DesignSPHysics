#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics FlowTool Box Edit Dialog."""

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.dialog_tools import error_dialog
from mod.gui_tools import get_icon

from mod.dataobjects.case import Case
from mod.dataobjects.flow_tool_box import FlowToolBox


class FlowToolBoxEditDialog(QtGui.QDialog):
    """ DesignSPHysics FlowTool Box Edit Dialog. """

    def __init__(self, box_id, parent=None):
        super().__init__(parent=parent)

        self.box_id = box_id

        self.box_edit_layout = QtGui.QVBoxLayout()

        # Find the box for which the button was pressed
        target_box = None

        for box in Case.the().flowtool_boxes:
            if box.id == self.box_id:
                target_box = box

        # This should not happen but if no box is found with reference id, it spawns an error.
        if target_box is None:
            error_dialog("There was an error opening the box to edit")
            return

        self.box_edit_name_layout = QtGui.QHBoxLayout()
        self.box_edit_name_label = QtGui.QLabel(__("Box Name"))
        self.box_edit_name_input = QtGui.QLineEdit(target_box.name)
        self.box_edit_name_layout.addWidget(self.box_edit_name_label)
        self.box_edit_name_layout.addWidget(self.box_edit_name_input)

        self.box_edit_description = QtGui.QLabel(__("Using multiple boxes with the same name will produce only one volume to measure.\n"
                                                    "Use that to create prisms and complex forms. "
                                                    "All points are specified in meters."))
        self.box_edit_description.setAlignment(QtCore.Qt.AlignCenter)

        # Reference image
        self.box_edit_image = QtGui.QLabel()
        self.box_edit_image.setPixmap(get_icon("flowtool_template.jpg", return_only_path=True))
        self.box_edit_image.setAlignment(QtCore.Qt.AlignCenter)

        # Point coords inputs
        self.box_edit_points_layout = QtGui.QVBoxLayout()

        self.box_edit_point_a_layout = QtGui.QHBoxLayout()
        self.box_edit_point_a_label = QtGui.QLabel(__("Point A (X, Y, Z)"))
        self.box_edit_point_a_x = QtGui.QLineEdit(str(target_box.point1[0]))
        self.box_edit_point_a_y = QtGui.QLineEdit(str(target_box.point1[1]))
        self.box_edit_point_a_z = QtGui.QLineEdit(str(target_box.point1[2]))
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_label)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_x)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_y)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_z)

        self.box_edit_point_b_layout = QtGui.QHBoxLayout()
        self.box_edit_point_b_label = QtGui.QLabel(__("Point B (X, Y, Z)"))
        self.box_edit_point_b_x = QtGui.QLineEdit(str(target_box.point2[0]))
        self.box_edit_point_b_y = QtGui.QLineEdit(str(target_box.point2[1]))
        self.box_edit_point_b_z = QtGui.QLineEdit(str(target_box.point2[2]))
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_label)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_x)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_y)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_z)

        self.box_edit_point_c_layout = QtGui.QHBoxLayout()
        self.box_edit_point_c_label = QtGui.QLabel(__("Point C (X, Y, Z)"))
        self.box_edit_point_c_x = QtGui.QLineEdit(str(target_box.point3[0]))
        self.box_edit_point_c_y = QtGui.QLineEdit(str(target_box.point3[1]))
        self.box_edit_point_c_z = QtGui.QLineEdit(str(target_box.point3[2]))
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_label)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_x)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_y)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_z)

        self.box_edit_point_d_layout = QtGui.QHBoxLayout()
        self.box_edit_point_d_label = QtGui.QLabel(__("Point D (X, Y, Z)"))
        self.box_edit_point_d_x = QtGui.QLineEdit(str(target_box.point4[0]))
        self.box_edit_point_d_y = QtGui.QLineEdit(str(target_box.point4[1]))
        self.box_edit_point_d_z = QtGui.QLineEdit(str(target_box.point4[2]))
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_label)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_x)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_y)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_z)

        self.box_edit_point_e_layout = QtGui.QHBoxLayout()
        self.box_edit_point_e_label = QtGui.QLabel(__("Point E (X, Y, Z)"))
        self.box_edit_point_e_x = QtGui.QLineEdit(str(target_box.point5[0]))
        self.box_edit_point_e_y = QtGui.QLineEdit(str(target_box.point5[1]))
        self.box_edit_point_e_z = QtGui.QLineEdit(str(target_box.point5[2]))
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_label)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_x)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_y)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_z)

        self.box_edit_point_f_layout = QtGui.QHBoxLayout()
        self.box_edit_point_f_label = QtGui.QLabel(__("Point F (X, Y, Z)"))
        self.box_edit_point_f_x = QtGui.QLineEdit(str(target_box.point6[0]))
        self.box_edit_point_f_y = QtGui.QLineEdit(str(target_box.point6[1]))
        self.box_edit_point_f_z = QtGui.QLineEdit(str(target_box.point6[2]))
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_label)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_x)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_y)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_z)

        self.box_edit_point_g_layout = QtGui.QHBoxLayout()
        self.box_edit_point_g_label = QtGui.QLabel(__("Point G (X, Y, Z)"))
        self.box_edit_point_g_x = QtGui.QLineEdit(str(target_box.point7[0]))
        self.box_edit_point_g_y = QtGui.QLineEdit(str(target_box.point7[1]))
        self.box_edit_point_g_z = QtGui.QLineEdit(str(target_box.point7[2]))
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_label)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_x)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_y)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_z)

        self.box_edit_point_h_layout = QtGui.QHBoxLayout()
        self.box_edit_point_h_label = QtGui.QLabel(__("Point H (X, Y, Z)"))
        self.box_edit_point_h_x = QtGui.QLineEdit(str(target_box.point8[0]))
        self.box_edit_point_h_y = QtGui.QLineEdit(str(target_box.point8[1]))
        self.box_edit_point_h_z = QtGui.QLineEdit(str(target_box.point8[2]))
        self.box_edit_point_h_layout.addWidget(self.box_edit_point_h_label)
        self.box_edit_point_h_layout.addWidget(self.box_edit_point_h_x)
        self.box_edit_point_h_layout.addWidget(self.box_edit_point_h_y)
        self.box_edit_point_h_layout.addWidget(self.box_edit_point_h_z)

        self.box_edit_points_layout.addLayout(self.box_edit_point_a_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_b_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_c_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_d_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_e_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_f_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_g_layout)
        self.box_edit_points_layout.addLayout(self.box_edit_point_h_layout)

        # Ok and cancel buttons
        self.box_edit_button_layout = QtGui.QHBoxLayout()
        self.box_edit_button_ok = QtGui.QPushButton(__("OK"))
        self.box_edit_button_cancel = QtGui.QPushButton(__("Cancel"))

        self.box_edit_button_layout.addStretch(1)
        self.box_edit_button_layout.addWidget(self.box_edit_button_ok)
        self.box_edit_button_layout.addWidget(self.box_edit_button_cancel)

        self.box_edit_layout.addLayout(self.box_edit_name_layout)
        self.box_edit_layout.addWidget(self.box_edit_description)
        self.box_edit_layout.addWidget(self.box_edit_image)
        self.box_edit_layout.addStretch(1)
        self.box_edit_layout.addLayout(self.box_edit_points_layout)
        self.box_edit_layout.addLayout(self.box_edit_button_layout)

        self.setLayout(self.box_edit_layout)

        self.box_edit_button_ok.clicked.connect(self.on_ok)
        self.box_edit_button_cancel.clicked.connect(self.on_cancel)

        self.exec_()

    def on_ok(self):
        """ FlowTool box edit ok behaviour."""
        box_to_edit: FlowToolBox = None

        for box in Case.the().flowtool_boxes:
            if box.id == self.box_id:
                box_to_edit = box
                break

        box_to_edit.name = str(self.box_edit_name_input.text())
        box_to_edit.point1 = [float(self.box_edit_point_a_x.text()), float(self.box_edit_point_a_y.text()), float(self.box_edit_point_a_z.text())]
        box_to_edit.point2 = [float(self.box_edit_point_b_x.text()), float(self.box_edit_point_b_y.text()), float(self.box_edit_point_b_z.text())]
        box_to_edit.point3 = [float(self.box_edit_point_c_x.text()), float(self.box_edit_point_c_y.text()), float(self.box_edit_point_c_z.text())]
        box_to_edit.point4 = [float(self.box_edit_point_d_x.text()), float(self.box_edit_point_d_y.text()), float(self.box_edit_point_d_z.text())]
        box_to_edit.point5 = [float(self.box_edit_point_e_x.text()), float(self.box_edit_point_e_y.text()), float(self.box_edit_point_e_z.text())]
        box_to_edit.point6 = [float(self.box_edit_point_f_x.text()), float(self.box_edit_point_f_y.text()), float(self.box_edit_point_f_z.text())]
        box_to_edit.point7 = [float(self.box_edit_point_g_x.text()), float(self.box_edit_point_g_y.text()), float(self.box_edit_point_g_z.text())]
        box_to_edit.point8 = [float(self.box_edit_point_h_x.text()), float(self.box_edit_point_h_y.text()), float(self.box_edit_point_h_z.text())]
        self.accept()

    def on_cancel(self):
        """ FlowTool box edit cancel button behaviour."""
        self.reject()
