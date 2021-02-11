#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono Link Coulomb Damping. """

from uuid import UUID, uuid4


class ChronoLinkCoulombDamping:
    """ Chrono Link Coulomb Damping. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.idbody1: str = ""
        self.idbody2: str = ""
        self.point_fb1: list = [0.0, 0.0, 0.0]
        self.point_fb2: list = [0.0, 0.0, 0.0]
        self.rest_length: float = 0.0
        self.damping: float = 0.0
        self.nside: int = 0
        self.radius: float = 3.0
        self.length: float = 1.0
