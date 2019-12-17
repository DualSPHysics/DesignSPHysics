#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MK Based Properties. """

from mod.dataobjects.properties.property import Property


class MaterialProperty(Property):
    """ Base class for composing custom properties for DualSPHysics. """

    def __init__(self, name=None):
        super().__init__(name)
        self.young_modulus: float = 1.0
        self.poisson_ratio: float = 1.0
        self.restitution_coefficient: float = 1.0
        self.kfric: float = 1.0

    def __str__(self):
        return """
        Name: {name}
            Young Modulus: {young_modulus}
            Poisson Ratio: {poisson_ratio}
            Restitution Coefficient: {restitution_coefficient}
            KFric: {kfric}
        """.format(**self.__dict__)
