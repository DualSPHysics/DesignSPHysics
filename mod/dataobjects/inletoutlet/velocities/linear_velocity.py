# -*- coding: utf-8 -*-
""" Linear velocity type for Inlet/Outlet. """


class LinearVelocity():
    """ Defines an Inlet/Oulet linear velocity. """

    def __init__(self, v1: float = 0.0, v2: float = 0.0, z1: float = 0.0, z2: float = 0.0) -> None:
        self.v1: float = v1
        self.v2: float = v2
        self.z1: float = z1
        self.z2: float = z2
