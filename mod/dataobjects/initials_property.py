#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Initials Property data """

class InitialsProperty():
    """ Initial movement property of an DSPH object.

    Attributes:
        mk: Mk to witch this InitialsProperty is binded.
        force: Force in [x, y, z] format.
    """

    def __init__(self, mk=-1, force=None):
        self.mk = mk
        self.force = force or []
