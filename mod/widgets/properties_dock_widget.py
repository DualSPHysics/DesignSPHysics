#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Object Properties Widget.'''

from traceback import print_exc

import FreeCAD
import FreeCADGui

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.enums import ObjectType, ObjectFillMode

from mod.widgets.damping_config_dialog import DampingConfigDialog
from mod.widgets.initials_dialog import InitialsDialog
from mod.widgets.movement_dialog import MovementDialog
from mod.widgets.float_state_dialog import FloatStateDialog
from mod.widgets.faces_dialog import FacesDialog

from mod.dataobjects.case import Case
from mod.dataobjects.simulation_object import SimulationObject


class PropertiesDockWidget(QtGui.QDockWidget):
    ''' DesignSPHysics object properties widget. '''

    NUMBER_OF_ROWS = 7
    NUMBER_OF_COLUMNS = 2

    MIN_HEIGHT = 220

    need_refresh = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("DSPH_Properties")
        self.setWindowTitle(__("DSPH Object Properties"))

        # Scaffolding widget, only useful to apply to the properties_dock widget
        self.properties_scaff_widget = QtGui.QWidget()
        self.property_widget_layout = QtGui.QVBoxLayout()

        # Property table
        self.object_property_table = QtGui.QTableWidget(self.NUMBER_OF_ROWS, self.NUMBER_OF_COLUMNS)
        self.object_property_table.setMinimumHeight(self.MIN_HEIGHT)
        self.object_property_table.setHorizontalHeaderLabels([__("Property Name"), __("Value")])
        self.object_property_table.verticalHeader().setVisible(False)
        self.object_property_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # Add an object to DSPH. Only appears when an object is not part of the simulation
        self.addtodsph_button = QtGui.QPushButton(__("Add to DSPH Simulation"))
        self.addtodsph_button.setToolTip(__("Adds the current selection to\nthe case. Objects not included will not be exported."))

        # Same as above, this time with remove
        self.removefromdsph_button = QtGui.QPushButton(__("Remove from DSPH Simulation"))
        self.removefromdsph_button.setToolTip(__("Removes the current selection from the case.\n"
                                                 "Objects not included in the case will not be exported."))

        # Damping configuration button
        self.damping_config_button = QtGui.QPushButton(__("Damping configuration"))
        self.damping_config_button.setToolTip(__("Opens the damping configuration for the selected object"))

        self.property_widget_layout.addWidget(self.object_property_table)
        self.property_widget_layout.addWidget(self.addtodsph_button)
        self.property_widget_layout.addWidget(self.removefromdsph_button)
        self.property_widget_layout.addWidget(self.damping_config_button)

        self.properties_scaff_widget.setLayout(self.property_widget_layout)

        self.setWidget(self.properties_scaff_widget)

        # Different labels to add to the property table
        self.mkgroup_label = QtGui.QLabel("   {}".format(__("MKGroup")))
        self.mkgroup_label.setOpenExternalLinks(True)
        self.mkgroup_label.setToolTip(__("Establishes the object group."))

        self.objtype_label = QtGui.QLabel("   {}".format(__("Type of object")))
        self.objtype_label.setToolTip(__("Establishes the object type: Fluid or bound"))

        self.fillmode_label = QtGui.QLabel("   {}".format(__("Fill mode")))
        self.fillmode_label.setToolTip(__("Sets fill mode.\nFull: generates internal volume and external mesh."
                                          "\nSolid: generates only internal volume."
                                          "\nFace: generates only external mesh."
                                          "\nWire: generates only external mesh polygon edges."))

        self.floatstate_label = QtGui.QLabel("   {}".format(__("Float state")))
        self.floatstate_label.setToolTip(__("Sets floating state for this object MK."))

        self.initials_label = QtGui.QLabel("   {}".format(__("Initials")))
        self.initials_label.setToolTip(__("Sets initials options for this object"))

        self.material_label = QtGui.QLabel("   {}".format(__("Material")))
        self.material_label.setToolTip(__("Sets material for this object"))

        self.motion_label = QtGui.QLabel("   {}".format(__("Motion")))
        self.motion_label.setToolTip(__("Sets motion for this object"))

        self.faces_label = QtGui.QLabel("   {}".format(__("Faces")))
        self.faces_label.setToolTip(__("Adds faces"))

        self.mkgroup_label.setAlignment(QtCore.Qt.AlignLeft)
        self.material_label.setAlignment(QtCore.Qt.AlignLeft)
        self.objtype_label.setAlignment(QtCore.Qt.AlignLeft)
        self.fillmode_label.setAlignment(QtCore.Qt.AlignLeft)
        self.floatstate_label.setAlignment(QtCore.Qt.AlignLeft)
        self.initials_label.setAlignment(QtCore.Qt.AlignLeft)
        self.motion_label.setAlignment(QtCore.Qt.AlignLeft)

        # Property change labels insertion
        self.object_property_table.setCellWidget(0, 0, self.objtype_label)
        self.object_property_table.setCellWidget(1, 0, self.mkgroup_label)
        self.object_property_table.setCellWidget(2, 0, self.fillmode_label)
        self.object_property_table.setCellWidget(3, 0, self.floatstate_label)
        self.object_property_table.setCellWidget(4, 0, self.initials_label)
        self.object_property_table.setCellWidget(5, 0, self.motion_label)
        self.object_property_table.setCellWidget(6, 0, self.faces_label)

        # Property change widgets
        self.mkgroup_prop = QtGui.QSpinBox()
        self.objtype_prop = QtGui.QComboBox()
        self.fillmode_prop = QtGui.QComboBox()
        self.floatstate_prop = QtGui.QPushButton(__("Configure"))
        self.initials_prop = QtGui.QPushButton(__("Configure"))
        self.motion_prop = QtGui.QPushButton(__("Configure"))
        self.faces_prop = QtGui.QPushButton(__("Configure"))

        self.faces_prop.setEnabled(False)
        self.mkgroup_prop.setRange(0, 240)
        self.objtype_prop.insertItems(0, ['Fluid', 'Bound'])
        self.fillmode_prop.insertItems(1, ['Full', 'Solid', 'Face', 'Wire'])

        # Property change connections
        self.mkgroup_prop.valueChanged.connect(self.on_mkgroup_change)
        self.objtype_prop.currentIndexChanged.connect(self.on_objtype_change)
        self.fillmode_prop.currentIndexChanged.connect(self.on_fillmode_change)
        self.floatstate_prop.clicked.connect(self.on_floatstate_change)
        self.initials_prop.clicked.connect(self.on_initials_change)
        self.motion_prop.clicked.connect(self.on_motion_change)
        self.faces_prop.clicked.connect(self.on_faces_clicked)

        # Property change widget insertion
        self.object_property_table.setCellWidget(0, 1, self.objtype_prop)
        self.object_property_table.setCellWidget(1, 1, self.mkgroup_prop)
        self.object_property_table.setCellWidget(2, 1, self.fillmode_prop)
        self.object_property_table.setCellWidget(3, 1, self.floatstate_prop)
        self.object_property_table.setCellWidget(4, 1, self.initials_prop)
        self.object_property_table.setCellWidget(5, 1, self.motion_prop)
        self.object_property_table.setCellWidget(6, 1, self.faces_prop)

        # By default all is hidden in the widget
        self.object_property_table.hide()
        self.addtodsph_button.hide()
        self.removefromdsph_button.hide()
        self.damping_config_button.hide()

        # Connects buttons to its functions
        self.addtodsph_button.clicked.connect(self.on_add_object_to_sim)
        self.removefromdsph_button.clicked.connect(self.on_remove_object_from_sim)
        self.damping_config_button.clicked.connect(self.on_damping_config)

    def on_add_object_to_sim(self, name=None):
        ''' Defines what happens when "Add object to sim" button is presseed. '''
        if not name:
            selection = FreeCADGui.Selection.getSelection()
        else:
            selection = list()
            selection.append(FreeCAD.ActiveDocument.getObject(name))

        for each in selection:
            if each.Name == "Case_Limits" or "_internal_" in each.Name or each.InList:
                continue
            if not Case.instance().is_object_in_simulation(each.Name):
                if "fillbox" in each.Name.lower():
                    mktoput = Case.instance().get_first_mk_not_used(ObjectType.FLUID)
                    Case.instance().add_object(SimulationObject(each.Name, mktoput, ObjectType.FLUID, ObjectFillMode.SOLID))
                else:
                    mktoput = Case.instance().get_first_mk_not_used(ObjectType.BOUND)
                    Case.instance().add_object(SimulationObject(each.Name, mktoput, ObjectType.BOUND, ObjectFillMode.FULL))

        self.need_refresh.emit()

    def on_remove_object_from_sim(self):
        ''' Defines what happens when pressing the remove objects from simulation button. '''
        for each in FreeCADGui.Selection.getSelection():
            if each.Name == "Case_Limits":
                continue
            Case.instance().remove_object(each.Name)

        self.need_refresh.emit()

    def on_damping_config(self):
        ''' Configures the damping configuration for the selected obejct '''
        DampingConfigDialog(FreeCADGui.Selection.getSelection()[0].Name)

    def on_mkgroup_change(self, value):
        ''' Defines what happens when MKGroup is changed. '''
        Case.instance().get_simulation_object(FreeCADGui.Selection.getSelection().Name).obj_mk = value

    def on_objtype_change(self, index):
        ''' Defines what happens when type of object is changed '''
        selection = FreeCADGui.Selection.getSelection()[0]
        selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
        simulation_object = Case.instance().get_simulation_object(selection.Name)
        mk_properties = Case.instance().get_mk_base_properties(simulation_object.obj_mk)

        if self.objtype_prop.itemText(index).lower() == "bound":
            self.mkgroup_prop.setRange(0, 240)
            if simulation_object.type != ObjectType.BOUND:
                self.mkgroup_prop.setValue(int(Case.instance().get_first_mk_not_used(ObjectType.BOUND)))
            try:
                selectiongui.ShapeColor = (0.80, 0.80, 0.80)
                selectiongui.Transparency = 0
            except AttributeError:
                # Can't change attributes
                pass
            self.floatstate_prop.setEnabled(True)
            self.initials_prop.setEnabled(False)
            self.mkgroup_label.setText("&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")
        elif self.objtype_prop.itemText(index).lower() == "fluid":
            self.mkgroup_prop.setRange(0, 10)
            if simulation_object.type != ObjectType.FLUID:
                self.mkgroup_prop.setValue(int(Case.instance().get_first_mk_not_used(ObjectType.FLUID)))
            try:
                selectiongui.ShapeColor = (0.00, 0.45, 1.00)
                selectiongui.Transparency = 30
            except AttributeError:
                # Can't change attributes
                pass
            # Remove floating properties if it is changed to fluid
            if mk_properties.float_property is not None:
                mk_properties.float_property = None

            # Remove motion properties if it is changed to fluid
            if mk_properties.has_movements():
                mk_properties.remove_all_movements()

            self.floatstate_prop.setEnabled(False)
            self.initials_prop.setEnabled(True)
            self.mkgroup_label.setText("&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")

        # Update simulation object type
        simulation_object.type = ObjectType.FLUID if index == 0 else ObjectType.BOUND

        self.need_refresh.emit()

    def on_fillmode_change(self, index):
        ''' Defines what happens when fill mode is changed '''
        selection = FreeCADGui.Selection.getSelection()[0]
        selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
        simulation_object = Case.instance().get_simulation_object(selection.Name)
        object_prop_item_text = self.objtype_prop.itemText(self.objtype_prop.currentIndex()).lower()

        # Update simulation object fill mode
        simulation_object.fillmode = [ObjectFillMode.FULL, ObjectFillMode.SOLID, ObjectFillMode.FACE, ObjectFillMode.WIRE][index]

        # Update faces property configuration only to be enabled on face type fill modes
        self.faces_prop.setEnabled(simulation_object.fillmode == ObjectFillMode.FACE)
        self.update_faces_property(selection)

        transparencies = {ObjectFillMode.FULL: 30 if object_prop_item_text == "fluid" else 0,
                          ObjectFillMode.SOLID: 30 if object_prop_item_text == "fluid" else 0,
                          ObjectFillMode.FACE: 80,
                          ObjectFillMode.WIRE: 85}

        try:
            selectiongui.Transparency = transparencies[simulation_object.fillmode]
        except AttributeError:
            print_exc()

    def on_initials_change(self):
        ''' Initials configuration button behaviour. '''
        InitialsDialog()

    def on_motion_change(self):
        ''' Movement configuration button behaviour. '''
        MovementDialog()

    def on_floatstate_change(self):
        ''' Float configuration button behaviour. '''
        FloatStateDialog()

    def on_faces_clicked(self):
        ''' Faces configuration button behaviour. '''
        FacesDialog(FreeCADGui.Selection.getSelection()[0].Name)

    def update_faces_property(self, selection):
        ''' Deletes information about faces if the new fill mode does not support it. '''
        if self.faces_prop.isEnabled():
            return

        sim_object = Case.instance().get_simulation_object(selection.Name)
        sim_object.clean_faces()

    def set_add_button_enabled(self, enabled: bool) -> None:
        ''' Sets the Add button enabled property. '''
        self.addtodsph_button.setEnabled(enabled)

    def set_add_button_visibility(self, visible: bool) -> None:
        ''' Sets the add button visibility. '''
        if visible:
            self.addtodsph_button.show()
        else:
            self.addtodsph_button.hide()

    def set_remove_button_visibility(self, visible: bool) -> None:
        ''' Sets the remove button visibility. '''
        if visible:
            self.removefromdsph_button.show()
        else:
            self.removefromdsph_button.hide()

    def set_damping_button_visibility(self, visible: bool) -> None:
        ''' Sets the damping button visibility. '''
        if visible:
            self.damping_config_button.show()
        else:
            self.damping_config_button.hide()

    def set_add_button_text(self, text: str) -> None:
        ''' Sets the Add button text. '''
        self.addtodsph_button.setText(text)

    def set_property_table_visibility(self, visible: bool) -> None:
        ''' Sets the property table visibility. '''
        if visible:
            self.object_property_table.show()
        else:
            self.object_property_table.hide()

    def set_mkgroup_range(self, obj_type: ObjectType) -> int:
        ''' Sets the mkgroup range according to the object type specified. '''
        mk_range = {ObjectType.BOUND: 240, ObjectType.FLUID: 10}[obj_type]
        self.mkgroup_prop.setRange(0, mk_range)
        return mk_range

    def set_mkgroup_text(self, text: str) -> None:
        ''' Sets the mkgroup label text. '''
        self.mkgroup_label.setText(text)

    def get_cell_widget(self, row: int, column: int) -> QtGui.QWidget:
        ''' Retrieves the appropiate QWidget for the row and column specified from the table. '''
        return self.object_property_table.cellWidget(row, column)

    def fit_size(self) -> None:
        ''' Fits the size of the widget to reduce the wasted space on screen. '''
        self.properties_scaff_widget.adjustSize()
        self.adjustSize()
