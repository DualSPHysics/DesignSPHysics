#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

""" FreeCAD related tools. """
from tempfile import gettempdir
from shutil import copyfile
from typing import Dict, Union

import FreeCAD
import FreeCADGui
import Draft
import Part

from PySide2 import QtWidgets

from mod.dataobjects.gauges.flow_gauge import FlowGauge
from mod.dataobjects.gauges.gauge_base import Gauge
from mod.dataobjects.gauges.mesh_gauge import MeshGauge
from mod.dataobjects.inletoutlet.inlet_outlet_zone_box_generator import InletOutletZoneBoxGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_circle_generator import InletOutletZoneCircleGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_direction import InletOutletZone3DDirection,InletOutletZone2DDirection
from mod.dataobjects.inletoutlet.inlet_outlet_zone_info import InletOutletZoneInfo
from mod.dataobjects.inletoutlet.inlet_outlet_zone_line_generator import InletOutletZoneLineGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_mk_generator import InletOutletZoneMKGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone3DRotation, InletOutletZone2DRotation
from mod.dataobjects.outparts_filter.filters import FilterPos, FilterSphere, FilterCylinder, FilterPlane, BaseFilter, \
    FilterMK, TypeFilter, FilterGroup
from mod.dataobjects.variable_res.bufferbox import BufferBox

from mod.tools.translation_tools import __
from mod.tools.stdout_tools import log, error, debug
from mod.tools.dialog_tools import ok_cancel_dialog, error_dialog, warning_dialog
from mod.appmode import AppMode

from mod.constants import APP_NAME, SINGLETON_DOCUMENT_NAME, DEFAULT_WORKBENCH, CASE_LIMITS_OBJ_NAME, \
    CASE_LIMITS_3D_LABEL, DIVIDER, IO_ZONES_GROUP_NAME, VRES_BOXES_GROUP_NAME, VARIABLES_SHEET_NAME, GAUGES_GROUP_NAME, \
    OUTFILTERS_GROUP_NAME, FLOWBOXES_GROUP_NAME, DAMPING_GROUP_NAME, GAUGES_COLOR, GAUGES_DIRECTION_COLOR, \
    OUTFILTERS_COLOR, VRES_BOXES_COLOR, DAMPING_COLOR, SIMULATION_DOMAIN_COLOR, HELPER_FOLDER_GROUP_NAME, \
    SIMULATION_DOMAIN_NAME, WIDTH_2D
from mod.constants import CASE_LIMITS_LINE_COLOR, CASE_LIMITS_LINE_WIDTH, CASE_LIMITS_DEFAULT_LENGTH, \
    FREECAD_MIN_VERSION
from mod.constants import MAIN_WIDGET_INTERNAL_NAME, PROP_WIDGET_INTERNAL_NAME, WIDTH_2D, FILLBOX_DEFAULT_LENGTH, \
    FILLBOX_DEFAULT_RADIUS
from mod.enums import FreeCADObjectType, FreeCADDisplayMode, DampingType, ObjectType, InletOutletDirection, \
    InletOutletZoneGeneratorType, FilterType


def delete_existing_docks():
    """ Searches for existing docks related to DesignSPHysics destroys them. """
    for previous_dock in [get_fc_main_window().findChild(QtWidgets.QDockWidget, MAIN_WIDGET_INTERNAL_NAME),
                          get_fc_main_window().findChild(QtWidgets.QDockWidget, PROP_WIDGET_INTERNAL_NAME)]:
        if previous_dock:
            log("Removing previous {} dock".format(APP_NAME))
            previous_dock.setParent(None)
            previous_dock = None


def check_compatibility():
    """ Ensures the current version of FreeCAD is compatible with the macro. Spawns an error dialog and throws exception to halt
        the execution if its not. """
    if not is_compatible_version():
        error_dialog(
            __("This FreeCAD version is not compatible. Please update FreeCAD to version {} or higher.").format(
                FREECAD_MIN_VERSION))
        raise EnvironmentError(
            __("This FreeCAD version is not compatible. Please update FreeCAD to version {} or higher.").format(
                FREECAD_MIN_VERSION))


def is_compatible_version():
    """ Checks if the current FreeCAD version is suitable for this macro. """
    version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
    if float(version_num) < float(FREECAD_MIN_VERSION):
        return False
    return True

def add_case_limits_object():
    obj = FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME)
    if not obj:
        FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, CASE_LIMITS_OBJ_NAME)
        case_limits_obj = FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME)
        case_limits_obj.Label = CASE_LIMITS_3D_LABEL
        case_limits_obj.Length = CASE_LIMITS_DEFAULT_LENGTH
        case_limits_obj.Width = CASE_LIMITS_DEFAULT_LENGTH
        case_limits_obj.Height = CASE_LIMITS_DEFAULT_LENGTH
        case_limits_obj.addProperty("App::PropertyVector", "lastposition")
        case_limits_obj.addProperty("App::PropertyDistance", "Dp")
        case_limits_gui_obj = FreeCADGui.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME)
        case_limits_gui_obj.DisplayMode = FreeCADDisplayMode.WIREFRAME
        case_limits_gui_obj.LineColor = CASE_LIMITS_LINE_COLOR
        case_limits_gui_obj.LineWidth = CASE_LIMITS_LINE_WIDTH
        case_limits_gui_obj.Selectable = False

    
    add_simulation_domain()

def add_simulation_domain():
    limits = get_case_limits()
    if get_fc_object(SIMULATION_DOMAIN_NAME):
        update_simulation_domain(*limits)
    else:
        draw_simulation_domain(*limits)

def get_case_limits():
    obj = FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME)
    if obj:
        values = (obj.Placement.Base.x,obj.Placement.Base.y,obj.Placement.Base.z,
                  obj.Placement.Base.x + obj.Length.Value,
                  obj.Placement.Base.y + obj.Width.Value,
                  obj.Placement.Base.z + obj.Height.Value)
    else:
        case_limits_length=float(CASE_LIMITS_DEFAULT_LENGTH.removesuffix("mm")) #In mm
        values = (0,0,0,case_limits_length,case_limits_length,case_limits_length)

    return tuple(v / 1000 for v in values) # in m

def add_tree_structure():
    helper_folder=FreeCAD.ActiveDocument.getObject(HELPER_FOLDER_GROUP_NAME)
    if not helper_folder:
        helper_folder=FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, HELPER_FOLDER_GROUP_NAME)
    io_zones_group = FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME)
    if not io_zones_group:
        io_zones_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, IO_ZONES_GROUP_NAME)
    vr_zones_group = FreeCAD.ActiveDocument.getObject(VRES_BOXES_GROUP_NAME)
    if not vr_zones_group:
        vr_zones_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, VRES_BOXES_GROUP_NAME)
    gauges_group = FreeCAD.ActiveDocument.getObject(GAUGES_GROUP_NAME)
    if not gauges_group:
        gauges_group=FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, GAUGES_GROUP_NAME)
    outparts_group = FreeCAD.ActiveDocument.getObject(OUTFILTERS_GROUP_NAME)
    if not outparts_group:
         outparts_group=FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, OUTFILTERS_GROUP_NAME)
    flowboxes_group=FreeCAD.ActiveDocument.getObject(FLOWBOXES_GROUP_NAME)
    if not flowboxes_group:
        flowboxes_group=FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, FLOWBOXES_GROUP_NAME)
    damping_group = FreeCAD.ActiveDocument.getObject(DAMPING_GROUP_NAME)
    if not damping_group:
        damping_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, DAMPING_GROUP_NAME)
    variables_sheet = FreeCAD.ActiveDocument.getObject(VARIABLES_SHEET_NAME)
    if not variables_sheet:
        variables_sheet = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.SPREADSHEET, VARIABLES_SHEET_NAME)
    for group in [io_zones_group,vr_zones_group,gauges_group,outparts_group,flowboxes_group,damping_group,variables_sheet]:
        helper_folder.addObject(group)



