#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics chrono collision dp configuration. """


from mod.enums import ContactMethod


class ChronoCollisionDP:
    """ Chrono collision DP configuration. """

    def __init__(self):
        self.enabled: bool = False
        self.distancedp: float = 0.5
        self.ompthreads: int = 1
        self.contactmethod: float = ContactMethod.NSC
