#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Define Constants.

This file contains a collection of constants meant to use with DesignSPHysics.
"""

from mod.enums import FreeCADObjectType

# ------ APP Constants ------

FREECAD_MIN_VERSION = "018"
APP_NAME = "DesignSPHysics"
DEBUGGING = False
VERBOSE = False
DIVIDER = 1000
LINE_END = "\n"
PICKLE_PROTOCOL = 1  # Binary mode
VERSION = "0.6.0.1911-13-1"
WIDTH_2D = 0.001
MAX_PARTICLE_WARNING = 2000000
DISK_DUMP_FILE_NAME = "designsphysics-{}.log".format(VERSION)


# ------ FreeCAD Related Constants -------

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

# ------ DEFINE CONSTANTS  ------

""" --------- Help Window -------------- """

HELP_GRAVITYX = "Gravitational acceleration in X direction."
HELP_GRAVITYY = "Gravitational acceleration in Y direction."
HELP_GRAVITYZ = "Gravitational acceleration in Z direction."
HELP_RHOP0 = "Reference density of the fluid."
HELP_HSWL = "Maximum still water level to calculate speedofsound as the celerity during dam-break propagation."
HELP_GAMMA = "Polytropic constant for ocean water used in the state equation."
HELP_SPEEDSYSTEM = "Maximum speed system (by default the celerity during dam-break propagation)."
HELP_COEFSOUND = "Coefficient to multiply speedsystem"
HELP_SPEEDSOUND = "Speed of sound (by default speedofsound=coefsound*speedsystem). "
HELP_COEFH = "Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)."
HELP_CFLNUMBER = "Coefficient to multiply variable dt."


# ------ EXECUTION PARAMETERS  ------

""" --------- ToolTip -------------- """

DOMAINFIXED = "The domain is fixed with the specified values (xmin:ymin:zmin:xmax:ymax:zmax)"

XMIN = "The domain is fixed in the specified limit (default=not applied)"
XMAX = "The domain is fixed in the specified limit (default=not applied)"

YMIN = "The domain is fixed in the specified limit (default=not applied)"
YMAX = "The domain is fixed in the specified limit (default=not applied)"

ZMIN = "The domain is fixed in the specified limit (default=not applied)"
ZMAX = "The domain is fixed in the specified limit (default=not applied)"

PERIODX = ""
YINCEMENTX = "Increase of Y with periodic BC in axis X"
ZINCREMENTX = "Increase of Z with periodic BC in axis X"

PERIODY = ""
XINCREMENTY = "Increase of X with periodic BC in axis Y"
ZINCREMENTY = "Increase of Z with periodic BC in axis Y"

PERIODZ = ""
XINCREMENTZ = "Increase of X with periodic BC in axis Z"
YINCREMENTZ = "Increase of Y with periodic BC in axis Z"

""" --------- Help Window -------------- """

HELP_POSDOUBLE = "Precision in particle interaction 0:Simple, 1:Double, 2:Uses and saves double (default=0)."
HELP_STEPALGORITHM = "Time-integrator algorithm 1:Verlet, 2:Symplectic (default=1)."
HELP_VERLETSTEPS = "Verlet only: Number of steps to apply Euler timestepping (default=40)."
HELP_KERNEL = "Interaction Kernel 1:Cubic Spline, 2:Wendland, 3:Gaussian (default=2)"
HELP_VISCOTREATMENT = "Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)"
HELP_VISCO = "Viscosity value (apha when VISCOTREATMENT=1 and kinematic viscosity when VISCOTREATMENT=2)."
HELP_VISCOBOUNDFACTOR = "Multiply viscosity value for fluid-boundary interaction (default=1)."
HELP_DELTASPH = "DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)."
HELP_DENSITYDT = "DDT value (default=0.1)."
HELP_SHIFTING = "Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)."
HELP_SHIFTINGCOEF = "Coefficient for shifting computation (default=-2)."
HELP_SHIFTINGTFS = "Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)."
HELP_RIGIDALGORITHM = "Rigid Algorithm 1:SPH, 2:DEM, 3:Chrono (default=1)."
HELP_FTPAUSE = "Time to freeze the floating objects at beginning of simulation (default=0)."
HELP_DTINI = "Initial time step (default=h/speedsound)."
HELP_DTMIN = "Minimum time step (default=coefdtmin*h/speedsound)."
HELP_COEFDTMIN = "Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05)."
HELP_TIMEMAX = "Time of simulation."
HELP_TIMEOUT = "Time to save output data."
HELP_INCZ = "Increase of Z+ (%) (default=0)."
HELP_PARTSOUTMAX = "%%/100 of fluid particles allowed to be excluded from domain (default=1)."
HELP_RHOPOUTMIN = "Minimum rhop valid (default=700)."
HELP_RHOPOUTMAX = "Maximum rhop valid (default=1300)."
HELP_DOMAINFIXED = "The domain is fixed with the specified values (xmin:ymin:zmin:xmax:ymax:zmax)."
HELP_YINCREMENTX = ""
HELP_ZINCREMENTX = ""
HELP_XINCREMENTY = ""
HELP_ZINCREMENTY = ""
HELP_XINCREMENTZ = ""
HELP_YINCREMENTZ = ""
HELP_POSMINX = ""
HELP_POSMINY = ""
HELP_POSMINZ = ""
HELP_POSMAXX = ""
HELP_POSMAXY = ""
HELP_POSMAXZ = ""
