#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Chrono configuration dialog.'''

import uuid

import FreeCAD
from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import debug

from mod.widgets.chrono_object_check_options import ChronoObjectCheckOptions
from mod.widgets.link_hinge_edit import LinkHingeEdit
from mod.widgets.link_linear_spring_edit import LinkLinearspringEdit
from mod.widgets.link_spheric_edit import LinkSphericEdit
from mod.widgets.link_point_line_edit import LinkPointlineEdit


class ChronoConfigDialog(QtGui.QDialog):
    ''' Defines the Chrono dialog window.
    Modifies data dictionary passed as parameter. '''

    def __init__(self):
        super(ChronoConfigDialog, self).__init__()

        # Creates a dialog
        self.setWindowTitle("Chrono configuration")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.main_layout = QtGui.QVBoxLayout()

        # Option for saves CSV with data exchange for each time interval
        self.csv_option_layout = QtGui.QHBoxLayout()
        self.csv_intervals_checkbox = QtGui.QCheckBox()
        if self.data['csv_intervals_check']:
            self.csv_intervals_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.csv_intervals_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.csv_intervals_checkbox.toggled.connect(self.on_csv_intervals_check)
        self.csv_intervals_option = QtGui.QLabel(__("CSV intervals:"))
        self.csv_intervals_line_edit = QtGui.QLineEdit(str(self.data['csv_intervals']))
        self.csv_option_layout.addWidget(self.csv_intervals_checkbox)
        self.csv_option_layout.addWidget(self.csv_intervals_option)
        self.csv_option_layout.addWidget(self.csv_intervals_line_edit)

        # Option for define scale used to create the initial scheme of Chrono objects
        self.scale_scheme_option_layout = QtGui.QHBoxLayout()
        self.scale_scheme_checkbox = QtGui.QCheckBox()
        if self.data['scale_scheme_check']:
            self.scale_scheme_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.scale_scheme_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.scale_scheme_checkbox.toggled.connect(self.on_scale_scheme_checkbox)
        self.scale_scheme_option = QtGui.QLabel(__("Scale for scheme:"))
        self.scale_scheme_line_edit = QtGui.QLineEdit(str(self.data['scale_scheme']))
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_checkbox)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_option)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_line_edit)

        # Option for allow collision overlap according Dp
        self.collisiondp_option_layout = QtGui.QHBoxLayout()
        self.collisiondp_checkbox = QtGui.QCheckBox()
        if self.data['collisiondp_check']:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.collisiondp_checkbox.toggled.connect(self.on_collisiondp_checkbox)
        self.collisiondp_option = QtGui.QLabel(__("Collision Dp:"))
        self.collisiondp_line_edit = QtGui.QLineEdit(str(self.data['collisiondp']))
        self.collisiondp_option_layout.addWidget(self.collisiondp_checkbox)
        self.collisiondp_option_layout.addWidget(self.collisiondp_option)
        self.collisiondp_option_layout.addWidget(self.collisiondp_line_edit)

        # Create the list for chrono objects
        self.main_chrono = QtGui.QGroupBox("Chrono objects")
        self.main_chrono.setMinimumHeight(150)
        self.chrono_layout = QtGui.QVBoxLayout()

        self.objectlist_table = QtGui.QTableWidget(0, 1)
        self.objectlist_table.setObjectName("Chrono objects table")
        self.objectlist_table.verticalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.objectlist_table.setEnabled(True)

        # Create the necessary spaces in the list
        self.count = 0
        for key in self.data['simobjects'].keys():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.data['simobjects'][self.context_object.Name][1] != "Fluid" and \
                    self.context_object.Name != "Case_Limits":
                self.count += 1
        self.objectlist_table.setRowCount(self.count)
        self.current_row = 0
        self.objects_with_parent = list()
        self.is_floating = ""
        # FIXME: This seems a quick way to not destroy objects from memory. Study and clean
        self.temp_data = list()

        # Select the objects that are going to be listed
        for key, _ in self.data['simobjects'].items():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.context_object.InList != list():
                self.objects_with_parent.append(self.context_object.Name)
                continue
            if self.context_object.Name == "Case_Limits":
                continue
            if self.data['simobjects'][self.context_object.Name][1] == "Fluid":
                continue

            # FIXME: Adapt to new refactored data
            # self.is_floating = "bodyfloating" if str(value[0]) in data['floating_mks'].keys() else "bodyfixed"

            # Collects the information of the object
            self.target_widget = ChronoObjectCheckOptions(
                key=key,
                object_mk=self.data['simobjects'][self.context_object.Name][0],
                mktype=self.data['simobjects'][self.context_object.Name][1],
                object_name=self.context_object.Label,
                is_floating=self.is_floating
            )

            # Actualices the state of list options
            # FIXME: Adapt to new refactored data
            # if len(self.data['chrono_objects']) > 0:
            #     for elem in self.data['chrono_objects']:
            #         if elem[0] == str(key) and elem[3] == 1:
            #             self.target_widget.object_check.setCheckState(QtCore.Qt.Checked)
            #             self.target_widget.geometry_check.setCheckState(QtCore.Qt.Checked)
            #             self.target_widget.modelnormal_input.setCurrentIndex(int(elem[4]))
            #         elif elem[0] == str(key) and elem[3] == 0:
            #             self.target_widget.object_check.setCheckState(QtCore.Qt.Checked)
            #             self.target_widget.geometry_check.setCheckState(QtCore.Qt.Unchecked)
            #             self.target_widget.modelnormal_input.setCurrentIndex(int(elem[4]))

            # Saves the information about object for being process later
            self.temp_data.append(self.target_widget)

            # Shows the object in table
            self.objectlist_table.setCellWidget(self.current_row, 0, self.target_widget)

            self.current_row += 1

        # Add table to the layout
        self.chrono_layout.addWidget(self.objectlist_table)

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Link Linearspring option list
        self.main_link_linearspring = QtGui.QGroupBox("Linearspring")
        self.link_linearspring_layout = QtGui.QVBoxLayout()
        self.link_linearspring_layout2 = QtGui.QVBoxLayout()

        self.link_linearspring_button_layout = QtGui.QHBoxLayout()
        self.button_link_linearspring = QtGui.QPushButton("Add")
        self.link_linearspring_button_layout.addStretch(1)
        self.link_linearspring_button_layout.addWidget(self.button_link_linearspring)
        self.button_link_linearspring.clicked.connect(self.on_link_linearspring_add)

        self.link_linearspring_layout.addLayout(self.link_linearspring_button_layout)
        self.link_linearspring_layout.addLayout(self.link_linearspring_layout2)
        self.main_link_linearspring.setLayout(self.link_linearspring_layout)

        self.refresh_link_linearspring()

        # Link hinge option list
        self.main_link_hinge = QtGui.QGroupBox("Hinge")
        self.link_hinge_layout = QtGui.QVBoxLayout()
        self.link_hinge_layout2 = QtGui.QVBoxLayout()

        self.link_hinge_button_layout = QtGui.QHBoxLayout()
        self.button_link_hinge = QtGui.QPushButton("Add")
        self.link_hinge_button_layout.addStretch(1)
        self.link_hinge_button_layout.addWidget(self.button_link_hinge)
        self.button_link_hinge.clicked.connect(self.on_link_hinge_add)

        self.link_hinge_layout.addLayout(self.link_hinge_button_layout)
        self.link_hinge_layout.addLayout(self.link_hinge_layout2)
        self.main_link_hinge.setLayout(self.link_hinge_layout)

        self.refresh_link_hinge()

        # Link Spheric option list
        self.main_link_spheric = QtGui.QGroupBox("Spheric")
        self.link_spheric_layout = QtGui.QVBoxLayout()
        self.link_spheric_layout2 = QtGui.QVBoxLayout()

        self.link_spheric_button_layout = QtGui.QHBoxLayout()
        self.button_link_spheric = QtGui.QPushButton("Add")
        self.link_spheric_button_layout.addStretch(1)
        self.link_spheric_button_layout.addWidget(self.button_link_spheric)
        self.button_link_spheric.clicked.connect(self.on_link_spheric_add)

        self.link_spheric_layout.addLayout(self.link_spheric_button_layout)
        self.link_spheric_layout.addLayout(self.link_spheric_layout2)
        self.main_link_spheric.setLayout(self.link_spheric_layout)

        self.refresh_link_spheric()

        # Link Pointline option list
        self.main_link_pointline = QtGui.QGroupBox("Pointline")
        self.link_pointline_layout = QtGui.QVBoxLayout()
        self.link_pointline_layout2 = QtGui.QVBoxLayout()

        self.link_pointline_button_layout = QtGui.QHBoxLayout()
        self.button_link_pointline = QtGui.QPushButton("Add")
        self.link_pointline_button_layout.addStretch(1)
        self.link_pointline_button_layout.addWidget(self.button_link_pointline)
        self.button_link_pointline.clicked.connect(self.on_link_pointline_add)

        self.link_pointline_layout.addLayout(self.link_pointline_button_layout)
        self.link_pointline_layout.addLayout(self.link_pointline_layout2)
        self.main_link_pointline.setLayout(self.link_pointline_layout)

        self.refresh_link_pointline()

        # Adds all layouts to main
        self.main_layout.addLayout(self.csv_option_layout)
        self.main_layout.addLayout(self.scale_scheme_option_layout)
        self.main_layout.addLayout(self.collisiondp_option_layout)
        self.main_chrono.setLayout(self.chrono_layout)
        self.main_layout.addWidget(self.main_chrono)
        self.main_layout.addWidget(self.main_link_linearspring)
        self.main_layout.addWidget(self.main_link_hinge)
        self.main_layout.addWidget(self.main_link_spheric)
        self.main_layout.addWidget(self.main_link_pointline)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        # Adds scroll area
        self.main_layout_dialog = QtGui.QVBoxLayout()
        self.main_layout_scroll = QtGui.QScrollArea()
        self.main_layout_scroll.setMinimumWidth(400)
        self.main_layout_scroll.setWidgetResizable(True)
        self.main_layout_scroll_widget = QtGui.QWidget()
        self.main_layout_scroll_widget.setMinimumWidth(400)

        self.main_layout_scroll_widget.setLayout(self.main_layout)
        self.main_layout_scroll.setWidget(self.main_layout_scroll_widget)
        self.main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout_dialog.addWidget(self.main_layout_scroll)
        self.main_layout_dialog.addLayout(self.button_layout)
        self.on_scale_scheme_checkbox()
        self.on_csv_intervals_check()
        self.on_collisiondp_checkbox()

        self.setLayout(self.main_layout_dialog)

        self.exec_()

    def on_collisiondp_checkbox(self):
        ''' Checks the collisiondp state '''
        if self.collisiondp_checkbox.isChecked():
            self.collisiondp_line_edit.setEnabled(True)
        else:
            self.collisiondp_line_edit.setEnabled(False)

    def on_scale_scheme_checkbox(self):
        ''' Checks the scale scheme state '''
        if self.scale_scheme_checkbox.isChecked():
            self.scale_scheme_line_edit.setEnabled(True)
        else:
            self.scale_scheme_line_edit.setEnabled(False)

    def on_csv_intervals_check(self):
        ''' Checks the csv intervals state '''
        if self.csv_intervals_checkbox.isChecked():
            self.csv_intervals_line_edit.setEnabled(True)
        else:
            self.csv_intervals_line_edit.setEnabled(False)

    def refresh_link_hinge(self):
        ''' Refreshes the link hinge list '''
        count = 0
        while self.link_hinge_layout2.count() > 0:
            target = self.link_hinge_layout2.takeAt(0)
            target.setParent(None)

        for linkhinge in self.data['link_hinge']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link hinge" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda lh=linkhinge[0]: self.link_hinge_edit(lh))
            to_add_deletebutton.clicked.connect(lambda lh=linkhinge[0]: self.link_hinge_delete(lh))
            self.link_hinge_layout2.addLayout(to_add_layout)

    def refresh_link_linearspring(self):
        ''' Refreshes the link linearspring list '''
        count = 0
        while self.link_linearspring_layout2.count() > 0:
            target = self.link_linearspring_layout2.takeAt(0)
            target.setParent(None)

        for linkLinearspring in self.data['link_linearspring']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link linearspring" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda ll=linkLinearspring[0]: self.link_linearspring_edit(ll))
            to_add_deletebutton.clicked.connect(lambda ll=linkLinearspring[0]: self.link_linearspring_delete(ll))
            self.link_linearspring_layout2.addLayout(to_add_layout)

    def refresh_link_spheric(self):
        ''' Refreshes the link spheric list '''
        count = 0
        while self.link_spheric_layout2.count() > 0:
            target = self.link_spheric_layout2.takeAt(0)
            target.setParent(None)

        for linkSpheric in self.data['link_spheric']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link spheric" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda ls=linkSpheric[0]: self.link_spheric_edit(ls))
            to_add_deletebutton.clicked.connect(lambda ls=linkSpheric[0]: self.link_spheric_delete(ls))
            self.link_spheric_layout2.addLayout(to_add_layout)

    def refresh_link_pointline(self):
        ''' Refreshes the link pointline list '''
        count = 0
        while self.link_pointline_layout2.count() > 0:
            target = self.link_pointline_layout2.takeAt(0)
            target.setParent(None)

        for linkPointline in self.data['link_pointline']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link pointline" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda lp=linkPointline[0]: self.link_pointline_edit(lp))
            to_add_deletebutton.clicked.connect(lambda lp=linkPointline[0]: self.link_pointline_delete(lp))
            self.link_pointline_layout2.addLayout(to_add_layout)

    def on_link_hinge_add(self):
        ''' Adds Link hinge option at list '''
        # data['link_hinge'] = [element id, body 1, body 2, rotpoint[x,y,z], rotvector[x,y,z], stiffness, damping]
        uid_temp = uuid.uuid4()
        self.data['link_hinge'].append([
            str(uid_temp), '', '', [0, 0, 0], [0, 0, 0], 0, 0])
        self.link_hinge_edit(str(uid_temp))

    def link_hinge_delete(self, link_hinge_id):
        ''' Delete a link hinge element '''
        link_hinge_to_remove = None
        for lh in self.data['link_hinge']:
            if lh[0] == link_hinge_id:
                link_hinge_to_remove = lh
        if link_hinge_to_remove is not None:
            self.data['link_hinge'].remove(link_hinge_to_remove)
            self.refresh_link_hinge()

    def link_hinge_edit(self, link_hinge_id):
        ''' Edit a link hinge element '''
        LinkHingeEdit(self.data, self.temp_data, link_hinge_id)
        self.refresh_link_hinge()

    def on_link_linearspring_add(self):
        ''' Adds Link linearspring option at list '''
        uid_temp = uuid.uuid4()
        # data['link_linearspring'] = [element id, body 1, body 2, point_fb1[x,y,z], point_fb2[x,y,z], stiffness,
        # damping, rest_length, savevtk[nside, radius, length]]
        self.data['link_linearspring'].append([
            str(uid_temp), '', '', [0, 0, 0], [0, 0, 0], 0, 0, 0, [0, 0, 0]])
        self.link_linearspring_edit(str(uid_temp))

    def link_linearspring_delete(self, link_linearspring_id):
        ''' Delete a link linearspring element '''
        link_linearspring_to_remove = None
        for ll in self.data['link_linearspring']:
            if ll[0] == link_linearspring_id:
                link_linearspring_to_remove = ll
        if link_linearspring_to_remove is not None:
            self.data['link_linearspring'].remove(link_linearspring_to_remove)
            self.refresh_link_linearspring()

    def link_linearspring_edit(self, link_linearspring_id):
        ''' Edit a link linearspring element '''
        LinkLinearspringEdit(self.data, self.temp_data, link_linearspring_id)
        self.refresh_link_linearspring()

    def on_link_spheric_add(self):
        ''' Adds Link spheric option at list '''
        uid_temp = uuid.uuid4()
        # data['link_spheric'] = [element id, body 1, body 2, rotpoint[x,y,z], stiffness, damping]
        self.data['link_spheric'].append([
            str(uid_temp), '', '', [0, 0, 0], 0, 0])
        self.link_spheric_edit(str(uid_temp))

    def link_spheric_delete(self, link_spheric_id):
        ''' Delete a link spheric element '''
        link_spheric_to_remove = None
        for ls in self.data['link_spheric']:
            if ls[0] == link_spheric_id:
                link_spheric_to_remove = ls
        if link_spheric_to_remove is not None:
            self.data['link_spheric'].remove(link_spheric_to_remove)
            self.refresh_link_spheric()

    def link_spheric_edit(self, link_spheric_id):
        ''' Edit a link spheric element '''
        LinkSphericEdit(self.data, self.temp_data, link_spheric_id)
        self.refresh_link_spheric()

    def on_link_pointline_add(self):
        ''' Adds Link pointline option at list '''
        uid_temp = uuid.uuid4()
        # data['link_pointline'] = [element id, body 1, slidingvector[x,y,z], rotpoint[x,y,z], rotvector[x,y,z],
        # rotvector2[x,y,z], stiffness, damping]
        self.data['link_pointline'].append([
            str(uid_temp), '', [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 0, 0])
        self.link_pointline_edit(str(uid_temp))

    def link_pointline_delete(self, link_pointline_id):
        ''' Delete a link pointline element '''
        link_pointline_to_remove = None
        for lp in self.data['link_pointline']:
            if lp[0] == link_pointline_id:
                link_pointline_to_remove = lp
        if link_pointline_to_remove is not None:
            self.data['link_pointline'].remove(link_pointline_to_remove)
            self.refresh_link_pointline()

    def link_pointline_edit(self, link_pointline_id):
        ''' Edit a link pointline element '''
        LinkPointlineEdit(self.data, self.temp_data, link_pointline_id)
        self.refresh_link_pointline()

    def on_cancel(self):
        self.reject()

    def update_to_save(self):
        ''' Check all the conditions before save '''

        # Clean the chrono object list
        self.data['chrono_objects'] = list()

        # Checks the chrono objects and options for save
        for elem in self.temp_data:
            if elem.object_check.isChecked() and elem.geometry_check.isChecked():
                self.data['chrono_objects'].append([elem.key, elem.object_name, elem.object_mk, 1,
                                                    elem.modelnormal_input.currentIndex(), elem.is_floating])
            elif elem.object_check.isChecked():
                self.data['chrono_objects'].append([elem.key, elem.object_name, elem.object_mk, 0, 0, elem.is_floating])

        # Checks the csv interval option for save
        if self.csv_intervals_checkbox.isChecked():
            self.data['csv_intervals_check'] = True
            try:
                self.data['csv_intervals'] = float(self.csv_intervals_line_edit.text())
            except ValueError:
                self.data['csv_intervals_check'] = False
                self.data['csv_intervals'] = ""
                debug("Introduced an invalid value for a float number.")
        else:
            self.data['csv_intervals_check'] = False
            self.data['csv_intervals'] = ""

        # Checks the scale scheme option for save
        if self.scale_scheme_checkbox.isChecked():
            self.data['scale_scheme_check'] = True
            try:
                self.data['scale_scheme'] = float(self.scale_scheme_line_edit.text())
            except ValueError:
                self.data['scale_scheme_check'] = False
                self.data['scale_scheme'] = ""
                debug("Introduced an invalid value for a float number.")
        else:
            self.data['scale_scheme_check'] = False
            self.data['scale_scheme'] = ""

        # Checks the collisiondp option for save
        if self.collisiondp_checkbox.isChecked():
            self.data['collisiondp_check'] = True
            try:
                self.data['collisiondp'] = float(self.collisiondp_line_edit.text())
            except ValueError:
                self.data['collisiondp_check'] = False
                self.data['collisiondp'] = ""
                debug("Introduced an invalid value for a float number.")
        else:
            self.data['collisiondp_check'] = False
            self.data['collisiondp'] = ""

    def on_ok(self):
        ''' Save data '''
        self.update_to_save()

        ChronoConfigDialog.accept(self)
