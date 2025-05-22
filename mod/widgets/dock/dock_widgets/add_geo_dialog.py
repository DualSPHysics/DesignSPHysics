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
from mod.tools.freecad_tools import get_fc_main_window, get_fc_object
from mod.tools.stdout_tools import debug, log
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.dock.dock_widgets.surface_stl_dialog import SurfaceStlDialog
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.xml.importer import import_vtm_file


class WorkingDialog(QtWidgets.QDialog):
    """ A modal dialog to show during BathymetryTool execution. """

    IS_DIALOG_MODAL: bool = True

    def __init__(self, parent=None, object_type:str="Bathymetry"):
        super().__init__(parent=parent)
        self.setModal(self.IS_DIALOG_MODAL)
        self.setWindowTitle(__(f"Import {object_type}"))

        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(__(f"Importing {object_type}..."))

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.adjustSize()


class AddGeoDialog(QtWidgets.QDialog):
    """ A dialog that shows option to import a geometry passed as parameter """

    IS_DIALOG_MODAL: bool = True
    MINIMUM_WIDTH = 780

    def __init__(self, file_name, parent=None):
        super().__init__(parent=parent)

        self.setMinimumWidth(self.MINIMUM_WIDTH)

        self.vtm_mode=False

        # Defines import stl dialog
        self.setModal(self.IS_DIALOG_MODAL)
        self.setWindowTitle(__("Import Geometry"))
        self.geo_dialog_layout = QtWidgets.QVBoxLayout()
        self.geo_group = QtWidgets.QGroupBox(__("Import Geometry options"))
        self.geo_group_layout = QtWidgets.QVBoxLayout()

        #  GEO File selection
        self.geo_file_layout = QtWidgets.QHBoxLayout()
        self.geo_file_label = QtWidgets.QLabel(__("Geometry File: "))
        self.geo_file_path = QtWidgets.QLineEdit()
        self.geo_file_browse = QtWidgets.QPushButton(__("Browse"))
        self.geo_surface_stl_button = QtWidgets.QPushButton(__("SurfaceSTL"))
        self.geo_surface_stl_button.setEnabled(False)
        self.geo_surface_stl_button.clicked.connect(self.on_surface_stl)

        for x in [self.geo_file_label, self.geo_file_path, self.geo_file_browse,self.geo_surface_stl_button]:
            self.geo_file_layout.addWidget(x)


        # Scaling factor
        self.geo_scaling_widget = QtWidgets.QWidget()
        self.geo_scaling_layout = QtWidgets.QHBoxLayout()
        self.geo_scaling_label = QtWidgets.QLabel(__("Scaling factor: "))
        self.geo_scaling_x_l = QtWidgets.QLabel("X: ")
        self.geo_scaling_x_e = ValueInput(value=1.0)
        self.geo_scaling_y_l = QtWidgets.QLabel("Y: ")
        self.geo_scaling_y_e = ValueInput(value=1.0)
        self.geo_scaling_z_l = QtWidgets.QLabel("Z: ")
        self.geo_scaling_z_e = ValueInput(value=1.0)

        for x in [self.geo_scaling_label,
                  self.geo_scaling_x_l,
                  self.geo_scaling_x_e,
                  self.geo_scaling_y_l,
                  self.geo_scaling_y_e,
                  self.geo_scaling_z_l,
                  self.geo_scaling_z_e, ]:
            self.geo_scaling_layout.addWidget(x)
        self.geo_scaling_layout.setContentsMargins(0, 0, 0, 0)
        self.geo_scaling_widget.setLayout(self.geo_scaling_layout)
        # END Scaling factor

        # Import object name
        self.geo_objname_layout = QtWidgets.QHBoxLayout()
        self.geo_objname_label = QtWidgets.QLabel(__("Import object name: "))
        self.geo_objname_text = QtWidgets.QLineEdit("GEO_{}".format(file_name.split("/")[-1]).split(".")[0].replace("-", "_"))
        for x in [self.geo_objname_label, self.geo_objname_text]:
            self.geo_objname_layout.addWidget(x)
        # End object name

        #Advanced Draw
        self.adv_draw_layout=QtWidgets.QHBoxLayout()
        self.adv_draw_label=QtWidgets.QLabel("Advanced Draw Mode")
        self.adv_draw_enabled_checkbox=QtWidgets.QCheckBox(__("Enabled"))
        self.adv_draw_reverse_checkbox = QtWidgets.QCheckBox(__("Reverse"))
        self.adv_draw_mindepth_checkbox = QtWidgets.QCheckBox(__("MinDepth(Dp)"))
        self.adv_draw_mindepth_input = ValueInput(value=0.1)
        self.adv_draw_maxdepth_checkbox=QtWidgets.QCheckBox(__("MaxDepth(Dp)"))
        self.adv_draw_maxdepth_input=ValueInput(value=3.0)
        for x in [self.adv_draw_label,self.adv_draw_enabled_checkbox,self.adv_draw_reverse_checkbox,
                  self.adv_draw_mindepth_checkbox,self.adv_draw_mindepth_input,self.adv_draw_maxdepth_checkbox,
                  self.adv_draw_maxdepth_input]:
            self.adv_draw_layout.addWidget(x)

        # Autofill
        self.geo_autofil_layout = QtWidgets.QHBoxLayout()
        self.geo_autofill_chck = QtWidgets.QCheckBox("Autofill")
        self.geo_autofil_layout.addWidget(self.geo_autofill_chck)
        self.geo_draw_as_points_chck = QtWidgets.QCheckBox("Draw as points")
        self.geo_autofil_layout.addWidget(self.geo_draw_as_points_chck)

        # Decimate
        self.geo_decimate_layout = QtWidgets.QHBoxLayout()
        self.geo_decimate_chck = QtWidgets.QCheckBox("Decimate")
        self.geo_decimate_layout.addWidget(self.geo_decimate_chck)
        self.geo_decimate_reduction_label=QtWidgets.QLabel(__("Reduction(0 to 1)"))
        self.geo_decimate_reduction_input = ValueInput(value=0.9)
        #Surface selection
        self.surface_selection_layout = QtWidgets.QHBoxLayout()
        self.geo_vtm_select_all_button = QtWidgets.QPushButton("Select All")
        self.geo_vtm_select_none_button = QtWidgets.QPushButton("Select None")
        self.geo_vtm_first_mkbound_label = QtWidgets.QLabel("First MkBound")
        self.geo_vtm_first_mkbound = IntValueInput(value=0)
        self.geo_vtm_set_first_mkbound_button= QtWidgets.QPushButton("Set mkbounds")

        self.geo_decimate_layout.addWidget(self.geo_decimate_reduction_label)
        self.geo_decimate_layout.addWidget(self.geo_decimate_reduction_input)
        self.surface_selection_layout.addWidget(self.geo_vtm_select_all_button)
        self.surface_selection_layout.addWidget(self.geo_vtm_select_none_button)
        self.surface_selection_layout.addWidget(self.geo_vtm_first_mkbound_label)
        self.surface_selection_layout.addWidget(self.geo_vtm_first_mkbound)
        self.surface_selection_layout.addWidget(self.geo_vtm_set_first_mkbound_button)
        self.geo_decimate_chck.clicked.connect(self.on_decimate_enable)
        self.geo_vtm_select_all_button.clicked.connect(self.on_vtm_select_all)
        self.geo_vtm_select_none_button.clicked.connect(self.on_vtm_select_none)
        self.geo_vtm_set_first_mkbound_button.clicked.connect(self.on_set_mkbounds_from)


        self.vtm_options_scroll = QtWidgets.QScrollArea() #"Import VTM options"
        self.vtm_options_scroll.setMinimumWidth(400)
        self.vtm_options_scroll.setWidgetResizable(True)
        self.vtm_options_scroll_widget = QtWidgets.QWidget()
        self.vtm_options_scroll_widget.setMinimumWidth(400)

        
        self.vtm_options_scroll.setWidget(self.vtm_options_scroll_widget)
        self.vtm_options_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vtm_options_layout=QtWidgets.QVBoxLayout()
        self.vtm_options_scroll_widget.setLayout(self.vtm_options_layout)
        
        self.vtm_surfaces_layout_list=[]
        self.vtm_surfaces_list = []


        self.geo_group_layout.addLayout(self.geo_file_layout)
        self.geo_group_layout.addWidget(self.geo_scaling_widget)
        self.geo_group_layout.addLayout(self.geo_objname_layout)
        self.geo_group_layout.addLayout(self.adv_draw_layout)
        self.geo_group_layout.addLayout(self.geo_autofil_layout)
        self.geo_group_layout.addLayout(self.geo_decimate_layout)
        self.geo_group_layout.addLayout(self.surface_selection_layout)
        self.geo_group_layout.addWidget(self.vtm_options_scroll)
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
        self.adv_draw_enabled_checkbox.stateChanged.connect(self.on_adv_draw_enable)
        self.adv_draw_mindepth_checkbox.stateChanged.connect(self.on_adv_draw_mindepth)
        self.adv_draw_maxdepth_checkbox.stateChanged.connect(self.on_adv_draw_maxdepth)

        self.geo_file_path.setText(file_name)

        self.geo_button_ok.setFocus()
        self.on_adv_draw_enable(False)
        self.on_file_path_change()



    def on_file_path_change(self):
        """ Defines behaviour when the file path changes. """
        if "vtm" in self.geo_file_path.text().lower()[-4:]:
            self.geo_scaling_widget.setVisible(True)
            self.geo_autofill_chck.setVisible(True)
            self.geo_objname_text.setVisible(False)
            self.geo_objname_label.setVisible(False)
            self.vtm_options_scroll.setVisible(True)
            self.vtm_mode = True
            vtm_surfaces_file = import_vtm_file(self.geo_file_path.text())
            self.vtm_surfaces_list = vtm_surfaces_file["VTKFile"]["vtkMultiBlockDataSet"]["Block"]["DataSet"]
            if not isinstance(self.vtm_surfaces_list, list):
                self.vtm_surfaces_list=[self.vtm_surfaces_list]
            self.geo_decimate_layout.addLayout(self.surface_selection_layout)
            self.geo_vtm_set_first_mkbound_button.setVisible(True)
            self.geo_vtm_first_mkbound_label.setVisible(True)
            self.geo_vtm_first_mkbound.setVisible(True)
            self.geo_vtm_select_all_button.setVisible(True)
            self.geo_vtm_select_none_button.setVisible(True)
            self.update_vtm_list()
        else: #Vtk, Stl
            self.geo_scaling_widget.setVisible(True)
            self.geo_autofill_chck.setVisible(True)
            self.geo_objname_text.setVisible(True)
            self.geo_objname_label.setVisible(True)
            self.vtm_options_scroll.setVisible(False)
            self.vtm_mode = False
            self.geo_vtm_set_first_mkbound_button.setVisible(False)
            self.geo_vtm_first_mkbound_label.setVisible(False)
            self.geo_vtm_first_mkbound.setVisible(False)
            self.geo_vtm_select_all_button.setVisible(False)
            self.geo_vtm_select_none_button.setVisible(False)
        self.geo_surface_stl_button.setEnabled(False)
        if "stl" in self.geo_file_path.text().lower()[-4:] and Case.the().executable_paths.surfacesstl:
            self.geo_surface_stl_button.setEnabled(True)

    def geo_ok_clicked(self):
        """ Defines ok button behaviour"""
        wait_dialog = WaitDialog("Geometry is being imported.Please wait")
        wait_dialog.show()
        if self.vtm_mode:
            for surf in self.vtm_surfaces_list:
                wait_dialog.update_info(f"Loading surface n {surf['@index']} named {surf['@name']}")
                try:
                    if self.vtm_surfaces_layout_list[int(surf["@index"])].vtm_surface_include.isChecked() :
                        import_geo(filename=os.path.dirname(self.geo_file_path.text())+ os.sep + surf["@file"],
                                   scale_x=self.geo_scaling_x_e.value(),
                                   scale_y=self.geo_scaling_y_e.value(),
                                   scale_z=self.geo_scaling_z_e.value(),
                                   name=(surf["@name"]),
                                   autofill=self.geo_autofill_chck.isChecked(),
                                   case=Case.the(),
                                   adm=self.adv_draw_enabled_checkbox.isChecked(),
                                   adm_reverse=self.adv_draw_reverse_checkbox.isChecked(),
                                   has_adm_mindepth=self.adv_draw_mindepth_checkbox.isChecked(),
                                   adm_mindepth=self.adv_draw_mindepth_input.value(),
                                   has_adm_maxdepth=self.adv_draw_maxdepth_checkbox.isChecked(),
                                   adm_maxdepth=self.adv_draw_maxdepth_input.value(),
                                   desired_mkbound=self.vtm_surfaces_layout_list[int(surf["@index"])].vtm_surface_mk.value(),
                                   draw_as_points=self.geo_draw_as_points_chck.isChecked(),
                                   decimate=self.geo_decimate_chck.isChecked(),
                                   reduction=self.geo_decimate_reduction_input.value()
                                   )
                except ValueError as err:
                    error_dialog(__(f"There was an loading error surface {surf['@name']}: {err.with_traceback(__tb=None).__str__()}"))

        else:
            name=self.geo_objname_text.text()
            internal_name = "external_{}".format(name).replace("-", "_")
            if get_fc_object(internal_name):  #If there is no object with the same name in FreeCAD
                warning_dialog("There is already an object in FreeCAD with this name. Choose another name")
                wait_dialog.close_dialog()
                return
            import_geo(filename=self.geo_file_path.text(),
                   scale_x=self.geo_scaling_x_e.value(),
                   scale_y=self.geo_scaling_y_e.value(),
                   scale_z=self.geo_scaling_z_e.value(),
                   name=name,
                   autofill=self.geo_autofill_chck.isChecked(),
                   case=Case.the(),
                   adm=self.adv_draw_enabled_checkbox.isChecked(),
                   adm_reverse=self.adv_draw_reverse_checkbox.isChecked(),
                   has_adm_mindepth=self.adv_draw_mindepth_checkbox.isChecked(),
                   adm_mindepth=self.adv_draw_mindepth_input.value(),
                   has_adm_maxdepth=self.adv_draw_maxdepth_checkbox.isChecked(),
                   adm_maxdepth= self.adv_draw_maxdepth_input.value(),
                   draw_as_points = self.geo_draw_as_points_chck.isChecked(),
                   decimate=self.geo_decimate_chck.isChecked(),
                   reduction=self.geo_decimate_reduction_input.value()
                   )
        wait_dialog.close_dialog()
        self.accept()


    def geo_dialog_browse(self):
        """ Defines the browse button behaviour."""
        file_name_temp, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"),
                                                                Case.the().info.last_used_directory, "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk);;VTU Files (*.vtu);;VTM Files (*.vtm)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.geo_file_path.setText(file_name_temp)
        self.raise_()
        self.activateWindow()
        self.geo_button_ok.setFocus()

    def on_adv_draw_enable(self,state):
        for x in [self.adv_draw_reverse_checkbox,self.adv_draw_maxdepth_checkbox,self.adv_draw_mindepth_checkbox,
                  self.adv_draw_maxdepth_input,self.adv_draw_mindepth_input]:
            x.setEnabled(state)
        if state:
            self.on_adv_draw_mindepth(self.adv_draw_mindepth_checkbox.isChecked())
            self.on_adv_draw_maxdepth(self.adv_draw_maxdepth_checkbox.isChecked())
        self.geo_autofill_chck.setEnabled(not state)

    def on_adv_draw_mindepth(self,state):
        self.adv_draw_mindepth_input.setEnabled(state)

    def on_adv_draw_maxdepth(self,state):
        self.adv_draw_maxdepth_input.setEnabled(state)

    def update_vtm_list(self):
        self.vtm_surfaces_layout_list = []
        for surf in self.vtm_surfaces_list:
            self.vtm_surfaces_layout_list.append(vtm_surface_widget(surf["@index"],surf["@name"]))
            self.vtm_options_layout.addLayout(self.vtm_surfaces_layout_list[int(surf["@index"])])

    def on_decimate_enable(self, state):
        self.geo_decimate_reduction_input.setEnabled(state)

    def on_surface_stl(self):
        dialog = SurfaceStlDialog(self.geo_file_path.text(), parent=None)
        res=dialog.exec_()
        if res==QtWidgets.QDialog.Accepted:
            filedir = dirname(self.geo_file_path.text())
            file_out = os.path.basename(self.geo_file_path.text()).replace("stl", "vtm")
            dir = filedir
            vtmout = f"{dir}{os.sep}{file_out}"
            self.geo_file_path.setText(vtmout)

    def on_vtm_select_all(self):
        for w in self.vtm_surfaces_layout_list:
            w.vtm_surface_include.setChecked(True)
    def on_vtm_select_none(self):
        for w in self.vtm_surfaces_layout_list:
            w.vtm_surface_include.setChecked(False)
    def on_set_mkbounds_from(self):
        i=self.geo_vtm_first_mkbound.value()
        for w in self.vtm_surfaces_layout_list:
            if w.vtm_surface_include.isChecked():
                w.vtm_surface_mk.setValue(i)
                i=i+1
            else:
                w.vtm_surface_mk.setValue(-1)


