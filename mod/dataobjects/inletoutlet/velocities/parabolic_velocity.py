# -*- coding: utf-8 -*-
""" Parabolic velocity type for Inlet/Outlet. """


class ParabolicVelocity():
    """ Defines an Inlet/Oulet parabolic velocity. """

    def __init__(self, v1: float = 0.0, v2: float = 0.0, v3: float = 0.0, z1: float = 0.0, z2: float = 0.0,  z3: float = 0.0) -> None:
        self.v1: float = v1
        self.v2: float = v2
        self.v3: float = v3
        self.z1: float = z1
        self.z2: float = z2
        self.z3: float = z3
