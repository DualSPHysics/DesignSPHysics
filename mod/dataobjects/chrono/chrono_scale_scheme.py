#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics chrono scale scheme configuration. """


class ChronoScaleScheme:
    """ DesignSPHysics crono scale scheme configuration. """

    def __init__(self):
        self.enabled: bool = False
        self.value: float = 0.0