class vtm_surface_widget(QtWidgets.QHBoxLayout):
    def __init__(self, surface_index , surface_name, parent = None):
        super().__init__(parent = parent)
        self.vtm_surface_id_label = QtWidgets.QLabel(surface_index)
        self.vtm_surface_id_label.setMaximumWidth(25)
        self.vtm_surface_name_label = QtWidgets.QLabel(surface_name)
        self.vtm_surface_include = QtWidgets.QCheckBox(__("Include surface"))
        self.vtm_surface_include.setChecked(True)
        self.vtm_surface_include.stateChanged.connect(self.on_include_surface_change)
        self.vtm_surface_mkbound_label = QtWidgets.QLabel("MkBound:")
        self.vtm_surface_mk = IntValueInput(min_val=0,max_val=999,maxwidth=50,value=surface_index)
        self.vtm_surface_mk_layout=QtWidgets.QHBoxLayout()
        self.vtm_surface_mk_layout.addWidget(self.vtm_surface_mkbound_label,stretch=0)
        self.vtm_surface_mk_layout.addWidget(self.vtm_surface_mk,stretch=0)
        for x in [self.vtm_surface_id_label,self.vtm_surface_name_label,self.vtm_surface_include]:
            self.addWidget(x,stretch=1)
        self.addLayout(self.vtm_surface_mk_layout,stretch=1)

    def on_include_surface_change(self,enabled):
        self.vtm_surface_mk.setEnabled(enabled)

