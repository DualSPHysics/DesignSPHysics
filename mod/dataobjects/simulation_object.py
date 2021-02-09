#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Simulation Object data. """

from mod.freecad_tools import get_fc_object
from mod.stdout_tools import debug

from mod.enums import ObjectType, ObjectFillMode, FreeCADObjectType
from mod.constants import SUPPORTED_TYPES, MKFLUID_LIMIT, MKFLUID_OFFSET

from mod.dataobjects.faces_property import FacesProperty


class SimulationObject():
    """ Represents an object on a DualSPHysics / GenCase case """

    def __init__(self, name: str, obj_mk: int, obj_type: ObjectType, fillmode: ObjectFillMode):
        self.name: str = name
        self.obj_mk: int = obj_mk
        self.type: ObjectType = obj_type
        self.fillmode: ObjectFillMode = fillmode
        self.autofill: bool = False  # Only set for imported objects
        self.frdrawmode: bool = False
        self.faces_configuration: FacesProperty = None

    def __getattr__(self, attr):
        if attr == "frdrawmode":
            debug("frdrawmode property in simulation object <{}> nonexistent: Creating one".format(self.name))
            self.frdrawmode: bool = False
            return self.frdrawmode
        raise AttributeError()

    def real_mk(self) -> int:
        """ Returns the object real MK. """
        return self.obj_mk + MKFLUID_OFFSET if self.type == ObjectType.FLUID else self.obj_mk + MKFLUID_LIMIT

    def clean_faces(self):
        """ Deletes face rendering information from this object """
        self.faces_configuration: FacesProperty = None

    def supports_changing_type(self) -> bool:
        """ Returns whether this object supports changing types or not. """
        fc_object = get_fc_object(self.name)
        return fc_object.TypeId in SUPPORTED_TYPES or \
            "part" in fc_object.TypeId.lower() or \
            "mesh" in fc_object.TypeId.lower() or \
            (fc_object.TypeId == FreeCADObjectType.FOLDER and "fillbox" in fc_object.Name.lower())

    def supports_changing_fillmode(self) -> bool:
        """ Returns whether this object supports changing its fillmode or not. """
        fc_object = get_fc_object(self.name)
        return fc_object.TypeId in SUPPORTED_TYPES

    def supports_floating(self) -> bool:
        """ Returns whether this object supports floating or not. """
        fc_object = get_fc_object(self.name)
        return fc_object.TypeId in SUPPORTED_TYPES or \
            (fc_object.TypeId == FreeCADObjectType.FOLDER and "fillbox" in fc_object.Name.lower())

    def supports_motion(self) -> bool:
        """ Returns whether this object supports motion or not. """
        return self.type == ObjectType.BOUND
