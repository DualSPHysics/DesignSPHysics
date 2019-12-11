#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono link linearspring. """

from uuid import UUID, uuid4


class ChronoLinkLinearSpring:
    """ Chrono Link LinearSpring. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.idbody1: str = ""
        self.idbody2: str = ""
        self.point_fb1: list = [0.0, 0.0, 0.0]
        self.point_fb2: list = [0.0, 0.0, 0.0]
        self.stiffness: float = 0.0
        self.damping: float = 0.0
        self.rest_length: float = 0.0
        self.number_of_sections: int = 16
        self.spring_radius: float = 3
        self.revolution_length: float = 1
