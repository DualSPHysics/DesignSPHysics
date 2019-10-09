#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Wait Motion data. '''

from mod.dataobjects.motion.base_motion import BaseMotion


class WaitMotion(BaseMotion):
    ''' DualSPHysics rectilinear motion.

        Attributes inherited from superclass.
        '''

    def __init__(self, duration=1, parent_movement=None):
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.type = "Wait Interval"

    def __str__(self):
        return "WaitMotion [Duration: {}]".format(self.duration)