def prepare_dsph_case():
    """ Creates a few objects and setups a new case for DesignSPHysics. """
    FreeCAD.setActiveDocument(SINGLETON_DOCUMENT_NAME)
    FreeCAD.ActiveDocument = FreeCAD.ActiveDocument  # ?
    FreeCADGui.ActiveDocument = FreeCADGui.ActiveDocument  # ?
    if FreeCADGui.activeWorkbench().name() != "DsphWorkbench":
        FreeCADGui.activateWorkbench(DEFAULT_WORKBENCH)
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    add_case_limits_object()
    add_tree_structure()

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def setup_damping_environment(damping_type: DampingType = DampingType.ZONE) -> str:
    """ Setups a damping group with its properties within FreeCAD. """
    if damping_type == DampingType.ZONE:
        damping_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Help_DampingZone")

        # Limits line
        points = [FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0)]
        limits_name=  draw_line(points[0],points[1],"Helper_Limits",draw_style="Solid")
        limits=get_fc_object(limits_name)
        limitsv = FreeCADGui.ActiveDocument.getObject(limits.Name)
        limitsv.ShapeColor = DAMPING_COLOR
        limitsv.LineColor = DAMPING_COLOR
        limitsv.PointColor = DAMPING_COLOR
        '''limitsv.EndArrow = True
        limitsv.ArrowSize = "10 mm"
        limitsv.ArrowType = "Dot"'''

        # Overlimit line
        points = [FreeCAD.Vector(1, 0, 0), FreeCAD.Vector(2, 0, 0)]
        overlimit_name= draw_line(points[0],points[1],"Helper_OverLimit",draw_style="Dotted")
        overlimit=get_fc_object(overlimit_name)
        #overlimit.AttachmentSupport = [limits, '']
        #overlimit.MapMode = 'ObjectXY'
        #overlimitv = FreeCADGui.ActiveDocument.getObject(overlimit.Name)
        '''overlimitv.EndArrow = True
        overlimitv.ArrowSize = "10 mm"
        overlimitv.ArrowType = "Dot"'''

        # Add the two lines to the group
        damping_group.addObject(limits)
        damping_group.addObject(overlimit)

    elif damping_type == DampingType.BOX:
        damping_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Help_DampingBox")
        limits_box_1 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, "Helper_Box1_limits")
        limits_box_2 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, "Helper_Box2_limits")
        limits_box_1.setExpression('.Placement.Rotation.Angle', u'Case_Limits.Placement.Rotation.Angle')
        limits_box_2.setExpression('.Placement.Rotation.Angle', u'Case_Limits.Placement.Rotation.Angle')
        limits_box_1_GUI = FreeCADGui.ActiveDocument.getObject(limits_box_1.Name)
        limits_box_2_GUI = FreeCADGui.ActiveDocument.getObject(limits_box_2.Name)
        limits_box_1_GUI.DisplayMode = FreeCADDisplayMode.WIREFRAME
        limits_box_2_GUI.DisplayMode = FreeCADDisplayMode.WIREFRAME
        limits_box_1_GUI.LineColor = DAMPING_COLOR
        limits_box_2_GUI.LineColor = DAMPING_COLOR
        damping_group.addObject(limits_box_1)
        damping_group.addObject(limits_box_2)

    elif damping_type == DampingType.CYLINDER:
        damping_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Help_DampingCylinder")
        limits_line = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.LINE, "Helper_Cylinder1_Line")
        limits_min_circle1 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CIRCLE, "Helper_Cylinder1_Min_Circle1")
        limits_min_circle2 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CIRCLE, "Helper_Cylinder1_Min_Circle2")
        limits_max_circle1 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CIRCLE, "Helper_Cylinder1_Max_Circle1")
        limits_max_circle2 = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CIRCLE, "Helper_Cylinder1_Max_Circle2")
        limits_line.setExpression('.Placement.Rotation.Angle', u'Case_Limits.Placement.Rotation.Angle')
        limits_line.setExpression('.X1', u'0 mm')
        limits_line.setExpression('.Y1', u'0 mm')
        limits_line.setExpression('.Z1', u'0 mm')
        limits_min_circle1.setExpression('.Placement.Base', f'{limits_line.Name}.Placement.Base')
        limits_max_circle1.setExpression('.Placement.Base', f'{limits_line.Name}.Placement.Base')
        limits_min_circle2.setExpression('.Placement.Base.x',
                                         f'{limits_line.Name}.Placement.Base.x + {limits_line.Name}.X2')
        limits_min_circle2.setExpression('.Placement.Base.y',
                                         f'{limits_line.Name}.Placement.Base.y + {limits_line.Name}.Y2')
        limits_min_circle2.setExpression('.Placement.Base.z',
                                         f'{limits_line.Name}.Placement.Base.z + {limits_line.Name}.Z2')
        limits_max_circle2.setExpression('.Placement.Base',
                                         f'{limits_min_circle2.Name}.Placement.Base')
        limits_min_circle2.setExpression('.Radius', f'{limits_min_circle1.Name}.Radius')
        limits_max_circle2.setExpression('.Radius', f'{limits_max_circle1.Name}.Radius')

        limits_min_circle2.setExpression('.Placement.Rotation', f'{limits_min_circle1.Name}.Placement.Rotation')
        limits_max_circle1.setExpression('.Placement.Rotation', f'{limits_min_circle1.Name}.Placement.Rotation')
        limits_max_circle2.setExpression('.Placement.Rotation', f'{limits_min_circle1.Name}.Placement.Rotation')
        limits_line_GUI = FreeCADGui.ActiveDocument.getObject(limits_line.Name)
        limits_min_circle1_GUI = FreeCADGui.ActiveDocument.getObject(limits_min_circle1.Name)
        limits_min_circle2_GUI = FreeCADGui.ActiveDocument.getObject(limits_min_circle2.Name)
        limits_max_circle1_GUI = FreeCADGui.ActiveDocument.getObject(limits_max_circle1.Name)
        limits_max_circle2_GUI = FreeCADGui.ActiveDocument.getObject(limits_max_circle2.Name)
        limits_line_GUI.LineColor = DAMPING_COLOR
        limits_min_circle1_GUI.LineColor = DAMPING_COLOR
        limits_min_circle2_GUI.LineColor = DAMPING_COLOR
        limits_max_circle1_GUI.LineColor = DAMPING_COLOR
        limits_max_circle2_GUI.LineColor = DAMPING_COLOR
        damping_group.addObject(limits_line)
        damping_group.addObject(limits_min_circle1)
        damping_group.addObject(limits_max_circle1)
        damping_group.addObject(limits_min_circle2)
        damping_group.addObject(limits_max_circle2)

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    get_fc_object(DAMPING_GROUP_NAME).addObject(damping_group)

    return damping_group.Name


def create_inout_zone_line(line_info: InletOutletZoneLineGenerator, direction: InletOutletZone2DDirection,
                           rotation: InletOutletZone2DRotation) -> str:
    zone_line_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_IOZoneLineGroup")
    zone_line = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.LINE, "Helper_IOZoneLine")

    zone_line_GUI = FreeCADGui.ActiveDocument.getObject(zone_line.Name)
    zone_line_GUI.LineColor = (0.32, 1.00, 0.00)
    line_vect = (FreeCAD.Vector(line_info.point2) - FreeCAD.Vector(line_info.point)) * DIVIDER
    position_vect = (FreeCAD.Vector(line_info.point)) * DIVIDER  # Start from beginning)
    direction_vect = FreeCAD.Vector(direction.direction[0], 0, direction.direction[1]) * DIVIDER
    zone_line.X1 = 0
    zone_line.Y1 = 0
    zone_line.Z1 = 0
    zone_line.X2 = line_vect.x
    zone_line.Y2 = line_vect.y
    zone_line.Z2 = line_vect.z
    zone_line.Placement.Base = position_vect
    zone_direction_line = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.LINE, "Helper_IODirectionLine")
    zone_direction_line.X1 = 0
    zone_direction_line.Y1 = 0
    zone_direction_line.Z1 = 0
    zone_direction_line.X2 = direction_vect.x
    zone_direction_line.Y2 = direction_vect.y
    zone_direction_line.Z2 = direction_vect.z
    name = zone_line.Name
    zone_direction_line.setExpression('.AttachmentOffset.Base.x', f'{name}.X2/2')
    zone_direction_line.setExpression('.AttachmentOffset.Base.y', f'{name}.Y2 / 2')
    zone_direction_line.setExpression('.AttachmentOffset.Base.z', f'{name}.Z2/2')
    zone_direction_line.AttachmentSupport = [zone_line, '']
    zone_direction_line.MapPathParameter = 0.0
    zone_direction_line.MapMode = 'ObjectXY'
    zone_direction_line.recompute()

    zone_direction_line_GUI = FreeCADGui.ActiveDocument.getObject(zone_direction_line.Name)
    zone_direction_line_GUI.DrawStyle = "Dotted"
    zone_direction_line_GUI.ShapeColor = (0.32, 1.00, 0.00)
    zone_direction_line_GUI.LineColor = (0.32, 1.00, 0.00)
    zone_direction_line_GUI.PointColor = (0.32, 1.00, 0.00)

    zone_line_gui = FreeCADGui.ActiveDocument.getObject(zone_direction_line.Name)
    zone_line_gui.ShowInTree = False
    zone_line_gui.Selectable = False

    # CHECK FOR CENTER
    axis = FreeCAD.Base.Vector(0, 1, 0)  # IOZone rotations go reverse in FreeCAD and in DS why?
    if rotation.rotation_enabled:
        angle = rotation.rotation_angle
    else:
        angle = 0
    rotation = FreeCAD.Base.Rotation(axis, angle)
    zone_line.Placement.Rotation = rotation
    zone_line_group.addObject(zone_line)
    zone_line_group.addObject(zone_direction_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_line_group)
    FreeCAD.ActiveDocument.recompute()
    return zone_line_group.Name


