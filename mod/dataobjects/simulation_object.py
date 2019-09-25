#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Simulation Object data. '''

from mod.enums import ObjectType, ObjectFillMode
from mod.dataobjects.faces_property import FacesProperty
from mod.dataobjects.damping import Damping


class SimulationObject():
    ''' Represents an object on a DualSPHysics / GenCase case '''

    def __init__(self, name: str, obj_mk: int, obj_type: ObjectType, fillmode: ObjectFillMode):
        self.name: str = name
        self.obj_mk: int = obj_mk
        self.type: ObjectType = obj_type
        self.fillmode: ObjectFillMode = fillmode
        self.damping: Damping = None
        self.faces_configuration: FacesProperty = None

    def clean_faces(self):
        ''' Deletes face rendering information from this object '''
        self.faces_configuration: FacesProperty = None
