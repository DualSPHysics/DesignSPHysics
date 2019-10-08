#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics chrono collision dp configuration. '''


class ChronoCollisionDP:
    ''' Chrono collision DP configuration. '''

    def __init__(self):
        super().__init__()
        self.enabled: bool = False
        self.value: float = 0.0
