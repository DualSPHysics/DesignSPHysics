#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono Link Pulley. """

from uuid import UUID, uuid4


class ChronoLinkPulley:
    """ Chrono Link Pulley. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.idbody1: str = ""
        self.idbody2: str = ""
        self.rotpoint: list = [0.0, 0.0, 0.0]
        self.rotvector: list = [0.0, 0.0, 0.0]
        self.radius: float = 0.0
        self.radius2: float = 0.0
