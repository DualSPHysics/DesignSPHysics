#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Rectilinear motion data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class RectMotion(BaseMotion):
    """ DualSPHysics rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
        """

    def __init__(self, duration=1, velocity=None, parent_movement=None):
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.type = MotionType.RECTILINEAR
        self.velocity = velocity or [0, 0, 0]

    def __str__(self):
        return "RectMotion [Duration: {} ; Velocity: {}]".format(self.duration, self.velocity)
