#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Accelerated Rectilinear motion data """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class AccRectMotion(BaseMotion):
    """ DualSPHysics accelerated rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
            acceleration: Acceleration vector that defines the acceleration
        """

    def __init__(self, duration=1, velocity=None, acceleration=None):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.ACCELERATED_RECTILINEAR
        self.velocity = velocity or [0, 0, 0]
        self.acceleration = acceleration or [0, 0, 0]

    def __str__(self):
        return "AccRectMotion [Duration: {} ; Velocity: {} ; Acceleration: {}]" \
            .format(self.duration, self.velocity, self.acceleration)
