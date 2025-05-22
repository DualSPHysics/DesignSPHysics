# -*- coding: utf-8 -*-
""" Jet Circle type for Inlet/Outlet. """


class JetCircle:
    """ Defines an Inlet/Oulet linear velocity. """

    def __init__(self, v: float = 0.0, distance: float = 0.0, radius: float = 0.0) -> None:
        self.v: float = v
        self.distance: float = distance
        self.radius: float = radius
