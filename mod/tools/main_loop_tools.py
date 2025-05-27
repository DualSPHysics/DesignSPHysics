import time
import sys
from PySide2.QtCore import Signal, Slot, QObject
from PySide2 import QtCore

from mod.constants import DIVIDER, CASE_LIMITS_OBJ_NAME, GAUGES_GROUP_NAME, VRES_BOXES_GROUP_NAME, \
    IO_ZONES_GROUP_NAME, OUTFILTERS_GROUP_NAME, VARIABLES_SHEET_NAME, DAMPING_GROUP_NAME, SIMULATION_DOMAIN_NAME, HELPER_FOLDER_GROUP_NAME
from mod.dataobjects.case import Case

import FreeCAD

from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.enums import DampingType, FreeCADDisplayMode, FreeCADObjectType
from mod.tools.dialog_tools import warning_dialog, error_dialog
from mod.tools.freecad_tools import get_fc_object, valid_document_environment, \
    get_fc_view_object, add_tree_structure, add_case_limits_object, draw_simulation_domain, get_case_limits

from mod.tools.translation_tools import __
from mod.widgets.designsphysics_dock import DesignSPHysicsDock
import FreeCADGui

from mod.widgets.properties_dock_widget import PropertiesDockWidget


def manage_damping_areas(damping_areas):
    # DAMPING AREAS
    for name, damping_zone in damping_areas:
        if FreeCAD.ActiveDocument:
            damping_group = FreeCAD.ActiveDocument.getObject(name)
            if damping_zone.damping_type == DampingType.ZONE:
                if len(damping_group.OutList) == 2:
                    damping_zone.overlimit = damping_group.OutList[1].Length.Value / DIVIDER
            elif damping_zone.damping_type == DampingType.BOX:
                pass
            elif damping_zone.damping_type == DampingType.CYLINDER:
                damping_group = FreeCAD.ActiveDocument.getObject(name)
                line = damping_group.OutList[0]
                circle_min1 = damping_group.OutList[1]
                orig_vec = FreeCAD.Base.Vector(0, 0, 1)
                line_vec = FreeCAD.Base.Vector(line.X2, line.Y2, line.Z2)
                rotation = FreeCAD.Base.Rotation(orig_vec, line_vec)
                circle_min1.Placement.Rotation = rotation


