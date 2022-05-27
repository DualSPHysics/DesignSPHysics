#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rectilinear Sinusoidal Motion Timeline """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.motion.rect_sinu_motion import RectSinuMotion

from mod.functions import make_float


class RectSinuMotionTimeline(QtGui.QWidget):
    """ A sinusoidal rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectSinuMotion)
    deleted = QtCore.Signal(int, RectSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rect_sinu_motion, parent=None):
        if not isinstance(rect_sinu_motion, RectSinuMotion):
            raise TypeError("You tried to spawn an accelerated circular motion widget in the timeline with a wrong object")
        if rect_sinu_motion is None:
            raise TypeError("You tried to spawn an accelerated circular motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtGui.QLabel("Sinusoidal \nRectilinear \nMotion ")
        self.label.setMinimumWidth(75)
        self.freq_amp_layout = QtGui.QVBoxLayout()
        self.freq_amp_first_row_layout = QtGui.QHBoxLayout()
        self.freq_amp_second_row_layout = QtGui.QHBoxLayout()
        self.freq_label = QtGui.QLabel("Freq (X, Y, Z): ")
        self.amp_label = QtGui.QLabel("Amp (X, Y, Z): ")
        self.freq_x_input = QtGui.QLineEdit()
        self.freq_y_input = QtGui.QLineEdit()
        self.freq_z_input = QtGui.QLineEdit()
        self.amp_x_input = QtGui.QLineEdit()
        self.amp_y_input = QtGui.QLineEdit()
        self.amp_z_input = QtGui.QLineEdit()

        self.phase_label = QtGui.QLabel("Phase (X, Y, Z): ")
        self.phase_x_input = QtGui.QLineEdit()
        self.phase_y_input = QtGui.QLineEdit()
        self.phase_z_input = QtGui.QLineEdit()

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
        self.freq_amp_first_row_layout.addWidget(self.freq_label)
        self.freq_amp_first_row_layout.addWidget(self.freq_x_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_y_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_z_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_label)
        self.freq_amp_second_row_layout.addWidget(self.amp_x_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_y_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_z_input)
        self.freq_amp_layout.addLayout(self.freq_amp_first_row_layout)
        self.freq_amp_layout.addLayout(self.freq_amp_second_row_layout)
        self.main_layout.addLayout(self.freq_amp_layout)
        self.main_layout.addWidget(self.phase_label)
        self.main_layout.addWidget(self.phase_x_input)
        self.main_layout.addWidget(self.phase_y_input)
        self.main_layout.addWidget(self.phase_z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rect_sinu_motion)
        self._init_connections()

    def fill_values(self, rect_sinu_motion):
        """ Fills the values from the data structure onto the widget. """
        self.freq_x_input.setText(str(rect_sinu_motion.freq[0]))
        self.freq_y_input.setText(str(rect_sinu_motion.freq[1]))
        self.freq_z_input.setText(str(rect_sinu_motion.freq[2]))
        self.amp_x_input.setText(str(rect_sinu_motion.ampl[0]))
        self.amp_y_input.setText(str(rect_sinu_motion.ampl[1]))
        self.amp_z_input.setText(str(rect_sinu_motion.ampl[2]))
        self.phase_x_input.setText(str(rect_sinu_motion.phase[0]))
        self.phase_y_input.setText(str(rect_sinu_motion.phase[1]))
        self.phase_z_input.setText(str(rect_sinu_motion.phase[2]))
        self.time_input.setText(str(rect_sinu_motion.duration))

    def _init_connections(self):
        self.freq_x_input.textChanged.connect(self.on_change)
        self.freq_y_input.textChanged.connect(self.on_change)
        self.freq_z_input.textChanged.connect(self.on_change)
        self.phase_x_input.textChanged.connect(self.on_change)
        self.phase_y_input.textChanged.connect(self.on_change)
        self.phase_z_input.textChanged.connect(self.on_change)
        self.amp_x_input.textChanged.connect(self.on_change)
        self.amp_y_input.textChanged.connect(self.on_change)
        self.amp_z_input.textChanged.connect(self.on_change)
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
        """ Reacts to any input changes, sanitizes it and fires a signal with the corresponding data object. """
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs a RectSinuMotion object from the values in the widget. """
        return RectSinuMotion(
            phase=[make_float(self.phase_x_input.text()),
                   make_float(self.phase_y_input.text()),
                   make_float(self.phase_z_input.text())],
            freq=[make_float(self.freq_x_input.text()),
                  make_float(self.freq_y_input.text()),
                  make_float(self.freq_z_input.text())],
            ampl=[make_float(self.amp_x_input.text()),
                  make_float(self.amp_y_input.text()),
                  make_float(self.amp_z_input.text())],
            duration=make_float(self.time_input.text()))

    def on_delete(self):
        """ Deletes the currently represented object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if not self.freq_x_input.text():
            self.freq_x_input.setText("0")
        if not self.freq_y_input.text():
            self.freq_y_input.setText("0")
        if not self.freq_z_input.text():
            self.freq_z_input.setText("0")
        if not self.amp_x_input.text():
            self.amp_x_input.setText("0")
        if not self.amp_y_input.text():
            self.amp_y_input.setText("0")
        if not self.amp_z_input.text():
            self.amp_z_input.setText("0")
        if not self.phase_x_input.text():
            self.phase_x_input.setText("0")
        if not self.phase_y_input.text():
            self.phase_y_input.setText("0")
        if not self.phase_z_input.text():
            self.phase_z_input.setText("0")
        if not self.time_input.text():
            self.time_input.setText("0")

        self.freq_x_input.setText(self.freq_x_input.text().replace(",", "."))
        self.freq_y_input.setText(self.freq_y_input.text().replace(",", "."))
        self.freq_z_input.setText(self.freq_z_input.text().replace(",", "."))
        self.amp_x_input.setText(self.amp_x_input.text().replace(",", "."))
        self.amp_y_input.setText(self.amp_y_input.text().replace(",", "."))
        self.amp_z_input.setText(self.amp_z_input.text().replace(",", "."))
        self.phase_x_input.setText(self.phase_x_input.text().replace(",", "."))
        self.phase_y_input.setText(self.phase_y_input.text().replace(",", "."))
        self.phase_z_input.setText(self.phase_z_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))
