#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Regular Piston Wave Generator data """

from mod.enums import MotionType

from mod.dataobjects.motion.wave_gen import WaveGen
from mod.dataobjects.motion.awas import AWAS


class SolitaryPistonWaveGen(WaveGen):
    """ Piston Solitary Wave Generator.

    Attributes:
        theory: Theory of generation 1:Rayleigh (Serre 1953), 2: Boussinesq (Goring 1978) 3: KdV (Clamond and Germain 1999) (def=2)
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        n_waves: Number of solitary waves (def=1)
        wave_height: First wave height
        wave_1_duration_coef: First wave coefficient of movement duration



        piston_dir: Movement direction (def [1,0,0])
        awas: AWAS object
    """

    def __init__(self, wave_order=2, start=0, duration=0, depth=0, wave_height=0, wave_period=1, gainstroke=1.0, phase=0, ramp=0,
                 savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2, savemotion_zpos=-0.15, piston_dir=None, awas=None ,
                 theory=2,n_waves=1,wave_1_duration_coef=1.0,
                 wave_2_start_coef=1.0,wave_2_height=1.0,wave_2_duration_coef=1.0,
                 wave_3_start_coef=1.0,wave_3_height=1.0,wave_3_duration_coef=1.0):
        WaveGen.__init__(self, wave_order, start, duration, depth, wave_height, wave_period, gainstroke)
        self.type = MotionType.SOLITARY_PISTON_WAVE_GENERATOR
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.piston_dir = piston_dir or [1, 0, 0]
        self.awas = AWAS() if awas is None else awas
        self.theory=theory
        self.n_waves=n_waves
        self.wave_1_duration_coef=wave_1_duration_coef
        self.wave_2_start_coef=wave_2_start_coef
        self.wave_2_height=wave_2_height
        self.wave_2_duration_coef=wave_2_duration_coef
        self.wave_3_start_coef=wave_3_start_coef
        self.wave_3_height=wave_3_height
        self.wave_3_duration_coef=wave_3_duration_coef