def update_inout_zone_line(fc_object_name: str, line_info: InletOutletZoneLineGenerator,
                           direction: InletOutletZone2DDirection, rotation: InletOutletZone2DRotation) -> str:
    zone_line_group = get_fc_object(fc_object_name)
    zone_line = zone_line_group.OutList[0]
    if line_info.manual_setting : # FreeCAD manual position and rotation
        zone_line.setPropertyStatus("Placement", ["-ReadOnly"])
    else :
        line_vect = (FreeCAD.Vector(line_info.point2) - FreeCAD.Vector(line_info.point)) * DIVIDER
        position_vect = (FreeCAD.Vector(line_info.point)) * DIVIDER  # Start from beginning)
        direction_vect = FreeCAD.Vector(direction.direction[0], 0, direction.direction[1]) * DIVIDER
        zone_line.X2 = line_vect.x
        zone_line.Y2 = line_vect.y
        zone_line.Z2 = line_vect.z
        # zone_line.Placement.Base=position_vect
        zone_direction_line = zone_line_group.OutList[1]
        zone_direction_line.X2 = direction_vect.x
        zone_direction_line.Y2 = direction_vect.y
        zone_direction_line.Z2 = direction_vect.z
        zone_direction_line.recompute()
        if rotation.rotation_enabled:
            rot_center = FreeCAD.Vector(rotation.rotation_center[0], 0,
                                        rotation.rotation_center[1]) * DIVIDER  # y = 0 is correct?¿ check
            rot_point = rot_center - position_vect
            axis = FreeCAD.Base.Vector(0, 1, 0)  # IOZone rotations go reverse in FreeCAD and in DS why? #y = 1 is correct¿?
            if rotation.rotation_enabled:
                angle = rotation.rotation_angle
            else:
                angle = 0
            fc_rotation = FreeCAD.Base.Rotation(axis, angle)
        else:
            fc_rotation = FreeCAD.Base.Rotation(FreeCAD.Vector(0,0,1),0)
            rot_point = position_vect
        zone_line.Placement = FreeCAD.Placement(position_vect, fc_rotation, rot_point)
        zone_line.setPropertyStatus("Placement", ["ReadOnly"])
        FreeCAD.ActiveDocument.recompute()
    return zone_line_group.Name


def create_inout_zone_box(box_info: InletOutletZoneBoxGenerator, direction: InletOutletZone3DDirection,
                          rotation: InletOutletZone3DRotation) -> str:
    zone_box_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_IOZoneboxGroup")
    zone_box_name = draw_box(point=box_info.point, size=box_info.size, name="Helper_IOZonebox",
                             rotation_angle=rotation.rotateaxis_angle, rotation_axis_p1=rotation.rotateaxis_point1,
                             rotation_axis_p2=rotation.rotateaxis_point2, )
    zone_box = get_fc_object(zone_box_name)
    zone_box.addProperty("App::PropertyVector", "lastposition")

    zone_line_name = draw_line(point1=[0, 0, 0], point2=direction.direction, name="Helper_IOZoneArrow")
    zone_line = get_fc_object(zone_line_name)

    name = zone_box.Name
    zone_line.setExpression('.AttachmentOffset.Base.x', f'{name}.Length / 2')
    zone_line.setExpression('.AttachmentOffset.Base.y', f'{name}.Width / 2')
    zone_line.setExpression('.AttachmentOffset.Base.z', f'{name}.Height / 2')
    zone_line.MapReversed = False
    zone_line.AttachmentSupport = [(zone_box, '')]
    zone_line.MapPathParameter = 0.000000
    zone_line.MapMode = 'ObjectXY'
    zone_line.recompute()

    zone_line_gui = FreeCADGui.ActiveDocument.getObject(zone_line.Name)
    zone_line_gui.ShowInTree = False
    zone_line_gui.Selectable = False

    zone_box_group.addObject(zone_box)
    zone_box_group.addObject(zone_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_box_group)
    FreeCAD.ActiveDocument.recompute()
    return zone_box_group.Name


def update_inout_zone_box(fc_obj_name: str, box_info: InletOutletZoneBoxGenerator,
                          direction: InletOutletZone3DDirection, rotation: InletOutletZone3DRotation):
    zone_box_group = get_fc_object(fc_obj_name)
    zone_box = zone_box_group.OutList[0]
    if box_info.manual_setting : # FreeCAD manual position and rotation
        zone_box.setPropertyStatus("Placement", ["-ReadOnly"])
    else :
        if rotation.rotation_type == 0:
            update_box(zone_box.Name, point=box_info.point, size=box_info.size,
                       rotation_angle=0, rotation_axis_p1=rotation.rotateaxis_point1,
                       rotation_axis_p2=rotation.rotateaxis_point2, )
        elif rotation.rotation_type == 1:
            update_box(zone_box.Name, point=box_info.point, size=box_info.size,
                       rotation_angle=rotation.rotateaxis_angle, rotation_axis_p1=rotation.rotateaxis_point1,
                       rotation_axis_p2=rotation.rotateaxis_point2, )
        elif rotation.rotation_type == 2:
            update_box_adv(zone_box.Name, point=box_info.point, size=box_info.size,
                           rotation_angle=rotation.rotateadv_angle, rotation_center=rotation.rotateadv_center)
        zone_box.setPropertyStatus("Placement", ["ReadOnly"])
    #zone_box.lastposition = zone_box.Placement.Base
    direction_vector = FreeCAD.Vector(direction.direction)
    zone_line = zone_box_group.OutList[1]
    update_line(zone_line.Name, point1=[0, 0, 0], point2=direction_vector)
    FreeCAD.ActiveDocument.recompute()
    return zone_box_group.Name


def create_inout_zone_circle(circle_info: InletOutletZoneCircleGenerator, direction: InletOutletZone3DDirection,
                             rotation: InletOutletZone3DRotation) -> str:
    zone_circle_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_IOZoneCircleGroup")
    zone_circle_name = draw_circle(circle_info.point, circle_info.radius, rotation.rotateaxis_angle,
                                   rotation.rotateaxis_point1, rotation.rotateaxis_point2, "Helper_IOZoneCircle")
    zone_circle = get_fc_object(zone_circle_name)
    zone_circle.addProperty("App::PropertyVector", "lastposition")
    direction_vector = FreeCAD.Vector(direction.direction) * DIVIDER
    zone_line_name = draw_line(point1=[0, 0, 0], point2=[0, 0, 1], name="Helper_IOZoneArrow")
    zone_line = get_fc_object(zone_line_name)

    zone_line_gui = FreeCADGui.ActiveDocument.getObject(zone_line.Name)
    zone_line_gui.ShowInTree = False
    zone_line_gui.Selectable = False

    pos_vector = FreeCAD.Vector(circle_info.point) * DIVIDER
    orig_vec = FreeCAD.Base.Vector(0, 0, 1)
    line_vec = direction_vector
    initial_rotation = FreeCAD.Base.Rotation(orig_vec, line_vec)
    initial_placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), initial_rotation)
    rotation_center = FreeCAD.Vector(rotation.rotateaxis_point1) * DIVIDER
    rotation_vector = -((FreeCAD.Vector(rotation.rotateaxis_point2) * DIVIDER) - rotation_center)  # Inverted, why?
    if rotation.rotateaxis_enabled:
        angle = rotation.rotateaxis_angle
    else:
        angle = 0
    user_rotation = FreeCAD.Base.Rotation(rotation_vector, angle)
    rotation_point = rotation_center - pos_vector
    user_placement = FreeCAD.Placement(pos_vector, user_rotation, rotation_point)
    final_placement = user_placement.multiply(initial_placement)
    zone_circle.Placement = final_placement

    zone_line.AttachmentOffset = FreeCAD.Placement(FreeCAD.Vector(0.0, 0.0, 0.0),
                                                   FreeCAD.Rotation(FreeCAD.Vector(1.0, 0.0, 0.0), 0))



    zone_line.MapReversed = False
    zone_line.AttachmentSupport = [(zone_circle, '')]
    zone_line.MapPathParameter = 0.000000
    zone_line.MapMode = 'ObjectXY'

    zone_line.recompute()

    #zone_circle.setExpression('.Placement.Rotation.Angle', f'{math.degrees(zone_circle.Placement.Rotation.Angle)}')

    zone_circle_group.addObject(zone_circle)
    zone_circle_group.addObject(zone_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_circle_group)

    FreeCAD.ActiveDocument.recompute()
    return zone_circle_group.Name


def update_inout_zone_circle(fc_object_name: str, circle_info: InletOutletZoneCircleGenerator,
                             direction: InletOutletZone3DDirection, rotation: InletOutletZone3DRotation) -> str:
    zone_circle_group = get_fc_object(fc_object_name)
    zone_circle = zone_circle_group.OutList[0]
    zone_line = zone_circle_group.OutList[1]
    if circle_info.manual_setting:
        zone_circle.setPropertyStatus("Placement", ["-ReadOnly"])
    else:
        direction_vector = FreeCAD.Vector(direction.direction) * DIVIDER
        pos_vector = FreeCAD.Vector(circle_info.point) * DIVIDER
        orig_vec = FreeCAD.Base.Vector(0, 0, 1)
        line_vec = direction_vector
        initial_rotation = FreeCAD.Base.Rotation(orig_vec, line_vec)
        initial_placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), initial_rotation)
        #zone_circle.Radius = circle_info.radius * DIVIDER
        if rotation.rotation_type == 0:
            zone_circle.Placement = FreeCAD.Placement(pos_vector, initial_rotation)
        elif rotation.rotation_type == 1:
            user_rotation = FreeCAD.Rotation(
                FreeCAD.Vector(rotation.rotateaxis_point1) - FreeCAD.Vector(rotation.rotateaxis_point2),
                rotation.rotateaxis_angle)
            rotation_center = FreeCAD.Vector(rotation.rotateaxis_point1) * DIVIDER
            rotation_point = rotation_center - pos_vector
            user_placement = FreeCAD.Placement(pos_vector, user_rotation, rotation_point)
            final_placement = user_placement.multiply(initial_placement)
            zone_circle.Placement = final_placement
            #zone_circle.setExpression('.Placement.Rotation.Angle', f'{math.degrees(zone_circle.Placement.Rotation.Angle)}')
            circle_info.size_from_freecad_circle(zone_circle)
            #rotation.rotate_axis_from_freecad_placement(user_placement)
        elif rotation.rotation_type == 2:
            user_rotation = FreeCAD.Rotation(rotation.rotateadv_angle[2], rotation.rotateadv_angle[1],
                                             rotation.rotateadv_angle[0])
            rotation_center = FreeCAD.Vector(rotation.rotateadv_center) * DIVIDER
            rotation_point = rotation_center - pos_vector
            user_placement = FreeCAD.Placement(pos_vector, user_rotation, rotation_point)
            final_placement = user_placement.multiply(initial_placement)
            zone_circle.Placement = final_placement
            #zone_circle.setExpression('.Placement.Rotation.Angle', f'{math.degrees(zone_circle.Placement.Rotation.Angle)}')
            circle_info.size_from_freecad_circle(zone_circle)
            #rotation.adv_rotation_from_freecad_placement(user_placement)
        zone_circle.setPropertyStatus("Placement", ["ReadOnly"])
        zone_line.recompute() #?

    return zone_circle_group.Name

