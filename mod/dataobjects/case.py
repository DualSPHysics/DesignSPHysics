#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics main data structure. """
import os
from typing import List

import FreeCAD

import mod.dataobjects
from mod.dataobjects.configuration.post_processing_settings import PostProcessingSettings
from mod.dataobjects.flow_tool_xml_box import FlowToolXmlBox
from mod.dataobjects.gauges.gauges_data import GaugesData
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone
from mod.dataobjects.outparts_filter.filters import OutputParts
from mod.dataobjects.variable_res.bufferbox import BufferBox
from mod.dataobjects.variable_res.variable_res_config import VariableResConfig
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import get_fc_object

from mod.tools.stdout_tools import debug, log

from mod.constants import VERSION, SUPPORTED_TYPES, MKFLUID_LIMIT, CASE_3D_MODE
from mod.enums import ObjectType

from mod.dataobjects.inletoutlet.inlet_outlet_config import InletOutletConfig
from mod.dataobjects.chrono.chrono_config import ChronoConfig
from mod.dataobjects.configuration.constants import Constants
from mod.dataobjects.configuration.execution_parameters import ExecutionParameters
from mod.dataobjects.configuration.periodicity import Periodicity
from mod.dataobjects.configuration.simulation_domain import SimulationDomain
from mod.dataobjects.configuration.executable_paths import ExecutablePaths
from mod.dataobjects.case_information import CaseInformation
from mod.dataobjects.acceleration_input.acceleration_input import AccelerationInput
from mod.dataobjects.relaxation_zone.relaxation_zone import RelaxationZone
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.dataobjects.properties.mk_based_properties import MKBasedProperties
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
        #CASE INFORMATION
        self.version: str = VERSION
        self.name: str = ""
        self.path: str = ""
        self.info: CaseInformation = CaseInformation()
        #CASE CONFIGURATION
        self.dp: float = self.DEFAULT_DP
        self.mode3d: bool = CASE_3D_MODE
        self.constants: Constants = Constants()
        self.execution_parameters: ExecutionParameters = ExecutionParameters()
        self.periodicity: Periodicity = Periodicity()
        self.domain: SimulationDomain = SimulationDomain()
        self.executable_paths: ExecutablePaths = ExecutablePaths()
        self.post_processing_settings = PostProcessingSettings()
        #GEOMETRY
        self.objects: list[SimulationObject] = list()  # [SimulationObject]
        self.tmp_objects: list[SimulationObject] = list()  # [SimulationObject]
        self.mkbasedproperties: dict = dict()  # {realmk: MKBasedProperties}
        #SPECIAL OBJECTS
        self.inlet_outlet: InletOutletConfig = InletOutletConfig()
        self.vres: VariableResConfig = VariableResConfig()
        self.gauges: GaugesData = GaugesData()
        self.outparts: OutputParts = OutputParts()
        self.chrono: ChronoConfig = ChronoConfig()
        self.moorings: MooringsConfiguration = MooringsConfiguration()
        self.damping_zones: dict = dict()  # {freecad_object_name: Damping}
        self.acceleration_input: AccelerationInput = AccelerationInput()
        self.relaxation_zone: RelaxationZone = None




    @staticmethod
    def the() -> "Case":
        """ Static access method. """
        if Case.__instance is None:
            Case()
        return Case.__instance

    @staticmethod
    def exists() -> bool:
        if Case.__instance:
            return True
        else:
            return False

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
        #log(f"Merging old {old.__class__.__name__} object to new")
        items = new.__dict__.items()  # RECHECK
        for attr, value in items:
            #log(f"Attribute: {attr} ({getattr(new, attr).__class__.__name__})")
            if not hasattr(old, attr):  # Update attribute
                log(f"Old object did not  have {attr} attribute. Just updating it and going forward")
                setattr(old, attr, value)
                continue
            if hasattr(value, "__dict__") and hasattr(old, attr):  # Merge attribute
                #log(f"Recursively update {attr} attribute")
                # FIXME: old.attr may not have __dict__...
                Case.merge_old_object(getattr(old, attr), value)
                continue
            #BufferBoxes
            if attr == "bufferbox_list":
                log(f"Recursively update bufferbox list: {attr}")
                Case.merge_bufferbox_list(getattr(old, attr))


    @staticmethod
    def merge_old_list(old, new):
        #log(f"Merging list")
        for ob in old:
            #log(f"Object: {ob}")
            if hasattr(ob, "__dict__"):
                cl = ob.__class__
                n: cl = cl()
                #log(f"Merging object {ob} to new {cl} object")
                Case.merge_old_object(ob, n)

    @staticmethod
    def merge_bufferbox_list(old):
        log(f"Merging bufferbox list")
        for bb in old:
            Case.merge_old_object(bb, BufferBox(1))

    def get_first_mk_not_used(self, object_type: ObjectType):
        """ Checks simulation objects to find the first not used MK group number. """
        mkset = set(map(lambda x: x.obj_mk, filter(lambda y: y.type == object_type, self.objects)))
        limit = {ObjectType.FLUID: 10, ObjectType.BOUND: 240}[object_type]
        start = 0
        if self.vres.active:
            start = {ObjectType.FLUID: 1, ObjectType.BOUND: 0}[object_type]
        for i in range(start, limit):
            if i not in mkset:
                return i
        warning_dialog(f"No free mk{object_type} values, mk{object_type} will be set to 0")
        return 0

    def get_all_simulation_object_names(self) -> List[str]:
        """ Returns a list with all the internal names used by the objects in the simulation. """
        return list(map(lambda obj: obj.name, self.objects))

    def get_all_tmp_object_names(self) -> List[SimulationObject]:
        """ Returns a list with all the internal names used by the temporal objects to be included to the simulation. """
        return list(map(lambda obj: obj.name, self.tmp_objects))

    def get_simulation_object(self, name) -> SimulationObject:
        """ Returns a simulation object from its internal name.
        Raises an exception if the selected object is not added to the simulation. """
        return next(filter(lambda obj: obj.name == name, self.objects), None)

    def get_tmp_object(self, name) -> SimulationObject:
        """ Returns a temporal object from its internal name.
        Raises an exception if the selected object is not added to the simulation. """
        return next(filter(lambda obj: obj.name == name, self.tmp_objects), None)

    def get_all_complex_objects(self) -> list:
        """ Returns all complex simulation objects. """
        return list(filter(lambda obj: FreeCAD.ActiveDocument.getObject(
            obj.name) and FreeCAD.ActiveDocument.getObject(
            obj.name).TypeId not in SUPPORTED_TYPES and "FillBox" not in obj.name, self.objects))

    def get_all_fluid_objects(self) -> List[SimulationObject]:
        """ Returns all the fluid objects in the simulation. """
        return list(filter(lambda obj: obj.type == ObjectType.FLUID, self.objects))

    def get_all_bound_objects(self) -> List[SimulationObject]:
        """ Returns all the bound objects in the simulation. """
        return list(filter(lambda obj: obj.type == ObjectType.BOUND, self.objects))

    def number_of_objects_in_simulation(self) -> int:
        """ Return the total number of objects in the simulation """
        return len(list(filter(lambda obj: obj.type != ObjectType.SPECIAL, self.objects)))

    # def _get_mk_based_properties(self, obj_type: ObjectType, mknumber: int) -> MKBasedProperties:
    #     """ Returns the properties set for a given MK number of a given type """
    #     if obj_type == ObjectType.BOUND:
    #         mknumber += MKFLUID_LIMIT
    #     if not self.has_mk_properties(mknumber):
    #         log("Creating MKBasedProperties on demand for realmk: {}".format(mknumber))
    #         self.mkbasedproperties[mknumber] = MKBasedProperties(mk=mknumber)
    #     log("Returning MKBasedProperties object for realmk: {}".format(mknumber))
    #     return self.mkbasedproperties[mknumber]

    def get_mk_based_properties(self,realmk) -> MKBasedProperties:
        if not self.has_mk_properties(realmk):              #MOVE TO ADD TO SIMULATION??
            self.mkbasedproperties[realmk] = MKBasedProperties(mk=realmk)
        return self.mkbasedproperties[realmk]

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
        if simobject.name in self.get_all_tmp_object_names():
            tmp_obj = self.get_tmp_object(simobject.name)
            tmp_obj.obj_mk = simobject.obj_mk
            #self.remove_tmp_object(simobject.name) #Remove from temporals? (but must be added again if removed from sim)
            self.objects.append(tmp_obj)
        else:
            self.objects.append(simobject)

    def add_tmp_object(self, simobject: SimulationObject):
        """ Adds an object to the current case but not to the simulation """
        if simobject.name in self.get_all_simulation_object_names() or simobject.name in self.get_all_tmp_object_names():
            warning_dialog(f"Object with the name: {format(simobject.name)} is already added to the case")
            # raise RuntimeError("Object with the name: {} is already added to the case".format(simobject.name))
        self.tmp_objects.append(simobject)

    def remove_object(self, object_name: str) -> SimulationObject:
        """ Tries to remove the given object name from the simulation.
        If no element is found an error is raised. """
        if object_name not in self.get_all_simulation_object_names():
            raise RuntimeError("The object that you are trying to remove ({}) is not present in the simulation")
        self.objects = list(filter(lambda obj: obj.name != object_name, self.objects))
        self.delete_orphan_mkbasedproperties()

    def remove_tmp_object(self, object_name: str) -> SimulationObject:
        """ Tries to remove the given object name from the temporal object list.
        If no element is found an error is raised. """
        if object_name in self.get_all_tmp_object_names():
            self.tmp_objects = list(filter(lambda obj: obj.name != object_name, self.tmp_objects))
            self.delete_orphan_mkbasedproperties()

    # MK_BASED_PROPERTIES
    def get_orphan_mkbasedproperties(self):
        """ Returns all MKBasedProperties that no longer have an object present in the case. """
        to_ret: list = list()
        for realmk in self.mkbasedproperties:
            if realmk not in map(lambda obj: obj.obj_mk if obj.type == ObjectType.FLUID else obj.obj_mk + MKFLUID_LIMIT,
                                 Case.the().objects):
                to_ret.append(realmk)
        return to_ret

    def delete_orphan_mkbasedproperties(self):
        """ Deletes all MKBasedProperties that no longer have an object present in the case. """
        for key in self.get_orphan_mkbasedproperties():
            self.mkbasedproperties.pop(key)

    # DAMPING ZONES
    def get_damping_zone(self, object_key: str) -> Damping:
        """ Returns the Damping Zone bound to the object key passed as parameter. Returns None if it's not defined. """
        return self.damping_zones.get(object_key)

    def remove_damping_zone(self, object_key: str) -> None:
        """ Removes the damping zone from the data structure. """
        self.damping_zones.pop(object_key)

    def add_damping_group(self, group_name: str) -> None:
        """ Adds a new freecad group/folder to a new Damping Zone. """
        self.damping_zones[group_name] = Damping()

    def is_damping_bound_to_object(self, freecad_object_name: str) -> bool:
        """ Returns whether the object passed has a damping object bound to it or not. """
        return freecad_object_name in self.damping_zones.keys()

    def get_damping_fc_group(self, damping: Damping):
        for k, d in self.damping_zones:
            if d == damping:
                return k
        return None

    def was_not_saved(self) -> bool:
        """ Returns whether this case was or not saved before """
        return self.path == "" and self.name == ""

    def reset_simulation_domain(self) -> None:
        """ Restores the Simulation Domain to the default one. """
        self.domain = SimulationDomain()

    def shift_object_up_in_order(self, index) -> None:
        """ Moves an object up in the order. """
        self.objects.insert(index - 1, self.objects.pop(index))

    def shift_object_down_in_order(self, index) -> None:
        """ Moves an object up in the order. """
        self.objects.insert(index + 1, self.objects.pop(index))

    def get_out_xml_file_path(self) -> str:
        """ Constructs the path for the out xml file needed to execute DualSPHysics. """
        return f"{self.path}/{self.name}_out/{self.name}" #OS.SEP???

    def get_out_folder_path(self,include_path:bool=True) -> str:
        """ Constructs the path for the output folder of the case. """
        if include_path:
            path = self.path+"/"
        else:
            path =""
        return "{path}{name}_out/".format(path=path, name=self.name)

    def get_out_data_folder_path(self,include_path:bool=True) -> str:
        """ Constructs the path for the output folder of the case. """
        if include_path:
            path = self.path+"/"
        else:
            path =""
        if not self.vres.active:
            path = "{path}/{name}_out/data/".format(path=path, name=self.name)
        else:
            path = "{path}/{name}_out/data_vres00".format(path=path, name=self.name)
        return path

    def has_materials(self) -> bool:
        """ Returns whether this case contains defined materials or not. """
        for mkbasedproperty in self.mkbasedproperties.values():
            if mkbasedproperty.property:
                return True
        return False

    def get_objects_by_mk(self, obj_type: ObjectType, mk: int) -> List[SimulationObject]:
        l = []
        if obj_type == ObjectType.BOUND:
            bounds = self.get_all_bound_objects()
            for b in bounds:
                if b.obj_mk == mk:
                    l.append(b)
        elif obj_type == ObjectType.FLUID:
            fluids = self.get_all_fluid_objects()
            for f in fluids:
                if f.obj_mk == mk:
                    l.append(f)
        return l

    def get_first_fc_object_from_mk(self, obj_type: ObjectType, mk: int):
        sim_objects = self.get_objects_by_mk(obj_type, mk)
        sim_obj = sim_objects[0]
        fc_obj = get_fc_object(sim_obj.name)
        return fc_obj.Name


def mk_help_list():
    mklist = mod.dataobjects.case.Case.the().objects
    info = ""
    for obj in mklist:
        if (obj.type != ObjectType.SPECIAL):
            info += f"realmk: {obj.real_mk()}: {get_fc_object(obj.name).Label} ({obj.name}) type: {obj.type} mk{obj.type}: {obj.obj_mk} \n"
    return info
