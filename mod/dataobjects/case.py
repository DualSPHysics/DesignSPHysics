#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics main data structure. '''

from mod.stdout_tools import debug
from mod.freecad_tools import get_fc_object

from mod.constants import VERSION
from mod.enums import ObjectType, FreeCADObjectType

from mod.dataobjects.constants import Constants
from mod.dataobjects.execution_parameters import ExecutionParameters
from mod.dataobjects.periodicity import Periodicity
from mod.dataobjects.simulation_domain import SimulationDomain
from mod.dataobjects.executable_paths import ExecutablePaths
from mod.dataobjects.case_information import CaseInformation
from mod.dataobjects.acceleration_input import AccelerationInput
from mod.dataobjects.relaxation_zone import RelaxationZone
from mod.dataobjects.simulation_object import SimulationObject
from mod.dataobjects.mk_based_properties import MKBasedProperties


class Case():
    ''' Main data structure for the data inside a case properties, objects
    etcetera. Used as a way to store information and transform it for multiple needs '''
    __instance: 'Case' = None
    SUPPORTED_TYPES = [FreeCADObjectType.BOX, FreeCADObjectType.SPHERE, FreeCADObjectType.CYLINDER]

    def __init__(self, reset=False):
        ''' Virtually private constructor. '''
        if Case.__instance is not None and not reset:
            raise Exception('Case class is a singleton and should not be initialized twice')
        super()
        Case.__instance = self
        self.version: str = VERSION
        self.name: str = ''
        self.path: str = ''
        self.dp: float = 0.01
        self.mode3d: bool = True
        self.constants: Constants = Constants()
        self.execution_parameters: ExecutionParameters = ExecutionParameters()
        self.objects: list = list()  # [SimulationObject]
        self.mkbasedproperties: dict = dict()  # {mk: MKBasedProperties}
        self.periodicity: Periodicity = Periodicity()
        self.domain: SimulationDomain = SimulationDomain()
        self.executable_paths: ExecutablePaths = ExecutablePaths()
        self.info: CaseInformation = CaseInformation()
        self.acceleration_input: AccelerationInput = AccelerationInput()
        self.relaxation_zone: RelaxationZone = None

    @staticmethod
    def instance() -> 'Case':
        ''' Static access method. '''
        if Case.__instance is None:
            Case()
        return Case.__instance

    def get_first_mk_not_used(self, object_type: ObjectType):
        ''' Checks simulation objects to find the first not used MK group number. '''
        mkset = set(map(lambda x: x.obj_mk, filter(lambda y: y.type == object_type, self.objects)))
        limit = {ObjectType.FLUID: 10, ObjectType.BOUND: 240}[object_type]
        for i in range(0, limit):
            if i not in mkset:
                return i
        return 0

    def get_all_simulation_object_names(self):
        ''' Returns a list with all the internal names used by the objects in the simulation. '''
        return list(map(lambda obj: obj.name, self.objects))

    def get_simulation_object(self, name) -> SimulationObject:
        ''' Returns a simulation object from its internal name.
        Raises an exception if the selected object is not added to the simulation. '''
        return next(filter(lambda obj: obj.name == name, self.objects), None)

    def number_of_objects_in_simulation(self):
        ''' Return the total number of objects in the simulation '''
        return len(list(filter(lambda obj: obj.type != ObjectType.SPECIAL, self.objects)))

    def get_mk_base_properties(self, mknumber: int) -> MKBasedProperties:
        ''' Returns the properties set for a given MK number '''
        if mknumber not in self.mkbasedproperties.keys():
            raise RuntimeError('MK has no properties applied! This should not happen.')
        return self.mkbasedproperties[mknumber]

    def has_mk_properties(self, mk) -> bool:
        ''' Returns whether a given mk has properties applier or not. '''
        return mk in self.mkbasedproperties.keys()

    def is_object_in_simulation(self, name) -> bool:
        ''' Returns whether an object is contained in the current case for simulating or not. '''
        return name in self.get_all_simulation_object_names()

    def reset(self):
        ''' Recreates the object from scratch. '''
        self.__init__(reset=True)

    def add_object(self, simobject: SimulationObject):
        ''' Adds an object to the current case '''
        if simobject.name in self.get_all_simulation_object_names():
            raise RuntimeError('Object with the name: {} is already added to the case'.format(simobject.name))
        self.objects.append(simobject)
        if not self.has_mk_properties(simobject.obj_mk):
            self.mkbasedproperties[simobject.obj_mk] = MKBasedProperties(mk=simobject.obj_mk)

    def remove_object(self, object_name: str) -> SimulationObject:
        ''' Tries to remove the given object name from the simulation.
        If no element is found an error is raised. '''
        if object_name not in self.get_all_simulation_object_names():
            raise RuntimeError('The object that you are trying to remove ({}) is not present in the simulation')
        self.objects = list(filter(lambda obj: obj.name != object_name, self.objects))

    def get_all_objects_with_damping(self):
        ''' Returns a list of SimulationObject that have damping '''
        return list(filter(lambda obj: obj.damping is not None, self.objects))

    def was_not_saved(self) -> bool:
        ''' Returns whether this case was or not saved before '''
        return self.path == '' and self.name == ''

    def reset_simulation_domain(self) -> None:
        ''' Restores the Simulation Domain to the default one. '''
        self.domain = SimulationDomain()

    def shift_object_up_in_order(self, index) -> None:
        ''' Moves an object up in the order. '''
        corrected_index = index + 1
        if 2 <= corrected_index < len(self.objects):
            debug("Object has right condition to shift up")
            self.objects.insert(corrected_index - 1, self.objects.pop(corrected_index))

    def shift_object_down_in_order(self, index) -> None:
        ''' Moves an object up in the order. '''
        corrected_index = index + 1
        if 1 <= corrected_index < len(self.objects) - 1:
            self.objects.insert(corrected_index + 1, self.objects.pop(corrected_index))

    def delete_invalid_objects(self) -> None:
        ''' Deletes invalid objects from the simulation. '''
        for object_name in self.get_all_simulation_object_names():
            fc_object = get_fc_object(object_name)
            if not fc_object or fc_object.InList:
                self.remove_object(object_name)
