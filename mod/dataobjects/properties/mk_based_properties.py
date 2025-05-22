#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MK Based Properties. """

from mod.dataobjects.properties.flexstruct import FlexStruct
from mod.dataobjects.properties.float_property import FloatProperty
from mod.dataobjects.properties.initials_property import InitialsProperty
from mod.dataobjects.properties.bound_normals_property import BoundNormals
from mod.dataobjects.properties.ml_piston.ml_piston import MLPiston
from mod.dataobjects.properties.property import Property
from mod.functions import migrate_state

class MKBasedProperties():
    """ Stores data related with an mk number on the case. """
   
    def __init__(self, mk=None):
        self.mk: int = mk  # This is a real mk (bound + MKFLUID_LIMIT)
        self.movements: list = list()  # [Movement]
        self.float_property: FloatProperty = None
        self.initials: InitialsProperty = None
        self.bound_normals: BoundNormals = None
        self.mlayerpiston: MLPiston = None
        self.property: Property = None
        self.flex_struct:FlexStruct = None
    
    def __setstate__(self, state: dict):
        # Attribute renaming map (old -> new)
        rename_map = {
            'bound_initials': 'bound_normals',  # Add other renames if needed
        }
        
        # Handle missing attributes (backward compatibility)
        default_attrs = {
            'mk': None,
            'movements': list(),
            'float_property': None,
            'initials': None,
            'bound_normals': None
        }
                
        # Restore the state
        self.__dict__.update(migrate_state(rename_map,default_attrs,state))

    def has_movements(self) -> bool:
        """ Returns whether this mk contains definition for movements or not """
        return len(self.movements) > 0

    def remove_all_movements(self) -> None:
        """ Removes all movements for the current mk properties """
        self.movements: list = []
