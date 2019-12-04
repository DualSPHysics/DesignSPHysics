#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Define Constants.
    This file contains a collection of constants meant to use with DesignSPHysics. """

from mod.enums import FreeCADObjectType

# APP Constants
FREECAD_MIN_VERSION = "018"
APP_NAME = "DesignSPHysics"
DEBUGGING = False
VERBOSE = False
DIVIDER = 1000
LINE_END = "\n"
PICKLE_PROTOCOL = 1  # Binary mode
VERSION = "0.6.0.1912-04-1"
WIDTH_2D = 0.001
MAX_PARTICLE_WARNING = 2000000
DISK_DUMP_FILE_NAME = "designsphysics-{}.log".format(VERSION)

# FreeCAD Related Constants
SINGLETON_DOCUMENT_NAME = "DSPH_Case"
DEFAULT_WORKBENCH = "PartWorkbench"
CASE_LIMITS_OBJ_NAME = "Case_Limits"
CASE_LIMITS_2D_LABEL = "Case Limits (2D)"
CASE_LIMITS_3D_LABEL = "Case Limits (3D)"
CASE_LIMITS_DEFAULT_LENGTH = "1000 mm"
CASE_LIMITS_LINE_COLOR = (1.00, 0.00, 0.00)
CASE_LIMITS_LINE_WIDTH = 2.00
FILLBOX_DEFAULT_LENGTH = "1000 mm"
FILLBOX_DEFAULT_RADIUS = 10

SUPPORTED_TYPES = [FreeCADObjectType.BOX, FreeCADObjectType.SPHERE, FreeCADObjectType.CYLINDER]

MAIN_WIDGET_INTERNAL_NAME = "DSPH Widget"
PROP_WIDGET_INTERNAL_NAME = "DSPH_Properties"
