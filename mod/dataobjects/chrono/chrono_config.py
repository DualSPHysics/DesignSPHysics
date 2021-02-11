#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono Configuration Data. """

from uuid import UUID

from mod.dataobjects.chrono.chrono_csv_intervals import ChronoCSVIntervals
from mod.dataobjects.chrono.chrono_scale_scheme import ChronoScaleScheme
from mod.dataobjects.chrono.chrono_collision_dp import ChronoCollisionDP
from mod.dataobjects.chrono.chrono_link_linear_spring import ChronoLinkLinearSpring
from mod.dataobjects.chrono.chrono_link_spheric import ChronoLinkSpheric
from mod.dataobjects.chrono.chrono_link_hinge import ChronoLinkHinge
from mod.dataobjects.chrono.chrono_link_point_line import ChronoLinkPointLine
from mod.dataobjects.chrono.chrono_link_coulomb_damping import ChronoLinkCoulombDamping
from mod.dataobjects.chrono.chrono_link_pulley import ChronoLinkPulley


class ChronoConfig:
    """ Dataobject to store Chrono related configuration and utilities. """

    def __init__(self):
        self.csv_intervals: ChronoCSVIntervals = ChronoCSVIntervals()
        self.scale_scheme: ChronoScaleScheme = ChronoScaleScheme()
        self.collisiondp: ChronoCollisionDP = ChronoCollisionDP()
        self.objects: list = list()  # [ChronoObject]
        self.link_spheric: list = list()  # [ChronoLinkSpheric]
        self.link_linearspring: list = list()  # [ChronoLinkLinearSpring]
        self.link_hinge: list = list()  # [ChronoLinkHinge]
        self.link_pointline: list = list()  # [ChronoLinkPointLine]
        self.link_coulombdamping: list = list()  # [ChronoLinkCoulombDamping]
        self.link_pulley: list = list()  # [ChronoLinkPulley]

    def get_link_spheric_for_id(self, uuid: UUID) -> ChronoLinkSpheric:
        """ Returns a ChronoLinkLinearSpring object matching the argument id, or None if not found. """
        for link in self.link_spheric:
            if link.id == uuid:
                return link

        return None

    def get_link_linearspring_for_id(self, uuid: UUID) -> ChronoLinkLinearSpring:
        """ Returns a ChronoLinkLinearSpring object matching the argument id, or None if not found. """
        for link in self.link_linearspring:
            if link.id == uuid:
                return link

        return None

    def get_link_hinge_for_id(self, uuid: UUID) -> ChronoLinkHinge:
        """ Returns a ChronoLinkHinge object matching the argument id, or None if not found. """
        for link in self.link_hinge:
            if link.id == uuid:
                return link

        return None

    def get_link_pointline_for_id(self, uuid: UUID) -> ChronoLinkPointLine:
        """ Returns a ChronoLinkPointLine object matching the argument id, or None if not found. """
        for link in self.link_pointline:
            if link.id == uuid:
                return link

        return None

    def get_link_coulombdamping_for_id(self, uuid: UUID) -> ChronoLinkCoulombDamping:
        """ Returns a ChronoLinkCoulombDamping object matching the argument id, or None if not found. """
        for link in self.link_coulombdamping:
            if link.id == uuid:
                return link

        return None

    def get_link_pulley_for_id(self, uuid: UUID) -> ChronoLinkPulley:
        """ Returns a ChronoLinkPulley object matching the argument id, or None if not found. """
        for link in self.link_pulley:
            if link.id == uuid:
                return link

        return None
