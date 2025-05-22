#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Boundary Initials Property data """

from mod.enums import BoundNormalsType
from mod.functions import migrate_state

class BoundNormals():
    """ Initial boundary property of an DSPH object. """

    def __init__(self, mk=-1, normals_type=BoundNormalsType.SET):
        self.mk = mk
        self.normals_type: BoundNormalsType = normals_type
        self.normal = [1.0, 0.0, 0.0]
        self.point_auto = True
        self.point = [1.0, 0.0, 0.0]
        self.maxdisth = 2.0
        self.limitdist = 0.5
        self.center = [1.0, 0.0, 0.0]
        self.radius = 1.0
        self.inside = True
        self.center1 = [1.0, 0.0, 0.0]
        self.center2 = [1.0, 0.0, 0.0]

    def __setstate__(self, state: dict):
        # Attribute renaming map (old -> new)
        rename_map = {
            'initials_type': 'normals_type',  # Add other renames if needed
        }
        
        # Handle missing attributes (backward compatibility)
        default_attrs = {
            'mk': -1,
            'normals_type': BoundNormalsType.SET,
            'normal' : [1.0, 0.0, 0.0],
            'point_auto' : True,
            'point' : [1.0, 0.0, 0.0],
            'maxdisth' : 2.0,
            'limitdist' : 0.5,
            'center' : [1.0, 0.0, 0.0],
            'radius' : 1.0,
            'inside' : True,
            'center1' : [1.0, 0.0, 0.0],
            'center2' : [1.0, 0.0, 0.0],
        }

        # Restore the state
        self.__dict__.update(migrate_state(rename_map,default_attrs,state))