def create_inout_zone_3d_mk_object(obj_name:str) -> str:
    zone_mk_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_IOZoneMKGroup")
    zone_object=get_fc_object(obj_name)
    clone_name = copy_object(obj_name)
    clone_obj=get_fc_object(clone_name)
    clone_obj.AttachmentSupport = [(zone_object, '')]
    clone_obj.MapMode = 'ObjectXY'
    clone_obj_gui = clone_obj.ViewObject
    clone_obj_gui.DisplayMode = FreeCADDisplayMode.WIREFRAME
    clone_obj_gui.DrawStyle = "Dotted"
    clone_obj_gui.LineColor = (0.32, 1.00, 0.00)

    zone_line_name = draw_line(point1=[0, 0, 0], point2=[0, 0, 1], name="Helper_IOZoneArrow")
    zone_line = get_fc_object(zone_line_name)
    zone_line.AttachmentSupport = [(zone_object, '')]
    zone_line.MapMode = 'ObjectXY'

    zone_line_gui = FreeCADGui.ActiveDocument.getObject(zone_line.Name)
    zone_line_gui.ShowInTree = False
    zone_line_gui.Selectable = False

    zone_mk_group.addObject(clone_obj)
    zone_mk_group.addObject(zone_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_mk_group)


    return zone_mk_group.Name

def change_mk_inout_zone_3d(fc_object_name,new_mk_object_name) -> str:
    zone_mk_group = get_fc_object(fc_object_name)
    old_zone_object=zone_mk_group.OutList[0]
    zone_line = zone_mk_group.OutList[1]
    delete_object(old_zone_object.Name)
    zone_mk_group.removeObject(zone_line)
    new_zone_object = get_fc_object(new_mk_object_name)
    clone_name = copy_object(new_mk_object_name)
    clone_obj = get_fc_object(clone_name)
    clone_obj.AttachmentSupport = [(new_zone_object, '')]
    clone_obj.MapMode = 'ObjectXY'
    clone_obj_gui = clone_obj.ViewObject
    clone_obj_gui.DisplayMode = FreeCADDisplayMode.WIREFRAME
    clone_obj_gui.DrawStyle = "Dotted"
    clone_obj_gui.LineColor = (0.32, 1.00, 0.00)

    zone_line.AttachmentSupport = [(clone_obj, '')]

    zone_mk_group.addObject(clone_obj)
    zone_mk_group.addObject(zone_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_mk_group)

    return zone_mk_group.Name


def update_inout_zone_3d_mk_object(fc_object_name,mk_info: InletOutletZoneMKGenerator, direction: InletOutletZone3DDirection,
                             rotation: InletOutletZone3DRotation,original_object_name:str) -> str:
    zone_mk_group =get_fc_object(fc_object_name)
    original_object=get_fc_object(original_object_name)
    clone_obj=zone_mk_group.OutList[0]
    zone_line=zone_mk_group.OutList[1]

    pos_vector=original_object.Placement.Base
    zero_vector=FreeCAD.Vector(0,0,0)

    if mk_info.direction==InletOutletDirection.LEFT:
        direction_vector=FreeCAD.Vector(-1,0,0)
    elif mk_info.direction==InletOutletDirection.RIGHT:
        direction_vector=FreeCAD.Vector(1,0,0)
    elif mk_info.direction==InletOutletDirection.TOP:
        direction_vector=FreeCAD.Vector(0,0,1)
    elif mk_info.direction==InletOutletDirection.BOTTOM:
        direction_vector=FreeCAD.Vector(0,0,-1)
    elif mk_info.direction==InletOutletDirection.FRONT:
        direction_vector=FreeCAD.Vector(0,1,0)
    elif mk_info.direction==InletOutletDirection.BACK:
        direction_vector=FreeCAD.Vector(0,-1,0)
    else: #CUSTOM
        direction_vector=FreeCAD.Vector(direction.direction)*DIVIDER
    update_line(zone_line.Name, point1=[0, 0, 0], point2=direction_vector)

    if rotation.rotation_type == 0:
        clone_obj.AttachmentOffset = FreeCAD.Placement(zero_vector, FreeCAD.Rotation(FreeCAD.Vector(1.0, 0.0, 0.0), 0))
        zone_line.AttachmentOffset = FreeCAD.Placement(zero_vector, FreeCAD.Rotation(FreeCAD.Vector(1.0, 0.0, 0.0), 0))
    elif rotation.rotation_type == 1:
        rotation_center = FreeCAD.Vector(rotation.rotateaxis_point1)*DIVIDER # Center
        rotation_vector = -((FreeCAD.Vector(rotation.rotateaxis_point2) ) - FreeCAD.Vector(rotation.rotateaxis_point1))
        fc_rotation = FreeCAD.Base.Rotation(rotation_vector, rotation.rotateaxis_angle)
        rotation_point = rotation_center - pos_vector
        final_placement = FreeCAD.Placement(zero_vector, fc_rotation, rotation_point)
        clone_obj.AttachmentOffset = final_placement
        zone_line.AttachmentOffset = final_placement
    elif rotation.rotation_type == 2:
        rotation_center = FreeCAD.Vector(rotation.rotateadv_center) * DIVIDER  # Center
        fc_rotation = FreeCAD.Base.Rotation(rotation.rotateadv_angle[2], rotation.rotateadv_angle[1], rotation.rotateadv_angle[0])
        rotation_point = rotation_center - pos_vector
        clone_obj.AttachmentOffset = FreeCAD.Placement(zero_vector, fc_rotation, rotation_point)
        zone_line.AttachmentOffset = FreeCAD.Placement(zero_vector, fc_rotation, rotation_point)
    FreeCAD.ActiveDocument.recompute()
    return zone_mk_group.Name


def update_inout_zone_2d_mk_object(fc_object_name,mk_info: InletOutletZoneMKGenerator, direction: InletOutletZone2DDirection,
                             rotation: InletOutletZone2DRotation,original_object_name) -> str:
    zone_mk_group =get_fc_object(fc_object_name)
    original_object=get_fc_object(original_object_name)
    clone_obj=zone_mk_group.OutList[0]
    zone_line=zone_mk_group.OutList[1]
    zone_mk_group.addObject(clone_obj)
    zone_mk_group.addObject(zone_line)
    FreeCAD.ActiveDocument.getObject(IO_ZONES_GROUP_NAME).addObject(zone_mk_group)

    pos_vector=original_object.Placement.Base
    zero_vector=FreeCAD.Vector(0,0,0)

    if mk_info.direction==InletOutletDirection.LEFT:
        direction_vector=FreeCAD.Vector(-1,0,0)
    elif mk_info.direction==InletOutletDirection.RIGHT:
        direction_vector=FreeCAD.Vector(1,0,0)
    elif mk_info.direction==InletOutletDirection.TOP:
        direction_vector=FreeCAD.Vector(0,0,1)
    elif mk_info.direction==InletOutletDirection.BOTTOM:
        direction_vector=FreeCAD.Vector(0,0,-1)
    else: #CUSTOM
        direction_vector=FreeCAD.Vector(direction.direction)*DIVIDER
    update_line(zone_line.Name, point1=[0, 0, 0], point2=direction_vector)

    if not rotation.rotation_enabled:
        clone_obj.AttachmentOffset = FreeCAD.Placement(zero_vector, FreeCAD.Rotation(FreeCAD.Vector(1.0, 0.0, 0.0), 0))
    else :
        axis = FreeCAD.Base.Vector(0, 1, 0)
        rot_center = FreeCAD.Vector(rotation.rotation_center[0], 0,
                                    rotation.rotation_center[1]) * DIVIDER  # y = 0 is correct?¿ check
        rot_point = rot_center - pos_vector
        fc_rotation = FreeCAD.Base.Rotation(axis, rotation.rotation_angle)
        clone_obj.AttachmentOffset = FreeCAD.Placement(FreeCAD.Vector(0,0,0), fc_rotation, rot_point)
        zone_line.AttachmentOffset = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), fc_rotation, rot_point)
    FreeCAD.ActiveDocument.recompute()
    return zone_mk_group.Name


def copy_object(fc_obj_name:str) -> str:
    obj = get_fc_object(fc_obj_name)
    clone=Draft.make_clone(obj)
    clone_name=clone.Name
    return clone_name

