#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Simulation Object data. """

from mod.tools.freecad_tools import get_fc_object
from mod.tools.stdout_tools import debug

from mod.enums import ObjectType, ObjectFillMode, FreeCADObjectType
from mod.constants import SUPPORTED_TYPES, MKFLUID_LIMIT, MKFLUID_OFFSET

from mod.dataobjects.properties.faces_property import FacesProperty


class SimulationObject():
    """ Represents an object on a DualSPHysics / GenCase case """

    def __init__(self, name: str, obj_mk: int, obj_type: ObjectType, fillmode: ObjectFillMode):
        self.name: str = name
        self.obj_mk: int = obj_mk
        self.type: ObjectType = obj_type
        self.fillmode: ObjectFillMode = fillmode
        self.faces_configuration: FacesProperty = None
        # Only set for imported objects
        self.autofill: bool = False
        self.frdrawmode: bool = False
        self.scale_factor = [1, 1, 1]
        self.advdraw_enabled: bool = False
        self.advdraw_reverse: bool = False
        self.advdraw_maxdepth_enabled: bool = False
        self.advdraw_mindepth_enabled: bool = False
        self.advdraw_maxdepth: float = 3.0
        self.advdraw_mindepth: float = 0.1
        self.load_as_points: bool = False
        self.filename = ""
        self.file_type = "stl"
        self.is_loaded_geometry:bool=False
        self.origin_filename:str=""
        self.full_filename:str=""
        #Mdbc properties
        self.use_mdbc:bool=False
        self.mdbc_dist_vdp:float=0.0
        self.mdbc_normal_invert:bool=False




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
