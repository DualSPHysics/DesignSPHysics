# -*- coding: utf-8 -*-
"""Data objects for DesignSPHysics

This module contains multiple data objects used in the execution
of DesignSPHysics.

"""


class Constants(object):
    pass


class ExecutionParameters(object):
    pass


class SimulationObject(object):
    pass


class PeriodicityInfo(object):
    pass


class SimulationDomain(object):
    pass


class ExecutablePaths(object):
    pass


class Case(object):
    """ Main data structure for the data inside a case properties, objects
    etcetera. Used as a way to store information and transform it for
    multiple needs """
    __instance = None
    constants = None
    execution_parameters = None
    objects = None
    periodicity = None
    domain = None
    executable_paths = None

    @staticmethod
    def instance() -> 'Case':
        """ Static access method. """
        if Case.__instance is None:
            Case()
        return Case.__instance

    def reset(self):
        self.__init__(reset=True)

    def __init__(self, reset=False):
        """ Virtually private constructor. """
        if Case.__instance is not None and not reset:
            raise Exception(
                "Case class is a singleton and should not be initialized twice")
        else:
            Case.__instance = self
            self.constants = Constants()
            self.execution_parameters = ExecutionParameters()
            self.objects = list()  # [SimulationObject, ...]
            self.periodicity = PeriodicityInfo()
            self.domain = SimulationDomain()
            self.executable_paths = ExecutablePaths()
