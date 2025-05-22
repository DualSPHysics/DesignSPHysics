#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics File Based Motion Timeline Widget. """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.motion.file_gen import FileGen
from mod.dataobjects.motion.path_file_gen import PathFileGen
from mod.dataobjects.motion.rotate_adv_file_gen import RotateAdvFileGen
from mod.functions import make_float, make_int
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.tools.dialog_tools import warning_dialog


class PathFileMotionTimeline(QtWidgets.QWidget):
    """ A File motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, FileGen)

    def __init__(self, file_wave_gen, project_folder_path, parent=None):
        if not isinstance(file_wave_gen, PathFileGen):
            raise TypeError("You tried to spawn a path file motion generator "
                            "motion widget in the timeline with a wrong object")
        if file_wave_gen is None:
            raise TypeError("You tried to spawn a path file motion generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(__("File movement: "))

        self.anglesunits_label = QtWidgets.QLabel(__("Angle Units: "))
        self.anglesunits_selector = QtWidgets.QComboBox()
        self.anglesunits_selector.insertItems(
            0, [__("Degrees"), __("Radians")])

        self.duration_label = QtWidgets.QLabel(__("Duration: "))
        self.duration_input = TimeInput()

        self.filename_label = QtWidgets.QLabel(__("File name: "))
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_browse = QtWidgets.QPushButton(__("Browse"))

        self.fields_label = QtWidgets.QLabel(__("Number of fields: "))
        self.fields_input = IntValueInput(min_val=0)

        self.fieldtime_label = QtWidgets.QLabel(__("Column with time: "))
        self.fieldtime_input = IntValueInput(min_val=0)

        self.fieldsxyz_label = QtWidgets.QLabel(__("Position columns for (X,Y,Z): "))
        self.fieldx_input = IntValueInput(min_val=0)
        self.fieldy_input = IntValueInput(min_val=0)
        self.fieldz_input = IntValueInput(min_val=0)

        self.fieldangs123_label = QtWidgets.QLabel(__("Angle columns for (ang1,ang2,ang3): "))
        self.fieldang1_input = IntValueInput(min_val=0)
        self.fieldang2_input = IntValueInput(min_val=0)
        self.fieldang3_input = IntValueInput(min_val=0)

        self.center_label = QtWidgets.QLabel(__("Rotation center"))
        self.fieldcenterx_input = SizeInput()
        self.fieldcentery_input = SizeInput()
        self.fieldcenterz_input = SizeInput()

        self.intrinsic_checkbox = QtWidgets.QCheckBox("Intrinsic rotation")
        self.movecenter_checkbox = QtWidgets.QCheckBox("MoveCenter")
        self.axes_label=QtWidgets.QLabel(__("Axes"))
        self.axes_input=QtWidgets.QLineEdit()
        self.axes_input.setMaxLength(3)


        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.anglesunits_label)
        self.root_layout.addWidget(self.anglesunits_selector)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_layout.addWidget(self.filename_label)
        self.file_layout.addWidget(self.filename_input)
        self.file_layout.addWidget(self.filename_browse)

        self.n_fields_layout_layout = QtWidgets.QHBoxLayout()
        self.n_fields_layout_layout.addWidget(self.fields_label)
        self.n_fields_layout_layout.addWidget(self.fields_input)
        self.n_fields_layout_layout.addWidget(self.fieldtime_label)
        self.n_fields_layout_layout.addWidget(self.fieldtime_input)

        self.fields_row1_layout = QtWidgets.QHBoxLayout()
        for x in [self.fieldsxyz_label,self.fieldx_input, self.fieldy_input, self.fieldz_input,
                  ]:
            self.fields_row1_layout.addWidget(x)

        self.fields_row2_layout = QtWidgets.QHBoxLayout()
        for x in [self.fieldangs123_label, self.fieldang1_input,  self.fieldang2_input,
                  self.fieldang3_input ]:
            self.fields_row2_layout.addWidget(x)



        self.center_layout=QtWidgets.QHBoxLayout()
        for x in [self.center_label,self.fieldcenterx_input,self.fieldcentery_input,self.fieldcenterz_input]:
            self.center_layout.addWidget(x)

        self.config_layout = QtWidgets.QHBoxLayout()
        for x in [self.intrinsic_checkbox,self.axes_label,self.axes_input,self.movecenter_checkbox]:
            self.config_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.file_layout, self.n_fields_layout_layout, self.fields_row1_layout,self.fields_row2_layout,
                  self.center_layout,self.config_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(file_wave_gen)
        self._init_connections()

    def fill_values(self, file_wave_gen:PathFileGen):
        """ Fills value from the data structure onto the widget. """
        self.anglesunits_selector.setCurrentIndex(0 if file_wave_gen.anglesunits == "degrees" else 1)
        self.duration_input.setValue(file_wave_gen.duration)
        self.filename_input.setText(file_wave_gen.filename)
        self.fields_input.setValue(file_wave_gen.fields)
        self.fieldtime_input.setValue(file_wave_gen.fieldtime)
        self.fieldx_input.setValue(file_wave_gen.fieldx)
        self.fieldy_input.setValue(file_wave_gen.fieldy)
        self.fieldz_input.setValue(file_wave_gen.fieldz)
        self.fieldang1_input.setValue(file_wave_gen.fieldang1)
        self.fieldang2_input.setValue(file_wave_gen.fieldang2)
        self.fieldang3_input.setValue(file_wave_gen.fieldang3)
        self.fieldcenterx_input.setValue(file_wave_gen.center[0])
        self.fieldcentery_input.setValue(file_wave_gen.center[1])
        self.fieldcenterz_input.setValue(file_wave_gen.center[2])
        self.intrinsic_checkbox.setChecked(file_wave_gen.intrinsic)
        self.axes_input.setText(file_wave_gen.axes)
        self.movecenter_checkbox.setChecked(file_wave_gen.movecenter)

    def _init_connections(self):
        for x in [self.duration_input, self.fields_input, self.fieldtime_input, self.fieldx_input,
                  self.fieldy_input, self.fieldz_input,self.fieldang1_input, self.fieldang2_input, self.fieldang3_input,
                  self.fieldcenterx_input, self.fieldcentery_input,    self.fieldcenterz_input]:
            x.value_changed.connect(self.on_change)
        self.filename_input.textChanged.connect(self.on_change)
        self.axes_input.value_changed.connect(self.on_change)
        self.intrinsic_checkbox.stateChanged.connect(self.on_change)
        self.movecenter_checkbox.stateChanged.connect(self.on_change)
        self.anglesunits_selector.currentIndexChanged.connect(self.on_change)
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
        return PathFileGen(duration=self.duration_input.value(),
                       filename=self.filename_input.text(),
                       fields=self.fields_input.value(),
                       fieldtime=self.fieldtime_input.value(),
                       fieldx=self.fieldx_input.value(),
                       fieldy=self.fieldy_input.value(),
                       fieldz=self.fieldz_input.value(),
                       fieldang1=self.fieldang1_input.value(),
                       fieldang2=self.fieldang2_input.value(),
                       fieldang3=self.fieldang3_input.value(),
                       intrinsic=self.intrinsic_checkbox.isChecked(),
                       center=[self.fieldcenterx_input.value(),
                               self.fieldcentery_input.value(),
                               self.fieldcenterz_input.value(),],
                       axes=self.axes_input.text(),
                       movecenter=self.movecenter_checkbox.isChecked(),
                                anglesunits=str(
                                    self.anglesunits_selector.currentText().lower())
                                )

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())