def manage_deleted_objects():
    # Delete invalid or already deleted (in FreeCAD) objects
    objects_list = FreeCAD.ActiveDocument.Objects
    names_list = [x.Name for x in objects_list]
    sim_objects_names_list = Case.the().get_all_simulation_object_names()
    missing_objs = list()
    for object_name in sim_objects_names_list:
        fc_object = get_fc_object(object_name)
        if not fc_object:  #Object deleted from freeCAD but not from SIM
            Case.the().remove_object(object_name)
            Case.the().remove_tmp_object(object_name)
    # Check deleting of damping zones
    for damping_to_delete in list(filter(lambda x: not get_fc_object(x), Case.the().damping_zones)):
        Case.the().remove_damping_zone(damping_to_delete)
    #Check for deleting in helper group folders
    if GAUGES_GROUP_NAME not in names_list or VRES_BOXES_GROUP_NAME not in names_list or IO_ZONES_GROUP_NAME not in names_list or OUTFILTERS_GROUP_NAME not in names_list or VARIABLES_SHEET_NAME not in names_list or DAMPING_GROUP_NAME not in names_list:
        add_tree_structure()
        missing_objs.append("Helper object groups.")
    # Check for deleting in inlet/outlet zone helpers
    for z in Case.the().inlet_outlet.zones:
        fc_name = z.fc_object_name
        if fc_name:
            if fc_name not in names_list:
                FreeCADGui.runCommand('Std_Undo', 0)
                missing_objs.append("Inlet/Outlet helper objects.")
            else:
                if len(get_fc_object(fc_name).OutList) < 2:
                    FreeCADGui.runCommand('Std_Undo', 0)
                    missing_objs.append("Inlet/Outlet helper objects.")
    # Check for deleting in Vres boxes helpers
    for vb in Case.the().vres.bufferbox_list:
        fc_name = vb.fc_object_name
        if fc_name:
            if fc_name not in names_list:
                FreeCADGui.runCommand('Std_Undo', 0)
                missing_objs.append("Variable Resolution bufferbox helper objects")
    # Check for deleting in gauges
    for g in Case.the().gauges.gauges_dict.values():
        fc_name = g.fc_object_name
        if fc_name:
            if fc_name not in names_list:
                FreeCADGui.runCommand('Std_Undo', 0)
                missing_objs.append("Gauges helper objects.")
    # Check for deleting in gauges
    for f in Case.the().outparts.filts.values():
        fc_name = f.fc_object_name
        if fc_name:
            if fc_name not in names_list:
                FreeCADGui.runCommand('Std_Undo', 0)
                missing_objs.append("Output particle filter helper objects.")
    # Check for deleting in flowboxes
    for fb in Case.the().post_processing_settings.flowtool_xml_boxes:
        fc_name = fb.fc_object_name
        if fc_name:
            if fc_name not in names_list:
                FreeCADGui.runCommand('Std_Undo', 0)
                missing_objs.append("Flowtool boxes helper objects.")
    # Manage Case Limits
    if CASE_LIMITS_OBJ_NAME not in names_list:
        add_case_limits_object()
        warning_dialog("Case Limits object cannot be deleted.")
        missing_objs.append("Case Limits object")
    # Manage Simulation domain
    if SIMULATION_DOMAIN_NAME not in names_list and CASE_LIMITS_OBJ_NAME in names_list:
        missing_objs.append("Simulation Domain object.")
        limits = get_case_limits()
        draw_simulation_domain(*limits)

    # Show missing objects
    if len(missing_objs)>0:    
        error_text = str("Following objects are missing because they were deleted or a case from older versions has been loadeed: " 
                        + "".join(f"\n   - {item}" for item in missing_objs))
        warning_dialog(error_text)


class MainLoopManager(QObject):

    def __init__(self, dock: DesignSPHysicsDock,properties :PropertiesDockWidget):
        super().__init__()
        self.dock = dock
        self.properties=properties

    @Slot()
    def deleted(self):
        try:
            manage_deleted_objects()
        except Exception:
            return None

    @Slot()
    def invalid_doc(self):
        self.dock.adapt_to_no_case()

    @Slot()
    def slot_damping(self):
        manage_damping_areas(Case.the().damping_zones.items())

    @Slot()
    def slot_selection(self):
        if not FreeCADGui.Selection.getSelection():
            self.properties.configure_to_no_selection()


class MainLoopEmiter(QtCore.QThread):
    enforce_valid_dock = Signal()
    manage_gauges = Signal()
    manage_partfilters = Signal()
    check_deleted = Signal()
    check_selection = Signal()
    check_properties = Signal()

    def __init__(self):
        super().__init__()

    # MAINLOOP
    def run(self):
        time.sleep(6.0)
        while 1:
            if not valid_document_environment():
                self.enforce_valid_dock.emit()
            else:
                self.check_deleted.emit()
                self.check_selection.emit()
            self.sleep(1.0)

    def update_properties(self):
        self.check_properties.emit()

class UnitWatcher(QtCore.QThread):
    unit_changed = QtCore.Signal(int, int)  # old_unit, new_unit

    def __init__(self, parent=None):
        super(UnitWatcher, self).__init__(parent)
        self.running = True
        self.last_unit = self.get_unit_system()
        self.interval_ms = 1000  # Check every second

    def get_unit_system(self):
        return FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("UserSchema")

    def run(self):
        while self.running:
            current_unit = self.get_unit_system()
            if current_unit != self.last_unit:
                self.unit_changed.emit(self.last_unit, current_unit)
                self.last_unit = current_unit
            self.msleep(self.interval_ms)

    def stop(self):
        self.running = False
        self.wait()
