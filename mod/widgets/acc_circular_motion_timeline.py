#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Accelerated Circular Motion Timeline widget'''

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.guiutils import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.acc_cir_motion import AccCirMotion


class AccCircularMotionTimeline(QtGui.QWidget):
    ''' An accelerated circular motion graphical representation for a table-based timeline '''

    changed = QtCore.Signal(int, AccCirMotion)
    deleted = QtCore.Signal(int, AccCirMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, acc_cir_motion):
        if not isinstance(acc_cir_motion, AccCirMotion):
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline with a wrong object")
        if acc_cir_motion is None:
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline without a motion object")
        super(AccCircularMotionTimeline, self).__init__()

        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = acc_cir_motion.parent_movement
        self.label = QtGui.QLabel("Accelerated \nCircular \nMotion ")
        self.label.setMinimumWidth(75)
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")

        self.reference_label = QtGui.QLabel("Ref (X, Y, Z): ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_x_input.setStyleSheet("width: 5px;")
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_y_input.setStyleSheet("width: 5px;")
        self.reference_z_input = QtGui.QLineEdit()
        self.reference_z_input.setStyleSheet("width: 5px;")

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            get_icon("down_arrow.png"), None)

        self.vel_layout.addWidget(self.velocity_label)
        self.vel_layout.addWidget(self.velocity_input)
        self.acc_layout.addWidget(self.acceleration_label)
        self.acc_layout.addWidget(self.acceleration_input)
        self.vel_and_acc_layout.addLayout(self.vel_layout)
        self.vel_and_acc_layout.addLayout(self.acc_layout)
        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.vel_and_acc_layout)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addWidget(self.reference_label)
        self.main_layout.addWidget(self.reference_x_input)
        self.main_layout.addWidget(self.reference_y_input)
        self.main_layout.addWidget(self.reference_z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_cir_motion)
        self._init_connections()

    def fill_values(self, acc_cir_motion):
        ''' Fills the widget values with the current data. '''
        self.x1_input.setText(str(acc_cir_motion.axis1[0]))
        self.y1_input.setText(str(acc_cir_motion.axis1[1]))
        self.z1_input.setText(str(acc_cir_motion.axis1[2]))
        self.x2_input.setText(str(acc_cir_motion.axis2[0]))
        self.y2_input.setText(str(acc_cir_motion.axis2[1]))
        self.z2_input.setText(str(acc_cir_motion.axis2[2]))
        self.reference_x_input.setText(str(acc_cir_motion.reference[0]))
        self.reference_y_input.setText(str(acc_cir_motion.reference[1]))
        self.reference_z_input.setText(str(acc_cir_motion.reference[2]))
        self.velocity_input.setText(str(acc_cir_motion.ang_vel))
        self.acceleration_input.setText(str(acc_cir_motion.ang_acc))
        self.time_input.setText(str(acc_cir_motion.duration))

    def _init_connections(self):
        ''' Setups widget connections with the different functions. '''
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.reference_x_input.textChanged.connect(self.on_change)
        self.reference_y_input.textChanged.connect(self.on_change)
        self.reference_z_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.velocity_input.textChanged.connect(self.on_change)
        self.acceleration_input.textChanged.connect(self.on_change)
        self.time_input.textChanged.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def disable_order_up_button(self):
        ''' Disables the up button to reorder the widget. '''
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        self.order_up.emit(self.index)

    def on_order_down(self):
        self.order_down.emit(self.index)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return AccCirMotion(
            ang_vel=float(self.velocity_input.text()),
            ang_acc=float(self.acceleration_input.text()),
            reference=[float(self.reference_x_input.text()),
                       float(self.reference_y_input.text()),
                       float(self.reference_z_input.text())],
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.reference_x_input.text()) is 0:
            self.reference_x_input.setText("0")
        if len(self.reference_y_input.text()) is 0:
            self.reference_y_input.setText("0")
        if len(self.reference_z_input.text()) is 0:
            self.reference_z_input.setText("0")
        if len(self.velocity_input.text()) is 0:
            self.velocity_input.setText("0")
        if len(self.acceleration_input.text()) is 0:
            self.acceleration_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.reference_x_input.setText(
            self.reference_x_input.text().replace(",", "."))
        self.reference_y_input.setText(
            self.reference_y_input.text().replace(",", "."))
        self.reference_z_input.setText(
            self.reference_z_input.text().replace(",", "."))
        self.velocity_input.setText(
            self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(
            self.acceleration_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))
