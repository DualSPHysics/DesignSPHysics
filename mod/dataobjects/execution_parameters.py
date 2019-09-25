#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Execution parameters data. '''


from mod.dataobjects.domain_fixed_parameter import DomainFixedParameter


class ExecutionParameters():
    ''' Execution parameters for the case '''

    def __init__(self):
        self.posdouble: int = 0
        self.stepalgorithm: int = 1
        self.verletsteps: int = 40
        self.kernel: int = 2
        self.viscotreatment: int = 1
        self.visco: float = 0.01
        self.viscoboundfactor: int = 1
        self.deltasph: int = 0
        self.deltasph_en: int = 0
        self.shifting: int = 0
        self.shiftcoef: int = -2
        self.shifttfs: int = 0
        self.rigidalgorithm: int = 1
        self.ftpause: float = 0.0
        self.coefdtmin: float = 0.05
        self.dtini: float = 0.0001
        self.dtini_auto: bool = True
        self.dtmin: float = 0.00001
        self.dtmin_auto: bool = True
        self.dtallparticles: int = 0
        self.dtfixed: str = 'DtFixed.dat'
        self.timemax: float = 1.5
        self.timeout: float = 0.01
        self.partsoutmax: int = 1
        self.rhopoutmin: int = 700
        self.rhopoutmax: int = 1300
        self.domainfixed: DomainFixedParameter = DomainFixedParameter(False, 0, 0, 0, 0, 0, 0)
