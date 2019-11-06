#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics FlowTool Config and Execution Dialog."""

from PySide import QtGui

from mod.translation_tools import __
from mod.file_tools import create_flowtool_boxes
from mod.post_processing_tools import flowtool_export
from mod.freecad_tools import get_fc_main_window

from mod.dataobjects.case import Case
from mod.dataobjects.flow_tool_box import FlowToolBox

from mod.widgets.postprocessing.flowtool_box_edit_dialog import FlowToolBoxEditDialog


class FlowToolDialog(QtGui.QDialog):
    """ DesignSPHysics FlowTool Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("FlowTool Tool"))
        self.flowtool_tool_layout = QtGui.QVBoxLayout()

        self.fltool_boxlist_groupbox = QtGui.QGroupBox(__("List of boxes"))
        self.fltool_csvname_layout = QtGui.QHBoxLayout()
        self.fltool_vtkname_layout = QtGui.QHBoxLayout()
        self.fltool_parameters_layout = QtGui.QHBoxLayout()
        self.fltool_buttons_layout = QtGui.QHBoxLayout()

        self.fltool_boxlist_groupbox_layout = QtGui.QVBoxLayout()

        self.fltool_addbox_layout = QtGui.QHBoxLayout()
        self.fltool_addbox_button = QtGui.QPushButton(__("New Box"))
        self.fltool_addbox_layout.addStretch(1)
        self.fltool_addbox_layout.addWidget(self.fltool_addbox_button)

        self.fltool_boxlist_layout = QtGui.QVBoxLayout()

        self.fltool_boxlist_groupbox_layout.addLayout(self.fltool_addbox_layout)
        self.fltool_boxlist_groupbox_layout.addLayout(self.fltool_boxlist_layout)
        self.fltool_boxlist_groupbox.setLayout(self.fltool_boxlist_groupbox_layout)

        self.fltool_csv_file_name_label = QtGui.QLabel(__("CSV file name"))
        self.fltool_csv_file_name_text = QtGui.QLineEdit()
        self.fltool_csv_file_name_text.setText("_ResultFlow")
        self.fltool_csvname_layout.addWidget(self.fltool_csv_file_name_label)
        self.fltool_csvname_layout.addWidget(self.fltool_csv_file_name_text)

        self.fltool_vtk_file_name_label = QtGui.QLabel(__("VTK file name"))
        self.fltool_vtk_file_name_text = QtGui.QLineEdit()
        self.fltool_vtk_file_name_text.setText("Boxes")
        self.fltool_vtkname_layout.addWidget(self.fltool_vtk_file_name_label)
        self.fltool_vtkname_layout.addWidget(self.fltool_vtk_file_name_text)

        self.fltool_parameters_label = QtGui.QLabel(__("Additional Parameters"))
        self.fltool_parameters_text = QtGui.QLineEdit()
        self.fltool_parameters_layout.addWidget(self.fltool_parameters_label)
        self.fltool_parameters_layout.addWidget(self.fltool_parameters_text)

        self.fltool_export_button = QtGui.QPushButton(__("Export"))
        self.fltool_cancel_button = QtGui.QPushButton(__("Cancel"))
        self.fltool_buttons_layout.addWidget(self.fltool_export_button)
        self.fltool_buttons_layout.addWidget(self.fltool_cancel_button)

        self.flowtool_tool_layout.addWidget(self.fltool_boxlist_groupbox)
        self.flowtool_tool_layout.addStretch(1)
        self.flowtool_tool_layout.addLayout(self.fltool_csvname_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_vtkname_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_parameters_layout)
        self.flowtool_tool_layout.addLayout(self.fltool_buttons_layout)

        self.setLayout(self.flowtool_tool_layout)

        self.fltool_addbox_button.clicked.connect(self.on_fltool_addbox)
        self.fltool_export_button.clicked.connect(self.on_fltool_export)
        self.fltool_cancel_button.clicked.connect(self.on_fltool_cancel)
        self.refresh_boxlist()
        self.exec_()

    def box_edit(self, box_id):
        """ Box edit button behaviour. Opens a dialog to edit the selected FlowTool Box"""
        FlowToolBoxEditDialog(box_id, parent=get_fc_main_window())
        self.refresh_boxlist()

    def box_delete(self, box_id):
        """ Box delete button behaviour. Tries to find the box for which the button was pressed and deletes it."""
        box_to_remove = None

        for box in Case.the().flowtool_boxes:
            if box.id == box_id:
                box_to_remove = box

        if box_to_remove is not None:
            Case.the().flowtool_boxes.remove(box_to_remove)
            self.refresh_boxlist()

    def refresh_boxlist(self):
        """ Refreshes the FlowTool box list."""
        while self.fltool_boxlist_layout.count() > 0:
            target = self.fltool_boxlist_layout.takeAt(0)
            target.setParent(None)

        for box in Case.the().flowtool_boxes:
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel(str(box.name))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, b=box.id: self.box_edit(b))
            to_add_deletebutton.clicked.connect(lambda _=False, b=box.id: self.box_delete(b))
            self.fltool_boxlist_layout.addLayout(to_add_layout)

    def on_fltool_addbox(self):
        """ Adds a box to the data structure."""
        Case.the().flowtool_boxes.append(FlowToolBox())
        self.refresh_boxlist()

    def on_fltool_cancel(self):
        """ FlowTool cancel button behaviour."""
        self.reject()

    def on_fltool_export(self):
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

        create_flowtool_boxes(Case.the().path + "/" + "fileboxes.txt", Case.the().flowtool_boxes)

        flowtool_export(export_parameters, Case.the(), self.post_processing_widget)
        self.accept()
