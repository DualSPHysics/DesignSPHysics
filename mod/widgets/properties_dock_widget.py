#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Object Properties Widget."""

import FreeCAD
import FreeCADGui

from PySide2 import QtCore, QtWidgets
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QWidget

from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.translation_tools import __
from mod.enums import ObjectType, ObjectFillMode, FreeCADObjectType, HelpURL, DampingType
from mod.constants import PROP_WIDGET_INTERNAL_NAME, MKFLUID_LIMIT, MKFLUID_OFFSET
from mod.tools.stdout_tools import log
from mod.tools.dialog_tools import warning_dialog
from mod.widgets.dock.special_widgets.damping.damping_box_config_dialog import DampingBoxConfigDialog
from mod.widgets.dock.special_widgets.damping.damping_zone_config_dialog import DampingZoneConfigDialog
from mod.widgets.dock.special_widgets.damping.damping_cylinder_dialog import DampingCylinderConfigDialog
from mod.widgets.properties_widgets.initials_dialog import InitialsDialog
from mod.widgets.properties_widgets.bound_normals_dialog import BoundNormalsDialog
from mod.widgets.properties_widgets.mdbc_dialog import MDBCDialog
from mod.widgets.properties_widgets.motion.movement_dialog import MovementDialog
from mod.widgets.properties_widgets.float_state_dialog import FloatStateDialog
from mod.widgets.properties_widgets.faces_dialog import FacesDialog
from mod.widgets.properties_widgets.material_dialog import MaterialDialog

from mod.dataobjects.case import Case
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.widgets.properties_widgets.sim_object_dialog import SimObjectDialog


