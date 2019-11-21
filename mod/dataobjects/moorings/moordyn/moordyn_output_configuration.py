#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn output configuration. """


class MoorDynOutputConfiguration():
    """ MoorDyn output configuration dataobject. """

    def __init__(self):
        super().__init__()
        self.startTime: float = 0
        self.endTime: float = 10
        self.dtOut: float = 0.01
        self.tension: str = "all"
        self.force: str = "all"
        self.velocity: str = "all"
        self.position: str = "all"
