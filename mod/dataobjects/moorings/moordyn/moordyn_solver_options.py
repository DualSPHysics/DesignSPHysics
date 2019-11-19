#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn solver options. """


class MoorDynSolverOptions():
    """ MoorDyn general solver options dataobject. """

    def __init__(self):
        super().__init__()
        self.gravity: float = 9.81
        self.water_depth: float = 0.5
        # FIXME: Finish this