#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Accelerated Circular Motion Data """

from mod.dataobjects.motion.base_motion import BaseMotion

class AccCirMotion(BaseMotion):
    """ DualSPHysics circular motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

    def __init__(self, duration=1, ang_vel=None, ang_acc=None, reference=None, axis1=None, axis2=None,
                 parent_movement=None):
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if ang_vel is None:
            ang_vel = 0
        if ang_acc is None:
            ang_acc = 0
        if reference is None:
            reference = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Circular Motion"
        self.parent_movement = parent_movement
        self.reference = reference
        self.axis1 = axis1
        self.axis2 = axis2
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc

    def __str__(self):
        return "AccCirMotion [Duration: {} ; AngVelocity: {} ; AngAccel: {} ; Reference: {} ; Axis: [{}, {}]]".format(
            self.duration,
            self.ang_vel,
            self.ang_acc,
            self.reference,
            self.axis1,
            self.axis2)
