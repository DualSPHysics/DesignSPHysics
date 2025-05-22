from typing import Union

from mod.dataobjects.configuration.simulation_domain import SimulationDomain


class BufferBox:

    def __init__(self, id: int):
        self.id = id
        self.active : bool = True
        self.manual_placement : bool = False
        self.point : list = [0.0,0.0,0.0]
        self.size : list = [0.0,0.0,0.0]
        self.dp_ratio : float = 1.0
        self.buffer_size_h : int = 2
        self.overlapping_h : float = 0.0
        self.tracking_active : bool = False
        self.tracking_mkbound : int = 0
        self.parent : Union[BufferBox,None] = None
        self.transform_enabled : bool = False
        self.transform_move : list = [0.0,0.0,0.0]
        self.transform_rotate : list = [0.0, 0.0, 0.0]
        self.transform_rotate_radians : bool = False
        self.transform_center_enabled : bool = False
        self.transform_center : list = [0.0, 0.0, 0.0]
        self.domain : SimulationDomain = SimulationDomain()
        self.depth : float = 0.0
        self.fc_object_name : str = ""
        self.vreswavegen : bool = False
        #self.simulation_domain : SimulationDomain = SimulationDomain()


    def __str__(self):
        return f"(Id : {self.id}  parent: {self.parent} depth : {self.depth})"

    def __repr__(self):
        return f"(Id : {self.id}  parent: {self.parent} depth : {self.depth})"
