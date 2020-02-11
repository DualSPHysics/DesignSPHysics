#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics main data structure. """

import FreeCAD

from mod.stdout_tools import debug

from mod.constants import VERSION, SUPPORTED_TYPES, MKFLUID_LIMIT
from mod.enums import ObjectType

from mod.dataobjects.inletoutlet.inlet_outlet_config import InletOutletConfig
from mod.dataobjects.chrono.chrono_config import ChronoConfig
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
from mod.dataobjects.damping import Damping
from mod.dataobjects.moorings.moorings_configuration import MooringsConfiguration


class Case():
    """ Main data structure for the data inside a case properties, objects
    etcetera. Used as a way to store information and transform it for multiple needs """
    __instance: "Case" = None

    DEFAULT_DP: float = 0.01

    def __init__(self, reset=False):
        """ Virtually private constructor. """
        if Case.__instance is not None and not reset:
            raise Exception("Case class is a singleton and should not be initialized twice")
        Case.__instance = self
        self.version: str = VERSION
        self.name: str = ""
        self.path: str = ""
        self.dp: float = self.DEFAULT_DP
        self.mode3d: bool = True
        self.constants: Constants = Constants()
        self.execution_parameters: ExecutionParameters = ExecutionParameters()
        self.objects: list = list()  # [SimulationObject]
        self.mkbasedproperties: dict = dict()  # {realmk: MKBasedProperties}
        self.damping_zones: dict = dict()  # {freecad_object_name: Damping}
        self.flowtool_boxes: list = list()  # [FlowToolBox]
        self.periodicity: Periodicity = Periodicity()
        self.domain: SimulationDomain = SimulationDomain()
        self.executable_paths: ExecutablePaths = ExecutablePaths()
        self.info: CaseInformation = CaseInformation()
        self.acceleration_input: AccelerationInput = AccelerationInput()
        self.relaxation_zone: RelaxationZone = None
        self.inlet_outlet: InletOutletConfig = InletOutletConfig()
        self.moorings: MooringsConfiguration = MooringsConfiguration()
        self.chrono: ChronoConfig = ChronoConfig()

    @staticmethod
    def the() -> "Case":
        """ Static access method. """
        if Case.__instance is None:
            Case()
        return Case.__instance

    @staticmethod
    def update_from_disk(disk_data: "Case") -> None:
        """ Updates the current instance for the one passed as parameter. """
        Case.the().reset()
        Case.merge_old_object(disk_data, Case.__instance)
        Case.__instance = disk_data

    @staticmethod
    def merge_old_object(old, new):
        """ Merges an old object with the current version. """
        # FIXME: Add support for dicts,lists,tuples...
        for attr, value in new.__dict__.items():
            debug("Evaluating attr {} from the new object of type {}, for the old object of type {}".format(attr, type(new), type(old)))
            if not hasattr(old, attr):
                debug("Old object didn't have that attribute. Just updating it and going forward")
                setattr(old, attr, value)
                continue
            if hasattr(value, "__dict__") and hasattr(old, attr):
                # FIXME: old.attr may not have __dict__...
                debug("The attr {} is an object, and the old object has it. Exploring...".format(attr))
                Case.merge_old_object(getattr(old, attr), value)
                continue

    def get_first_mk_not_used(self, object_type: ObjectType):
        """ Checks simulation objects to find the first not used MK group number. """
        mkset = set(map(lambda x: x.obj_mk, filter(lambda y: y.type == object_type, self.objects)))
        limit = {ObjectType.FLUID: 10, ObjectType.BOUND: 240}[object_type]
        for i in range(0, limit):
            if i not in mkset:
                return i
        return 0

    def get_all_simulation_object_names(self):
        """ Returns a list with all the internal names used by the objects in the simulation. """
        return list(map(lambda obj: obj.name, self.objects))

    def get_simulation_object(self, name) -> SimulationObject:
        """ Returns a simulation object from its internal name.
        Raises an exception if the selected object is not added to the simulation. """
        return next(filter(lambda obj: obj.name == name, self.objects), None)

    def get_all_complex_objects(self) -> list:
        """ Returns all complex simulation objects. """
        return list(filter(lambda obj: FreeCAD.ActiveDocument.getObject(obj.name).TypeId not in SUPPORTED_TYPES and "FillBox" not in obj.name, self.objects))

    def get_all_fluid_objects(self) -> list:
        """ Returns all the fluid objects in the simulation. """
        return list(filter(lambda obj: obj.type == ObjectType.FLUID, self.objects))

    def get_all_bound_objects(self) -> list:
        """ Returns all the bound objects in the simulation. """
        return list(filter(lambda obj: obj.type == ObjectType.BOUND, self.objects))

    def number_of_objects_in_simulation(self) -> int:
        """ Return the total number of objects in the simulation """
        return len(list(filter(lambda obj: obj.type != ObjectType.SPECIAL, self.objects)))

    def get_mk_based_properties(self, obj_type: ObjectType, mknumber: int) -> MKBasedProperties:
        """ Returns the properties set for a given MK number of a given type """
        if obj_type == ObjectType.BOUND:
            mknumber += MKFLUID_LIMIT
        if not self.has_mk_properties(mknumber):
            debug("Creating MKBasedProperties on demand for realmk: {}".format(mknumber))
            self.mkbasedproperties[mknumber] = MKBasedProperties(mk=mknumber)
        debug("Returning MKBasedProperties object for realmk: {}".format(mknumber))
        return self.mkbasedproperties[mknumber]

    def has_mk_properties(self, realmk: int) -> bool:
        """ Returns whether a given realmk has properties applier or not. """
        return realmk in self.mkbasedproperties.keys()

    def is_object_in_simulation(self, name) -> bool:
        """ Returns whether an object is contained in the current case for simulating or not. """
        return name in self.get_all_simulation_object_names()

    def reset(self):
        """ Recreates the object from scratch. """
        self.__init__(reset=True)

    def add_object(self, simobject: SimulationObject):
        """ Adds an object to the current case """
        if simobject.name in self.get_all_simulation_object_names():
            raise RuntimeError("Object with the name: {} is already added to the case".format(simobject.name))
        self.objects.append(simobject)

    def remove_object(self, object_name: str) -> SimulationObject:
        """ Tries to remove the given object name from the simulation.
        If no element is found an error is raised. """
        if object_name not in self.get_all_simulation_object_names():
            raise RuntimeError("The object that you are trying to remove ({}) is not present in the simulation")
        self.objects = list(filter(lambda obj: obj.name != object_name, self.objects))
        self.delete_orphan_mkbasedproperties()

    def get_orphan_mkbasedproperties(self):
        """ Returns all MKBasedProperties that no longer have an object present in the case. """
        to_ret: list = list()
        for realmk in self.mkbasedproperties:
            if realmk not in map(lambda obj: obj.obj_mk if obj.type == ObjectType.FLUID else obj.obj_mk + MKFLUID_LIMIT, Case.the().objects):
                to_ret.append(realmk)
        return to_ret

    def delete_orphan_mkbasedproperties(self):
        """ Deletes all MKBasedProperties that no longer have an object present in the case. """
        for key in self.get_orphan_mkbasedproperties():
            self.mkbasedproperties.pop(key)

    def get_damping_zone(self, object_key: str) -> Damping:
        """ Returns the Damping Zone bound to the object key passed as parameter. Returns None if it's not defined. """
        return self.damping_zones.get(object_key, None)

    def remove_damping_zone(self, object_key: str) -> None:
        """ Removes the damping zone from the data structure. """
        self.damping_zones.pop(object_key)

    def add_damping_group(self, group_name: str) -> None:
        """ Adds a new freecad group/folder to a new Damping Zone. """
        self.damping_zones[group_name] = Damping()

    def is_damping_bound_to_object(self, freecad_object_name: str) -> bool:
        """ Returns whether the object passed has a damping object bound to it or not. """
        return freecad_object_name in self.damping_zones.keys()

    def was_not_saved(self) -> bool:
        """ Returns whether this case was or not saved before """
        return self.path == "" and self.name == ""

    def reset_simulation_domain(self) -> None:
        """ Restores the Simulation Domain to the default one. """
        self.domain = SimulationDomain()

    def shift_object_up_in_order(self, index) -> None:
        """ Moves an object up in the order. """
        corrected_index = index + 1
        if 2 <= corrected_index < len(self.objects):
            debug("Object has right condition to shift up")
            self.objects.insert(corrected_index - 1, self.objects.pop(corrected_index))

    def shift_object_down_in_order(self, index) -> None:
        """ Moves an object up in the order. """
        corrected_index = index + 1
        if 1 <= corrected_index < len(self.objects) - 1:
            self.objects.insert(corrected_index + 1, self.objects.pop(corrected_index))

    def get_out_xml_file_path(self) -> str:
        """ Constructs the path for the out xml file needed to execute DualSPHysics. """
        return "{path}/{name}_out/{name}".format(path=self.path, name=self.name)

    def get_out_folder_path(self) -> str:
        """ Constructs the path for the output folder of the case. """
        return "{path}/{name}_out/".format(path=self.path, name=self.name)

    def has_materials(self) -> bool:
        """ Returns whether this case contains defined materials or not. """
        for mkbasedproperty in self.mkbasedproperties.values():
            if mkbasedproperty.property:
                return True
        return False