def create_vres_buffer_box(bufferbox_info: BufferBox) -> str:
    zone_box_name = draw_box(point=bufferbox_info.point, size=bufferbox_info.size, name="Helper_VresBufferBox",
                             rotation_angle=0,
                             rotation_axis_p1=[0, 0, 0], rotation_axis_p2=[0, 0, 1],color=VRES_BOXES_COLOR )
    zone_box = get_fc_object(zone_box_name)
    FreeCAD.ActiveDocument.getObject(VRES_BOXES_GROUP_NAME).addObject(zone_box)
    return zone_box_name


def update_vres_buffer_box(bufferbox_info: BufferBox):
    box=get_fc_object(bufferbox_info.fc_object_name)
    if bufferbox_info.manual_placement:
        box.setPropertyStatus("Placement", ["-ReadOnly"])
    else:
        if bufferbox_info.transform_enabled:
            point = list(FreeCAD.Vector(bufferbox_info.point) + FreeCAD.Vector(bufferbox_info.transform_move))
        else :
            point = bufferbox_info.point
        mult = 57.2958 if bufferbox_info.transform_rotate_radians else 1
        angle = [bufferbox_info.transform_rotate[0]*mult,bufferbox_info.transform_rotate[1]*mult,bufferbox_info.transform_rotate[2]*mult]
        update_box_adv(box.Name,point=point,size=bufferbox_info.size,rotation_angle=angle,
                       rotation_center=bufferbox_info.transform_center)
        box.setPropertyStatus("Placement", ["ReadOnly"])


def create_mesh_gauge_axes(mesh_gauge: MeshGauge) -> str:
    mesh_gauge_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_MeshGauge")
    axis_1_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_1stAxis")
    axis_2_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_2stAxis")
    axis_3_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_3stAxis")
    mesh_gauge_group.addObject(get_fc_object(axis_1_name))
    mesh_gauge_group.addObject(get_fc_object(axis_2_name))
    mesh_gauge_group.addObject(get_fc_object(axis_3_name))
    FreeCAD.ActiveDocument.getObject(GAUGES_GROUP_NAME).addObject(mesh_gauge_group)
    return mesh_gauge_group.Name


def update_mesh_gauge_axes(fc_object_name: str, mesh_gauge: MeshGauge):
    mesh_gauge_group = get_fc_object(fc_object_name)
    axis_1_name = mesh_gauge_group.OutList[0].Name
    axis_1_end = FreeCAD.Vector(mesh_gauge.point0) + FreeCAD.Vector(mesh_gauge.vec1) * mesh_gauge.size1_length
    update_line(axis_1_name, mesh_gauge.point0, axis_1_end)
    axis_2_name = mesh_gauge_group.OutList[1].Name
    axis_2_end = FreeCAD.Vector(mesh_gauge.point0) + FreeCAD.Vector(mesh_gauge.vec2) * mesh_gauge.size2_length
    update_line(axis_2_name, mesh_gauge.point0, axis_2_end)
    axis_3_name = mesh_gauge_group.OutList[2].Name
    axis_3_end = FreeCAD.Vector(mesh_gauge.point0) + FreeCAD.Vector(mesh_gauge.vec3) * mesh_gauge.size3_length
    update_line(axis_3_name, mesh_gauge.point0, axis_3_end)


def create_mesh_gauge_box(mesh_gauge: MeshGauge) -> str:
    mesh_gauge_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_MeshGauge")
    axis_1_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_1stAxis",color=GAUGES_COLOR)
    axis_2_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_2stAxis",color=GAUGES_COLOR)
    axis_3_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_3stAxis",color=GAUGES_COLOR)
    axis_4_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_4stAxis",color=GAUGES_COLOR)
    axis_5_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_5stAxis",color=GAUGES_COLOR)
    axis_6_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_6stAxis",color=GAUGES_COLOR)
    direction_name = draw_line(point1=mesh_gauge.point0, point2=mesh_gauge.point0, name="Helper_MeshGauge_Direction",
                               color=GAUGES_DIRECTION_COLOR)
    mesh_gauge_group.addObject(get_fc_object(axis_1_name))
    mesh_gauge_group.addObject(get_fc_object(axis_2_name))
    mesh_gauge_group.addObject(get_fc_object(axis_3_name))
    mesh_gauge_group.addObject(get_fc_object(axis_4_name))
    mesh_gauge_group.addObject(get_fc_object(axis_5_name))
    mesh_gauge_group.addObject(get_fc_object(axis_6_name))
    mesh_gauge_group.addObject(get_fc_object(direction_name))
    FreeCAD.ActiveDocument.getObject(GAUGES_GROUP_NAME).addObject(mesh_gauge_group)
    return mesh_gauge_group.Name


def update_mesh_gauge_box(fc_object_name: str, mesh_gauge: MeshGauge):
    mesh_gauge_group = get_fc_object(fc_object_name)
    init_point = FreeCAD.Vector(mesh_gauge.point0)
    vec1 = FreeCAD.Vector(mesh_gauge.vec1)
    vec2 = FreeCAD.Vector(mesh_gauge.vec2)
    vec3 = FreeCAD.Vector(mesh_gauge.vec3)
    axis1_vect = vec1.normalize() * mesh_gauge.size1_length if vec1.Length > 0 else FreeCAD.Vector(0, 0, 0)
    axis2_vect = vec2.normalize() * mesh_gauge.size2_length if vec2.Length > 0 else FreeCAD.Vector(0, 0, 0)
    axis3_vect = vec3.normalize() * mesh_gauge.size3_length if vec3.Length > 0 else FreeCAD.Vector(0, 0, 0)
    opposite_point = init_point + axis1_vect + axis2_vect + axis3_vect
    direction_start = init_point + axis1_vect / 2 + axis2_vect / 2 + axis3_vect / 2
    direction_end = direction_start + FreeCAD.Vector(mesh_gauge.dirdat)
    axis_1_name = mesh_gauge_group.OutList[0].Name
    axis_1_end = init_point + axis1_vect
    axis_2_name = mesh_gauge_group.OutList[1].Name
    axis_2_end = init_point + axis2_vect
    axis_3_name = mesh_gauge_group.OutList[2].Name
    axis_3_end = init_point + axis3_vect
    axis_4_name = mesh_gauge_group.OutList[3].Name
    axis_4_end = (opposite_point - axis1_vect)
    axis_5_name = mesh_gauge_group.OutList[4].Name
    axis_5_end = (opposite_point - axis2_vect)
    axis_6_name = mesh_gauge_group.OutList[5].Name
    axis_6_end = (opposite_point - axis3_vect)
    direction_name = mesh_gauge_group.OutList[6].Name
    update_line(axis_1_name, init_point, axis_1_end)
    update_line(axis_2_name, init_point, axis_2_end)
    update_line(axis_3_name, init_point, axis_3_end)
    update_line(axis_4_name, opposite_point, axis_4_end)
    update_line(axis_5_name, opposite_point, axis_5_end)
    update_line(axis_6_name, opposite_point, axis_6_end)
    update_line(direction_name, direction_start, direction_end)

def create_flow_gauge_box(flow_gauge: FlowGauge) -> str:
    flow_gauge_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "Helper_FlowGauge")
    axis_1_name = draw_line(point1=flow_gauge.point0, point2=flow_gauge.point0, name="Helper_FlowGauge_1stAxis",color=GAUGES_COLOR)
    axis_2_name = draw_line(point1=flow_gauge.point0, point2=flow_gauge.point0, name="Helper_FlowGauge_2stAxis",color=GAUGES_COLOR)
    axis_3_name = draw_line(point1=flow_gauge.point0, point2=flow_gauge.point0, name="Helper_FlowGauge_3stAxis",color=GAUGES_COLOR)
    axis_4_name = draw_line(point1=flow_gauge.point0, point2=flow_gauge.point0, name="Helper_FlowGauge_4stAxis",color=GAUGES_COLOR)
    direction_name = draw_line(point1=flow_gauge.point0, point2=flow_gauge.point0, name="Helper_FlowGauge_Direction",
                               color=GAUGES_DIRECTION_COLOR)
    flow_gauge_group.addObject(get_fc_object(axis_1_name))
    flow_gauge_group.addObject(get_fc_object(axis_2_name))
    flow_gauge_group.addObject(get_fc_object(axis_3_name))
    flow_gauge_group.addObject(get_fc_object(axis_4_name))
    flow_gauge_group.addObject(get_fc_object(direction_name))
    FreeCAD.ActiveDocument.getObject(GAUGES_GROUP_NAME).addObject(flow_gauge_group)
    return flow_gauge_group.Name


def update_flow_gauge_box(fc_object_name: str, flow_gauge:FlowGauge):
    flow_gauge_group = get_fc_object(fc_object_name)
    init_point = FreeCAD.Vector(flow_gauge.point0)
    vec1 = FreeCAD.Vector(flow_gauge.vec1)
    vec2 = FreeCAD.Vector(flow_gauge.vec2)
    axis1_vect = vec1.normalize() * flow_gauge.size1_length if vec1.Length > 0 else FreeCAD.Vector(0, 0, 0)
    axis2_vect = vec2.normalize() * flow_gauge.size2_length if vec2.Length > 0 else FreeCAD.Vector(0, 0, 0)
    opposite_point = init_point + axis1_vect + axis2_vect
    direction_start = init_point + axis1_vect / 2 + axis2_vect / 2
    direction_end = direction_start + FreeCAD.Vector(flow_gauge.dirdat)
    axis_1_name = flow_gauge_group.OutList[0].Name
    axis_1_end = init_point + axis1_vect
    axis_2_name = flow_gauge_group.OutList[1].Name
    axis_2_end = init_point + axis2_vect
    axis_3_name = flow_gauge_group.OutList[2].Name
    axis_3_end = (opposite_point - axis1_vect)
    axis_4_name = flow_gauge_group.OutList[3].Name
    axis_4_end = (opposite_point - axis2_vect)
    direction_name = flow_gauge_group.OutList[4].Name
    update_line(axis_1_name, init_point, axis_1_end)
    update_line(axis_2_name, init_point, axis_2_end)
    update_line(axis_3_name, opposite_point, axis_3_end)
    update_line(axis_4_name, opposite_point, axis_4_end)
    update_line(direction_name, direction_start, direction_end)



