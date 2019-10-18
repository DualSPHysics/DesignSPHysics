#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Property enums.

This file holds a collection of useful enums
in class forms, for code organization
"""


class IrregularSpectrum():
    """ Types of supported wave spectrums. """
    JONSWAP = 0
    PIERSON_MOSKOWITZ = 1

    def __init__(self):
        # Dummy init
        pass


class IrregularDiscretization():
    """ Types of supported spectrum discretization. """
    REGULAR = 0
    RANDOM = 1
    STRETCHED = 2
    COSSTRETCHED = 3

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


class Template:
    """ Text templates stored in disk. """
    CASE_SUMMARY = "case_summary_template.html"


class InletOutletDetermLimit:
    """ Inlet/Oulet DetermLimit Value. """
    ZEROTH_ORDER = "1e+3"
    FIRST_ORDER = "1e-3"


class InletOutletZoneType:
    """ Inlet/Oulet Zone Type. """
    ZONE_2D = "zone2d"
    ZONE_3D = "zone3d"


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
    FIXED = "fixed"
    VARIABLE = "variable"
    EXTRAPOLATED = "extrapolated"
    INTERPOLATED = "interpolated"


class InletOutletDensityType:
    """ Inlet/Outlet Density Type. """
    FIXED = "fixed"
    HYDROSTATIC = "hydrostatic"
    EXTRAPOLATED = "extrapolated"


class InletOutletElevationType:
    """ Inlet/Outler Elevation Type. """
    FIXED = "fixed"
    VARIABLE = "variable"
    AUTOMATIC = "automatic"


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
    FILE_WAVE_GENERATOR = "File Wave Generator"
    FILE_ROTATIONAL_WAVE_GENERATOR = "Rotational File Wave Generator"


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
