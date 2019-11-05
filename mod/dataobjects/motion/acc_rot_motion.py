#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Accelerated Rotational Motion data """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class AccRotMotion(BaseMotion):
    """ DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

    def __init__(self, duration=1, ang_vel=0, ang_acc=0, axis1=None, axis2=None):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.ACCELERATED_ROTATIONAL
        self.axis1 = axis1 or [0, 0, 0]
        self.axis2 = axis2 or [0, 0, 0]
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc

    def __str__(self):
        return "AccRotMotion [Duration: {} ; AngVelocity: {} ; AngAccel: {} ; Axis: [{}, {}]]" \
            .format(self.duration, self.ang_vel, self.ang_acc, self.axis1, self.axis2)
