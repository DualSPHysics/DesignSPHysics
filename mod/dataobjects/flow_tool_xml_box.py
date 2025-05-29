#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Flow Tool Box. """

from uuid import UUID, uuid4

from mod.functions import migrate_state


class FlowToolXmlBox():
    """ A structure representing a box used by FlowTool to measure data. """

    DEFAULT_NAME: str = "FLOWBOX"

    def __init__(self):
        self.id: UUID = uuid4()
        self.name: str = self.DEFAULT_NAME
        self.point: list[float] = [0.0, 0.0, 0.0]
        self.size: list() = [0.0, 0.0, 0.0]
        self.angle: list() = [0.0, 0.0, 0.0]
        self.divide_axis:bool=False
        self.axis:str="x"
        self.fc_object_name:str=""

    def __setstate__(self, state: dict):
        # Attribute renaming map (old -> new)
        rename_map = dict()

        # Handle missing attributes (backward compatibility)
        default_attrs = {
            'point1': [0.0, 0.0, 0.0],
            'point2': [0.0, 0.0, 0.0],
            'point3': [0.0, 0.0, 0.0],
            'point4': [0.0, 0.0, 0.0],
            'point5': [0.0, 0.0, 0.0],
            'point6': [0.0, 0.0, 0.0],
            'point7': [0.0, 0.0, 0.0],
            'point8': [0.0, 0.0, 0.0],
        }

        # Restore the state
        self.__dict__.update(migrate_state(rename_map,default_attrs,state))

