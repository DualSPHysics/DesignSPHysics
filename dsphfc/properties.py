#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DesignSPHysics Properties.

This file contains a collection of Properties to add
in a DSPH related case.

"""
# Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.


class FloatProperty(object):
    """ Float property of an DSPH object.

    Attributes:
        mk: Mk to witch this FloatProperty is binded.
        mass_density_type: Density type 0 is massbody; 1 is rhopbody.
        mass_density_value: Value for mass/density
        gravity_center: Coords in [x, y, z] format. Blank list() for auto.
        inertia: Coords in [x, y, z] format. Blank list() for auto.
        initial_linear_velocity: Coords in [x, y, z] format. Blank list() for auto.
        initial_angular_velocity: Coords in [x, y, z] format. Blank list() for auto.
    """

    def __init__(self, mk=-1, mass_density_type=0, mass_density_value=100,
                 gravity_center=list(), inertia=list(), initial_linear_velocity=list(),
                 initial_angular_velocity=list()):
        self.mk = mk
        self.mass_density_type = mass_density_type
        self.mass_density_value = mass_density_value
        self.gravity_center = gravity_center
        self.inertia = inertia
        self.initial_linear_velocity = initial_linear_velocity
        self.initial_angular_velocity = initial_angular_velocity


class InitialsProperty(object):
    """ Initial movement property of an DSPH object.

    Attributes:
        mk: Mk to witch this InitialsProperty is binded.
        force: Force in [x, y, z] format.
    """

    def __init__(self, mk=-1, force=list()):
        self.mk = mk
        self.force = force


class Material(object):
    """ DualSPHysics compatible material.

    Attributes:
        bound_mk: List of mk groups this material is binded
    """

    def __init__(self, mk=list()):
        self.bound_mk = mk


class Movement(object):
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
        if not motion_list:
            motion_list = list()
        self.motion_list = motion_list
        self.loop = loop

    def add_motion(self, motion):
        if isinstance(motion, BaseMotion):
            motion.parent_movement = self
            self.motion_list.append(motion)
        else:
            raise TypeError("You are trying to append a non-motion object to a movement list.")

    def set_loop(self, state):
        if isinstance(state, bool):
            self.loop = state
        else:
            raise TypeError("Tried to set a boolean with an {}".format(state.__class__.__name__))

    def remove_motion(self, position):
        self.motion_list.pop(position)

    def __str__(self):
        to_ret = "Movement <{}>".format(self.name) + "\n"
        to_ret += "Motion List:\n"
        for motion in self.motion_list:
            to_ret += str(motion) + "\n"
        return to_ret


class BaseMotion(object):
    """ Base motion class to inherit by others.

        Attributes:
            duration: Movement duration in seconds
        """

    def __init__(self, duration=1, parent_movement=None):
        self.duration = duration
        self.parent_movement = parent_movement

    def __str__(self):
        return "BaseMotion [Duration: {}]".format(self.duration)


class RectMotion(BaseMotion):
    """ DualSPHysics rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
        """

    def __init__(self, duration=1, velocity=None, parent_movement=None):
        if velocity is None:
            velocity = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.velocity = velocity

    def __str__(self):
        return "RectMotion [Duration: {} ; Velocity: {}]".format(self.duration, self.velocity)


class WaitMotion(BaseMotion):
    """ DualSPHysics rectilinear motion.

        Attributes inherited from superclass.
        """

    def __init__(self, duration=1, parent_movement=None):
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement

    def __str__(self):
        return "WaitMotion [Duration: {}]".format(self.duration)