#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A Zone Generator based on a current simulation MK. """

from mod.enums import InletOutletDirection

class InletOutletZoneMKGenerator():
    """ A Zone Generator based on a current simulation MK. """

    def __init__(self) -> None:
        self.mkfluid: int = 0
        self.direction: InletOutletDirection = InletOutletDirection.LEFT