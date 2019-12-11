#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono Link Hinge. """

from uuid import UUID, uuid4


class ChronoLinkHinge:
    """ Chrono Link Hinge. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.idbody1: str = ""
        self.idbody2: str = ""
        self.rotpoint: list = [0.0, 0.0, 0.0]
        self.rotvector: list = [0.0, 0.0, 0.0]
        self.stiffness: float = 0.0
        self.damping: float = 0.0
