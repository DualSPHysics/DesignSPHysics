#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MK Based Properties. """

from mod.dataobjects.float_property import FloatProperty
from mod.dataobjects.initials_property import InitialsProperty
from mod.dataobjects.ml_piston import MLPiston


class MKBasedProperties():
    """ Stores data related with an mk number on the case. """

    def __init__(self, mk=None):
        self.mk: int = mk # This is a realmk (bound + MKFLUID_LIMIT)
        self.movements: list = list()  # [Movement]
        self.float_property: FloatProperty = None
        self.initials: InitialsProperty = None
        self.mlayerpiston: MLPiston = None

    def has_movements(self) -> bool:
        """ Returns whether this mk contains definition for movements or not """
        return len(self.movements) > 0

    def remove_all_movements(self) -> None:
        """ Removes all movements for the current mk properties """
        self.movements: list = []
