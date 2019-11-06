#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Rotational Motion data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class RotMotion(BaseMotion):
    """ DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

    def __init__(self, duration=1, ang_vel=0, axis1=None, axis2=None):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.ROTATIONAL
        self.axis1 = axis1 or [0, 0, 0]
        self.axis2 = axis2 or [0, 0, 0]
        self.ang_vel = ang_vel

    def __str__(self):
        return "RotMotion [Duration: {} ; AngVelocity: {} ; Axis: [{}, {}]]" \
            .format(self.duration, self.ang_vel, self.axis1, self.axis2)
