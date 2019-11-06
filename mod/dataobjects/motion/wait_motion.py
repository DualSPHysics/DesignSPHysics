#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Wait Motion data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class WaitMotion(BaseMotion):
    """ DualSPHysics rectilinear motion.

        Attributes inherited from superclass.
        """

    def __init__(self, duration=1):
        BaseMotion.__init__(self, duration)
        self.type = MotionType.WAIT

    def __str__(self):
        return "WaitMotion [Duration: {}]".format(self.duration)
