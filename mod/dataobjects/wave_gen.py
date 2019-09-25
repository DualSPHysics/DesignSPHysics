#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Wave Generator data. '''


class WaveGen():
    ''' Base Wave Generator. It holds properties common to Regular and Irregular waves.

    Attributes:
        parent_movement: The movement in which this property is contained
        mk_bound: Particle MK (for bounds) to which this property will be applied
        wave_order: Order wave generation (def 1, [1,2])
        start: Start time (def 0)
        duration: Movement duration, 0 means until simulation end
        depth: Fluid depth (def 0)
        wave_height: Wave height (def 0.5)
        wave_period: Wave period (def 1)
    '''

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1):
        super(WaveGen, self).__init__()
        self.parent_movement = parent_movement
        self.type = "Base Wave Generator"
        self.wave_order = wave_order
        self.start = start
        self.duration = duration
        self.depth = depth
        self.wave_height = wave_height
        self.wave_period = wave_period
