#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn output configuration. """


class MoorDynOutputConfiguration():
    """ MoorDyn output configuration dataobject. """

    def __init__(self):
        self.startTime: float = 0
        self.endTime: float = 10
        self.dtOut: float = 0.01
        self.tension: bool = True
        self.force: bool = True
        self.velocity: bool = True
        self.position: bool = True
