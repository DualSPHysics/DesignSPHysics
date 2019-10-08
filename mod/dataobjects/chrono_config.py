#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Chrono Configuration Data. '''

from mod.dataobjects.chrono_csv_intervals import ChronoCSVIntervals
from mod.dataobjects.chrono_scale_scheme import ChronoScaleScheme
from mod.dataobjects.chrono_collision_dp import ChronoCollisionDP


class ChronoConfig:
    ''' Dataobject to store Chrono related configuration and utilities. '''

    def __init__(self):
        super().__init__()
        self.csv_intervals: ChronoCSVIntervals = ChronoCSVIntervals()
        self.scale_scheme: ChronoScaleScheme = ChronoScaleScheme()
        self.collisiondp: ChronoCollisionDP = ChronoCollisionDP()
        self.objects: list = list()  # [ChronoObject]
        self.link_spheric: list = list()  # [ChronoLinkSpheric]
        self.link_linearspring: list = list()  # [ChronoLinkLinearSpring]
        self.link_hinge: list = list()  # [ChronoLinkHinge]
        self.link_pointline: list = list()  # [ChronoLinkPointLine]
