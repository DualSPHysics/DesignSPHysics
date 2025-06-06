#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Add STL Dialog. """
import os
from os.path import dirname
from tempfile import gettempdir
from uuid import uuid4

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.tools.dialog_tools import error_dialog, WaitDialog, warning_dialog
from mod.tools.executable_tools import ensure_process_is_executable_or_fail
from mod.tools.file_tools import import_geo
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.stdout_tools import log
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.dock.dock_widgets.add_geo_dialog import WorkingDialog

class AddBathymetryDialog(QtWidgets.QDialog):
    """ A dialog that shows option to import a geometry passed as parameter """

    IS_DIALOG_MODAL: bool = True
    MINIMUM_WIDTH = 956

    def __init__(self, file_name, parent=None):
        super().__init__(parent=parent)

        self.setMinimumWidth(self.MINIMUM_WIDTH)

        self.bathymetry_mode = True

        # Defines import stl dialog
        self.setModal(self.IS_DIALOG_MODAL)
        self.setWindowTitle(__("Import Bathymetry"))
        self.geo_dialog_layout = QtWidgets.QVBoxLayout()
        self.geo_group = QtWidgets.QGroupBox(__("Import Bathymetry options"))
        self.geo_group_layout = QtWidgets.QVBoxLayout()

        #  GEO File selection
        self.geo_file_layout = QtWidgets.QHBoxLayout()
        self.geo_file_label = QtWidgets.QLabel(__("GEO File: "))
        self.geo_file_path = QtWidgets.QLineEdit()
        self.geo_file_browse = QtWidgets.QPushButton(__("Browse"))

        for x in [self.geo_file_label, self.geo_file_path, self.geo_file_browse]:
            self.geo_file_layout.addWidget(x)


        ######################################### BATHYMETRY  ###########################################################
        # Bathymetry Options
        self.geo_bathymetry_options_scroll = QtWidgets.QScrollArea()
        self.geo_bathymetry_options_scroll.setWidgetResizable(True)
        self.geo_bathymetry_options_widget = QtWidgets.QWidget()
        self.geo_bathymetry_options_layout = QtWidgets.QVBoxLayout()

        self.bath_input_options_header_label = QtWidgets.QLabel("<h4>{}</h4>".format("Input configuration"))

        self.bath_move_layout = QtWidgets.QHBoxLayout()
        self.bath_move_label = QtWidgets.QLabel(__("Move: "))
        self.bath_move_x_l = QtWidgets.QLabel("X: ")
        self.bath_move_x_e = SizeInput()
        self.bath_move_y_l = QtWidgets.QLabel("Y: ")
        self.bath_move_y_e = SizeInput()
        self.bath_move_z_l = QtWidgets.QLabel("Z: ")
        self.bath_move_z_e = SizeInput()
        for x in [self.bath_move_label,
                  self.bath_move_x_l,
                  self.bath_move_x_e,
                  self.bath_move_y_l,
                  self.bath_move_y_e,
                  self.bath_move_z_l,
                  self.bath_move_z_e, ]:
            self.bath_move_layout.addWidget(x)

        self.bath_rotate_layout = QtWidgets.QHBoxLayout()
        self.bath_rotate_label = QtWidgets.QLabel(__("Rotate: "))
        self.bath_rotate_x_l = QtWidgets.QLabel("X: ")
        self.bath_rotate_x_e = ValueInput()
        self.bath_rotate_y_l = QtWidgets.QLabel("Y: ")
        self.bath_rotate_y_e = ValueInput()
        self.bath_rotate_z_l = QtWidgets.QLabel("Z: ")
        self.bath_rotate_z_e = ValueInput()
        for x in [self.bath_rotate_label,
                  self.bath_rotate_x_l,
                  self.bath_rotate_x_e,
                  self.bath_rotate_y_l,
                  self.bath_rotate_y_e,
                  self.bath_rotate_z_l,
                  self.bath_rotate_z_e, ]:
            self.bath_rotate_layout.addWidget(x)

        self.bath_scale_layout = QtWidgets.QHBoxLayout()
        self.bath_scale_label = QtWidgets.QLabel(__("Scale: "))
        self.bath_scale_x_l = QtWidgets.QLabel("X: ")
        self.bath_scale_x_e = ValueInput()
        self.bath_scale_y_l = QtWidgets.QLabel("Y: ")
        self.bath_scale_y_e = ValueInput()
        self.bath_scale_z_l = QtWidgets.QLabel("Z: ")
        self.bath_scale_z_e = ValueInput()
        for x in [self.bath_scale_label,
                  self.bath_scale_x_l,
                  self.bath_scale_x_e,
                  self.bath_scale_y_l,
                  self.bath_scale_y_e,
                  self.bath_scale_z_l,
                  self.bath_scale_z_e, ]:
            self.bath_scale_layout.addWidget(x)

        self.bath_selection_layout = QtWidgets.QVBoxLayout()
        self.bath_selection_enabled_chk = QtWidgets.QCheckBox(__("Enable selection"))

        self.bath_selection_point_layout = QtWidgets.QHBoxLayout()
        self.bath_selection_point_label = QtWidgets.QLabel(__("Point: "))
        self.bath_selection_point_x_l = QtWidgets.QLabel("X: ")
        self.bath_selection_point_x_e = SizeInput()
        self.bath_selection_point_y_l = QtWidgets.QLabel("Y: ")
        self.bath_selection_point_y_e = SizeInput()
        for x in [self.bath_selection_point_label,
                  self.bath_selection_point_x_l,
                  self.bath_selection_point_x_e,
                  self.bath_selection_point_y_l,
                  self.bath_selection_point_y_e,
                  ]:
            self.bath_selection_point_layout.addWidget(x)

        self.bath_selection_size_layout = QtWidgets.QHBoxLayout()
        self.bath_selection_size_label = QtWidgets.QLabel(__("Size: "))
        self.bath_selection_size_x_l = QtWidgets.QLabel("X: ")
        self.bath_selection_size_x_e = SizeInput()
        self.bath_selection_size_y_l = QtWidgets.QLabel("Y: ")
        self.bath_selection_size_y_e = SizeInput()
        for x in [self.bath_selection_size_label,
                  self.bath_selection_size_x_l,
                  self.bath_selection_size_x_e,
                  self.bath_selection_size_y_l,
                  self.bath_selection_size_y_e,
                  ]:
            self.bath_selection_size_layout.addWidget(x)

        self.bath_selection_layout.addWidget(self.bath_selection_enabled_chk)
        self.bath_selection_layout.addLayout(self.bath_selection_point_layout)
        self.bath_selection_layout.addLayout(self.bath_selection_size_layout)

        self.bath_selection_enabled_chk.toggled.connect(self.on_bath_selection_toggled)
        self.on_bath_selection_toggled()

        self.bath_grid_options_header_label = QtWidgets.QLabel("<h4>{}</h4>".format("Grid configuration"))

        self.bath_grid_dp_layout = QtWidgets.QHBoxLayout()
        self.bath_grid_dp_label = QtWidgets.QLabel(__("Grid DP: "))
        self.bath_grid_dp_x_e = ValueInput()
        for x in [self.bath_grid_dp_label,
                  self.bath_grid_dp_x_e]:
            self.bath_grid_dp_layout.addWidget(x)

        self.bath_initdomain_layout = QtWidgets.QVBoxLayout()
        self.bath_initdomain_enabled_chk = QtWidgets.QCheckBox(__("Enable initdomain"))

        self.bath_initdomain_point_layout = QtWidgets.QHBoxLayout()
        self.bath_initdomain_point_label = QtWidgets.QLabel(__("Point: "))
        self.bath_initdomain_point_x_l = QtWidgets.QLabel("X: ")
        self.bath_initdomain_point_x_e = SizeInput()
        self.bath_initdomain_point_y_l = QtWidgets.QLabel("Y: ")
        self.bath_initdomain_point_y_e = SizeInput()
        for x in [self.bath_initdomain_point_label,
                  self.bath_initdomain_point_x_l,
                  self.bath_initdomain_point_x_e,
                  self.bath_initdomain_point_y_l,
                  self.bath_initdomain_point_y_e,
                  ]:
            self.bath_initdomain_point_layout.addWidget(x)

        self.bath_initdomain_size_layout = QtWidgets.QHBoxLayout()
        self.bath_initdomain_size_label = QtWidgets.QLabel(__("Size: "))
        self.bath_initdomain_size_x_l = QtWidgets.QLabel("X: ")
        self.bath_initdomain_size_x_e = SizeInput()
        self.bath_initdomain_size_y_l = QtWidgets.QLabel("Y: ")
        self.bath_initdomain_size_y_e = SizeInput()
        for x in [self.bath_initdomain_size_label,
                  self.bath_initdomain_size_x_l,
                  self.bath_initdomain_size_x_e,
                  self.bath_initdomain_size_y_l,
                  self.bath_initdomain_size_y_e,
                  ]:
            self.bath_initdomain_size_layout.addWidget(x)

        self.bath_initdomain_layout.addWidget(self.bath_initdomain_enabled_chk)
        self.bath_initdomain_layout.addLayout(self.bath_initdomain_point_layout)
        self.bath_initdomain_layout.addLayout(self.bath_initdomain_size_layout)

        self.bath_initdomain_enabled_chk.toggled.connect(self.on_bath_initdomain_toggled)
        self.on_bath_initdomain_toggled()

        self.bath_expands_layout = QtWidgets.QVBoxLayout()

        self.bath_xmin_layout = QtWidgets.QHBoxLayout()
        self.bath_xmin_check = QtWidgets.QCheckBox()
        self.bath_xmin_label = QtWidgets.QLabel(__("XMin: "))
        self.bath_xmin_size_l = QtWidgets.QLabel("Size: ")
        self.bath_xmin_size_e = SizeInput()
        self.bath_xmin_z_l = QtWidgets.QLabel("Z: ")
        self.bath_xmin_z_e = SizeInput()
        self.bath_xmin_size2_l = QtWidgets.QLabel("Size2: ")
        self.bath_xmin_size2_e = SizeInput()
        self.bath_xmin_z2_l = QtWidgets.QLabel("Z2: ")
        self.bath_xmin_z2_e = SizeInput()
        for x in [
            self.bath_xmin_check,
            self.bath_xmin_label,
            self.bath_xmin_size_l,
            self.bath_xmin_size_e,
            self.bath_xmin_z_l,
            self.bath_xmin_z_e,
            self.bath_xmin_size2_l,
            self.bath_xmin_size2_e,
            self.bath_xmin_z2_l,
            self.bath_xmin_z2_e
        ]:
            self.bath_xmin_layout.addWidget(x)

        self.bath_xmax_layout = QtWidgets.QHBoxLayout()
        self.bath_xmax_check = QtWidgets.QCheckBox()
        self.bath_xmax_label = QtWidgets.QLabel(__("XMax: "))
        self.bath_xmax_size_l = QtWidgets.QLabel("Size: ")
        self.bath_xmax_size_e = SizeInput()
        self.bath_xmax_z_l = QtWidgets.QLabel("Z: ")
        self.bath_xmax_z_e = SizeInput()
        self.bath_xmax_size2_l = QtWidgets.QLabel("Size2: ")
        self.bath_xmax_size2_e = SizeInput()
        self.bath_xmax_z2_l = QtWidgets.QLabel("Z2: ")
        self.bath_xmax_z2_e = SizeInput()
        for x in [
            self.bath_xmax_check,
            self.bath_xmax_label,
            self.bath_xmax_size_l,
            self.bath_xmax_size_e,
            self.bath_xmax_z_l,
            self.bath_xmax_z_e,
            self.bath_xmax_size2_l,
            self.bath_xmax_size2_e,
            self.bath_xmax_z2_l,
            self.bath_xmax_z2_e
        ]:
            self.bath_xmax_layout.addWidget(x)

        self.bath_ymin_layout = QtWidgets.QHBoxLayout()
        self.bath_ymin_check = QtWidgets.QCheckBox()
        self.bath_ymin_label = QtWidgets.QLabel(__("YMin: "))
        self.bath_ymin_size_l = QtWidgets.QLabel("Size: ")
        self.bath_ymin_size_e = SizeInput()
        self.bath_ymin_z_l = QtWidgets.QLabel("Z: ")
        self.bath_ymin_z_e = SizeInput()
        self.bath_ymin_size2_l = QtWidgets.QLabel("Size2: ")
        self.bath_ymin_size2_e = SizeInput()
        self.bath_ymin_z2_l = QtWidgets.QLabel("Z2: ")
        self.bath_ymin_z2_e = SizeInput()
        for x in [
            self.bath_ymin_check,
            self.bath_ymin_label,
            self.bath_ymin_size_l,
            self.bath_ymin_size_e,
            self.bath_ymin_z_l,
            self.bath_ymin_z_e,
            self.bath_ymin_size2_l,
            self.bath_ymin_size2_e,
            self.bath_ymin_z2_l,
            self.bath_ymin_z2_e
        ]:
            self.bath_ymin_layout.addWidget(x)

        self.bath_ymax_layout = QtWidgets.QHBoxLayout()
        self.bath_ymax_check = QtWidgets.QCheckBox()
        self.bath_ymax_label = QtWidgets.QLabel(__("YMax: "))
        self.bath_ymax_size_l = QtWidgets.QLabel("Size: ")
        self.bath_ymax_size_e = SizeInput()
        self.bath_ymax_z_l = QtWidgets.QLabel("Z: ")
        self.bath_ymax_z_e = SizeInput()
        self.bath_ymax_size2_l = QtWidgets.QLabel("Size2: ")
        self.bath_ymax_size2_e = SizeInput()
        self.bath_ymax_z2_l = QtWidgets.QLabel("Z2: ")
        self.bath_ymax_z2_e = SizeInput()
        for x in [
            self.bath_ymax_check,
            self.bath_ymax_label,
            self.bath_ymax_size_l,
            self.bath_ymax_size_e,
            self.bath_ymax_z_l,
            self.bath_ymax_z_e,
            self.bath_ymax_size2_l,
            self.bath_ymax_size2_e,
            self.bath_ymax_z2_l,
            self.bath_ymax_z2_e
        ]:
            self.bath_ymax_layout.addWidget(x)

        self.bath_expands_layout.addLayout(self.bath_xmin_layout)
        self.bath_expands_layout.addLayout(self.bath_xmax_layout)
        self.bath_expands_layout.addLayout(self.bath_ymin_layout)
        self.bath_expands_layout.addLayout(self.bath_ymax_layout)
        self.bath_xmin_check.toggled.connect(self.on_xmin_check)
        self.bath_xmax_check.toggled.connect(self.on_xmax_check)
        self.bath_ymin_check.toggled.connect(self.on_ymin_check)
        self.bath_ymax_check.toggled.connect(self.on_ymax_check)
        self.on_xmin_check()
        self.on_xmax_check()
        self.on_ymin_check()
        self.on_ymax_check()

        self.bath_periodicx_layout = QtWidgets.QVBoxLayout()
        self.bath_periodicx_enabled_chk = QtWidgets.QCheckBox(__("Enable periodicx"))

        self.bath_periodicx_rampwidth_layout = QtWidgets.QHBoxLayout()
        self.bath_periodicx_rampwidth_x_l = QtWidgets.QLabel("Rampwidth: ")
        self.bath_periodicx_rampwidth_x_e = ValueInput()
        self.bath_periodicx_flatwidth_x_l = QtWidgets.QLabel("Flatwidth: ")
        self.bath_periodicx_flatwidth_x_e = ValueInput()
        for x in [self.bath_periodicx_rampwidth_x_l,
                  self.bath_periodicx_rampwidth_x_e,
                  self.bath_periodicx_flatwidth_x_l,
                  self.bath_periodicx_flatwidth_x_e,
                  ]:
            self.bath_periodicx_rampwidth_layout.addWidget(x)

        self.bath_periodicx_layout.addWidget(self.bath_periodicx_enabled_chk)
        self.bath_periodicx_layout.addLayout(self.bath_periodicx_rampwidth_layout)
        self.bath_periodicx_enabled_chk.toggled.connect(self.on_bath_periodicx_toggled)
        self.on_bath_periodicx_toggled()

        self.bath_periodicy_layout = QtWidgets.QVBoxLayout()
        self.bath_periodicy_enabled_chk = QtWidgets.QCheckBox(__("Enable periodicy"))

        self.bath_periodicy_rampwidth_layout = QtWidgets.QHBoxLayout()
        self.bath_periodicy_rampwidth_x_l = QtWidgets.QLabel("Rampwidth: ")
        self.bath_periodicy_rampwidth_x_e = ValueInput()
        self.bath_periodicy_flatwidth_x_l = QtWidgets.QLabel("Flatwidth: ")
        self.bath_periodicy_flatwidth_x_e = ValueInput()
        for x in [self.bath_periodicy_rampwidth_x_l,
                  self.bath_periodicy_rampwidth_x_e,
                  self.bath_periodicy_flatwidth_x_l,
                  self.bath_periodicy_flatwidth_x_e,
                  ]:
            self.bath_periodicy_rampwidth_layout.addWidget(x)

        self.bath_periodicy_layout.addWidget(self.bath_periodicy_enabled_chk)
        self.bath_periodicy_layout.addLayout(self.bath_periodicy_rampwidth_layout)
        self.bath_periodicy_enabled_chk.toggled.connect(self.on_bath_periodicy_toggled)
        self.on_bath_periodicy_toggled()

        self.bath_finalmove_layout = QtWidgets.QVBoxLayout()
        self.bath_finalmove_enabled_chk = QtWidgets.QCheckBox(__("Enable finalmove"))

        self.bath_finalmove_data_layout = QtWidgets.QHBoxLayout()
        self.bath_finalmove_label = QtWidgets.QLabel(__("Move grid: "))
        self.bath_finalmove_x_l = QtWidgets.QLabel("X: ")
        self.bath_finalmove_x_e = SizeInput()
        self.bath_finalmove_y_l = QtWidgets.QLabel("Y: ")
        self.bath_finalmove_y_e = SizeInput()
        self.bath_finalmove_z_l = QtWidgets.QLabel("Z: ")
        self.bath_finalmove_z_e = SizeInput()
        for x in [self.bath_finalmove_label,
                  self.bath_finalmove_x_l,
                  self.bath_finalmove_x_e,
                  self.bath_finalmove_y_l,
                  self.bath_finalmove_y_e,
                  self.bath_finalmove_z_l,
                  self.bath_finalmove_z_e, ]:
            self.bath_finalmove_data_layout.addWidget(x)

        self.bath_finalmove_layout.addWidget(self.bath_finalmove_enabled_chk)
        self.bath_finalmove_layout.addLayout(self.bath_finalmove_data_layout)

        self.bath_finalmove_enabled_chk.toggled.connect(self.on_bath_finalmove_toggled)
        self.on_bath_finalmove_toggled()

        self.geo_bathymetry_options_layout.addWidget(self.bath_input_options_header_label)
        self.geo_bathymetry_options_layout.addLayout(self.bath_move_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_rotate_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_scale_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_selection_layout)
        self.geo_bathymetry_options_layout.addWidget(self.bath_grid_options_header_label)
        self.geo_bathymetry_options_layout.addLayout(self.bath_grid_dp_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_initdomain_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_expands_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_periodicx_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_periodicy_layout)
        self.geo_bathymetry_options_layout.addLayout(self.bath_finalmove_layout)

        self.geo_bathymetry_options_widget.setLayout(self.geo_bathymetry_options_layout)

        ###############################################################################################
        ########################## END Bathymetry Options #####################################################################
        #################################################################################

        # Import object name
        self.geo_objname_layout = QtWidgets.QHBoxLayout()
        self.geo_objname_label = QtWidgets.QLabel(__("Import object name: "))
        self.geo_objname_text = QtWidgets.QLineEdit("GEO_{}".format(file_name.split("/")[-1]).split(".")[0].replace("-", "_"))
        for x in [self.geo_objname_label, self.geo_objname_text]:
            self.geo_objname_layout.addWidget(x)
        # End object name
        # Add component layouts to group layout
        self.geo_bathymetry_options_scroll.setWidget(self.geo_bathymetry_options_widget)
        self.geo_bathymetry_options_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Autofill
        self.geo_autofil_layout = QtWidgets.QHBoxLayout()
        self.geo_autofill_chck = QtWidgets.QCheckBox("Autofill")
        self.geo_autofil_layout.addWidget(self.geo_autofill_chck)

        self.geo_group_layout.addLayout(self.geo_file_layout)
        self.geo_group_layout.addWidget(self.geo_bathymetry_options_scroll)
        self.geo_group_layout.addLayout(self.geo_objname_layout)
        self.geo_group_layout.addLayout(self.geo_autofil_layout)
        self.geo_group.setLayout(self.geo_group_layout)

        # Create button layout
        self.geo_button_layout = QtWidgets.QHBoxLayout()
        self.geo_button_ok = QtWidgets.QPushButton(__("Import"))
        self.geo_button_cancel = QtWidgets.QPushButton(__("Cancel"))
        self.geo_button_cancel.clicked.connect(self.reject)

        self.geo_button_layout.addStretch(1)
        self.geo_button_layout.addWidget(self.geo_button_cancel)
        self.geo_button_layout.addWidget(self.geo_button_ok)

        # Compose main window layout
        self.geo_dialog_layout.addWidget(self.geo_group)
        self.geo_dialog_layout.addLayout(self.geo_button_layout)

        self.setLayout(self.geo_dialog_layout)

        self.geo_button_cancel.clicked.connect(self.reject)
        self.geo_button_ok.clicked.connect(self.geo_ok_clicked)
        self.geo_file_browse.clicked.connect(self.geo_dialog_browse)
        self.geo_file_path.textChanged.connect(self.on_file_path_change)

        self.geo_file_path.setText(file_name)

        self.geo_button_ok.setFocus()

        self.fill_default_data()

    def fill_default_data(self):
        """ Fills GUI items with the default data """
        data = Case.the().info.last_used_bathymetry_data
        self.bath_move_x_e.setValue(data.move[0])
        self.bath_move_y_e.setValue(data.move[1])
        self.bath_move_z_e.setValue(data.move[2])
        self.bath_rotate_x_e.setValue(data.rotate[0])
        self.bath_rotate_y_e.setValue(data.rotate[1])
        self.bath_rotate_z_e.setValue(data.rotate[2])
        self.bath_scale_x_e.setValue(data.scale[0])
        self.bath_scale_y_e.setValue(data.scale[1])
        self.bath_scale_z_e.setValue(data.scale[2])
        self.bath_selection_enabled_chk.setChecked(data.selection_enabled)
        self.bath_selection_point_x_e.setValue(data.selection_point[0])
        self.bath_selection_point_y_e.setValue(data.selection_point[1])
        self.bath_selection_size_x_e.setValue(data.selection_size[0])
        self.bath_selection_size_y_e.setValue(data.selection_size[1])
        self.bath_grid_dp_x_e.setValue(data.gdp)
        self.bath_initdomain_enabled_chk.setChecked(data.initdomain_enabled)
        self.bath_initdomain_point_x_e.setValue(data.initdomain_point[0])
        self.bath_initdomain_point_y_e.setValue(data.initdomain_point[1])
        self.bath_initdomain_size_x_e.setValue(data.initdomain_size[0])
        self.bath_initdomain_size_y_e.setValue(data.initdomain_size[1])
        self.bath_xmin_check.setChecked(data.xmin_enabled)
        self.bath_xmin_size_e.setValue(data.expands_xmin[0])
        self.bath_xmin_z_e.setValue(data.expands_xmin[1])
        self.bath_xmin_size2_e.setValue(data.expands_xmin[2])
        self.bath_xmin_z2_e.setValue(data.expands_xmin[3])
        self.bath_xmax_check.setChecked(data.xmax_enabled)
        self.bath_xmax_size_e.setValue(data.expands_xmax[0])
        self.bath_xmax_z_e.setValue(data.expands_xmax[1])
        self.bath_xmax_size2_e.setValue(data.expands_xmax[2])
        self.bath_xmax_z2_e.setValue(data.expands_xmax[3])
        self.bath_ymin_check.setChecked(data.ymin_enabled)
        self.bath_ymin_size_e.setValue(data.expands_ymin[0])
        self.bath_ymin_z_e.setValue(data.expands_ymin[1])
        self.bath_ymin_size2_e.setValue(data.expands_ymin[2])
        self.bath_ymin_z2_e.setValue(data.expands_ymin[3])
        self.bath_ymax_check.setChecked(data.ymax_enabled)
        self.bath_ymax_size_e.setValue(data.expands_ymax[0])
        self.bath_ymax_z_e.setValue(data.expands_ymax[1])
        self.bath_ymax_size2_e.setValue(data.expands_ymax[2])
        self.bath_ymax_z2_e.setValue(data.expands_ymax[3])
        self.bath_periodicx_enabled_chk.setChecked(data.periodicx_enabled)
        self.bath_periodicx_rampwidth_x_e.setValue(data.periodicx_rampwidth)
        self.bath_periodicx_flatwidth_x_e.setValue(data.periodicx_flatwidth)
        self.bath_periodicy_enabled_chk.setChecked(data.periodicy_enabled)
        self.bath_periodicy_rampwidth_x_e.setValue(data.periodicy_rampwidth)
        self.bath_periodicy_flatwidth_x_e.setValue(data.periodicy_flatwidth)
        self.bath_finalmove_enabled_chk.setChecked(data.finalmove_enabled)
        self.bath_finalmove_x_e.setValue(data.finalmove[0])
        self.bath_finalmove_y_e.setValue(data.finalmove[1])
        self.bath_finalmove_z_e.setValue(data.finalmove[2])

    def save_default_data(self):
        """ Saves GUI items in the case data """
        data = Case.the().info.last_used_bathymetry_data
        data.move[0] = self.bath_move_x_e.value()
        data.move[1] = self.bath_move_y_e.value()
        data.move[2] = self.bath_move_z_e.value()
        data.rotate[0] = self.bath_rotate_x_e.value()
        data.rotate[1] = self.bath_rotate_y_e.value()
        data.rotate[2] = self.bath_rotate_z_e.value()
        data.scale[0] = self.bath_scale_x_e.value()
        data.scale[1] = self.bath_scale_y_e.value()
        data.scale[2] = self.bath_scale_z_e.value()
        data.selection_enabled = self.bath_selection_enabled_chk.isChecked()
        data.selection_point[0] = self.bath_selection_point_x_e.value()
        data.selection_point[1] = self.bath_selection_point_y_e.value()
        data.selection_size[0] = self.bath_selection_size_x_e.value()
        data.selection_size[1] = self.bath_selection_size_y_e.value()
        data.gdp = self.bath_grid_dp_x_e.value()
        data.initdomain_enabled = self.bath_initdomain_enabled_chk.isChecked()
        data.initdomain_point[0] = self.bath_initdomain_point_x_e.value()
        data.initdomain_point[1] = self.bath_initdomain_point_y_e.value()
        data.initdomain_size[0] = self.bath_initdomain_size_x_e.value()
        data.initdomain_size[1] = self.bath_initdomain_size_y_e.value()
        data.xmin_enabled = self.bath_xmin_check.isChecked()
        data.expands_xmin[0] = self.bath_xmin_size_e.value()
        data.expands_xmin[1] = self.bath_xmin_z_e.value()
        data.expands_xmin[2] = self.bath_xmin_size2_e.value()
        data.expands_xmin[3] = self.bath_xmin_z2_e.value()
        data.xmax_enabled = self.bath_xmax_check.isChecked()
        data.expands_xmax[0] = self.bath_xmax_size_e.value()
        data.expands_xmax[1] = self.bath_xmax_z_e.value()
        data.expands_xmax[2] = self.bath_xmax_size2_e.value()
        data.expands_xmax[3] = self.bath_xmax_z2_e.value()
        data.ymin_enabled = self.bath_ymin_check.isChecked()
        data.expands_ymin[0] = self.bath_ymin_size_e.value()
        data.expands_ymin[1] = self.bath_ymin_z_e.value()
        data.expands_ymin[2] = self.bath_ymin_size2_e.value()
        data.expands_ymin[3] = self.bath_ymin_z2_e.value()
        data.ymax_enabled = self.bath_ymax_check.isChecked()
        data.expands_ymax[0] = self.bath_ymax_size_e.value()
        data.expands_ymax[1] = self.bath_ymax_z_e.value()
        data.expands_ymax[2] = self.bath_ymax_size2_e.value()
        data.expands_ymax[3] = self.bath_ymax_z2_e.value()
        data.periodicx_enabled = self.bath_periodicx_enabled_chk.isChecked()
        data.periodicx_rampwidth = self.bath_periodicx_rampwidth_x_e.value()
        data.periodicx_flatwidth = self.bath_periodicx_flatwidth_x_e.value()
        data.periodicy_enabled = self.bath_periodicy_enabled_chk.isChecked()
        data.periodicy_rampwidth = self.bath_periodicy_rampwidth_x_e.value()
        data.periodicy_flatwidth = self.bath_periodicy_flatwidth_x_e.value()
        data.finalmove_enabled = self.bath_finalmove_enabled_chk.isChecked()
        data.finalmove[0] = self.bath_finalmove_x_e.value()
        data.finalmove[1] = self.bath_finalmove_y_e.value()
        data.finalmove[2] = self.bath_finalmove_z_e.value()

    def on_xmin_check(self):
        """ Reacts to the xmin checkbox being pressed. """
        if self.bath_xmin_check.isChecked():
            self.bath_xmin_size_e.setEnabled(True)
            self.bath_xmin_z_e.setEnabled(True)
            self.bath_xmin_size2_e.setEnabled(True)
            self.bath_xmin_z2_e.setEnabled(True)
        else:
            self.bath_xmin_size_e.setEnabled(False)
            self.bath_xmin_z_e.setEnabled(False)
            self.bath_xmin_size2_e.setEnabled(False)
            self.bath_xmin_z2_e.setEnabled(False)

    def on_xmax_check(self):
        """ Reacts to the xmax checkbox being pressed. """
        if self.bath_xmax_check.isChecked():
            self.bath_xmax_size_e.setEnabled(True)
            self.bath_xmax_z_e.setEnabled(True)
            self.bath_xmax_size2_e.setEnabled(True)
            self.bath_xmax_z2_e.setEnabled(True)
        else:
            self.bath_xmax_size_e.setEnabled(False)
            self.bath_xmax_z_e.setEnabled(False)
            self.bath_xmax_size2_e.setEnabled(False)
            self.bath_xmax_z2_e.setEnabled(False)

    def on_ymin_check(self):
        """ Reacts to the ymin checkbox being pressed. """
        if self.bath_ymin_check.isChecked():
            self.bath_ymin_size_e.setEnabled(True)
            self.bath_ymin_z_e.setEnabled(True)
            self.bath_ymin_size2_e.setEnabled(True)
            self.bath_ymin_z2_e.setEnabled(True)
        else:
            self.bath_ymin_size_e.setEnabled(False)
            self.bath_ymin_z_e.setEnabled(False)
            self.bath_ymin_size2_e.setEnabled(False)
            self.bath_ymin_z2_e.setEnabled(False)

    def on_ymax_check(self):
        """ Reacts to the ymax checkbox being pressed. """
        if self.bath_ymax_check.isChecked():
            self.bath_ymax_size_e.setEnabled(True)
            self.bath_ymax_z_e.setEnabled(True)
            self.bath_ymax_size2_e.setEnabled(True)
            self.bath_ymax_z2_e.setEnabled(True)
        else:
            self.bath_ymax_size_e.setEnabled(False)
            self.bath_ymax_z_e.setEnabled(False)
            self.bath_ymax_size2_e.setEnabled(False)
            self.bath_ymax_z2_e.setEnabled(False)

    def on_bath_finalmove_toggled(self):
        """ Reacts to the finalmove checkbox being pressed. """
        if self.bath_finalmove_enabled_chk.isChecked():
            self.bath_finalmove_x_e.setEnabled(True)
            self.bath_finalmove_y_e.setEnabled(True)
            self.bath_finalmove_z_e.setEnabled(True)
        else:
            self.bath_finalmove_x_e.setEnabled(False)
            self.bath_finalmove_y_e.setEnabled(False)
            self.bath_finalmove_z_e.setEnabled(False)

    def on_bath_periodicy_toggled(self):
        """ Reacts to the periodicy checkbox being pressed. """
        if self.bath_periodicy_enabled_chk.isChecked():
            self.bath_periodicy_rampwidth_x_e.setEnabled(True)
            self.bath_periodicy_flatwidth_x_e.setEnabled(True)
        else:
            self.bath_periodicy_rampwidth_x_e.setEnabled(False)
            self.bath_periodicy_flatwidth_x_e.setEnabled(False)

    def on_bath_periodicx_toggled(self):
        """ Reacts to the periodicx checkbox being pressed. """
        if self.bath_periodicx_enabled_chk.isChecked():
            self.bath_periodicx_rampwidth_x_e.setEnabled(True)
            self.bath_periodicx_flatwidth_x_e.setEnabled(True)
        else:
            self.bath_periodicx_rampwidth_x_e.setEnabled(False)
            self.bath_periodicx_flatwidth_x_e.setEnabled(False)

    def on_bath_selection_toggled(self):
        """ Reacts to the selection checkbox being pressed. """
        if self.bath_selection_enabled_chk.isChecked():
            self.bath_selection_point_x_e.setEnabled(True)
            self.bath_selection_point_y_e.setEnabled(True)
            self.bath_selection_size_x_e.setEnabled(True)
            self.bath_selection_size_y_e.setEnabled(True)
        else:
            self.bath_selection_point_x_e.setEnabled(False)
            self.bath_selection_point_y_e.setEnabled(False)
            self.bath_selection_size_x_e.setEnabled(False)
            self.bath_selection_size_y_e.setEnabled(False)

    def on_bath_initdomain_toggled(self):
        """ Reacts to the initdomain checkbox being pressed. """
        if self.bath_initdomain_enabled_chk.isChecked():
            self.bath_initdomain_point_x_e.setEnabled(True)
            self.bath_initdomain_point_y_e.setEnabled(True)
            self.bath_initdomain_size_x_e.setEnabled(True)
            self.bath_initdomain_size_y_e.setEnabled(True)
        else:
            self.bath_initdomain_point_x_e.setEnabled(False)
            self.bath_initdomain_point_y_e.setEnabled(False)
            self.bath_initdomain_size_x_e.setEnabled(False)
            self.bath_initdomain_size_y_e.setEnabled(False)

    def on_file_path_change(self): #Check to delete
        """ Defines behaviour when the file path changes. """
        if "xyz" in self.geo_file_path.text().lower()[-4:]:
            pass
        else:
            pass

    def geo_ok_clicked(self):
        """ Defines ok button behaviour"""
        wait_dialog = WaitDialog("Geometry is being imported.Please wait")
        wait_dialog.show()
        try:
            self.execute_bathymetry_tool()
        except ValueError:
            error_dialog(__("There was an error with bathymetry tool"))

    def execute_bathymetry_tool(self):
        """ Executes bathymetry tool and returns the output path of the generated file. """

        export_process = QtCore.QProcess(get_fc_main_window())
        temp_dir = gettempdir()
        working_dialog = WorkingDialog(self)

        def on_export_finished():
            temp_bathymetry_file_path = "{}/output.stl".format(temp_dir)
            import_geo(filename=str(temp_bathymetry_file_path),
                       scale_x=1.0,
                       scale_y=1.0,
                       scale_z=1.0,
                       name=str(self.geo_objname_text.text()),
                       autofill=self.geo_autofill_chck.isChecked(),
                       case=Case.the())
            working_dialog.accept()

        executable_parameters = [
            "-loadpos",
            self.geo_file_path.text(),
            "-move:{}:{}:{}".format(self.bath_move_x_e.value(),self.bath_move_y_e.value(),self.bath_move_z_e.value()),
            "-rotate:{}:{}:{}".format(self.bath_rotate_x_e.value(),self.bath_rotate_y_e.value(),
                                     self.bath_rotate_z_e.value()),
            "-scale:{}:{}:{}".format(self.bath_scale_x_e.value(),self.bath_scale_y_e.value(),self.bath_scale_z_e.value())
        ]

        if self.bath_selection_enabled_chk.isChecked():
            executable_parameters.append(
                "-selposmin:{}:{}".format(self.bath_selection_point_x_e.value(),self.bath_selection_point_y_e.value()))
            executable_parameters.append(
                "-selsize:{}:{}".format(self.bath_selection_size_x_e.value(),self.bath_selection_size_y_e.value()))

        executable_parameters.append("-gdp:{}".format(self.bath_grid_dp_x_e.value()))

        if self.bath_initdomain_enabled_chk.isChecked():
            executable_parameters.append(
                "-gposmin:{}:{}".format(self.bath_initdomain_point_x_e.value(),self.bath_initdomain_point_y_e.value()))
            executable_parameters.append(
                "-gsize:{}:{}".format(self.bath_initdomain_size_x_e.value(),self.bath_initdomain_size_y_e.value()))

        if self.bath_xmin_check.isChecked():
            executable_parameters.append(
                "-gexpandxmin:{}:{}:{}:{}".format(self.bath_xmin_size_e.value(),self.bath_xmin_z_e.value(),
                                                 self.bath_xmin_size2_e.value(), self.bath_xmin_z2_e.value()))

        if self.bath_xmax_check.isChecked():
            executable_parameters.append(
                "-gexpandxmax:{}:{}:{}:{}".format(self.bath_xmax_size_e.value(),self.bath_xmax_z_e.value(),
                                                 self.bath_xmax_size2_e.value(), self.bath_xmax_z2_e.value()))

        if self.bath_ymin_check.isChecked():
            executable_parameters.append(
                "-gexpandymin:{}:{}:{}:{}".format(self.bath_ymin_size_e.value(),self.bath_ymin_z_e.value(),
                                                 self.bath_ymin_size2_e.value(), self.bath_ymin_z2_e.value()))

        if self.bath_ymax_check.isChecked():
            executable_parameters.append(
                "-gexpandymax:{}:{}:{}:{}".format(self.bath_ymax_size_e.value(),self.bath_ymax_z_e.value(),
                                                 self.bath_ymax_size2_e.value(), self.bath_ymax_z2_e.value()))

        if self.bath_periodicx_enabled_chk.isChecked():
            executable_parameters.append("-gperix:{}:{}".format(self.bath_periodicx_rampwidth_x_e.value(),
                                                               self.bath_periodicx_flatwidth_x_e.value()))

        if self.bath_periodicy_enabled_chk.isChecked():
            executable_parameters.append("-gperiy:{}:{}".format(self.bath_periodicy_rampwidth_x_e.value(),
                                                               self.bath_periodicy_flatwidth_x_e.value()))

        if self.bath_finalmove_enabled_chk.isChecked():
            executable_parameters.append(
                "-gmove:{}:{}:{}".format(self.bath_finalmove_x_e.value(),self.bath_finalmove_y_e.value(),
                                        self.bath_finalmove_z_e.value()))

        executable_parameters.append("-savegrid:stl:m")
        executable_parameters.append("{}/output.stl".format(temp_dir))

        self.save_default_data()

        export_process.finished.connect(on_export_finished)
        ensure_process_is_executable_or_fail(Case.the().executable_paths.bathymetrytool)
        log("Executing: {} {}".format(Case.the().executable_paths.bathymetrytool, " ".join(executable_parameters)))
        export_process.start(Case.the().executable_paths.bathymetrytool, executable_parameters)
        working_dialog.exec()

    def geo_dialog_browse(self):
        """ Defines the browse button behaviour."""
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"),
                                                                Case.the().info.last_used_directory,
                                                                "XYZ Files (*.xyz)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.geo_file_path.setText(file_name_temp)
        self.raise_()
        self.activateWindow()
        self.geo_button_ok.setFocus()



