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
        to_ret = "Name: {name}\n"
        to_ret += "Young Modulus: {young_modulus}\n"
        to_ret += "Poisson Ratio: {poisson_ratio}\n"
        to_ret += "Restitution Coefficient: {restitution_coefficient}\n"
        to_ret += "KFric: {kfric}"

        return to_ret.format(**self.__dict__)

    def html_str(self):
        """ Returns the object details as an HTML string. """
        to_ret = "<b>Name:</b> {name}<br>"
        to_ret += "<b>Young Modulus:</b> {young_modulus}<br>"
        to_ret += "<b>Poisson Ratio:</b> {poisson_ratio}<br>"
        to_ret += "<b>Restitution Coefficient:</b> {restitution_coefficient}<br>"
        to_ret += "<b>KFric:</b> {kfric}"

        return to_ret.format(**self.__dict__)
