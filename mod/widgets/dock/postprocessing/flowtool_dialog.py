#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics FlowTool Config and Execution Dialog."""
import os

import FreeCAD
from PySide2 import QtWidgets
from mod.constants import FLOWBOXES_GROUP_NAME, FLOWBOXES_COLOR
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.dataobjects.flow_tool_xml_box import FlowToolXmlBox
from mod.enums import FlowUnits
from mod.tools.freecad_tools import draw_box, get_fc_object, update_flow_box, delete_object
from mod.tools.post_processing_tools import flowtool_export
from mod.tools.template_tools import get_template_text
from mod.tools.translation_tools import __
from mod.widgets.dock.postprocessing.flowtool_xml_box_dialog import FlowToolXmlBoxDialog

flow_units_list=[FlowUnits.LITERSSECOND,FlowUnits.GALLONSMIN,FlowUnits.GALLONSSECOND]

TEMPLATE_BOX_BASE=os.sep+"templates"+os.sep+"flowtool"+os.sep+ "base.xml"
TEMPLATE_BOX_EACH=os.sep+"templates"+os.sep+"flowtool"+os.sep+ "each.xml"

class FlowToolDialog(QtWidgets.QDialog):
    """ DesignSPHysics FlowTool Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("Flow Tool"))
        self.flowtool_tool_layout = QtWidgets.QVBoxLayout()

        self.fltool_boxlist_groupbox = QtWidgets.QGroupBox(__("List of boxes"))
        self.fltool_loadxml_groupbox = QtWidgets.QGroupBox(__("Load xml file"))
        self.fltool_csvname_layout = QtWidgets.QHBoxLayout()
        self.fltool_vtkname_layout = QtWidgets.QHBoxLayout()
        self.fltool_parameters_layout = QtWidgets.QHBoxLayout()
        self.fltool_buttons_layout = QtWidgets.QHBoxLayout()

        self.fltool_combo_layout = QtWidgets.QHBoxLayout()
        self.fltool_combo_label = QtWidgets.QLabel(__("Flowtool: "))
        self.fltool_combo = QtWidgets.QComboBox()
        self.fltool_combo.addItems(["Create flow boxes", "Use existing xml file"])
        self.fltool_combo.currentIndexChanged.connect(self.on_fltool_combo_change)
        self.fltool_combo_layout.addWidget(self.fltool_combo_label)
        self.fltool_combo_layout.addWidget(self.fltool_combo)

        self.fltool_pages_widget = QtWidgets.QStackedWidget(None)

        self.fltool_boxlist_groupbox_layout = QtWidgets.QVBoxLayout()

        self.fltool_addbox_layout = QtWidgets.QHBoxLayout()
        self.fltool_addbox_button = QtWidgets.QPushButton(__("New Box"))
        self.fltool_addbox_layout.addStretch(1)
        self.fltool_addbox_layout.addWidget(self.fltool_addbox_button)

        self.units_layout = QtWidgets.QHBoxLayout()
        self.units_label = QtWidgets.QLabel(__("Units for flow calculation:"))
        self.units_combo = QtWidgets.QComboBox()
        self.units_combo.addItems(flow_units_list)
        self.units_combo.setCurrentIndex(flow_units_list.index(Case.the().post_processing_settings.flowtool_units))
        self.units_layout.addWidget(self.units_label)
        self.units_layout.addWidget(self.units_combo)

        self.xmlsave_layout = QtWidgets.QHBoxLayout()
        self.xmlsave_label = QtWidgets.QLabel(__("Xml file save name"))
        self.xmlsave_input = QtWidgets.QLineEdit(__("flow_boxes.xml"))
        self.xmlsave_layout.addWidget(self.xmlsave_label)
        self.xmlsave_layout.addWidget(self.xmlsave_input)

        self.fltool_boxlist_layout = QtWidgets.QVBoxLayout()

        self.fltool_boxlist_groupbox_layout.addLayout(self.fltool_addbox_layout)
        self.fltool_boxlist_groupbox_layout.addLayout(self.fltool_boxlist_layout)
        self.fltool_boxlist_groupbox_layout.addLayout(self.units_layout)
        self.fltool_boxlist_groupbox_layout.addLayout(self.xmlsave_layout)


        self.fltool_boxlist_groupbox.setLayout(self.fltool_boxlist_groupbox_layout)
        self.fltool_loadxml_groupbox_layout = QtWidgets.QVBoxLayout()

        self.fltool_loadxml_layout = QtWidgets.QHBoxLayout()
        self.fltool_loadxml_filename_label = QtWidgets.QLabel(__("Filename"))
        self.fltool_loadxml_path_input = QtWidgets.QLineEdit()
        self.fltool_loadxml_layout.addWidget(self.fltool_loadxml_filename_label)
        self.fltool_loadxml_layout.addWidget(self.fltool_loadxml_path_input)

        self.fltool_loadxml_groupbox_layout.addLayout(self.fltool_loadxml_layout)
        self.fltool_loadxml_groupbox.setLayout(self.fltool_loadxml_groupbox_layout)

        self.fltool_csv_file_name_label = QtWidgets.QLabel(__("CSV file name"))
        self.fltool_csv_file_name_text = QtWidgets.QLineEdit()
        self.fltool_csv_file_name_text.setText("_ResultFlow")
        self.fltool_csvname_layout.addWidget(self.fltool_csv_file_name_label)
        self.fltool_csvname_layout.addWidget(self.fltool_csv_file_name_text)

        self.fltool_vtk_file_name_checkbox = QtWidgets.QCheckBox(__("Save VTK files"))
        self.fltool_vtk_file_name_label = QtWidgets.QLabel(__("VTK file name"))
        self.fltool_vtk_file_name_text = QtWidgets.QLineEdit()
        self.fltool_vtk_file_name_text.setText("Boxes")
        self.fltool_vtk_file_name_text.setEnabled(False)

        self.fltool_vtkname_layout.addWidget(self.fltool_vtk_file_name_checkbox)
        self.fltool_vtkname_layout.addWidget(self.fltool_vtk_file_name_label)
        self.fltool_vtkname_layout.addWidget(self.fltool_vtk_file_name_text)

        self.fltool_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.fltool_parameters_text = QtWidgets.QLineEdit()


        self.fltool_parameters_layout.addWidget(self.fltool_parameters_label)
        self.fltool_parameters_layout.addWidget(self.fltool_parameters_text)

        self.fltool_export_button = QtWidgets.QPushButton(__("Export"))
        self.fltool_generate_script_button = QtWidgets.QPushButton(__("Generate script"))
        self.fltool_generate_xml_button = QtWidgets.QPushButton(__("Generate xml file"))
        self.fltool_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.fltool_buttons_layout.addWidget(self.fltool_export_button)
        if not ApplicationSettings.the().basic_visualization:
            self.fltool_buttons_layout.addWidget(self.fltool_generate_script_button)
            self.fltool_buttons_layout.addWidget(self.fltool_generate_xml_button)
        self.fltool_buttons_layout.addWidget(self.fltool_cancel_button)

        self.fltool_pages_widget.addWidget(self.fltool_boxlist_groupbox)
        self.fltool_pages_widget.addWidget(self.fltool_loadxml_groupbox)

        self.flowtool_tool_layout.addLayout(self.fltool_combo_layout)
        self.flowtool_tool_layout.addWidget(self.fltool_pages_widget)

        self.flowtool_tool_layout.addStretch(1)
        self.flowtool_tool_layout.addLayout(self.fltool_csvname_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_vtkname_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_parameters_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_buttons_layout)

        self.setLayout(self.flowtool_tool_layout)

        self.fltool_addbox_button.clicked.connect(self.on_fltool_addbox)
        self.fltool_export_button.clicked.connect(self.on_fltool_local_run)
        self.fltool_generate_script_button.clicked.connect(self.on_fltool_generate_script)
        self.fltool_generate_xml_button.clicked.connect(self.on_fltool_generate_xml)
        self.fltool_cancel_button.clicked.connect(self.on_fltool_cancel)
        self.fltool_vtk_file_name_checkbox.stateChanged.connect(self.on_vtk_changed)
        self.refresh_boxlist()
        self.exec_()

    def on_fltool_combo_change(self):
        index = self.fltool_combo.currentIndex()
        self.fltool_pages_widget.setCurrentIndex(index)
        self.fltool_generate_xml_button.setEnabled(not index)

    def on_vtk_changed(self):
        state = self.fltool_vtk_file_name_checkbox.isChecked()
        self.fltool_vtk_file_name_text.setEnabled(state)


    def box_edit(self, box_id):
        """ Box edit button behaviour. Opens a dialog to edit the selected FlowTool Box"""
        dialog=FlowToolXmlBoxDialog(box_id, parent=None)
        dialog.exec_()
        self.refresh_boxlist()

    def box_delete(self, box_id):
        """ Box delete button behaviour. Tries to find the box for which the button was pressed and deletes it."""
        box_to_remove = None

        for box in Case.the().post_processing_settings.flowtool_xml_boxes:
            if box.id == box_id:
                box_to_remove = box

        if box_to_remove is not None:
            delete_object(box_to_remove.fc_object_name)
            Case.the().post_processing_settings.flowtool_xml_boxes.remove(box_to_remove)
            self.refresh_boxlist()

    def refresh_boxlist(self):
        """ Refreshes the FlowTool box list."""
        #Should delete all the list but does not work
        for child in self.fltool_boxlist_layout.children():
            child.takeAt(0).widget().setParent(None)
            child.takeAt(0)
            child.takeAt(0).widget().setParent(None)
            child.takeAt(0).widget().setParent(None)
            child.setParent(None)


        for box in Case.the().post_processing_settings.flowtool_xml_boxes:
            to_add_layout = QtWidgets.QHBoxLayout()
            to_add_label = QtWidgets.QLabel(str(box.name))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtWidgets.QPushButton("Edit")
            to_add_deletebutton = QtWidgets.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, b=box.id: self.box_edit(b))
            to_add_deletebutton.clicked.connect(lambda _=False, b=box.id: self.box_delete(b))
            self.fltool_boxlist_layout.addLayout(to_add_layout)
            if box.fc_object_name:
                update_flow_box(box.fc_object_name,box.point,box.size,box.angle)



    def on_fltool_addbox(self):
        """ Adds a box to the data structure."""
        newbox=FlowToolXmlBox()
        newbox.fc_object_name=draw_box([0,0,0],[0,0,0],"Helper_flow_box",color=FLOWBOXES_COLOR)
        FreeCAD.ActiveDocument.getObject(FLOWBOXES_GROUP_NAME).addObject(get_fc_object(newbox.fc_object_name))
        Case.the().post_processing_settings.flowtool_xml_boxes.append(newbox)
        self.box_edit(newbox.id)
        self.refresh_boxlist()

    def on_fltool_cancel(self):
        """ FlowTool cancel button behaviour."""
        self.reject()

    def on_fltool_generate_xml(self):
        boxes=""
        for box in Case.the().post_processing_settings.flowtool_xml_boxes:
            if box.divide_axis:
                box.first_box_name=f'name1="{box.name}a"'
                box.second_box_name=f'name2="{box.name}b"'
                box.divide_string=f'\n        <divide axis="{box.axis}" />'
                box.boxtype="boxanglediv"
            else:
                box.first_box_name = f'name="{box.name}"'
                box.second_box_name = ""
                box.divide_string = ""
                box.boxtype = "boxangle"
            boxes=boxes + get_template_text(TEMPLATE_BOX_EACH).format(**vars(box))
        if boxes:
            export=get_template_text(TEMPLATE_BOX_BASE).format(units=Case.the().post_processing_settings.flowtool_units,each=boxes)
            with open("{}{}{}".format(Case.the().path, os.sep,self.xmlsave_input.text()), "w", encoding="utf-8") as file:
                file.write(export)


    def on_fltool_local_run(self):
        self.on_fltool_export(False)
    def on_fltool_generate_script(self):
        self.on_fltool_export(True)
    def on_fltool_export(self,generate_script):
        """ FlowTool export button behaviour."""
        export_parameters = dict()

        if self.fltool_csv_file_name_text.text():
            export_parameters["csv_name"] = self.fltool_csv_file_name_text.text()
        else:
            export_parameters["csv_name"] = "_ResultFlow"

        if self.fltool_vtk_file_name_text.text():
            export_parameters["vtk_name"] = self.fltool_vtk_file_name_text.text()
        else:
            export_parameters["vtk_name"] = "Boxes"

        if self.fltool_parameters_text.text():
            export_parameters["additional_parameters"] = self.fltool_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""

        if self.fltool_combo.currentIndex()==0:
            self.on_fltool_generate_xml()
            flowtool_export(export_parameters, Case.the(), self.post_processing_widget,self.xmlsave_input.text(),generate_script,self.fltool_vtk_file_name_checkbox.isChecked())
        else:
            flowtool_export(export_parameters, Case.the(), self.post_processing_widget, self.fltool_loadxml_path_input.text(),generate_script,self.fltool_vtk_file_name_checkbox.isChecked())
        self.accept()
