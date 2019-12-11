#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono link pointline. """

from uuid import UUID, uuid4


class ChronoLinkPointLine:
    """ Chrono Link PointLine. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.idbody1: str = ""
        self.slidingvector: list = [0.0, 0.0, 0.0]
        self.rotpoint: list = [0.0, 0.0, 0.0]
        self.rotvector: list = [0.0, 0.0, 0.0]
        self.rotvector2: list = [0.0, 0.0, 0.0]
        self.stiffness: float = 0.0
        self.damping: float = 0.0
