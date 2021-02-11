#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Chrono configuration dialog."""

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import debug
from mod.enums import ChronoModelNormalType, ContactMethod, OMPThreads
from mod.freecad_tools import get_fc_main_window, get_fc_object

from mod.dataobjects.case import Case
from mod.dataobjects.chrono.chrono_object import ChronoObject
from mod.dataobjects.chrono.chrono_link_hinge import ChronoLinkHinge
from mod.dataobjects.chrono.chrono_link_linear_spring import ChronoLinkLinearSpring
from mod.dataobjects.chrono.chrono_link_point_line import ChronoLinkPointLine
from mod.dataobjects.chrono.chrono_link_spheric import ChronoLinkSpheric
from mod.dataobjects.chrono.chrono_link_pulley import ChronoLinkPulley
from mod.dataobjects.chrono.chrono_link_coulomb_damping import ChronoLinkCoulombDamping

from mod.widgets.chrono.chrono_object_check_options import ChronoObjectCheckOptions
from mod.widgets.chrono.link_hinge_edit import LinkHingeEdit
from mod.widgets.chrono.link_linear_spring_edit import LinkLinearspringEdit
from mod.widgets.chrono.link_spheric_edit import LinkSphericEdit
from mod.widgets.chrono.link_point_line_edit import LinkPointlineEdit
from mod.widgets.chrono.link_pulley_edit import LinkPulleyEdit
from mod.widgets.chrono.link_coulombdamping_edit import LinkCoulombDampingEdit


