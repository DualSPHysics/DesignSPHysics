#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Property enums.

This file holds a collection of useful enums
in class forms, for code organization
'''


class IrregularSpectrum():
    ''' Types of supported wave spectrums. '''
    JONSWAP = 0
    PIERSON_MOSKOWITZ = 1

    def __init__(self):
        # Dummy init
        pass


class IrregularDiscretization():
    ''' Types of supported spectrum discretization. '''
    REGULAR = 0
    RANDOM = 1
    STRETCHED = 2
    COSSTRETCHED = 3

    def __init__(self):
        # Dummy init
        pass


class AWASWaveOrder():
    ''' Wave order to calculate elevation '''
    FIRST_ORDER = 1
    SECOND_ORDER = 2


class AWASSaveMethod:
    ''' Saving method for AWAS CSV '''
    BY_PART = 1
    MORE_INFO = 2
    BY_STEP = 3


class SDPositionPropertyType:
    ''' Simulation domain property type. '''
    DEFAULT = 0
    VALUE = 1
    DEFAULT_VALUE = 2
    DEFAULT_PERCENTAGE = 3


class ObjectType:
    ''' Simulation domain property type. '''
    BOUND = "bound"
    FLUID = "fluid"
    SPECIAL = "mkspecial"


class ObjectFillMode:
    ''' Simulation domain property type. '''
    FULL = "full"
    SOLID = "solid"
    FACE = "face"
    WIRE = "wire"
    SPECIAL = "fillspecial"


class FloatingDensityType:
    ''' Density type for floating mks. '''
    MASSBODY = 0
    RHOPBODY = 1


class FreeCADObjectType:
    ''' FreeCAD Types enums wrapping strings. '''
    BOX = "Part::Box"
    FOLDER = "App::DocumentObjectGroup"
    SPHERE = "Part::Sphere"
    CYLINDER = "Part::Cylinder"
    CUSTOM_MESH = "Mesh::Feature"


class FreeCADDisplayMode:
    ''' FreeCAD DisplayMode Strings. '''
    WIREFRAME = "Wireframe"
    FLAT_LINES = "Flat Lines"


class Template:
    ''' Text templates stored in disk. '''
    CASE_SUMMARY = "case_summary_template.html"
