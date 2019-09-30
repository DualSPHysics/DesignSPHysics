#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics FlowTool Box Edit Dialog.'''

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.dialog_tools import error_dialog
from mod.gui_tools import get_icon

# FIXME: Replace data occurrences for new Case structure
data = {}


class FlowToolBoxEditDialog(QtGui.QDialog):
    ''' DesignSPHysics FlowTool Box Edit Dialog. '''

    def __init__(self, box_id):
        super().__init__()

        self.box_id = box_id

        self.box_edit_layout = QtGui.QVBoxLayout()

        # Find the box for which the button was pressed
        target_box = None

        for box in data['flowtool_boxes']:
            if box[0] == self.box_id:
                target_box = box

        # This should not happen but if no box is found with reference id, it spawns an error.
        if target_box is None:
            error_dialog("There was an error opening the box to edit")
            return

        self.box_edit_name_layout = QtGui.QHBoxLayout()
        self.box_edit_name_label = QtGui.QLabel(__("Box Name"))
        self.box_edit_name_input = QtGui.QLineEdit(str(target_box[1]))
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
        self.box_edit_point_a_x = QtGui.QLineEdit(str(target_box[2][0]))
        self.box_edit_point_a_y = QtGui.QLineEdit(str(target_box[2][1]))
        self.box_edit_point_a_z = QtGui.QLineEdit(str(target_box[2][2]))
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_label)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_x)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_y)
        self.box_edit_point_a_layout.addWidget(self.box_edit_point_a_z)

        self.box_edit_point_b_layout = QtGui.QHBoxLayout()
        self.box_edit_point_b_label = QtGui.QLabel(__("Point B (X, Y, Z)"))
        self.box_edit_point_b_x = QtGui.QLineEdit(str(target_box[3][0]))
        self.box_edit_point_b_y = QtGui.QLineEdit(str(target_box[3][1]))
        self.box_edit_point_b_z = QtGui.QLineEdit(str(target_box[3][2]))
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_label)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_x)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_y)
        self.box_edit_point_b_layout.addWidget(self.box_edit_point_b_z)

        self.box_edit_point_c_layout = QtGui.QHBoxLayout()
        self.box_edit_point_c_label = QtGui.QLabel(__("Point C (X, Y, Z)"))
        self.box_edit_point_c_x = QtGui.QLineEdit(str(target_box[4][0]))
        self.box_edit_point_c_y = QtGui.QLineEdit(str(target_box[4][1]))
        self.box_edit_point_c_z = QtGui.QLineEdit(str(target_box[4][2]))
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_label)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_x)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_y)
        self.box_edit_point_c_layout.addWidget(self.box_edit_point_c_z)

        self.box_edit_point_d_layout = QtGui.QHBoxLayout()
        self.box_edit_point_d_label = QtGui.QLabel(__("Point D (X, Y, Z)"))
        self.box_edit_point_d_x = QtGui.QLineEdit(str(target_box[5][0]))
        self.box_edit_point_d_y = QtGui.QLineEdit(str(target_box[5][1]))
        self.box_edit_point_d_z = QtGui.QLineEdit(str(target_box[5][2]))
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_label)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_x)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_y)
        self.box_edit_point_d_layout.addWidget(self.box_edit_point_d_z)

        self.box_edit_point_e_layout = QtGui.QHBoxLayout()
        self.box_edit_point_e_label = QtGui.QLabel(__("Point E (X, Y, Z)"))
        self.box_edit_point_e_x = QtGui.QLineEdit(str(target_box[6][0]))
        self.box_edit_point_e_y = QtGui.QLineEdit(str(target_box[6][1]))
        self.box_edit_point_e_z = QtGui.QLineEdit(str(target_box[6][2]))
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_label)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_x)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_y)
        self.box_edit_point_e_layout.addWidget(self.box_edit_point_e_z)

        self.box_edit_point_f_layout = QtGui.QHBoxLayout()
        self.box_edit_point_f_label = QtGui.QLabel(__("Point F (X, Y, Z)"))
        self.box_edit_point_f_x = QtGui.QLineEdit(str(target_box[7][0]))
        self.box_edit_point_f_y = QtGui.QLineEdit(str(target_box[7][1]))
        self.box_edit_point_f_z = QtGui.QLineEdit(str(target_box[7][2]))
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_label)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_x)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_y)
        self.box_edit_point_f_layout.addWidget(self.box_edit_point_f_z)

        self.box_edit_point_g_layout = QtGui.QHBoxLayout()
        self.box_edit_point_g_label = QtGui.QLabel(__("Point G (X, Y, Z)"))
        self.box_edit_point_g_x = QtGui.QLineEdit(str(target_box[8][0]))
        self.box_edit_point_g_y = QtGui.QLineEdit(str(target_box[8][1]))
        self.box_edit_point_g_z = QtGui.QLineEdit(str(target_box[8][2]))
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_label)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_x)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_y)
        self.box_edit_point_g_layout.addWidget(self.box_edit_point_g_z)

        self.box_edit_point_h_layout = QtGui.QHBoxLayout()
        self.box_edit_point_h_label = QtGui.QLabel(__("Point H (X, Y, Z)"))
        self.box_edit_point_h_x = QtGui.QLineEdit(str(self.target_box[9][0]))
        self.box_edit_point_h_y = QtGui.QLineEdit(str(self.target_box[9][1]))
        self.box_edit_point_h_z = QtGui.QLineEdit(str(self.target_box[9][2]))
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

        self.self.setLayout(self.box_edit_layout)

        self.box_edit_button_ok.clicked.connect(self.on_ok)
        self.box_edit_button_cancel.clicked.connect(self.on_cancel)

        self.exec_()

    def on_ok(self):
        ''' FlowTool box edit ok behaviour.'''
        box_to_edit_index = -1

        for box_index, box_value in enumerate(data['flowtool_boxes']):
            if box_value[0] == self.box_id:
                box_to_edit_index = box_index

        data['flowtool_boxes'][box_to_edit_index][1] = str(self.box_edit_name_input.text())
        data['flowtool_boxes'][box_to_edit_index][2] = [float(self.box_edit_point_a_x.text()),
                                                        float(self.box_edit_point_a_y.text()),
                                                        float(self.box_edit_point_a_z.text())]
        data['flowtool_boxes'][box_to_edit_index][3] = [float(self.box_edit_point_b_x.text()),
                                                        float(self.box_edit_point_b_y.text()),
                                                        float(self.box_edit_point_b_z.text())]
        data['flowtool_boxes'][box_to_edit_index][4] = [float(self.box_edit_point_c_x.text()),
                                                        float(self.box_edit_point_c_y.text()),
                                                        float(self.box_edit_point_c_z.text())]
        data['flowtool_boxes'][box_to_edit_index][5] = [float(self.box_edit_point_d_x.text()),
                                                        float(self.box_edit_point_d_y.text()),
                                                        float(self.box_edit_point_d_z.text())]
        data['flowtool_boxes'][box_to_edit_index][6] = [float(self.box_edit_point_e_x.text()),
                                                        float(self.box_edit_point_e_y.text()),
                                                        float(self.box_edit_point_e_z.text())]
        data['flowtool_boxes'][box_to_edit_index][7] = [float(self.box_edit_point_f_x.text()),
                                                        float(self.box_edit_point_f_y.text()),
                                                        float(self.box_edit_point_f_z.text())]
        data['flowtool_boxes'][box_to_edit_index][8] = [float(self.box_edit_point_g_x.text()),
                                                        float(self.box_edit_point_g_y.text()),
                                                        float(self.box_edit_point_g_z.text())]
        data['flowtool_boxes'][box_to_edit_index][9] = [float(self.box_edit_point_h_x.text()),
                                                        float(self.box_edit_point_h_y.text()),
                                                        float(self.box_edit_point_h_z.text())]
        self.accept()

    def on_cancel(self):
        ''' FlowTool box edit cancel button behaviour.'''
        self.reject()
