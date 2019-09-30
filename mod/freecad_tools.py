#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

''' FreeCAD related tools. '''

from tempfile import gettempdir
from shutil import copyfile

import FreeCAD
import FreeCADGui
import Draft

from PySide import QtGui

from mod.stdout_tools import log
from mod.constants import APP_NAME, SINGLETON_DOCUMENT_NAME, DEFAULT_WORKBENCH, CASE_LIMITS_OBJ_NAME, CASE_LIMITS_3D_LABEL
from mod.constants import CASE_LIMITS_LINE_COLOR, CASE_LIMITS_LINE_WIDTH, CASE_LIMITS_DEFAULT_LENGTH
from mod.enums import FreeCADObjectType, FreeCADDisplayMode
from mod.dialog_tools import ok_cancel_dialog
from mod.translation_tools import __


def prepare_dsph_case():
    ''' Creates a few objects and setups a new case for DesignSPHysics. '''
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
    ''' Setups a damping group with its properties within FreeCAD. '''
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
    ''' Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. '''
    FreeCAD.newDocument(SINGLETON_DOCUMENT_NAME)
    prepare_dsph_case()


def create_dsph_document_from_fcstd(document_path):
    ''' Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. '''
    temp_document_path = gettempdir() + "/" + "DSPH_Case.fcstd"
    copyfile(document_path, temp_document_path)
    FreeCAD.open(temp_document_path)
    prepare_dsph_case()


def document_count() -> int:
    ''' Returns an integer representing the number of current opened documents in FreeCAD. '''
    return len(FreeCAD.listDocuments().keys())


def document_open(document_name: str) -> bool:
    ''' Returns whether the specified document name is opened within freecad. '''
    return document_name.lower() in list(FreeCAD.listDocuments().keys())[0].lower()


def valid_document_environment() -> bool:
    ''' Returns a boolean if a correct document environment is found.
    A correct document environment is defined if only a DSPH_Case document is currently opened in FreeCAD. '''
    return document_count() == 1 and document_open(SINGLETON_DOCUMENT_NAME)


def prompt_close_all_documents(prompt: bool = True) -> bool:
    ''' Shows a dialog to close all the current documents.
        If accepted, close all the current documents and return True, else returns False. '''
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
    ''' Returns FreeCAD main window. '''
    return FreeCADGui.getMainWindow()


def get_fc_object(internal_name):
    ''' Returns a FreeCAD internal object by a name. '''
    return FreeCAD.ActiveDocument.getObject(internal_name)


def get_fc_view_object(internal_name):
    ''' Returns a FreeCADGui View provider object by a name. '''
    return FreeCADGui.ActiveDocument.getObject(internal_name)