def create_parts_out_box(box: FilterPos) -> str:
    box_pos = box.pos_min
    box_pos2 = box.pos_max
    for i in range(3):
        if not box.enable_pos_min[i]:
            box_pos[i] = -999
        if not box.enable_pos_max[i]:
            box_pos2[i] = 999
    box_size = [y - x for x, y in zip(box_pos, box_pos2)]
    zone_box_name = draw_box(point=box.pos_min, size=box_size, name="Helper_PosFilter", rotation_angle=0,
                             rotation_axis_p1=[0, 0, 0], rotation_axis_p2=[0, 0, 1], color=OUTFILTERS_COLOR)
    return zone_box_name


def create_parts_out_sphere(sphere: FilterSphere) -> str:
    zone_sphere_name = draw_sphere(sphere.center, sphere.radius, "Helper_SphereFilter",color=OUTFILTERS_COLOR)
    zone_sphere = get_fc_object(zone_sphere_name)
    return zone_sphere.Name


def create_parts_out_cylinder(cylinder: FilterCylinder) -> str:
    zone_cylinder_name = draw_cylinder(cylinder.point1, cylinder.point2, cylinder.radius, "Helper_CylinderFilter",color=OUTFILTERS_COLOR)
    zone_cylinder = get_fc_object(zone_cylinder_name)
    return zone_cylinder.Name


def create_parts_out_plane(plane: FilterPlane) -> str:
    zone_plane_name = draw_infinite_plane(plane.point, plane.vector, "Helper_PlaneFilter")
    return zone_plane_name


def draw_box(point, size, name: str = "Box", rotation_angle=0.0, rotation_axis_p1=[0, 0, 0],
             rotation_axis_p2=[0, 0, 1], color=(0.32, 1.00, 0.00)) -> str:
    box = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, name)
    box_GUI = FreeCADGui.ActiveDocument.getObject(box.Name)
    box_GUI.LineColor = color
    box_GUI.DisplayMode = FreeCADDisplayMode.WIREFRAME
    box_vector = FreeCAD.Vector(size) * DIVIDER
    pos_vector = FreeCAD.Vector(point) * DIVIDER

    box.Length = box_vector[0] if box_vector[0] > 0.001 else 0.001
    box.Width = box_vector[1] if box_vector[1] > 0.001 else 0.001
    box.Height = box_vector[2] if box_vector[2] > 0.001 else 0.001

    rotation_center = FreeCAD.Vector(rotation_axis_p1) * DIVIDER  # Center
    rotation_vector = -((FreeCAD.Vector(rotation_axis_p2) * DIVIDER) - rotation_center)  # Inverted, why?
    rotation = FreeCAD.Base.Rotation(rotation_vector, rotation_angle)
    rotation_point = rotation_center - pos_vector
    box.Placement = FreeCAD.Placement(pos_vector, rotation, rotation_point)
    FreeCAD.ActiveDocument.recompute()
    return box.Name

def draw_plane(point, size, name: str = "Plane", rotation_angle=0.0, rotation_axis_p1=[0, 0, 0],
             rotation_axis_p2=[0, 0, 1], color=(0.32, 1.00, 0.00)) -> str:
    plane = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.PLANE, name)
    plane_GUI = FreeCADGui.ActiveDocument.getObject(plane.Name)
    plane_GUI.LineColor = color
    plane_GUI.DisplayMode = FreeCADDisplayMode.WIREFRAME

    point = [point[0],point[2],point[1]]

    plane_vector = FreeCAD.Vector(size) * DIVIDER
    pos_vector = FreeCAD.Vector(point) * DIVIDER

    plane.Length = plane_vector[0] if plane_vector[0] > 0.001 else 0.001
    plane.Width = plane_vector[2] if plane_vector[2] > 0.001 else 0.001  # Treat Z as "depth"

    # Start with rotation to stand the plane up (from XY to XZ)
    base_rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)  # Rotate 90° around X

    # Additional custom rotation if specified
    rotation_center = FreeCAD.Vector(rotation_axis_p1) * DIVIDER
    rotation_vector = -((FreeCAD.Vector(rotation_axis_p2) * DIVIDER) - rotation_center)
    custom_rotation = FreeCAD.Base.Rotation(rotation_vector, rotation_angle)

    # Combine both rotations
    total_rotation = base_rotation.multiply(custom_rotation)
    rotation_point = rotation_center - pos_vector

    plane.Placement = FreeCAD.Placement(pos_vector, total_rotation, rotation_point)

    FreeCAD.ActiveDocument.recompute()
    return plane.Name

def update_box(fc_object_name: str, point, size, rotation_angle=0.0, rotation_axis_p1=[0, 0, 0],
               rotation_axis_p2=[0, 0, 1]):
    box = get_fc_object(fc_object_name)
    box_vector = FreeCAD.Vector(size) * DIVIDER
    pos_vector = FreeCAD.Vector(point) * DIVIDER

    box.Length = box_vector[0] if box_vector[0] > 0.001 else 0.001
    box.Width = box_vector[1] if box_vector[1] > 0.001 else 0.001
    box.Height = box_vector[2] if box_vector[2] > 0.001 else 0.001

    rotation_center = FreeCAD.Vector(rotation_axis_p1) * DIVIDER  # Center
    rotation_vector = -((FreeCAD.Vector(rotation_axis_p2) * DIVIDER) - rotation_center)  # Inverted, why?
    rotation = FreeCAD.Base.Rotation(rotation_vector, rotation_angle)
    rotation_point = rotation_center - pos_vector
    final_placement = FreeCAD.Placement(pos_vector, rotation, rotation_point)
    box.Placement = final_placement

    # FreeCAD.ActiveDocument.recompute()

def update_flow_box(fc_obj_name:str,point, size, rotation_angle=[0.0, 0.0, 0.0]):
    get_fc_object(fc_obj_name).setPropertyStatus("Placement",-2)
    update_box_adv(fc_obj_name, point, size, rotation_angle, point)
    get_fc_object(fc_obj_name).setPropertyStatus("Placement", 2)

def update_box_adv(fc_object_name: str, point, size, rotation_angle=[0.0, 0.0, 0.0], rotation_center=[0.0, 0.0, 0.0]):
    box = get_fc_object(fc_object_name)
    box_vector = FreeCAD.Vector(size) * DIVIDER
    pos_vector = FreeCAD.Vector(point) * DIVIDER

    box.Length = box_vector[0] if box_vector[0] > 0.001 else 0.001
    box.Width = box_vector[1] if box_vector[1] > 0.001 else 0.001
    box.Height = box_vector[2] if box_vector[2] > 0.001 else 0.001

    rotation_center = FreeCAD.Vector(rotation_center) * DIVIDER  # Center
    rotation = FreeCAD.Base.Rotation(rotation_angle[2], rotation_angle[1], rotation_angle[0])
    rotation_point = rotation_center - pos_vector
    box.Placement = FreeCAD.Placement(pos_vector, rotation, rotation_point)
    # FreeCAD.ActiveDocument.recompute()


def draw_sphere(center, radius, name: str,color=(0.32, 1.00, 0.00)) -> str:
    zone_sphere = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.SPHERE, name)
    zone_sphere_GUI = FreeCADGui.ActiveDocument.getObject(zone_sphere.Name)
    zone_sphere_GUI.LineColor = color
    zone_sphere_GUI.DisplayMode = FreeCADDisplayMode.FLAT_LINES
    zone_sphere_GUI.Transparency = 80
    pos_vector = FreeCAD.Vector(center) * DIVIDER

    zone_sphere.Placement.Base = pos_vector
    zone_sphere.Radius = radius * DIVIDER

    FreeCAD.ActiveDocument.recompute()
    return zone_sphere.Name


def update_sphere(fc_object_name, center, radius) -> str:
    zone_sphere = get_fc_object(fc_object_name)
    pos_vector = FreeCAD.Vector(center) * DIVIDER

    zone_sphere.Placement.Base = pos_vector
    zone_sphere.Radius = radius * DIVIDER

    FreeCAD.ActiveDocument.recompute()
    return zone_sphere.Name


def draw_circle(center, radius, rotation_angle, rotation_axis_p1, rotation_axis_p2, name: str) -> str:
    circle = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CIRCLE, name)
    circle_GUI = FreeCADGui.ActiveDocument.getObject(circle.Name)
    circle_GUI.LineColor = (0.32, 1.00, 0.00)
    circle.Radius = radius * DIVIDER
    pos_vector = FreeCAD.Vector(center) * DIVIDER
    rotation_center = FreeCAD.Vector(rotation_axis_p1) * DIVIDER
    rotation_vector = -((FreeCAD.Vector(rotation_axis_p2) * DIVIDER) - rotation_center)  # Inverted, why?
    user_rotation = FreeCAD.Base.Rotation(rotation_vector, rotation_angle)
    rotation_point = rotation_center - pos_vector
    circle.Placement = FreeCAD.Placement(pos_vector, user_rotation, rotation_point)

    FreeCAD.ActiveDocument.recompute()
    return circle.Name


