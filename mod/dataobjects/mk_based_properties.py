#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MK Based Properties. """

from typing import Union
from mod.dataobjects.float_property import FloatProperty
from mod.dataobjects.initials_property import InitialsProperty
from mod.dataobjects.bound_initials_property import BoundInitialsProperty
from mod.dataobjects.ml_piston import MLPiston
from mod.dataobjects.properties.property import Property


class MKBasedProperties():
    """ Stores data related with an mk number on the case. """

    def __init__(self, mk=None):
        self.mk: int = mk  # This is a realmk (bound + MKFLUID_LIMIT)
        self.movements: list = list()  # [Movement]
        self.float_property: FloatProperty = None
        self.initials: InitialsProperty = None
        self.bound_initials: BoundInitialsProperty = None
        self.mlayerpiston: MLPiston = None
        self.property: Property = None

    def has_movements(self) -> bool:
        """ Returns whether this mk contains definition for movements or not """
        return len(self.movements) > 0

    def remove_all_movements(self) -> None:
        """ Removes all movements for the current mk properties """
        self.movements: list = []
