#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Define Constants.
    This file contains a collection of constants meant to use with DesignSPHysics. """

from mod.enums import FreeCADObjectType

# APP Constants
FREECAD_MIN_VERSION = "0.21"
APP_NAME = "DesignSPHysics"
DIVIDER = 1000
LINE_END = "\n"
PICKLE_PROTOCOL = 1  # Binary mode
VERSION = "0.8.1" # Version must be M.m.p (dd-mm-yyyy)
REVISION = "006" # Revision number must be rrr
VER_DATE = "(29-05-2025)" # Date version must be (dd-mm-yyyy)
WIDTH_2D = 0.001
DISK_DUMP_FILE_NAME = "designsphysics-{}.log".format(VERSION)
MKFLUID_LIMIT = 10
MKFLUID_OFFSET = 1
GITHUB_MASTER_CONSTANTS_URL = "https://raw.githubusercontent.com/DualSPHysics/DesignSPHysics/master/mod/constants.py"

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
CASE_3D_MODE = True
#Names for helper objects group folders
HELPER_FOLDER_GROUP_NAME = "Helper_Objects"
IO_ZONES_GROUP_NAME = "InOut_Zones"
VRES_BOXES_GROUP_NAME = "VResolution_Boxes"
GAUGES_GROUP_NAME = "Gauges"
VARIABLES_SHEET_NAME = "Variables"
OUTFILTERS_GROUP_NAME = "OutPartFilters"
FLOWBOXES_GROUP_NAME = "Flowtool_Boxes"
DAMPING_GROUP_NAME = "Damping_Zones"
SIMULATION_DOMAIN_NAME = "Simulation_domain"
#Colors for helper objects
IO_ZONES_COLOR = ((0.32, 1.00, 0.00))
VRES_BOXES_COLOR = (0.4,0.6,1.0)
GAUGES_COLOR = (1.0,1.0,0.0)
GAUGES_DIRECTION_COLOR = (1.0,1.0,0.4)
FLOWBOXES_COLOR = (0.1,0.1,1.0)
OUTFILTERS_COLOR = (1.0,0.4,0.6)
DAMPING_COLOR = (1.0,0.4,0.4)
SIMULATION_DOMAIN_COLOR = (0.1,0.1,0.0)

#Default widget sizes (for UnitInputs)
DEFAULT_MIN_WIDGET_WIDTH = 160
DEFAULT_MAX_WIDGET_WIDTH = 180
DEFAULT_WIDGET_HEIGHT = 24
DEFAULT_UNITS_CONFIG = 1 # 0: "mm" Millimeter; 1: "m" Meter
DEFAULT_DECIMALS = 3
AUTO_UNITS_SELECT = False
SUPPORTED_TYPES = [FreeCADObjectType.BOX, FreeCADObjectType.SPHERE, FreeCADObjectType.CYLINDER]

MAIN_WIDGET_INTERNAL_NAME = "DSPH Widget"
PROP_WIDGET_INTERNAL_NAME = "DSPH_Properties"


# In your mod/constants.py:
class Constants:
    """Dummy class that contains all module-level constants"""
    pass

# Copy all module-level constants into the class
import sys
module = sys.modules[__name__]
for name in dir(module):
    if not name.startswith('_'):
        setattr(Constants, name, getattr(module, name))

# Create an instance that pickle can find
constants = Constants()
