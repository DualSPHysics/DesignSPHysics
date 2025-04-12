#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics """

# from PySide import QtCore, QtGui
from PySide6 import QtCore, QtWidgets

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.stdout_tools import debug

from mod.dataobjects.case import Case
from mod.dataobjects.motion.rotation_file_gen import RotationFileGen

from mod.functions import make_float


class RotationFileMotionTimeline(QtWidgets.QWidget):
    """ A rotation file motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, RotationFileGen)

    def __init__(self, rot_file_gen, project_folder_path, parent=None):
        if not isinstance(rot_file_gen, RotationFileGen):
            raise TypeError("You tried to spawn a rotation file generator "
                            "motion widget in the timeline with a wrong object")
        if rot_file_gen is None:
            raise TypeError("You tried to spawn a rotation file generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(__("Rotation file movement"))

        self.duration_label = QtWidgets.QLabel(__("Duration (s): "))
        self.duration_input = QtWidgets.QLineEdit()

        self.filename_label = QtWidgets.QLabel(__("File name: "))
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_browse = QtWidgets.QPushButton(__("Browse"))

        self.anglesunits_label = QtWidgets.QLabel(__("Angle Units: "))
        self.anglesunits_selector = QtWidgets.QComboBox()
        self.anglesunits_selector.insertItems(
            0, [__("Degrees"), __("Radians")])

        self.axisp1x_label = QtWidgets.QLabel(__("Axis 1 X: "))
        self.axisp1x_input = QtWidgets.QLineEdit()

        self.axisp1y_label = QtWidgets.QLabel(__("Axis 1 Y: "))
        self.axisp1y_input = QtWidgets.QLineEdit()

        self.axisp1z_label = QtWidgets.QLabel(__("Axis 1 Z: "))
        self.axisp1z_input = QtWidgets.QLineEdit()

        self.axisp2x_label = QtWidgets.QLabel(__("Axis 2 X: "))
        self.axisp2x_input = QtWidgets.QLineEdit()

        self.axisp2y_label = QtWidgets.QLabel(__("Axis 2 Y: "))
        self.axisp2y_input = QtWidgets.QLineEdit()

        self.axisp2z_label = QtWidgets.QLabel(__("Axis 2 Z: "))
        self.axisp2z_input = QtWidgets.QLineEdit()

        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.anglesunits_label)
        self.root_layout.addWidget(self.anglesunits_selector)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.first_row_layout.addWidget(self.filename_label)
        self.first_row_layout.addWidget(self.filename_input)
        self.first_row_layout.addWidget(self.filename_browse)

        self.second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.axisp1x_label, self.axisp1x_input, self.axisp1y_label, self.axisp1y_input, self.axisp1z_label, self.axisp1z_input]:
            self.second_row_layout.addWidget(x)

        self.third_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.axisp2x_label, self.axisp2x_input, self.axisp2y_label, self.axisp2y_input, self.axisp2z_label, self.axisp2z_input]:
            self.third_row_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(rot_file_gen)
        self._init_connections()

    def fill_values(self, rot_file_wave_gen):
        """ Fills values from the data structure into the widget. """
        self.anglesunits_selector.setCurrentIndex(0 if rot_file_wave_gen.anglesunits == "degrees" else 1)
        self.duration_input.setText(str(rot_file_wave_gen.duration))
        self.filename_input.setText(str(rot_file_wave_gen.filename))
        self.axisp1x_input.setText(str(rot_file_wave_gen.axisp1[0]))
        self.axisp1y_input.setText(str(rot_file_wave_gen.axisp1[1]))
        self.axisp1z_input.setText(str(rot_file_wave_gen.axisp1[2]))
        self.axisp2x_input.setText(str(rot_file_wave_gen.axisp2[0]))
        self.axisp2y_input.setText(str(rot_file_wave_gen.axisp2[1]))
        self.axisp2z_input.setText(str(rot_file_wave_gen.axisp2[2]))

    def _init_connections(self):
        for x in [self.duration_input, self.filename_input,
                  self.axisp1x_input, self.axisp1y_input, self.axisp1z_input,
                  self.axisp2x_input, self.axisp2y_input, self.axisp2z_input]:
            x.textChanged.connect(self.on_change)
        self.anglesunits_selector.currentIndexChanged.connect(self.on_change)
        self.filename_browse.clicked.connect(self.on_file_browse)

    def on_file_browse(self):
        """ Opens a file dialog to open the filename, then puts it into the widget. """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, __("Open file"), Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(filename)
        self.filename_input.setText(filename)

    def on_change(self):
        """ Reacts to input change, sanitizing it and firing a signal with the appropriate data object. """
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs a motion object from the data on the widget. """
        return RotationFileGen(duration=make_float(self.duration_input.text()),
                               filename=str(self.filename_input.text()),
                               anglesunits=str(
                                   self.anglesunits_selector.currentText().lower()),
                               axisp1=[make_float(self.axisp1x_input.text()),
                                       make_float(self.axisp1y_input.text()),
                                       make_float(self.axisp1z_input.text())],
                               axisp2=[make_float(self.axisp2x_input.text()),
                                       make_float(self.axisp2y_input.text()),
                                       make_float(self.axisp2z_input.text())])

    def on_delete(self):
        """ Deletes the currently represented object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.axisp1x_input, self.axisp1y_input, self.axisp1z_input,
                  self.axisp2x_input, self.axisp2y_input, self.axisp2z_input]:
            x.setText("0" if not x.text() else x.text().replace(",", "."))