def update_circle(fc_object_name, center, radius, rotation_angle, rotation_axis_p1, rotation_axis_p2, name: str) -> str:
    circle = FreeCAD.ActiveDocument.getObject(fc_object_name)
    circle.Radius = radius * DIVIDER
    pos_vector = FreeCAD.Vector(center) * DIVIDER
    rotation_center = FreeCAD.Vector(rotation_axis_p1) * DIVIDER
    rotation_vector = -((FreeCAD.Vector(rotation_axis_p2) * DIVIDER) - rotation_center)  # Inverted, why?
    user_rotation = FreeCAD.Base.Rotation(rotation_vector, rotation_angle)
    rotation_point = rotation_center - pos_vector
    circle.Placement = FreeCAD.Placement(pos_vector, user_rotation, rotation_point)

    FreeCAD.ActiveDocument.recompute()


def draw_cylinder(point1, point2, radius, name: str,color=(0.32, 1.00, 0.00)) -> str:
    cylinder = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.CYLINDER, name)
    cylinder_GUI = FreeCADGui.ActiveDocument.getObject(cylinder.Name)
    cylinder_GUI.LineColor = color
    cylinder_GUI.DisplayMode = FreeCADDisplayMode.WIREFRAME
    pos_vector = FreeCAD.Vector(point1) * DIVIDER
    cylinder_vector = (FreeCAD.Vector(point2) * DIVIDER) - pos_vector
    cylinder_height = cylinder_vector.Length
    origin_vector = FreeCAD.Vector(0, 0, 1)
    cylinder.Placement.Base = pos_vector
    cylinder.Height = cylinder_height
    cylinder.Radius = radius * DIVIDER
    rotation = FreeCAD.Base.Rotation(origin_vector, cylinder_vector)
    position = FreeCAD.Placement(pos_vector, rotation)
    cylinder.Placement = position  # FreeCAD.Placement(pos_vector, rotation, rotation_point)
    FreeCAD.ActiveDocument.recompute()
    return cylinder.Name


def update_cylinder(fc_object_name: str, point1, point2, radius) :
    cylinder = get_fc_object(fc_object_name)
    pos_vector = FreeCAD.Vector(point1) * DIVIDER
    cylinder_vector = (FreeCAD.Vector(point2) * DIVIDER) - pos_vector
    cylinder_height = cylinder_vector.Length
    origin_vector = FreeCAD.Vector(0, 0, 1)
    cylinder.Placement.Base = pos_vector
    cylinder.Height = cylinder_height
    cylinder.Radius = radius * DIVIDER
    rotation = FreeCAD.Base.Rotation(origin_vector, cylinder_vector)
    position = FreeCAD.Placement(pos_vector, rotation)
    cylinder.Placement = position
    FreeCAD.ActiveDocument.recompute()


# Alternative (cylinder from two points and radius)

def draw_line(point1, point2, name: str, color=(0.32, 1.00, 0.00),draw_style="Dotted") -> str:
    line = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.LINE, name)
    line.Label = name
    line_GUI = FreeCADGui.ActiveDocument.getObject(line.Name)
    start = FreeCAD.Vector(point1) * DIVIDER
    end = FreeCAD.Vector(point2) * DIVIDER
    line.Placement.Base = start

    line.X1 = 0
    line.Y1 = 0
    line.Z1 = 0
    line.X2 = end[0] - start[0]
    line.Y2 = end[1] - start[1]
    line.Z2 = end[2] - start[2]
    line_GUI.DrawStyle = draw_style
    line_GUI.ShapeColor = color
    line_GUI.LineColor = color
    line_GUI.PointColor = color
    #  FreeCAD.ActiveDocument.recompute()  @TEST
    return line.Name


def update_line(fc_object_name, point1, point2):
    line = get_fc_object(fc_object_name)
    start = FreeCAD.Vector(point1) * DIVIDER
    end = FreeCAD.Vector(point2) * DIVIDER
    line.Placement.Base = start
    line.X1 = 0
    line.Y1 = 0
    line.Z1 = 0
    line.X2 = end[0] - start[0]
    line.Y2 = end[1] - start[1]
    line.Z2 = end[2] - start[2]
    FreeCAD.ActiveDocument.recompute()


def draw_infinite_plane(point, vector, name: str) -> str:
    plane = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.PLANE, name)
    plane_GUI = FreeCADGui.ActiveDocument.getObject(plane.Name)
    plane_GUI.LineColor = (0.32, 1.00, 0.00)
    plane_GUI.DisplayMode = FreeCADDisplayMode.FLAT_LINES
    length = 1000000
    width = 1000000
    plane.Length = length
    plane.Width = width
    plane_vector = FreeCAD.Vector(vector) * DIVIDER
    pos_vector = FreeCAD.Vector(point) * DIVIDER
    rotation_point = FreeCAD.Vector(length / 2, width / 2, 0)
    orig = FreeCAD.Vector(0, 0, 1)
    dest = plane_vector
    rotation = FreeCAD.Rotation(orig, dest)
    position = FreeCAD.Placement(pos_vector, FreeCAD.Rotation(0, 0, 0))
    displaze = FreeCAD.Placement(FreeCAD.Vector(-length / 2, -width / 2, 0), FreeCAD.Rotation(0, 0, 0))
    rotate = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), rotation, rotation_point)
    plane.Placement = position * displaze * rotate
    plane.ViewObject.Transparency = 90
    FreeCAD.ActiveDocument.recompute()
    return plane.Name


def delete_object(name: str):
    if FreeCAD.ActiveDocument.getObject(name):
        FreeCAD.ActiveDocument.removeObject(name)
        FreeCAD.ActiveDocument.recompute()


def delete_group(name: str):
    if FreeCAD.ActiveDocument.getObject(name):
        FreeCAD.ActiveDocument.getObject(name).removeObjectsFromDocument()
        FreeCAD.ActiveDocument.removeObject(name)
        FreeCAD.ActiveDocument.recompute()


def create_empty_document():
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    FreeCAD.newDocument(SINGLETON_DOCUMENT_NAME)

def create_dsph_document():
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    FreeCAD.newDocument(SINGLETON_DOCUMENT_NAME)
    prepare_dsph_case()


def create_dsph_document_from_fcstd(document_path):
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    temp_document_path = gettempdir() + "/" + "DSPH_Case.fcstd"
    copyfile(document_path, temp_document_path)
    FreeCAD.open(temp_document_path)
    prepare_dsph_case()


def document_count() -> int:
    """ Returns an integer representing the number of current opened documents in FreeCAD. """
    return len(FreeCAD.listDocuments().keys())


def document_open(document_name: str) -> bool:
    """ Returns whether the specified document name is opened within freecad. """
    return document_name.lower() in list(FreeCAD.listDocuments().keys())[0].lower()


def valid_document_environment() -> bool:
    """ Returns a boolean if a correct document environment is found.
    A correct document environment is defined if only a DSPH_Case document is currently opened in FreeCAD. """
    return document_count() == 1 and document_open(SINGLETON_DOCUMENT_NAME)


def prompt_close_all_documents(prompt: bool = True) -> bool:
    """ Shows a dialog to close all the current documents.
        If accepted, close all the current documents and return True, else returns False. """
    if prompt:
        user_selection = ok_cancel_dialog(APP_NAME, "All documents will be closed")
    if not prompt or user_selection == QtWidgets.QMessageBox.Ok:
        # Close all current documents.
        log(__("Closing all current documents"))
        for doc in FreeCAD.listDocuments().keys():
            FreeCAD.closeDocument(doc)
        return True
    return False


def get_fc_main_window():
    """ Returns FreeCAD main window. """
    return FreeCADGui.getMainWindow()


def get_fc_object(internal_name):
    """ Returns a FreeCAD internal object by a name. """
    return FreeCAD.ActiveDocument.getObject(internal_name)


def get_fc_view_object(internal_name):
    """ Returns a FreeCADGui View provider object by a name. """
    return FreeCADGui.ActiveDocument.getObject(internal_name)


def save_current_freecad_document(project_path: str) -> None:
    """ Saves the current freecad document with the common name. """
    FreeCAD.ActiveDocument.saveAs("{}/DSPH_Case.FCStd".format(project_path))
    FreeCADGui.SendMsgToActiveView("Save")


def add_fillbox_objects() -> None:
    """ Adds the necessary objects for a fillbox and sets its properties. """
    fillbox_gp = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "FillBox")
    fillbox_point = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.SPHERE, "FillPoint")
    fillbox_limits = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, "FillLimit")
    fillbox_limits.Length = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.Width = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.Height = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.ViewObject.DisplayMode = FreeCADDisplayMode.WIREFRAME
    fillbox_limits.ViewObject.LineColor = (0.00, 0.78, 1.00)
    fillbox_limits.addProperty("App::PropertyVector", "lastposition")
    fillbox_point.Radius.Value = FILLBOX_DEFAULT_RADIUS
    fillbox_point.Placement.Base = FreeCAD.Vector(500, 500, 500)
    fillbox_point.ViewObject.ShapeColor = (0.00, 0.00, 0.00)
    fillbox_point.addProperty("App::PropertyVector", "lastposition")
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    #Auto edit fillbox
    #FreeCADGui.ActiveDocument.setEdit(fillbox_limits, 0)


