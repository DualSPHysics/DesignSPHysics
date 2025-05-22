#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus connect object. """


class MoorDynPlusConnect():
    """ MoorDynPlus connect object representation. """

    def __init__(self, conref=-1, point=None, m=1000.0, v=120.0):
        self.conref: int = conref
        self.point: list() = point or [0.0, 0.0, 0.0]
        self.m: float = m
        self.v: float = v
