#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Accelerated Rectilinear motion data '''

from mod.dataobjects.base_motion import BaseMotion

class AccRectMotion(BaseMotion):
    ''' DualSPHysics accelerated rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
            acceleration: Acceleration vector that defines the acceleration
        '''

    def __init__(self, duration=1, velocity=None, acceleration=None, parent_movement=None):
        if velocity is None:
            velocity = [0, 0, 0]
        if acceleration is None:
            acceleration = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Accelerated Rectilinear motion"
        self.parent_movement = parent_movement
        self.velocity = velocity
        self.acceleration = acceleration

    def __str__(self):
        return "AccRectMotion [Duration: {} ; Velocity: {} ; Acceleration: {}]" \
            .format(self.duration, self.velocity, self.acceleration)
