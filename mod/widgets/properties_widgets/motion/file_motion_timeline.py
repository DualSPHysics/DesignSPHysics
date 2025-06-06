#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics File Based Motion Timeline Widget. """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.motion.file_gen import FileGen
from mod.functions import make_float, make_int
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.tools.dialog_tools import warning_dialog


class FileMotionTimeline(QtWidgets.QWidget):
    """ A File motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, FileGen)

    def __init__(self, file_wave_gen, project_folder_path, parent=None):
        if not isinstance(file_wave_gen, FileGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if file_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(__("File movement: "))

        self.duration_label = QtWidgets.QLabel(__("Duration: "))
        self.duration_input = TimeInput()

        self.filename_label = QtWidgets.QLabel(__("File name: "))
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_browse = QtWidgets.QPushButton(__("Browse"))

        self.fields_label = QtWidgets.QLabel(__("Number of fields: "))
        self.fields_input = IntValueInput(min_val=0)

        self.fieldtime_label = QtWidgets.QLabel(__("Column with time: "))
        self.fieldtime_input = IntValueInput(min_val=0)

        self.fieldx_label = QtWidgets.QLabel(__("X position column: "))
        self.fieldx_input = IntValueInput(min_val=-1)

        self.fieldy_label = QtWidgets.QLabel(__("Y position column: "))
        self.fieldy_input = IntValueInput(min_val=-1)

        self.fieldz_label = QtWidgets.QLabel(__("Z position column: "))
        self.fieldz_input = IntValueInput(min_val=-1)

        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.first_row_layout.addWidget(self.filename_label)
        self.first_row_layout.addWidget(self.filename_input)
        self.first_row_layout.addWidget(self.filename_browse)

        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout.addWidget(self.fields_label)
        self.second_row_layout.addWidget(self.fields_input)

        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout.addWidget(self.fieldtime_label)
        self.third_row_layout.addWidget(self.fieldtime_input)

        self.fourth_row_layout = QtWidgets.QHBoxLayout()
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
        """ Fills value from the data structure onto the widget. """
        self.duration_input.setValue(file_wave_gen.duration)
        self.filename_input.setText(file_wave_gen.filename)
        self.fields_input.setValue(file_wave_gen.fields)
        self.fieldtime_input.setValue(file_wave_gen.fieldtime)
        self.fieldx_input.setValue(file_wave_gen.fieldx)
        self.fieldy_input.setValue(file_wave_gen.fieldy)
        self.fieldz_input.setValue(file_wave_gen.fieldz)

    def _init_connections(self):
        for x in [self.duration_input, self.fields_input, self.fieldtime_input, self.fieldx_input, self.fieldy_input, self.fieldz_input]:
            x.value_changed.connect(self.on_change)
        self.filename_input.textChanged.connect(self.on_change)
        self.filename_browse.clicked.connect(self.on_file_browse)

    def on_file_browse(self):
        """ Opens a file browser dialog and sets the path on the widget. """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, __("Open file"), Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(filename)
        self.filename_input.setText(filename)

    def on_change(self):
        """ Reacts to any change on the widget, fires a signal with the corresponding motion object """
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            warning_dialog("Introduced an invalid value for a number.")

    def construct_motion_object(self):
        """ Constructs an FileGen object based on the widget data. """
        return FileGen(duration=self.duration_input.value(),
                       filename=self.filename_input.text(),
                       fields=self.fields_input.value(),
                       fieldtime=self.fieldtime_input.value(),
                       fieldx=self.fieldx_input.value(),
                       fieldy=self.fieldy_input.value(),
                       fieldz=self.fieldz_input.value())

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())
