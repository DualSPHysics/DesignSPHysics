#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Sinusoidal Circular Motion widget."""

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.motion.cir_sinu_motion import CirSinuMotion

from mod.functions import make_float

class CirSinuMotionTimeline(QtGui.QWidget):
    """ A sinusoidal circular motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, CirSinuMotion)
    deleted = QtCore.Signal(int, CirSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, cir_sinu_motion, parent=None):
        if not isinstance(cir_sinu_motion, CirSinuMotion):
            raise TypeError("You tried to spawn a sinusoidal circular "
                            "motion widget in the timeline with a wrong object")
        if cir_sinu_motion is None:
            raise TypeError("You tried to spawn a sinusoidal circular "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtGui.QLabel("Sinusoidal \nCircular \nMotion ")
        self.label.setMinimumWidth(75)
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.y1_input = QtGui.QLineEdit()
        self.z1_input = QtGui.QLineEdit()
        self.x2_input = QtGui.QLineEdit()
        self.y2_input = QtGui.QLineEdit()
        self.z2_input = QtGui.QLineEdit()

        self.ref_layout = QtGui.QVBoxLayout()
        self.ref_first_row = QtGui.QHBoxLayout()
        self.ref_second_row = QtGui.QHBoxLayout()
        self.freq_label = QtGui.QLabel("Freq ")
        self.freq_input = QtGui.QLineEdit()

        self.ampl_label = QtGui.QLabel("Ampl ")
        self.ampl_input = QtGui.QLineEdit()

        self.phase_label = QtGui.QLabel("Phase ")
        self.phase_input = QtGui.QLineEdit()

        self.reference_label = QtGui.QLabel("Ref (X, Y, Z): ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_z_input = QtGui.QLineEdit()

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.delete_button = QtGui.QPushButton(
            get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
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

        self.ref_first_row.addWidget(self.freq_label)
        self.ref_first_row.addWidget(self.freq_input)
        self.ref_first_row.addWidget(self.ampl_label)
        self.ref_first_row.addWidget(self.ampl_input)
        self.ref_first_row.addWidget(self.phase_label)
        self.ref_first_row.addWidget(self.phase_input)

        self.ref_second_row.addWidget(self.reference_label)
        self.ref_second_row.addWidget(self.reference_x_input)
        self.ref_second_row.addWidget(self.reference_y_input)
        self.ref_second_row.addWidget(self.reference_z_input)

        self.ref_layout.addLayout(self.ref_first_row)
        self.ref_layout.addLayout(self.ref_second_row)

        self.main_layout.addLayout(self.ref_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(cir_sinu_motion)
        self._init_connections()

    def fill_values(self, cir_sinu_motion):
        """ Fills the values from the data structure onto the widget. """
        self.x1_input.setText(str(cir_sinu_motion.axis1[0]))
        self.y1_input.setText(str(cir_sinu_motion.axis1[1]))
        self.z1_input.setText(str(cir_sinu_motion.axis1[2]))
        self.x2_input.setText(str(cir_sinu_motion.axis2[0]))
        self.y2_input.setText(str(cir_sinu_motion.axis2[1]))
        self.z2_input.setText(str(cir_sinu_motion.axis2[2]))
        self.reference_x_input.setText(str(cir_sinu_motion.reference[0]))
        self.reference_y_input.setText(str(cir_sinu_motion.reference[1]))
        self.reference_z_input.setText(str(cir_sinu_motion.reference[2]))
        self.freq_input.setText(str(cir_sinu_motion.freq))
        self.ampl_input.setText(str(cir_sinu_motion.ampl))
        self.phase_input.setText(str(cir_sinu_motion.phase))
        self.time_input.setText(str(cir_sinu_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.reference_x_input.textChanged.connect(self.on_change)
        self.reference_y_input.textChanged.connect(self.on_change)
        self.reference_z_input.textChanged.connect(self.on_change)
        self.freq_input.textChanged.connect(self.on_change)
        self.ampl_input.textChanged.connect(self.on_change)
        self.phase_input.textChanged.connect(self.on_change)
        self.time_input.textChanged.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def disable_order_up_button(self):
        """ Disables the order up button. """
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        """ Disables the order down button. """
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        """ Reacts to the order up button being pressed. """
        self.order_up.emit(self.index)

    def on_order_down(self):
        """ Reacts to the order down button being pressed. """
        self.order_down.emit(self.index)

    def on_change(self):
        """ Reacts to any change made sanitizing it and firing a signal with the appropriate data object. """
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs a new CirSinuMotion from the data on the widget. """
        return CirSinuMotion(
            axis1=[make_float(self.x1_input.text()),
                   make_float(self.y1_input.text()),
                   make_float(self.z1_input.text())],
            axis2=[make_float(self.x2_input.text()),
                   make_float(self.y2_input.text()),
                   make_float(self.z2_input.text())],
            reference=[make_float(self.reference_x_input.text()),
                       make_float(self.reference_y_input.text()),
                       make_float(self.reference_z_input.text())],
            duration=make_float(self.time_input.text()), freq=make_float(self.freq_input.text()),
            ampl=make_float(self.ampl_input.text()), phase=make_float(self.phase_input.text()))

    def on_delete(self):
        """ Deletes the currenlty represented motion object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if self.x1_input.text():
            self.x1_input.setText("0")
        if self.y1_input.text():
            self.y1_input.setText("0")
        if self.z1_input.text():
            self.z1_input.setText("0")
        if self.x2_input.text():
            self.x2_input.setText("0")
        if self.y2_input.text():
            self.y2_input.setText("0")
        if self.z2_input.text():
            self.z2_input.setText("0")
        if self.reference_x_input.text():
            self.reference_x_input.setText("0")
        if self.reference_y_input.text():
            self.reference_y_input.setText("0")
        if self.reference_z_input.text():
            self.reference_z_input.setText("0")
        if self.freq_input.text():
            self.freq_input.setText("0")
        if self.ampl_input.text():
            self.ampl_input.setText("0")
        if self.phase_input.text():
            self.phase_input.setText("0")
        if self.time_input.text():
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
        self.freq_input.setText(self.freq_input.text().replace(",", "."))
        self.ampl_input.setText(self.ampl_input.text().replace(",", "."))
        self.phase_input.setText(self.phase_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))