class PropertiesDockWidget(QtWidgets.QDockWidget):
    """ DesignSPHysics object properties widget. """

    FULL_NUMBER_OF_ROWS = 11
    BASIC_NUMBER_OF_ROWS =9
    NUMBER_OF_COLUMNS = 2

    MIN_HEIGHT = 220
    FIXED_WIDTH= 370

    need_refresh = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.last_mk_value: int = 0

        self.setObjectName(PROP_WIDGET_INTERNAL_NAME)
        self.setWindowTitle(__("DSPH Object Properties"))
        self.setFixedWidth(self.FIXED_WIDTH)
        #self.setSizePolicy(QtWidgets.QSizePolicy.Fixed)


        # Scaffolding widget, only useful to apply to the properties_dock widget
        self.properties_scaff_widget = QtWidgets.QWidget()
        self.properties_scaff_widget.setFixedWidth(self.FIXED_WIDTH)
        self.property_widget_layout = QtWidgets.QVBoxLayout()

        # Property table

        self.object_property_table = QtWidgets.QTableWidget(self.FULL_NUMBER_OF_ROWS, self.NUMBER_OF_COLUMNS)
        self.object_property_table.setMinimumHeight(self.MIN_HEIGHT)
        self.object_property_table.setHorizontalHeaderLabels([__("Property Name"), __("Value")])
        self.object_property_table.verticalHeader().setVisible(False)
        self.object_property_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Add an object to DSPH. Only appears when an object is not part of the simulation
        self.addtodsph_button = QtWidgets.QPushButton(__("Add to DSPH Simulation"))
        self.addtodsph_button.setToolTip(__("Adds the current selection to\nthe case. Objects not included will not be exported."))

        # Same as above, this time with remove
        self.removefromdsph_button = QtWidgets.QPushButton(__("Remove from DSPH Simulation"))
        self.removefromdsph_button.setToolTip(__("Removes the current selection from the case.\n"
                                                 "Objects not included in the case will not be exported."))

        # Damping configuration button
        self.damping_config_button = QtWidgets.QPushButton(__("Damping configuration"))
        self.damping_config_button.setToolTip(__("Opens the damping configuration for the selected object"))

        self.property_widget_layout.addWidget(self.object_property_table)
        self.property_widget_layout.addWidget(self.addtodsph_button)
        self.property_widget_layout.addWidget(self.removefromdsph_button)
        self.property_widget_layout.addWidget(self.damping_config_button)

        self.properties_scaff_widget.setLayout(self.property_widget_layout)

        self.setWidget(self.properties_scaff_widget)

        # Different labels to add to the property table
        self.geometry_properties_label = QtWidgets.QLabel()
        self.geometry_properties_label.setText("&nbsp;<span>{}</span>".format(__("Geometry properties")))
        self.geometry_properties_label.setToolTip(__("Properties established for each geometry"))

        self.geometry_properties_2_label = QtWidgets.QLabel()
        self.geometry_properties_2_label.setText("&nbsp;<span>{}</span>".format(__("Properties for FreeCAD Geos")))
        self.geometry_properties_2_label.setToolTip(__("Properties established for each geometry"))

        self.objtype_label = QtWidgets.QLabel()
        self.objtype_label.setText("&nbsp;<span>{}</span>".format(__("Type of object")))
        self.objtype_label.setToolTip(__("Establishes the object type: Fluid or bound"))

        self.mkgroup_label = QtWidgets.QLabel()
        self.mkgroup_label.setText("&nbsp;<span>{}</span>".format(__("MKGroup")))
        self.mkgroup_label.setOpenExternalLinks(True)
        self.mkgroup_label.setToolTip(__("Establishes the object group."))

        self.fillmode_label = QtWidgets.QLabel()
        self.fillmode_label.setText("&nbsp;<span>{}</span>".format(__("Fill mode")))
        self.fillmode_label.setToolTip(__("Sets fill mode.\nFull: generates internal volume and external mesh."
                                          "\nSolid: generates only internal volume."
                                          "\nFace: generates only external mesh."
                                          "\nWire: generates only external mesh polygon edges."))

        self.faces_label = QtWidgets.QLabel()
        self.faces_label.setText("&nbsp;<span>{}</span>".format(__("Layers and Faces")))
        self.faces_label.setToolTip(__("Configure layers for default geometries and faces for cubes"))

        self.geometry_label = QtWidgets.QLabel()
        self.geometry_label.setText("&nbsp;<span>{}</span>".format(__("Geometry")))
        self.geometry_label.setToolTip(__("Controls geometry options"))

        self.mDBC_label = QtWidgets.QLabel()
        self.mDBC_label.setText("&nbsp;<span>{}</span>".format(__("mDBC")))
        self.mDBC_label.setToolTip(__("Controls mDBC options"))

        self.frdrawmode_label = QtWidgets.QLabel()
        self.frdrawmode_label.setText("&nbsp;<span>{}</span>".format(__("FreeDraw")))
        self.frdrawmode_label.setToolTip(__("Controls geometry frdrawmode"))

        self.mk_properties_label = QtWidgets.QLabel()
        self.mk_properties_label.setText("&nbsp;<span>{}</span>".format(__("MK properties")))
        self.mk_properties_label.setToolTip(__("Properties established for each mk group"))

        self.mk_properties_2_label = QtWidgets.QLabel()
        self.mk_properties_2_label.setText("&nbsp;<span>{}</span>".format(__("Properties for MK groups")))
        self.mk_properties_2_label.setToolTip(__("Properties established for each mk group"))

        self.floatstate_label = QtWidgets.QLabel()
        self.floatstate_label.setText("&nbsp;<span>{}</span>".format(__("Float state")))
        self.floatstate_label.setToolTip(__("Sets floating state for this object MK."))

        self.initials_label = QtWidgets.QLabel()
        self.initials_label.setText("&nbsp;<span>{}</span>".format(__("Initials")))
        self.initials_label.setToolTip(__("Sets initials options for this object"))

        self.motion_label = QtWidgets.QLabel()
        self.motion_label.setText("&nbsp;<span>{}</span>".format(__("Motion")))
        self.motion_label.setToolTip(__("Sets motion for this object"))

        self.material_label = QtWidgets.QLabel()
        self.material_label.setText("&nbsp;<span>{}</span>".format(__("Material")))
        self.material_label.setToolTip(__("Configures the selected object material"))

        self.objtype_label.setAlignment(QtCore.Qt.AlignLeft)
        self.mkgroup_label.setAlignment(QtCore.Qt.AlignLeft)
        self.fillmode_label.setAlignment(QtCore.Qt.AlignLeft)
        self.floatstate_label.setAlignment(QtCore.Qt.AlignLeft)
        self.initials_label.setAlignment(QtCore.Qt.AlignLeft)
        self.motion_label.setAlignment(QtCore.Qt.AlignLeft)
        self.faces_label.setAlignment(QtCore.Qt.AlignLeft)
        self.material_label.setAlignment(QtCore.Qt.AlignLeft)
        self.geometry_label.setAlignment(QtCore.Qt.AlignLeft)
        self.mDBC_label.setAlignment(QtCore.Qt.AlignLeft)
        self.frdrawmode_label.setAlignment(QtCore.Qt.AlignLeft)


        # Property change widgets
        self.objtype_prop = QtWidgets.QComboBox()
        self.mkgroup_prop = QtWidgets.QSpinBox()
        self.fillmode_prop = QtWidgets.QComboBox()
        self.floatstate_prop = QtWidgets.QPushButton(__("Configure"))
        self.initials_prop = QtWidgets.QPushButton(__("Configure"))
        self.motion_prop = QtWidgets.QPushButton(__("Configure"))
        self.faces_prop = QtWidgets.QPushButton(__("Configure"))
        self.material_prop = QtWidgets.QPushButton(__("Configure"))
        self.geometry_prop =  QtWidgets.QPushButton(__("Configure"))
        self.mDBC_prop =  QtWidgets.QPushButton(__("Configure"))
        self.frdrawmode_prop = QtWidgets.QCheckBox("Enabled")

        self.objtype_prop.insertItems(0, ["Fluid", "Bound"])
        self.mkgroup_prop.setRange(0, 240)
        self.fillmode_prop.insertItems(1, ["Full", "Solid", "Face", "Wire"])
        self.faces_prop.setEnabled(False)

        # Property change connections
        self.objtype_prop.currentIndexChanged.connect(self.on_objtype_change)
        self.mkgroup_prop.valueChanged.connect(self.on_mkgroup_change)
        self.fillmode_prop.currentIndexChanged.connect(self.on_fillmode_change)
        self.floatstate_prop.clicked.connect(self.on_floatstate_change)
        self.initials_prop.clicked.connect(self.on_initials_change)
        self.motion_prop.clicked.connect(self.on_motion_change)
        self.faces_prop.clicked.connect(self.on_faces_clicked)
        self.material_prop.clicked.connect(self.on_material_clicked)
        self.geometry_prop.clicked.connect(self.on_geometry_clicked)
        self.mDBC_prop.clicked.connect(self.on_mDBC_clicked)
        self.frdrawmode_prop.stateChanged.connect(self.on_frdrawmode_check)

        # Property change labels insertion

        self.full_widget_table_list=[
            [self.geometry_properties_label,self.geometry_properties_2_label],
            [self.objtype_label, self.objtype_prop],
            [self.mkgroup_label, self.mkgroup_prop],
            [self.fillmode_label, self.fillmode_prop],
            [self.faces_label, self.faces_prop],
            [self.geometry_label, self.geometry_prop],
            [self.mDBC_label, self.mDBC_prop],
            [self.frdrawmode_label, self.frdrawmode_prop],
            [self.mk_properties_label,self.mk_properties_2_label],
            [self.floatstate_label, self.floatstate_prop],
            [self.initials_label, self.initials_prop],
            [self.motion_label, self.motion_prop],
            [self.material_label, self.material_prop],

        ]

        self.object_property_table.setRowCount(len(self.full_widget_table_list))
        for index,row in enumerate(self.full_widget_table_list):
            self.object_property_table.setCellWidget(index, 0, row[0])
            self.object_property_table.setCellWidget(index, 1, row[1])


        # By default, all is hidden in the widget
        self.object_property_table.hide()
        self.addtodsph_button.hide()
        self.removefromdsph_button.hide()
        self.damping_config_button.hide()

        # Connects buttons to its functions
        self.addtodsph_button.clicked.connect(self.on_add_object_to_sim)
        self.removefromdsph_button.clicked.connect(self.on_remove_object_from_sim)
        self.damping_config_button.clicked.connect(self.on_damping_config)

    def on_add_object_to_sim(self, name=None):
        """ Defines what happens when "Add object to sim" button is presseed. """
        if not name:
            selection = FreeCADGui.Selection.getSelection()
        else:
            selection = list()
            selection.append(FreeCAD.ActiveDocument.getObject(name))

        for each in selection:
            if each.Name == "Case_Limits" or "_internal_" in each.Name:# or each.InList: #Check more stuff...
                continue
            if not Case.the().is_object_in_simulation(each.Name):
                mktoput=-1
                if "fillbox" in each.Name.lower():
                    mktoput = Case.the().get_first_mk_not_used(ObjectType.FLUID)
                    Case.the().add_object(SimulationObject(each.Name, mktoput, ObjectType.FLUID, ObjectFillMode.SOLID))
                else:
                    object = Case.the().get_tmp_object(each.Name)
                    if object:
                        mktoput= object.obj_mk
                    if mktoput == -1:
                        mktoput = Case.the().get_first_mk_not_used(ObjectType.BOUND)
                    Case.the().add_object(SimulationObject(each.Name, mktoput, ObjectType.BOUND, ObjectFillMode.FULL))
            else:
                warning_dialog(f"There is already an object with name {each.Name} in the simulation")
        self.need_refresh.emit()

    def on_remove_object_from_sim(self):
        """ Defines what happens when pressing the remove objects from simulation button. """
        for each in FreeCADGui.Selection.getSelection():
            if each.Name == "Case_Limits":
                continue
            Case.the().remove_object(each.Name)

        self.need_refresh.emit()

    def on_damping_config(self):
        """ Configures the damping configuration for the selected object """

        damping=Case.the().get_damping_zone(FreeCADGui.Selection.getSelection()[0].Name)
        group=FreeCAD.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name)
        if damping.damping_type==DampingType.ZONE :
            DampingZoneConfigDialog(damping=damping,group=group ,parent=None).exec_()
        elif damping.damping_type==DampingType.BOX :
            DampingBoxConfigDialog(damping=damping, group=group, parent=None).exec_()
        elif damping.damping_type == DampingType.CYLINDER:
            DampingCylinderConfigDialog(damping=damping, group=group, parent=None).exec_()
        
    def on_objtype_change(self, index):
        """ Defines what happens when type of object is changed """
        selection = FreeCADGui.Selection.getSelection()[0]
        selectiongui = FreeCADGui.ActiveDocument.getObject(selection.Name)
        simulation_object = Case.the().get_simulation_object(selection.Name)
        mk_properties = Case.the().get_mk_based_properties(simulation_object.real_mk())

        if self.objtype_prop.itemText(index).lower() == "bound":
            self.mkgroup_prop.setRange(0, 240)
            if simulation_object.type != ObjectType.BOUND:
                self.mkgroup_prop.setValue(int(Case.the().get_first_mk_not_used(ObjectType.BOUND)))
            try:
                selectiongui.ShapeColor = (0.80, 0.80, 0.80)
                selectiongui.Transparency = 0
            except AttributeError:
                # Cannot change attributes
                pass
            self.floatstate_prop.setEnabled(True)
            self.set_mkgroup_text("{} <a href='{}'>?</a>".format(__("MKBound"), HelpURL.BASIC_CONCEPTS))
            self.set_initials_text("Bound Normals")
        elif self.objtype_prop.itemText(index).lower() == "fluid":
            min= 1 if Case.the().vres.active else 0
            self.mkgroup_prop.setRange(min, MKFLUID_LIMIT - MKFLUID_OFFSET - 1)
            if simulation_object.type != ObjectType.FLUID:
                self.mkgroup_prop.setValue(int(Case.the().get_first_mk_not_used(ObjectType.FLUID)))
            try:
                selectiongui.ShapeColor = (0.00, 0.45, 1.00)
                selectiongui.Transparency = 30
            except AttributeError:
                # Cannot change attributes
                pass
            # Remove floating properties if it is changed to fluid
            if mk_properties.float_property is not None:
                mk_properties.float_property = None

            # Remove motion properties if it is changed to fluid
            if mk_properties.has_movements():
                mk_properties.remove_all_movements()

            self.floatstate_prop.setEnabled(False)
            self.set_mkgroup_text("{} <a href='{}'>?</a>".format(__("MKFluid"), HelpURL.BASIC_CONCEPTS))
            self.set_initials_text("Fluid Initials")

        # Update simulation object type
        simulation_object.type = ObjectType.FLUID if index == 0 else ObjectType.BOUND
        self.last_mk_value = int(self.mkgroup_prop.value())

        self.need_refresh.emit()

    def on_mkgroup_change(self, value):
        """ Defines what happens when MKGroup is changed. """
        new_value: int = value
        old_value: int = self.last_mk_value

        # First we do what the user want
        Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name).obj_mk = new_value
        #self.last_mk_value = new_value   #Hace el cambio solo si no se cancela, evita que entre en bucle

        # Then we check that it is sensible
        orphan_mkbasedproperties: list = Case.the().get_orphan_mkbasedproperties()
        if orphan_mkbasedproperties and new_value != old_value:
            #response = ok_cancel_dialog(__("Changing MK value"), __("By doing this you will loose all MK configuration for the previous MK: {}. Are you sure you want to do this?").format(old_value))
            #if response == QtWidgets.QMessageBox.Ok:
            #    log("Changing from mk {} to {} caused orphan mkbasedproperties. Deleting...".format(old_value, new_value))
                self.last_mk_value = new_value #Cambia el last value solo si no se cancela, de lo contrario entra en bucle
            #    Case.the().delete_orphan_mkbasedproperties()
            #else:  TODO Eliminado provisionalmente, ver si es necesario por algo
            #    self.mkgroup_prop.setValue(old_value)


    def on_fillmode_change(self, index):
        """ Defines what happens when fill mode is changed """
        selection = FreeCADGui.Selection.getSelection()[0]
        selectiongui = FreeCADGui.ActiveDocument.getObject(selection.Name)
        simulation_object = Case.the().get_simulation_object(selection.Name)
        object_prop_item_text = self.objtype_prop.itemText(self.objtype_prop.currentIndex()).lower()

        # Update simulation object fill mode
        simulation_object.fillmode = [ObjectFillMode.FULL, ObjectFillMode.SOLID, ObjectFillMode.FACE, ObjectFillMode.WIRE][index]

        # Update faces property configuration only to be enabled on face type fill modes
        self.faces_prop.setEnabled(simulation_object.fillmode == ObjectFillMode.FACE and simulation_object.supports_changing_fillmode())
        self.update_faces_property(selection)

        transparencies = {ObjectFillMode.FULL: 30 if object_prop_item_text == "fluid" else 0,
                          ObjectFillMode.SOLID: 30 if object_prop_item_text == "fluid" else 0,
                          ObjectFillMode.FACE: 80,
                          ObjectFillMode.WIRE: 85}

        if hasattr(selectiongui, "Transparency"):
            selectiongui.Transparency = transparencies[simulation_object.fillmode]



    def on_geometry_clicked(self):
        selection = FreeCADGui.Selection.getSelection()[0]
        simulation_object = Case.the().get_simulation_object(selection.Name)
        dialog=SimObjectDialog(simulation_object)
        dialog.exec_()

    def on_mDBC_clicked(self):
        selection = FreeCADGui.Selection.getSelection()[0]
        # selectiongui = FreeCADGui.ActiveDocument.getObject(selection.Name)
        simulation_object = Case.the().get_simulation_object(selection.Name)
        dialog = MDBCDialog(simulation_object)
        dialog.exec_()


    def on_frdrawmode_check(self):
        """ FrDrawMode checkbox behaviour. """
        Case.the().get_simulation_object(FreeCADGui.Selection.getSelection()[0].Name).frdrawmode = self.frdrawmode_prop.isChecked()

    def on_initials_change(self):
        """ Initials configuration button behaviour. """
        selection = FreeCADGui.Selection.getSelection()[0]
        sim_object = Case.the().get_simulation_object(selection.Name)
        if sim_object.type == ObjectType.FLUID:
            InitialsDialog(parent=None)
        elif sim_object.type == ObjectType.BOUND:
            BoundNormalsDialog(parent=None)

    def on_motion_change(self):
        """ Movement configuration button behaviour. """
        MovementDialog(parent=None)

    def on_floatstate_change(self):
        """ Float configuration button behaviour. """
        FloatStateDialog(parent=None)

    def on_faces_clicked(self):
        """ Faces configuration button behaviour. """
        FacesDialog(FreeCADGui.Selection.getSelection()[0].Name, self)

    def on_material_clicked(self):
        """ Material configuration button behaviour. """
        MaterialDialog(FreeCADGui.Selection.getSelection()[0].Name, self)

    def update_faces_property(self, selection):
        """ Deletes information about faces if the new fill mode does not support it. """
        if self.faces_prop.isEnabled():
            return

        sim_object = Case.the().get_simulation_object(selection.Name)
        sim_object.clean_faces()

    def set_add_button_enabled(self, enabled: bool) -> None:
        """ Sets the Add button enabled property. """
        self.addtodsph_button.setEnabled(enabled)

    def set_add_button_visibility(self, visible: bool) -> None:
        """ Sets the add button visibility. """
        if visible:
            self.addtodsph_button.setVisible(True)
        else:
            self.addtodsph_button.setVisible(False)

    def set_remove_button_visibility(self, visible: bool) -> None:
        """ Sets the remove button visibility. """
        if visible:
            self.removefromdsph_button.setVisible(True)
        else:
            self.removefromdsph_button.setVisible(False)

    def set_damping_button_visibility(self, visible: bool) -> None:
        """ Sets the damping button visibility. """
        if visible:
            self.damping_config_button.setVisible(True)
        else:
            self.damping_config_button.setVisible(False)

    def set_add_button_text(self, text: str) -> None:
        """ Sets the Add button text. """
        self.addtodsph_button.setText(text)

    def set_property_table_visibility(self, visible: bool) -> None:
        """ Sets the property table visibility. """
        if visible:
            self.object_property_table.setVisible(True)
        else:
            self.object_property_table.setVisible(False)


    def set_mkgroup_range(self, obj_type: ObjectType) -> int:
        """ Sets the mkgroup range according to the object type specified. """
        mk_range = {ObjectType.BOUND: 240, ObjectType.FLUID: MKFLUID_LIMIT - MKFLUID_OFFSET}[obj_type]
        self.mkgroup_prop.setRange(0, mk_range)
        return mk_range

    def set_mkgroup_text(self, text: str) -> None:
        """ Sets the mkgroup label text. """
        self.mkgroup_label.setText("&nbsp;<span>{}</span>".format(text))

    def set_initials_text(self, text: str) -> None:
        """ Sets the mkgroup label text. """
        self.initials_label.setText("&nbsp;<span>{}</span>".format(text))

    def get_cell_widget(self, row: int, column: int) -> QtWidgets.QWidget:
        """ Retrieves the appropriate QWidget for the row and column specified from the table. """
        return self.object_property_table.cellWidget(row, column)

    def fit_size(self) -> None:
        """ Fits the size of the widget to reduce the wasted space on screen. """
        self.properties_scaff_widget.adjustSize()
        self.adjustSize()

    def configure_to_no_selection(self):
        """ Configures the property widget to hide everything. """
        self.set_property_table_visibility(False)
        self.set_add_button_visibility(False)
        self.set_remove_button_visibility(False)
        self.set_damping_button_visibility(False)

    def configure_to_add_multiple_selection(self):
        """ Configures the property widget to show tools to handle a multiple selection. """
        self.set_add_button_text(__("Add all possible objects to DSPH Simulation"))
        self.set_property_table_visibility(False)
        self.set_add_button_visibility(True)
        self.set_remove_button_visibility(False)
        self.set_damping_button_visibility(False)

    def configure_to_damping_selection(self):
        """ Configures the property widget to show tools to handle a selected damping zone. """
        self.set_property_table_visibility(False)
        self.set_add_button_visibility(False)
        self.set_remove_button_visibility(False)
        self.set_damping_button_visibility(True)

    def configure_to_regular_selection(self):
        """ Configures the property widget to show tools to handle a regular selected object. """
        self.set_property_table_visibility(True)
        self.set_add_button_visibility(False)
        self.set_remove_button_visibility(True)
        self.set_damping_button_visibility(False)

    def configure_to_incompatible_object(self):
        """ Configures the property widgeet to show a message warning of an incompatible object. """
        self.set_add_button_text(__("Cannot add this object to the simulation"))
        self.set_property_table_visibility(False)
        self.set_add_button_visibility(True)
        self.set_add_button_enabled(False)
        self.set_remove_button_visibility(False)
        self.set_damping_button_visibility(False)

    def configure_to_add_single_selection(self):
        """ Configures the property widget to show a button to add the currently selected object. """
        self.set_add_button_text(__("Add to DSPH Simulation"))
        self.set_property_table_visibility(False)
        self.set_add_button_visibility(True)
        self.set_remove_button_visibility(False)
        self.set_damping_button_visibility(False)

    def adapt_to_simulation_object(self, sim_object: SimulationObject, fc_object):
        """ Adapts the contents of the property widget to the specifications of the simulation object passed as a parameter. """
        #prop_dock=FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget,"DSPH_Properties")[0]
        self.mkgroup_prop.setValue(sim_object.obj_mk)
        self.last_mk_value = int(self.mkgroup_prop.value())

        self.frdrawmode_prop.setChecked(bool(sim_object.frdrawmode))

        log("Object {} supports changing type? {}. Its type is {} with mk {}".format(sim_object.name, sim_object.supports_changing_type(), sim_object.type, sim_object.obj_mk))

        # Object Type selector adaptation
        if sim_object.supports_changing_type():
            log("Changing objtype_prop to {} in PropertiesDockWidget.adapt_to_simulation_object".format("Fluid" if sim_object.type == ObjectType.FLUID else "Bound"))
            self.objtype_prop.setEnabled(True)
            self.objtype_prop.setCurrentIndex(0 if sim_object.type == ObjectType.FLUID else 1)
            self.set_mkgroup_range(sim_object.type)
            self.set_mkgroup_text("{} <a href='{}'>?</a>".format(__("MKFluid" if sim_object.type == ObjectType.FLUID else "MKBound"), HelpURL.BASIC_CONCEPTS))
        else:
            # Everything else
            log("Changing objtype_prop to {} in PropertiesDockWidget.adapt_to_simulation_object".format("Fluid" if sim_object.type == ObjectType.FLUID else "Bound"))
            self.set_mkgroup_range(ObjectType.BOUND)
            self.objtype_prop.setCurrentIndex(1)
            self.objtype_prop.setEnabled(False)

        # Object Fillmode selector adaptation
        self.fillmode_prop.setEnabled(False)
        self.faces_prop.setEnabled(False)
        if sim_object.supports_changing_fillmode():
            self.fillmode_prop.setEnabled(True)
            self.fillmode_prop.setCurrentIndex({ObjectFillMode.FULL: 0, ObjectFillMode.SOLID: 1, ObjectFillMode.FACE: 2, ObjectFillMode.WIRE: 3}[sim_object.fillmode])
            self.faces_prop.setEnabled(self.fillmode_prop.currentIndex()==2)
        else:
            # Object not supported. Put Solid if it's a fillbox or face if not
            self.fillmode_prop.setCurrentIndex(1 if fc_object.TypeId == FreeCADObjectType.FOLDER else 2)

        # Object Float State button adaptation
        if sim_object.supports_floating():
            self.floatstate_prop.setEnabled(sim_object.type != ObjectType.FLUID)

        # Object Motion button adaptation
        self.motion_prop.setEnabled(sim_object.supports_motion())

        # Object Material button adaptation
        self.material_prop.setEnabled(sim_object.type == ObjectType.BOUND)

        # Is an external object that supports autofill,scale,etc
        supports_geom= sim_object in Case.the().get_all_complex_objects() or sim_object.name.startswith("external_")
        self.geometry_prop.setEnabled(supports_geom)

        supports_mdbc = sim_object.type==ObjectType.BOUND and Case.the().execution_parameters.boundary==2
        self.mDBC_prop.setEnabled(supports_mdbc)
        # Is an object that supports frdrawmode
        self.frdrawmode_prop.setEnabled(fc_object.TypeId in (FreeCADObjectType.BOX, FreeCADObjectType.CYLINDER, FreeCADObjectType.SPHERE))

