#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MK Based Properties. """


class Property():
    """ Base class for composing custom properties for DualSPHysics. """

    def __init__(self, name=None):
        self.name: str = name or "New Property"
