#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Float Property dat. """


from mod.enums import FloatingDensityType


class FloatProperty():
    """ Float property of an DSPH object.

    Attributes:
        mk: Mk to witch this FloatProperty is binded.
        mass_density_type: Density type 0 is massbody; 1 is rhopbody.
        mass_density_value: Value for mass/density
        gravity_center: Coords in [x, y, z] format. None for auto.
        inertia: Coords in [x, y, z] format. None for auto.
        initial_linear_velocity: Coords in [x, y, z] format. None for auto.
        initial_angular_velocity: Coords in [x, y, z] format. None for auto.
        rotation_restriction: Coords in [x,y,z] format. None for auto.
    """

    def __init__(self, mk=-1, mass_density_type=FloatingDensityType.MASSBODY, mass_density_value=100,
                 gravity_center=None, inertia=None, initial_linear_velocity=None,
                 initial_angular_velocity=None, translation_restriction=None,
                 rotation_restriction=None, material=None):
        self.mk = mk
        self.mass_density_type = mass_density_type
        self.mass_density_value = mass_density_value
        self.gravity_center = gravity_center
        self.inertia = inertia
        self.initial_linear_velocity = initial_linear_velocity
        self.initial_angular_velocity = initial_angular_velocity
        self.translation_restriction = translation_restriction
        self.rotation_restriction = rotation_restriction
        self.material = material
