from typing import Union, Dict

from mod.enums import FilterOperations, ObjectType, FilterType
from mod.tools.stdout_tools import debug


class BaseFilter():


    def __init__(self):
        self.filt_type=FilterType.BASE
        self.ftfollow_mk: int = -1
        self.ftfollow_active: bool = False
        self.ftfollow: str = ""
        self.fc_object_name: str=""
        self.active: bool
        self.operation: FilterOperations = FilterOperations.ADD
        self.inverse: bool = False
        self.parent = None
        self.name: str = ""

    def process_strings(self):
        if self.ftfollow_active:
            self.ftfollow=f"<ftfollow mk=\"{self.ftfollow_mk}\"/>"


class FilterPos(BaseFilter):
    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.POS
        self.pos_min_str = ""
        self.pos_max_str = ""
        self.pos_min: list = [0.0, 0.0, 0.0]
        self.pos_max: list = [0.0, 0.0, 0.0]
        self.enable_pos_min: list = [True, True, True]
        self.enable_pos_max: list = [True, True, True]

    def check(self):
        return sum(self.enable_pos_min)+sum(self.enable_pos_max)

    def process_strings(self):
        super().process_strings()
        posmin_x_str=posmin_y_str=posmin_z_str=""
        posmax_x_str = posmax_y_str = posmax_z_str = ""
        if self.enable_pos_min[0]:
            posmin_x_str=f"x = \"{self.pos_min[0]}\""
        if self.enable_pos_min[1]:
            posmin_y_str = f"y = \"{self.pos_min[1]}\""
        if self.enable_pos_min[2]:
            posmin_z_str = f"z = \"{self.pos_min[2]}\""
        if posmin_x_str+posmin_y_str+posmin_z_str != "":
            self.pos_min_str = f"<posmin {posmin_x_str} {posmin_y_str} {posmin_z_str} />"
        if self.enable_pos_max[0]:
            posmax_x_str=f"x = \"{self.pos_max[0]}\""
        if self.enable_pos_max[1]:
            posmax_y_str = f"y = \"{self.pos_max[1]}\""
        if self.enable_pos_max[2]:
            posmax_z_str = f"z = \"{self.pos_max[2]}\""
        if posmax_x_str+posmax_y_str+posmax_z_str != "":
            self.pos_max_str = f"<posmax {posmax_x_str} {posmax_y_str} {posmax_z_str} />"

class FilterPlane(BaseFilter):


    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.PLANE
        self.point: list = [0.0, 0.0, 0.0]
        self.vector: list = [0.0, 0.0, 0.0]
        self.distance: float = 0.0
        self.distance_enabled: bool = False
        self.distance_str = ""

    def check(self):
        return sum(self.vector)

    def process_strings(self):
        super().process_strings()
        if self.distance_enabled:
            self.distance_str=f"\n<distance v=\"{self.distance}\"/>"

class FilterSphere(BaseFilter):

    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.SPHERE
        self.center: list = [0.0, 0.0, 0.0]
        self.radius: float = 0.01

    def check(self):
        return self.radius!=0.0

class FilterCylinder(BaseFilter):

    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.CYLINDER
        self.point1: list = [0.0, 0.0, 0.0]
        self.point2: list = [0.0, 0.0, 0.001]
        self.radius: float = 0.001


class TypeFilter(BaseFilter):

    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.TYPE
        self.bound: bool = False
        self.fixed: bool = False
        self.moving: bool = False
        self.floating: bool = False
        self.fluid: bool = False
        self.type_str = ""

    def process_strings(self):
        super().process_strings()
        self.type_str=""
        if self.bound:
            self.type_str = self.type_str + "bound,"
        if self.fixed:
            self.type_str = self.type_str + "fixed,"
        if self.moving:
            self.type_str = self.type_str + "moving,"
        if self.floating:
            self.type_str = self.type_str + "floating,"
        if self.fluid:
            self.type_str = self.type_str + "fluid"

class FilterMK(BaseFilter):

    def __init__(self):
        super().__init__()
        self.filt_type=FilterType.MK
        self.is_range: bool = False
        self.mk_value: int = -1
        self.range_min: int = 0
        self.range_max: int = 0
        self.obj_type: ObjectType = ObjectType.BOUND
        self.mk_type_str: str = ""
        self.mk_str: str = ""

    def process_strings(self):
        super().process_strings()
        if self.obj_type is None:
            self.mk_type_str = "mk"
        elif self.obj_type == ObjectType.BOUND:
            self.mk_type_str = "mkbound"
        if self.obj_type == ObjectType.FLUID:
            self.mk_type_str = "mkfluid"
        if not self.is_range:
            self.mk_str = str(self.mk_value)
        else:
            self.mk_str = f"{self.range_min}-{self.range_max}"

class FilterGroup(BaseFilter):


    def __init__(self):
        super().__init__()
        self.filt_type = FilterType.GROUP
        self.filts:dict  ={}
        self.preselection_all:bool=True

    def add_filter(self, filter):
        name = filter.name
        self.filts[name] = filter

    def remove_filter(self, name):
        del self.filts[name]

    def process_strings(self):
        super().process_strings()
        if self.preselection_all:
            self.preselection_str="all"
        else:
            self.preselection_str="none"


class OutputParts:

    def __init__(self):
        self.filts: Dict[str,Union[BaseFilter,FilterPos,FilterSphere,FilterPlane,FilterCylinder,FilterMK,TypeFilter,FilterGroup]] = dict()
        self.active: bool = True
        self.preselection_all: bool = True
        self.ignore_nparts:int=0

    def add_filter(self,filter):
        name=filter.name
        self.filts[name]=filter

    def remove_filter(self,name):

        del self.filts[name]

