#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Movement data. """

from mod.enums import MotionType

from mod.dataobjects.motion.base_motion import BaseMotion


class Movement():
    """ DualSPHysics compatible movement.
        It includes a list of different motions to represent an entire simulation
        movement.

        Attributes:
            name: Name for this motion given by the user
            motion_list: List of motion objects in order
            loop: Boolean indicating if it is a loop
        """

    def __init__(self, name="New Movement", motion_list=None, loop=False):
        self.name = name
        self.type = MotionType.MOVEMENT
        self.motion_list = motion_list or []
        self.loop = loop

    def add_motion(self, motion):
        """ Adds a motion to the movement """
        if isinstance(motion, BaseMotion):
            self.motion_list.append(motion)
        else:
            raise TypeError(
                "You are trying to append a non-motion object to a movement list.")

    def set_loop(self, state):
        """ Set loop state for the movement """
        if isinstance(state, bool):
            self.loop = state
        else:
            raise TypeError("Tried to set a boolean with an {}".format(
                state.__class__.__name__))

    def remove_motion(self, position):
        """ Removes a motion from the list """
        self.motion_list.pop(position)

    def __str__(self):
        to_ret = "Movement <{}>".format(self.name) + "\n"
        to_ret += "Motion List:\n"
        for motion in self.motion_list:
            to_ret += str(motion) + "\n"
        return to_ret
