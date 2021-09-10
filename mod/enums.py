#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Property enums.

This file holds a collection of useful enums
in class forms, for code organization
"""

from mod.translation_tools import __


class IrregularSpectrum():
    """ Types of supported wave spectrums. """
    JONSWAP = "jonswap"
    PIERSON_MOSKOWITZ = "pierson-moskowitz"

    def __init__(self):
        # Dummy init
        pass


class IrregularDiscretization():
    """ Types of supported spectrum discretization. """
    REGULAR = "regular"
    RANDOM = "random"
    STRETCHED = "stretched"
    COSSTRETCHED = "cosstretched"

    def __init__(self):
        # Dummy init
        pass


class AWASWaveOrder():
    """ Wave order to calculate elevation """
    FIRST_ORDER = 1
    SECOND_ORDER = 2


class AWASSaveMethod:
    """ Saving method for AWAS CSV """
    BY_PART = 1
    MORE_INFO = 2
    BY_STEP = 3


class SDPositionPropertyType:
    """ Simulation domain property type. """
    DEFAULT = 0
    VALUE = 1
    DEFAULT_VALUE = 2
    DEFAULT_PERCENTAGE = 3


class ObjectType:
    """ Simulation domain property type. """
    BOUND = "bound"
    FLUID = "fluid"
    SPECIAL = "mkspecial"


class ObjectFillMode:
    """ Simulation domain property type. """
    FULL = "full"
    SOLID = "solid"
    FACE = "face"
    WIRE = "wire"
    SPECIAL = "fillspecial"


class FloatingDensityType:
    """ Density type for floating mks. """
    MASSBODY = 0
    RHOPBODY = 1


class FreeCADObjectType:
    """ FreeCAD Types enums wrapping strings. """
    BOX = "Part::Box"
    FOLDER = "App::DocumentObjectGroup"
    SPHERE = "Part::Sphere"
    CYLINDER = "Part::Cylinder"
    CUSTOM_MESH = "Mesh::Feature"


class FreeCADDisplayMode:
    """ FreeCAD DisplayMode Strings. """
    WIREFRAME = "Wireframe"
    FLAT_LINES = "Flat Lines"


class InletOutletDetermLimit:
    """ Inlet/Oulet DetermLimit Value. """
    ZEROTH_ORDER = "1e+3"
    FIRST_ORDER = "1e-3"


class InletOutletZoneType:
    """ Inlet/Oulet Zone Type. """
    ZONE_2D = "zone2d"
    ZONE_3D = "zone3d"


class InletOutletZoneGeneratorType:
    """ Inlet/Outlet Zone Generator Type. """
    MK = 0
    LINE = 1
    BOX = 2
    CIRCLE = 3


class InletOutletDirection:
    """ Inlet/Outlet Zone Direction. """
    LEFT = "left"
    RIGHT = "right"
    FRONT = "front"
    BACK = "back"
    TOP = "top"
    BOTTOM = "bottom"


class InletOutletVelocityType:
    """ Inlet/Outlet Velocity Type """
    FIXED = 0
    VARIABLE = 1
    EXTRAPOLATED = 2
    INTERPOLATED = 3


class InletOutletVelocitySpecType:
    """ Inlet/Outlet Velocity Specification Type """
    FIXED_CONSTANT = 0
    FIXED_LINEAR = 1
    FIXED_PARABOLIC = 2
    VARIABLE_UNIFORM = 3
    VARIABLE_LINEAR = 4
    VARIABLE_PARABOLIC = 5
    FILE_UNIFORM = 6
    FILE_LINEAR = 7
    FILE_PARABOLIC = 8
    FILE_INTERPOLATED = 9


class InletOutletDensityType:
    """ Inlet/Outlet Density Type. """
    FIXED = 0
    HYDROSTATIC = 1
    EXTRAPOLATED = 2


class InletOutletElevationType:
    """ Inlet/Outlet Elevation Type. """
    FIXED = 0
    VARIABLE = 1
    AUTOMATIC = 2


class InletOutletZSurfMode:
    """ Inlet/Outlet ZSurf Mode. """
    FIXED = 0
    TIMELIST = 1
    FILE = 2


class InletOutletExtrapolateMode:
    """ Types of extrapolatemode for Inlet/Outlet configuration. """
    FAST_SINGLE = 1
    SINGLE = 2
    DOUBLE = 3


class InletOutletRefillingMode:
    """ Types of refilling for Inlet/Outlet configuration. """
    SIMPLE_FULL = 0
    SIMPLE_BELOW_ZSURF = 1
    ADVANCED_FOR_REVERSE_FLOWS = 2


class InletOutletInputTreatment:
    """ Types of inputtreatment for Inlet/Outlet configuration. """
    NO_CHANGES = 0
    CONVERT_FLUID = 1
    REMOVE_FLUID = 2


class ChronoModelNormalType:
    """ Chrono ModelNormal types. """
    ORIGINAL = "original"
    INVERT = "invert"
    TWOFACE = "twoface"


class ChronoFloatingType:
    """ Chrono Floating types. """
    BODYFLOATING = "bodyfloating"
    BODYFIXED = "bodyfixed"


class MotionType:
    """ Motion types """
    BASE = "Base Motion"
    BASE_WAVE_GENERATOR = "Base Wave Generator"
    MOVEMENT = "Movement"
    WAIT = "Wait Interval"
    WAVE = "Wave Movement"
    CIRCULAR = "Circular Motion"
    ROTATIONAL = "Rotational Motion"
    RECTILINEAR = "Rectilinear Motion"
    ACCELERATED_RECTILINEAR = "Accelerated Rectilinear motion"
    ACCELERATED_ROTATIONAL = "Accelerated Rotational Motion"
    SINUSOIDAL_RECTILINEAR = "Sinusoidal Rectilinear Motion"
    SINUSOIDAL_ROTATIONAL = "Sinusoidal Rotational Motion"
    SINUSOIDAL_CIRCULAR = "Sinusoidal Circular Motion"
    REGULAR_PISTON_WAVE_GENERATOR = "Regular Piston Wave Generator"
    IRREGULAR_PISTON_WAVE_GENERATOR = "Irregular Piston Wave Generator"
    REGULAR_FLAP_WAVE_GENERATOR = "Regular Flap Wave Generator"
    IRREGULAR_FLAP_WAVE_GENERATOR = "Irregular Flap Wave Generator"
    FILE_GENERATOR = "File Generator"
    FILE_ROTATIONAL_GENERATOR = "Rotational File Generator"


class MLPistonType:
    """ MLPiston Types """
    BASE = "Base"
    MLPISTON1D = "MLPiston1D"
    MLPISTON2D = "MLPiston2D"


class HelpURL:
    """ DesignSPHysics help URLS. """
    WIKI_HOME = "https://github.com/DualSPHysics/DesignSPHysics/wiki"
    MOTION_HELP = "https://github.com/DualSPHysics/DesignSPHysics/wiki/Feature-Reference#configure-object-motion"
    BASIC_CONCEPTS = "https://github.com/DualSPHysics/DesignSPHysics/wiki/Concepts-and-Clarifications"
    GITHUB_ISSUES = "https://github.com/DualSPHysics/DesignSPHysics/issues"


class DensityDTType:
    """ Density DT types. """
    NONE = 0
    MOLTENI = 1
    FOURTAKAS = 2
    FOURTAKAS_FULL = 3


class MooringsConfigurationMethod:
    """ Types of MoorDyn configuration types. """
    EMBEDDED = 0
    FROM_XML = 1


class InitialsType:
    """ Types of initials velocity """
    UNIFORM = 0
    LINEAR = 1
    PARABOLIC = 2


class BoundInitialsType:
    """ Types of initials for boundaries """
    SET = 0
    PLANE = 1
    SPHERE = 2
    CYLINDER = 3
    PARTS = 4


class InformationDetailsMode:
    """ Types of detailed text for the information dialog. """
    PLAIN = 0
    HTML = 1


class OMPThreads:
    """ Types of contact methods for CHRONO collisions. """
    MULTI_CORE = 0
    SINGLE_CORE = 1


class ContactMethod:
    """ Types of contact methods for CHRONO collisions. """
    NSC = 0
    SMC = 1


class HelpText:
    """ Help strings for different zones of the application GUIs. """
    GRAVITYX = __("Gravitational acceleration in X direction.")
    GRAVITYY = __("Gravitational acceleration in Y direction.")
    GRAVITYZ = __("Gravitational acceleration in Z direction.")
    RHOP0 = __("Reference density of the fluid.")
    HSWL = __("Maximum still water level to calculate speedofsound as the celerity during dam-break propagation.")
    GAMMA = __("Polytropic constant for ocean water used in the state equation.")
    SPEEDSYSTEM = __("Maximum speed system (by default the celerity during dam-break propagation).")
    COEFSOUND = __("Coefficient to multiply speedsystem")
    SPEEDSOUND = __("Speed of sound (by default speedofsound=coefsound*speedsystem). ")
    COEFH = __("Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D).")
    CFLNUMBER = __("Coefficient to multiply variable dt.")
    XMIN = __("The domain is fixed in the specified limit (default=not applied)")
    XMAX = __("The domain is fixed in the specified limit (default=not applied)")
    YMIN = __("The domain is fixed in the specified limit (default=not applied)")
    YMAX = __("The domain is fixed in the specified limit (default=not applied)")
    ZMIN = __("The domain is fixed in the specified limit (default=not applied)")
    ZMAX = __("The domain is fixed in the specified limit (default=not applied)")
    SAVEPOSDOUBLE = __("Saves particle position using double precision (default=0).")
    BOUNDARY = __("Boundary method 1:DBC, 2:mDBC (default=1).")
    POSDOUBLE = __("Precision in particle interaction 0:Simple, 1:Double, 2:Uses and saves double (default=0).")
    STEPALGORITHM = __("Time-integrator algorithm 1:Verlet, 2:Symplectic (default=1).")
    VERLETSTEPS = __("Verlet only: Number of steps to apply Euler timestepping (default=40).")
    KERNEL = __("Interaction Kernel 1:Cubic Spline, 2:Wendland, 3:Gaussian (default=2)")
    VISCOTREATMENT = __("Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)")
    VISCO = __("Viscosity value (apha when VISCOTREATMENT=1 and kinematic viscosity when VISCOTREATMENT=2).")
    VISCOBOUNDFACTOR = __("Multiply viscosity value for fluid-boundary interaction (default=1).")
    DELTASPH = __("DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0).")
    DENSITYDT = __("DDT value (default=0.1).")
    SHIFTING = __("Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0).")
    SHIFTINGCOEF = __("Coefficient for shifting computation (default=-2).")
    SHIFTINGTFS = __("Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0).")
    RIGIDALGORITHM = __("Rigid Algorithm 1:SPH, 2:DEM, 3:Chrono (default=1).")
    FTPAUSE = __("Time to freeze the floating objects at beginning of simulation (default=0).")
    DTINI = __("Initial time step (default=h/speedsound).")
    DTMIN = __("Minimum time step (default=coefdtmin*h/speedsound).")
    COEFDTMIN = __("Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05).")
    TIMEMAX = __("Time of simulation.")
    TIMEOUT = __("Time to save output data.")
    INCZ = __("Increase of Z+ (%) (default=0).")
    PARTSOUTMAX = __("%%/100 of fluid particles allowed to be excluded from domain (default=1).")
    RHOPOUTMIN = __("Minimum rhop valid (default=700).")
    RHOPOUTMAX = __("Maximum rhop valid (default=1300).")
    DOMAINFIXED = __("The domain is fixed with the specified values (xmin:ymin:zmin:xmax:ymax:zmax).")
    YINCREMENTX = __("")
    ZINCREMENTX = __("")
    XINCREMENTY = __("")
    ZINCREMENTY = __("")
    XINCREMENTZ = __("")
    YINCREMENTZ = __("")
    POSMINX = __("")
    POSMINY = __("")
    POSMINZ = __("")
    POSMAXX = __("")
    POSMAXY = __("")
    POSMAXZ = __("")
