#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A generator that cretes partiles along the surface of a circle. """


class InletOutletZoneCircleGenerator():
    """ A generator that cretes partiles along the surface of a circle. """

    def __init__(self) -> None:
        self.point: list = [0.0, 0.0, 0.0]
        self.radius: float = 0.0
        self.direction: list = [0.0, 0.0, 0.0]