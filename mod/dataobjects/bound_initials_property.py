#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Boundary Initials Property data """

from mod.enums import BoundInitialsType


class BoundInitialsProperty():
    """ Initial boundary property of an DSPH object. """

    def __init__(self, mk=-1, initials_type=BoundInitialsType.SET):
        self.mk = mk
        self.initials_type: BoundInitialsType = initials_type
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
