#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

""" FreeCAD related tools. """

from tempfile import gettempdir
from shutil import copyfile

import FreeCAD
import FreeCADGui
import Draft

from PySide import QtGui

from mod.translation_tools import __
from mod.stdout_tools import log, error, debug
from mod.dialog_tools import ok_cancel_dialog, error_dialog

from mod.constants import APP_NAME, SINGLETON_DOCUMENT_NAME, DEFAULT_WORKBENCH, CASE_LIMITS_OBJ_NAME, CASE_LIMITS_3D_LABEL
from mod.constants import CASE_LIMITS_LINE_COLOR, CASE_LIMITS_LINE_WIDTH, CASE_LIMITS_DEFAULT_LENGTH, FREECAD_MIN_VERSION
from mod.constants import MAIN_WIDGET_INTERNAL_NAME, PROP_WIDGET_INTERNAL_NAME, WIDTH_2D, FILLBOX_DEFAULT_LENGTH, FILLBOX_DEFAULT_RADIUS
from mod.enums import FreeCADObjectType, FreeCADDisplayMode


def delete_existing_docks():
    """ Searches for existing docks related to DesignSPHysics destroys them. """
    for previous_dock in [get_fc_main_window().findChild(QtGui.QDockWidget, MAIN_WIDGET_INTERNAL_NAME),
                          get_fc_main_window().findChild(QtGui.QDockWidget, PROP_WIDGET_INTERNAL_NAME)]:
        if previous_dock:
            debug("Removing previous {} dock".format(APP_NAME))
            previous_dock.setParent(None)
            previous_dock = None


def check_compatibility():
    """ Ensures the current version of FreeCAD is compatible with the macro. Spawns an error dialog and throws exception to halt
        the execution if its not. """
    if not is_compatible_version():
        error_dialog(__("This FreeCAD version is not compatible. Please update FreeCAD to version {} or higher.").format(FREECAD_MIN_VERSION))
        raise EnvironmentError(__("This FreeCAD version is not compatible. Please update FreeCAD to version {} or higher.").format(FREECAD_MIN_VERSION))


def is_compatible_version():
    """ Checks if the current FreeCAD version is suitable for this macro. """
    version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
    if float(version_num) < float(FREECAD_MIN_VERSION):
        return False
    return True


def prepare_dsph_case():
    """ Creates a few objects and setups a new case for DesignSPHysics. """
    FreeCAD.setActiveDocument(SINGLETON_DOCUMENT_NAME)
    FreeCAD.ActiveDocument = FreeCAD.ActiveDocument
    FreeCADGui.ActiveDocument = FreeCADGui.ActiveDocument
    FreeCADGui.activateWorkbench(DEFAULT_WORKBENCH)
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, CASE_LIMITS_OBJ_NAME)
    FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).Label = CASE_LIMITS_3D_LABEL
    FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).Length = CASE_LIMITS_DEFAULT_LENGTH
    FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).Width = CASE_LIMITS_DEFAULT_LENGTH
    FreeCAD.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).Height = CASE_LIMITS_DEFAULT_LENGTH
    FreeCADGui.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).DisplayMode = FreeCADDisplayMode.WIREFRAME
    FreeCADGui.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).LineColor = CASE_LIMITS_LINE_COLOR
    FreeCADGui.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).LineWidth = CASE_LIMITS_LINE_WIDTH
    FreeCADGui.ActiveDocument.getObject(CASE_LIMITS_OBJ_NAME).Selectable = False
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def setup_damping_environment() -> str:
    """ Setups a damping group with its properties within FreeCAD. """
    damping_group = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "DampingZone")

    # Limits line
    points = [FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1000, 1000, 1000)]
    limits = Draft.makeWire(points, closed=False, face=False, support=None)
    Draft.autogroup(limits)
    limits.Label = "Limits"
    limitsv = FreeCADGui.ActiveDocument.getObject(limits.Name)
    limitsv.ShapeColor = (0.32, 1.00, 0.00)
    limitsv.LineColor = (0.32, 1.00, 0.00)
    limitsv.PointColor = (0.32, 1.00, 0.00)
    limitsv.EndArrow = True
    limitsv.ArrowSize = "10 mm"
    limitsv.ArrowType = "Dot"

    # Overlimit line
    points = [FreeCAD.Vector(*limits.End), FreeCAD.Vector(1580, 1577.35, 1577.35)]
    overlimit = Draft.makeWire(points, closed=False, face=False, support=None)
    Draft.autogroup(overlimit)
    overlimit.Label = "Overlimit"
    overlimitv = FreeCADGui.ActiveDocument.getObject(overlimit.Name)
    overlimitv.DrawStyle = "Dotted"
    overlimitv.ShapeColor = (0.32, 1.00, 0.00)
    overlimitv.LineColor = (0.32, 1.00, 0.00)
    overlimitv.PointColor = (0.32, 1.00, 0.00)
    overlimitv.EndArrow = True
    overlimitv.ArrowSize = "10 mm"
    overlimitv.ArrowType = "Dot"

    # Add the two lines to the group
    damping_group.addObject(limits)
    damping_group.addObject(overlimit)

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")

    return damping_group.Name


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
    if not prompt or user_selection == QtGui.QMessageBox.Ok:
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


def enforce_case_limits_restrictions(mode_3d_enabled: bool = True):
    """ Enforces restrictions on the case limit object within FreeCAD, like rotation and width (in 2D mode). """
    case_limits_view = get_fc_view_object(CASE_LIMITS_OBJ_NAME)
    case_limits = get_fc_object(CASE_LIMITS_OBJ_NAME)
    if case_limits_view.DisplayMode != FreeCADDisplayMode.WIREFRAME:
        case_limits_view.DisplayMode = FreeCADDisplayMode.WIREFRAME
    if case_limits_view.LineColor != (1.00, 0.00, 0.00):
        case_limits_view.LineColor = (1.00, 0.00, 0.00)
    if case_limits_view.Selectable:
        case_limits_view.Selectable = False
    if case_limits.Placement.Rotation.Angle != 0.0:
        case_limits.Placement.Rotation.Angle = 0.0
        error(__("Can't change rotation on the Case Limits object."))
    if not mode_3d_enabled and case_limits.Width.Value != WIDTH_2D:
        case_limits.Width.Value = WIDTH_2D
        error(__("Can't change width of the Case Limits object while being in 2D mode."))


def enforce_fillbox_restrictions():
    """ Enforces restrictions on all fillboxes, resetting their rotations to 0. """
    for target in filter(lambda obj: obj.TypeId == FreeCADObjectType.FOLDER and "fillbox" in obj.Name.lower(), FreeCAD.ActiveDocument.Objects):
        for sub_element in target.OutList:
            if sub_element.Placement.Rotation.Angle != 0.0:
                sub_element.Placement.Rotation.Angle = 0.0
                error(__("Can't change rotation on Fillbox inner objects"))


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
    fillbox_point.Radius.Value = FILLBOX_DEFAULT_RADIUS
    fillbox_point.Placement.Base = FreeCAD.Vector(500, 500, 500)
    fillbox_point.ViewObject.ShapeColor = (0.00, 0.00, 0.00)
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
