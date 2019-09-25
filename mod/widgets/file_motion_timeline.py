#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics File Based Motion Timeline Widget. '''

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.guiutils import h_line_generator
from mod.stdout_tools import debug

from mod.dataobjects.file_gen import FileGen


class FileMotionTimeline(QtGui.QWidget):
    ''' A File motion graphical representation for a table-based timeline '''
    changed = QtCore.Signal(int, FileGen)

    def __init__(self, file_wave_gen, project_folder_path):
        if not isinstance(file_wave_gen, FileGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if file_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super(FileMotionTimeline, self).__init__()

        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = file_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(__("File movement: "))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.filename_label = QtGui.QLabel(__("File name: "))
        self.filename_input = QtGui.QLineEdit()
        self.filename_browse = QtGui.QPushButton(__("Browse"))

        self.fields_label = QtGui.QLabel(__("Number of fields: "))
        self.fields_input = QtGui.QLineEdit()

        self.fieldtime_label = QtGui.QLabel(__("Column with time: "))
        self.fieldtime_input = QtGui.QLineEdit()

        self.fieldx_label = QtGui.QLabel(__("X position column: "))
        self.fieldx_input = QtGui.QLineEdit()

        self.fieldy_label = QtGui.QLabel(__("Y position column: "))
        self.fieldy_input = QtGui.QLineEdit()

        self.fieldz_label = QtGui.QLabel(__("Z position column: "))
        self.fieldz_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.first_row_layout = QtGui.QHBoxLayout()
        self.first_row_layout.addWidget(self.filename_label)
        self.first_row_layout.addWidget(self.filename_input)
        self.first_row_layout.addWidget(self.filename_browse)

        self.second_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout.addWidget(self.fields_label)
        self.second_row_layout.addWidget(self.fields_input)

        self.third_row_layout = QtGui.QHBoxLayout()
        self.third_row_layout.addWidget(self.fieldtime_label)
        self.third_row_layout.addWidget(self.fieldtime_input)

        self.fourth_row_layout = QtGui.QHBoxLayout()
        for x in [self.fieldx_label, self.fieldx_input, self.fieldy_label, self.fieldy_input, self.fieldz_label, self.fieldz_input]:
            self.fourth_row_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(file_wave_gen)
        self._init_connections()

    def fill_values(self, file_wave_gen):
        self.duration_input.setText(str(file_wave_gen.duration))
        self.filename_input.setText(str(file_wave_gen.filename))
        self.fields_input.setText(str(file_wave_gen.fields))
        self.fieldtime_input.setText(str(file_wave_gen.fieldtime))
        self.fieldx_input.setText(str(file_wave_gen.fieldx))
        self.fieldy_input.setText(str(file_wave_gen.fieldy))
        self.fieldz_input.setText(str(file_wave_gen.fieldz))

    def _init_connections(self):
        for x in [self.duration_input, self.filename_input, self.fields_input, self.fieldtime_input, self.fieldx_input, self.fieldy_input, self.fieldz_input]:
            x.textChanged.connect(self.on_change)
        self.filename_browse.clicked.connect(self.on_file_browse)

    def on_file_browse(self):
        # noinspection PyArgumentList
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self, __("Open file"), QtCore.QDir.homePath())
        self.filename_input.setText(filename)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return FileGen(parent_movement=self.parent_movement,
                       duration=float(self.duration_input.text()),
                       filename=str(self.filename_input.text()),
                       fields=str(self.fields_input.text()),
                       fieldtime=str(self.fieldtime_input.text()),
                       fieldx=str(self.fieldx_input.text()),
                       fieldy=str(self.fieldy_input.text()),
                       fieldz=str(self.fieldz_input.text()))

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.fields_input, self.fieldtime_input, self.fieldx_input, self.fieldy_input, self.fieldz_input]:
            x.setText("0" if x.text() else x.text().replace(",", "."))
