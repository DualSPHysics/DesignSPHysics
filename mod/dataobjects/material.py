#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Material data """


class Material():
    """ DualSPHysics compatible material.

    Attributes:
        bound_mk: List of mk groups this material is binded
    """

    def __init__(self, mk=None):
        self.bound_mk = mk or []