class ChronoConfigDialog(QtGui.QDialog):
    """ Defines the Chrono dialog window.
    Modifies data dictionary passed as parameter. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Reference to avoid calling instance every time
        self.case = Case.the()

        # Creates a dialog
        self.setWindowTitle("Chrono configuration")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.main_layout = QtGui.QVBoxLayout()

        # Option for saves CSV with data exchange for each time interval
        self.csv_option_layout = QtGui.QHBoxLayout()
        self.csv_intervals_checkbox = QtGui.QCheckBox()
        self.csv_intervals_checkbox.setCheckState(QtCore.Qt.Checked if self.case.chrono.csv_intervals.enabled else QtCore.Qt.Unchecked)
        self.csv_intervals_checkbox.toggled.connect(self.on_csv_intervals_check)
        self.csv_intervals_option = QtGui.QLabel(__("CSV intervals:"))
        self.csv_intervals_line_edit = QtGui.QLineEdit(str(self.case.chrono.csv_intervals.value))
        self.csv_option_layout.addWidget(self.csv_intervals_checkbox)
        self.csv_option_layout.addWidget(self.csv_intervals_option)
        self.csv_option_layout.addWidget(self.csv_intervals_line_edit)

        # Option for define scale used to create the initial scheme of Chrono objects
        self.scale_scheme_option_layout = QtGui.QHBoxLayout()
        self.scale_scheme_checkbox = QtGui.QCheckBox()
        self.scale_scheme_checkbox.setCheckState(QtCore.Qt.Checked if self.case.chrono.scale_scheme.enabled else QtCore.Qt.Unchecked)
        self.scale_scheme_checkbox.toggled.connect(self.on_scale_scheme_checkbox)
        self.scale_scheme_option = QtGui.QLabel(__("Scale for scheme:"))
        self.scale_scheme_line_edit = QtGui.QLineEdit(str(self.case.chrono.scale_scheme.value))
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_checkbox)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_option)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_line_edit)

        # Option for allow collision overlap according Dp
        self.collisiondp_option_layout = QtGui.QHBoxLayout()
        self.collisiondp_checkbox = QtGui.QCheckBox()
        if self.case.chrono.collisiondp.enabled:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.collisiondp_checkbox.toggled.connect(self.on_collisiondp_checkbox)
        self.collisiondp_option = QtGui.QLabel(__("Enable/Disable Collision"))
        self.collisiondp_option_layout.addWidget(self.collisiondp_checkbox)
        self.collisiondp_option_layout.addWidget(self.collisiondp_option)
        self.collisiondp_option_layout.addStretch(1)

        # Collision related fields
        self.collision_fields_widget = QtGui.QWidget();
        self.collision_fields_widget_layout = QtGui.QVBoxLayout()
        
        self.collision_fields_distancedp_layout = QtGui.QHBoxLayout()
        self.collision_fields_distancedp_label = QtGui.QLabel("Allowed collision overlap:")
        self.collision_fields_distancedp_edit = QtGui.QLineEdit(str(self.case.chrono.collisiondp.distancedp))
        self.collision_fields_distancedp_layout.addWidget(self.collision_fields_distancedp_label)
        self.collision_fields_distancedp_layout.addWidget(self.collision_fields_distancedp_edit)

        self.collision_fields_ompthreads_layout = QtGui.QHBoxLayout()
        self.collision_fields_ompthreads_label = QtGui.QLabel("Parallel execution type:")
        self.collision_fields_ompthreads_combo = QtGui.QComboBox()
        self.collision_fields_ompthreads_combo.insertItems(0, ["Multi-Core", "Single-Core"])
        self.collision_fields_ompthreads_combo.setCurrentIndex(self.case.chrono.collisiondp.ompthreads)
        self.collision_fields_ompthreads_layout.addWidget(self.collision_fields_ompthreads_label)
        self.collision_fields_ompthreads_layout.addWidget(self.collision_fields_ompthreads_combo)

        self.collision_fields_contactmethod_layout = QtGui.QHBoxLayout()
        self.collision_fields_contactmethod_label = QtGui.QLabel("Contact method type:")
        self.collision_fields_contactmethod_combo = QtGui.QComboBox()
        self.collision_fields_contactmethod_combo.insertItems(0, ["Non Smooth Contacts (NSC)", "Smooth Contacts (SMC)"])
        self.collision_fields_contactmethod_combo.setCurrentIndex(self.case.chrono.collisiondp.contactmethod)
        self.collision_fields_contactmethod_layout.addWidget(self.collision_fields_contactmethod_label)
        self.collision_fields_contactmethod_layout.addWidget(self.collision_fields_contactmethod_combo)

        self.collision_fields_widget_layout.addLayout(self.collision_fields_distancedp_layout)
        self.collision_fields_widget_layout.addLayout(self.collision_fields_ompthreads_layout)
        self.collision_fields_widget_layout.addLayout(self.collision_fields_contactmethod_layout)
        self.collision_fields_widget.setLayout(self.collision_fields_widget_layout)
        
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
        self.objectlist_table.setRowCount(len(self.case.get_all_bound_objects()))
        self.current_row = 0
        self.objects_with_parent = list()
        self.is_floating = ""
        self.chrono_object_options_widgets = list()

        # Select the objects that are going to be listed
        for sim_object in self.case.get_all_bound_objects():
            freecad_object = get_fc_object(sim_object.name)
            self.is_floating = "bodyfloating" if self.case.get_mk_based_properties(sim_object.type, sim_object.obj_mk).float_property else "bodyfixed"

            # Collects the information of the object
            self.target_widget = ChronoObjectCheckOptions(
                key=sim_object.name,
                object_mk=sim_object.obj_mk,
                mktype=sim_object.type,
                object_name=freecad_object.Label,
                is_floating=self.is_floating,
                parent=get_fc_main_window()
            )

            # Updates the state of list options
            if self.case.chrono.objects:
                for elem in self.case.chrono.objects:
                    if elem.id == sim_object.name:
                        self.target_widget.object_check.setCheckState(QtCore.Qt.Checked)
                        self.target_widget.geometry_check.setCheckState(QtCore.Qt.Checked if elem.modelnormal_enabled else QtCore.Qt.Unchecked)
                        self.target_widget.modelnormal_input.setCurrentIndex({ChronoModelNormalType.ORIGINAL: 0, ChronoModelNormalType.INVERT: 1, ChronoModelNormalType.TWOFACE: 2}[elem.modelnormal_type])

            # Saves the information about object for being process later
            self.chrono_object_options_widgets.append(self.target_widget)

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

        # Link Coulombdamping option list
        self.main_link_coulombdamping = QtGui.QGroupBox("Coulombdamping")
        self.link_coulombdamping_layout = QtGui.QVBoxLayout()
        self.link_coulombdamping_layout2 = QtGui.QVBoxLayout()

        self.link_coulombdamping_button_layout = QtGui.QHBoxLayout()
        self.button_link_coulombdamping = QtGui.QPushButton("Add")
        self.link_coulombdamping_button_layout.addStretch(1)
        self.link_coulombdamping_button_layout.addWidget(self.button_link_coulombdamping)
        self.button_link_coulombdamping.clicked.connect(self.on_link_coulombdamping_add)

        self.link_coulombdamping_layout.addLayout(self.link_coulombdamping_button_layout)
        self.link_coulombdamping_layout.addLayout(self.link_coulombdamping_layout2)
        self.main_link_coulombdamping.setLayout(self.link_coulombdamping_layout)

        self.refresh_link_coulombdamping()

        # Link Pulley option list
        self.main_link_pulley = QtGui.QGroupBox("Pulley")
        self.link_pulley_layout = QtGui.QVBoxLayout()
        self.link_pulley_layout2 = QtGui.QVBoxLayout()

        self.link_pulley_button_layout = QtGui.QHBoxLayout()
        self.button_link_pulley = QtGui.QPushButton("Add")
        self.link_pulley_button_layout.addStretch(1)
        self.link_pulley_button_layout.addWidget(self.button_link_pulley)
        self.button_link_pulley.clicked.connect(self.on_link_pulley_add)

        self.link_pulley_layout.addLayout(self.link_pulley_button_layout)
        self.link_pulley_layout.addLayout(self.link_pulley_layout2)
        self.main_link_pulley.setLayout(self.link_pulley_layout)

        self.refresh_link_pulley()

        # Adds all layouts to main
        self.main_layout.addLayout(self.csv_option_layout)
        self.main_layout.addLayout(self.scale_scheme_option_layout)
        self.main_layout.addLayout(self.collisiondp_option_layout)
        self.main_layout.addWidget(self.collision_fields_widget)
        self.main_chrono.setLayout(self.chrono_layout)
        self.main_layout.addWidget(self.main_chrono)
        self.main_layout.addWidget(self.main_link_linearspring)
        self.main_layout.addWidget(self.main_link_hinge)
        self.main_layout.addWidget(self.main_link_spheric)
        self.main_layout.addWidget(self.main_link_pointline)
        self.main_layout.addWidget(self.main_link_coulombdamping)
        self.main_layout.addWidget(self.main_link_pulley)

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

        self.ok_button.setFocus()

        self.exec_()

    def on_collisiondp_checkbox(self):
        """ Checks the collisiondp state """
        if self.collisiondp_checkbox.isChecked():
            self.collision_fields_widget.setVisible(True)
        else:
            self.collision_fields_widget.setVisible(False)

    def on_scale_scheme_checkbox(self):
        """ Checks the scale scheme state """
        if self.scale_scheme_checkbox.isChecked():
            self.scale_scheme_line_edit.setEnabled(True)
        else:
            self.scale_scheme_line_edit.setEnabled(False)

    def on_csv_intervals_check(self):
        """ Checks the csv intervals state """
        if self.csv_intervals_checkbox.isChecked():
            self.csv_intervals_line_edit.setEnabled(True)
        else:
            self.csv_intervals_line_edit.setEnabled(False)

    def refresh_link_hinge(self):
        """ Refreshes the link hinge list """
        count = 0
        while self.link_hinge_layout2.count() > 0:
            target = self.link_hinge_layout2.takeAt(0)
            target.setParent(None)

        for linkhinge in self.case.chrono.link_hinge:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link hinge" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, lh=linkhinge.id: self.link_hinge_edit(lh))
            to_add_deletebutton.clicked.connect(lambda _=False, lh=linkhinge.id: self.link_hinge_delete(lh))
            self.link_hinge_layout2.addLayout(to_add_layout)

    def refresh_link_linearspring(self):
        """ Refreshes the link linearspring list """
        count = 0
        while self.link_linearspring_layout2.count() > 0:
            target = self.link_linearspring_layout2.takeAt(0)
            target.setParent(None)

        for linkLinearspring in self.case.chrono.link_linearspring:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link linearspring" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, ll=linkLinearspring.id: self.link_linearspring_edit(ll))
            to_add_deletebutton.clicked.connect(lambda _=False, ll=linkLinearspring.id: self.link_linearspring_delete(ll))
            self.link_linearspring_layout2.addLayout(to_add_layout)

    def refresh_link_spheric(self):
        """ Refreshes the link spheric list """
        count = 0
        while self.link_spheric_layout2.count() > 0:
            target = self.link_spheric_layout2.takeAt(0)
            target.setParent(None)

        for linkSpheric in self.case.chrono.link_spheric:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link spheric" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, ls=linkSpheric.id: self.link_spheric_edit(ls))
            to_add_deletebutton.clicked.connect(lambda _=False, ls=linkSpheric.id: self.link_spheric_delete(ls))
            self.link_spheric_layout2.addLayout(to_add_layout)

    def refresh_link_pointline(self):
        """ Refreshes the link pointline list """
        count = 0
        while self.link_pointline_layout2.count() > 0:
            target = self.link_pointline_layout2.takeAt(0)
            target.setParent(None)

        for linkPointline in self.case.chrono.link_pointline:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link pointline" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, lp=linkPointline.id: self.link_pointline_edit(lp))
            to_add_deletebutton.clicked.connect(lambda _=False, lp=linkPointline.id: self.link_pointline_delete(lp))
            self.link_pointline_layout2.addLayout(to_add_layout)

    def refresh_link_coulombdamping(self):
        """ Refreshes the link coulombdamping list """
        count = 0
        while self.link_coulombdamping_layout2.count() > 0:
            target = self.link_coulombdamping_layout2.takeAt(0)
            target.setParent(None)

        for linkCoulombdamping in self.case.chrono.link_coulombdamping:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link coulombdamping" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, lp=linkCoulombdamping.id: self.link_coulombdamping_edit(lp))
            to_add_deletebutton.clicked.connect(lambda _=False, lp=linkCoulombdamping.id: self.link_coulombdamping_delete(lp))
            self.link_coulombdamping_layout2.addLayout(to_add_layout)

    def refresh_link_pulley(self):
        """ Refreshes the link pulley list """
        count = 0
        while self.link_pulley_layout2.count() > 0:
            target = self.link_pulley_layout2.takeAt(0)
            target.setParent(None)

        for linkPulley in self.case.chrono.link_pulley:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link pulley" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda _=False, lp=linkPulley.id: self.link_pulley_edit(lp))
            to_add_deletebutton.clicked.connect(lambda _=False, lp=linkPulley.id: self.link_pulley_delete(lp))
            self.link_pulley_layout2.addLayout(to_add_layout)

    def on_link_hinge_add(self):
        """ Adds Link hinge option at list """
        link_hinge_to_add = ChronoLinkHinge()
        self.case.chrono.link_hinge.append(link_hinge_to_add)
        self.link_hinge_edit(link_hinge_to_add.id)

    def link_hinge_delete(self, link_hinge_id):
        """ Delete a link hinge element """
        link_hinge_to_remove = None
        for lh in self.case.chrono.link_hinge:
            if lh.id == link_hinge_id:
                link_hinge_to_remove = lh
        if link_hinge_to_remove is not None:
            self.case.chrono.link_hinge.remove(link_hinge_to_remove)
            self.refresh_link_hinge()

    def link_hinge_edit(self, link_hinge_id):
        """ Edit a link hinge element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkHingeEdit(link_hinge_id=link_hinge_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_hinge()

    def on_link_linearspring_add(self):
        """ Adds Link linearspring option at list """
        linearspring_to_add = ChronoLinkLinearSpring()
        self.case.chrono.link_linearspring.append(linearspring_to_add)
        self.link_linearspring_edit(linearspring_to_add.id)

    def link_linearspring_delete(self, link_linearspring_id):
        """ Delete a link linearspring element """
        link_linearspring_to_remove = None
        for ll in self.case.chrono.link_linearspring:
            if ll.id == link_linearspring_id:
                link_linearspring_to_remove = ll
        if link_linearspring_to_remove is not None:
            self.case.chrono.link_linearspring.remove(link_linearspring_to_remove)
            self.refresh_link_linearspring()

    def link_linearspring_edit(self, link_linearspring_id):
        """ Edit a link linearspring element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkLinearspringEdit(link_linearspring_id=link_linearspring_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_linearspring()

    def on_link_spheric_add(self):
        """ Adds Link spheric option at list """
        link_spheric_to_add = ChronoLinkSpheric()
        self.case.chrono.link_spheric.append(link_spheric_to_add)
        self.link_spheric_edit(link_spheric_to_add.id)

    def link_spheric_delete(self, link_spheric_id):
        """ Delete a link spheric element """
        link_spheric_to_remove = None
        for ls in self.case.chrono.link_spheric:
            if ls.id == link_spheric_id:
                link_spheric_to_remove = ls
        if link_spheric_to_remove is not None:
            self.case.chrono.link_spheric.remove(link_spheric_to_remove)
            self.refresh_link_spheric()

    def link_spheric_edit(self, link_spheric_id):
        """ Edit a link spheric element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkSphericEdit(link_spheric_id=link_spheric_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_spheric()

    def on_link_pointline_add(self):
        """ Adds Link pointline option at list """
        link_pointline_to_add = ChronoLinkPointLine()
        self.case.chrono.link_pointline.append(link_pointline_to_add)
        self.link_pointline_edit(link_pointline_to_add.id)

    def link_pointline_delete(self, link_pointline_id):
        """ Delete a link pointline element """
        link_pointline_to_remove = None
        for lp in self.case.chrono.link_pointline:
            if lp.id == link_pointline_id:
                link_pointline_to_remove = lp
        if link_pointline_to_remove is not None:
            self.case.chrono.link_pointline.remove(link_pointline_to_remove)
            self.refresh_link_pointline()

    def link_pointline_edit(self, link_pointline_id):
        """ Edit a link pointline element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkPointlineEdit(link_pointline_id=link_pointline_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_pointline()

    def on_link_coulombdamping_add(self):
        """ Adds Link coulombdamping option at list """
        link_coulombdamping_to_add = ChronoLinkCoulombDamping()
        self.case.chrono.link_coulombdamping.append(link_coulombdamping_to_add)
        self.link_coulombdamping_edit(link_coulombdamping_to_add.id)

    def link_coulombdamping_delete(self, link_coulombdamping_id):
        """ Delete a link coulombdamping element """
        link_coulombdamping_to_remove = None
        for lp in self.case.chrono.link_coulombdamping:
            if lp.id == link_coulombdamping_id:
                link_coulombdamping_to_remove = lp
        if link_coulombdamping_to_remove is not None:
            self.case.chrono.link_coulombdamping.remove(link_coulombdamping_to_remove)
            self.refresh_link_coulombdamping()

    def link_coulombdamping_edit(self, link_coulombdamping_id):
        """ Edit a link coulombdamping element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkCoulombDampingEdit(link_coulombdamping_id=link_coulombdamping_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_coulombdamping()

    def on_link_pulley_add(self):
        """ Adds Link pulley option at list """
        link_pulley_to_add = ChronoLinkPulley()
        self.case.chrono.link_pulley.append(link_pulley_to_add)
        self.link_pulley_edit(link_pulley_to_add.id)

    def link_pulley_delete(self, link_pulley_id):
        """ Delete a link pulley element """
        link_pulley_to_remove = None
        for lp in self.case.chrono.link_pulley:
            if lp.id == link_pulley_id:
                link_pulley_to_remove = lp
        if link_pulley_to_remove is not None:
            self.case.chrono.link_pulley.remove(link_pulley_to_remove)
            self.refresh_link_pulley()

    def link_pulley_edit(self, link_pulley_id):
        """ Edit a link pulley element """
        selected_chrono_object_widgets = list(filter(lambda x: x.object_check.isChecked(), self.chrono_object_options_widgets))
        LinkPulleyEdit(link_pulley_id=link_pulley_id, bodies_widgets=selected_chrono_object_widgets, parent=get_fc_main_window())
        self.refresh_link_pulley()

    def on_cancel(self):
        """ Defines cancel button behaviour. """
        self.reject()

    def update_to_save(self):
        """ Check all the conditions before save """

        # Clean the chrono object list
        self.case.chrono.objects = list()

        # Checks the chrono objects and options for save
        for elem in self.chrono_object_options_widgets:
            if not elem.object_check.isChecked():
                continue
            chrono_object = ChronoObject()
            chrono_object.id = elem.key
            chrono_object.name = elem.object_name
            chrono_object.mkbound = elem.object_mk
            chrono_object.modelnormal_enabled = elem.geometry_check.isChecked()
            chrono_object.modelnormal_type = {0: ChronoModelNormalType.ORIGINAL, 1: ChronoModelNormalType.INVERT, 2: ChronoModelNormalType.TWOFACE}[elem.modelnormal_input.currentIndex()]
            chrono_object.floating_type = elem.is_floating
            self.case.chrono.objects.append(chrono_object)

        # Checks the csv interval option for save
        if self.csv_intervals_checkbox.isChecked():
            self.case.chrono.csv_intervals.enabled = True
            try:
                self.case.chrono.csv_intervals.value = float(self.csv_intervals_line_edit.text())
            except ValueError:
                self.case.chrono.csv_intervals.enabled = False
                self.case.chrono.csv_intervals.value = ""
                debug("Introduced an invalid value for a float number.")
        else:
            self.case.chrono.csv_intervals.enabled = False
            self.case.chrono.csv_intervals.value = ""

        # Checks the scale scheme option for save
        if self.scale_scheme_checkbox.isChecked():
            self.case.chrono.scale_scheme.enabled = True
            try:
                self.case.chrono.scale_scheme.value = float(self.scale_scheme_line_edit.text())
            except ValueError:
                self.case.chrono.scale_scheme.enabled = False
                self.case.chrono.scale_scheme.value = ""
                debug("Introduced an invalid value for a float number.")
        else:
            self.case.chrono.scale_scheme.enabled = False
            self.case.chrono.scale_scheme.value = ""

        # Checks the collisiondp option for save
        if self.collisiondp_checkbox.isChecked():
            self.case.chrono.collisiondp.enabled = True
            try:
                self.case.chrono.collisiondp.distancedp = float(self.collision_fields_distancedp_edit.text())
                self.case.chrono.collisiondp.ompthreads = OMPThreads.MULTI_CORE if self.collision_fields_ompthreads_combo.currentIndex() == 0 else OMPThreads.SINGLE_CORE
                self.case.chrono.collisiondp.contactmethod = ContactMethod.NSC if self.collision_fields_contactmethod_combo.currentIndex() == 0 else ContactMethod.SMC
            except ValueError:
                self.case.chrono.collisiondp.enabled = False
                debug("Introduced an invalid value in collision widgets.")
        else:
            self.case.chrono.collisiondp.enabled = False

    def on_ok(self):
        """ Save data """
        self.update_to_save()

        ChronoConfigDialog.accept(self)
