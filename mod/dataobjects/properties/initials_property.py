#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Initials Property data """

from mod.enums import InitialsType


class InitialsProperty():
    """ Initial movement property of an DSPH object.

    Attributes:
        mk: Mk to witch this InitialsProperty is binded.
        force: Force in [x, y, z] format.
    """

    def __init__(self, mk=-1, force=None, initials_type=InitialsType.LINEAR, v1=0.0, v2=0.0, v3=0.0, z1=0.0, z2=0.0, z3=0.0):
        self.mk = mk
        self.force = force or []
        self.initials_type: InitialsType = initials_type
        self.v1: float = v1
        self.v2: float = v2
        self.v3: float = v3
        self.z1: float = z1
        self.z2: float = z2
        self.z3: float = z3