def manage_inlet_outlet_zones(zones):
    for input_zone in zones:
        if input_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.BOX:
            fc_group_obj = get_fc_object(input_zone.fc_object_name)
            update_box_inlet_data(fc_group_obj, input_zone.zone_info)
        elif input_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
            fc_group_obj = get_fc_object(input_zone.fc_object_name)
            update_circle_inlet_data(fc_group_obj, input_zone.zone_info)
        elif input_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.LINE:
            fc_group_obj = get_fc_object(input_zone.fc_object_name)
            update_line_inlet_data(fc_group_obj, input_zone.zone_info)

def update_box_inlet_data(fc_group_obj, zone_info: InletOutletZoneInfo):
    fc_obj = fc_group_obj.OutList[0]
    if zone_info.zone_box_generator.manual_setting:  # Get data from freeCAD object
        zone_info.zone_rotation_3d.adv_rotation_from_freecad_placement(fc_obj.Placement)
        zone_info.zone_box_generator.from_freecad_box(fc_obj)


def update_circle_inlet_data(fc_group_obj, zone_info: InletOutletZoneInfo):
    fc_obj = fc_group_obj.OutList[0]
    if zone_info.zone_circle_generator.manual_setting:  # Get data from freeCAD object
        zone_info.zone_rotation_3d.adv_rotation_from_freecad_placement(fc_obj.Placement)
        zone_info.zone_circle_generator.from_freecad_circle(fc_obj)

def update_line_inlet_data(fc_group_obj, zone_info: InletOutletZoneInfo):
    fc_obj = fc_group_obj.OutList[0]
    if zone_info.zone_line_generator.manual_setting:  # Get data from freeCAD object
        zone_info.zone_rotation_2d.rotation_from_freecad_placement(fc_obj.Placement)
        zone_info.zone_line_generator.from_freecad_line(fc_obj)

def manage_vres_bufferboxes(bufferboxes):
    for bbox in bufferboxes:
        fc_box = get_fc_object(bbox.fc_object_name)
        update_vres_data(fc_box, bbox)

def update_vres_data(fc_box, bbox: BufferBox):
    if bbox.manual_placement:
        bbox.point = list(fc_box.Placement.Base/DIVIDER)
        bbox.size = [
            fc_box.Length.Value / DIVIDER if fc_box.Length.Value / DIVIDER > 10e-6 else 0,
            fc_box.Width.Value / DIVIDER if fc_box.Width.Value / DIVIDER > 10e-6 else 0,
            fc_box.Height.Value / DIVIDER if fc_box.Height.Value / DIVIDER > 10e-6 else 0]
        bbox.transform_move=[0,0,0]
        bbox.transform_rotate=list(fc_box.Placement.Rotation.getYawPitchRoll())
        bbox.transform_rotate.reverse()
        bbox.transform_center=bbox.point.copy()

def manage_partfilters(filters: Dict[
    str, Union[BaseFilter, FilterPos, FilterSphere, FilterPlane, FilterCylinder, FilterMK, TypeFilter, FilterGroup]]):
    for po_filter in filters.values():
        if po_filter.filt_type in [FilterType.POS, FilterType.SPHERE, FilterType.CYLINDER]:
            fc_obj = get_fc_object(po_filter.fc_object_name)
            if fc_obj.Placement.Rotation.Angle != 0.0:
                if fc_obj.Placement.Base != fc_obj.lastposition:
                    fc_obj.Placement.Base = fc_obj.lastposition
                fc_obj.Placement.Rotation.Angle = 0.0
                warning_dialog(__("Rotation on Gauge objects cannot be modified"))
            fc_obj.lastposition = fc_obj.Placement.Base
            if po_filter.filt_type == FilterType.POS:
                po_filter.pos_min = list(fc_obj.Placement.Base / DIVIDER)
                po_filter.pos_max = [(fc_obj.Placement.Base[0] + fc_obj.Length.Value) / DIVIDER,
                                     (fc_obj.Placement.Base[1] + fc_obj.Width.Value) / DIVIDER,
                                     (fc_obj.Placement.Base[2] + fc_obj.Height.Value) / DIVIDER]
            elif po_filter.filt_type == FilterType.SPHERE:
                po_filter.center = list(fc_obj.Placement.Base / DIVIDER)
                po_filter.radius = (fc_obj.Radius / DIVIDER).Value
            elif po_filter.filt_type == FilterType.CYLINDER:
                po_filter.point1 = list(fc_obj.Placement.Base / DIVIDER)
                po_filter.radius = (fc_obj.Radius / DIVIDER).Value

def manage_gauges(gauges: Dict[str, Gauge]):
    for gauge in gauges.values():
        if gauge.type in ["velocity", "maxz", "swl"]:
            fc_obj = get_fc_object(gauge.fc_object_name)
            if list(fc_obj.Placement.Base / DIVIDER) != gauge.point0:
                gauge.point0 = list(fc_obj.Placement.Base / DIVIDER)
            if fc_obj.Placement.Rotation.Angle != 0.0:
                if fc_obj.Placement.Base != fc_obj.lastposition:
                    fc_obj.Placement.Base = fc_obj.lastposition
                fc_obj.Placement.Rotation.Angle = 0.0
                warning_dialog(__("Rotation on Gauge objects cannot be modified"))
            fc_obj.lastposition = fc_obj.Placement.Base
            if gauge.type == "maxz":
                if gauge.height != (fc_obj.Z2.Value - fc_obj.Z1.Value) / DIVIDER :
                    gauge.height = (fc_obj.Z2.Value - fc_obj.Z1.Value) / DIVIDER
            if gauge.type == "swl":
                if gauge.point1 != [(fc_obj.Placement.Base.x+fc_obj.X2.Value) / DIVIDER,
                                (fc_obj.Placement.Base.y+fc_obj.Y2.Value) / DIVIDER,
                                (fc_obj.Placement.Base.z+fc_obj.Z2.Value) / DIVIDER]:
                    gauge.point1 = [(fc_obj.Placement.Base.x+fc_obj.X2.Value) / DIVIDER,
                                (fc_obj.Placement.Base.y+fc_obj.Y2.Value) / DIVIDER,
                                (fc_obj.Placement.Base.z+fc_obj.Z2.Value) / DIVIDER]


def update_dp(dp:float):
    get_fc_object(CASE_LIMITS_OBJ_NAME).Dp = f'{dp}  m'

def draw_simulation_domain(min_x,min_y,min_z,max_x,max_y,max_z):
    size = [max_x - min_x, max_y - min_y, max_z - min_z]
    pos = [min_x, min_y, min_z]
    if AppMode.is_3d():
        # Create 3D box
        draw_box(point=pos,
            size=size,
            name=SIMULATION_DOMAIN_NAME,
            rotation_angle=0.0,
            rotation_axis_p1=[0, 0, 0],
            rotation_axis_p2=[0, 0, 1],
            color=SIMULATION_DOMAIN_COLOR
        )
    else:
        # Create 2D box (flat in XY plane)
        draw_plane(
            point=pos,
            size=size,
            name=SIMULATION_DOMAIN_NAME,
            rotation_angle=0.0,
            rotation_axis_p1=[0, 0, 0],
            rotation_axis_p2=[0, 0, 1],
            color=SIMULATION_DOMAIN_COLOR
        )
    
    simulation_domain = get_fc_object(SIMULATION_DOMAIN_NAME)
    # Make properties read-only
    props = ["Placement", "Length", "Width", "Height"] if AppMode.is_3d() else ["Placement", "Length", "Width"]
    for prop in props:
        simulation_domain.setPropertyStatus(prop, ["ReadOnly"])
    
    return simulation_domain

def update_simulation_domain(min_x,min_y,min_z,max_x,max_y,max_z):
    simulation_domain = get_fc_object(SIMULATION_DOMAIN_NAME)
        
    # Check if we need to switch between 3D and 2D
    current_obj_type = simulation_domain.TypeId if simulation_domain else ""
    
    # Delete old object and create new one
    if (AppMode.is_3d() and current_obj_type != FreeCADObjectType.BOX) \
        or (not AppMode.is_3d() and current_obj_type == FreeCADObjectType.BOX):
        FreeCAD.ActiveDocument.removeObject(SIMULATION_DOMAIN_NAME)
        FreeCAD.ActiveDocument.recompute()
        return draw_simulation_domain(min_x, min_y, min_z, max_x, max_y, max_z)
    
    # Normal update case
    size_x = max_x - min_x
    size_y = max_y - min_y
    size_z = max_z - min_z
    
    # Update position (convert meters to mm)
    simulation_domain.Placement.Base = FreeCAD.Vector(min_x * 1000,min_y * 1000 if AppMode.is_3d() else AppMode.get_2d_pos_y(),min_z * 1000)
    
    # Update dimensions
    simulation_domain.Length = f"{size_x} m"
    if AppMode.is_3d():
        simulation_domain.Width = f"{size_y} m"
        simulation_domain.Height = f"{size_z} m"
    else:
        simulation_domain.Width = f"{size_z} m"
    
    FreeCAD.ActiveDocument.recompute()
    return simulation_domain
