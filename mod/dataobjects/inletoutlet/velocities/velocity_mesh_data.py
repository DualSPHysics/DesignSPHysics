# -*- coding: utf-8 -*-
""" MeshData velocity type for Inlet/Outlet. """
from typing import List


class VelocityMeshData():
    """ Defines Meshdata velocity for Inlet/outlet """

    def __init__(self, filepath : str="",magnitude: bool = False, reverse:bool = False, initial_time: float = 0.0,
                 timeloop_tbegin: float = 0.0,timeloop_tend:float=0.0,setpos:List =[0.0,0.0,0.0],
                 setvelmul:List =[1.0,1.0,1.0],setveladd:List =[0.0,0.0,0.0]) -> None:
        self.filepath=filepath
        self.magnitude=magnitude
        self.reverse=reverse
        self.initial_time=initial_time
        self.timeloop_tbegin=timeloop_tbegin
        self.timeloop_tend=timeloop_tend
        self.setpos=setpos
        self.setvelmul=setvelmul
        self.setveladd=setveladd

    def save(self,values):
        self.filepath = values["filepath"]
        self.magnitude = values["magnitude"]
        self.reverse = values["reverse"]
        self.initial_time = values["initial_time"]
        self.timeloop_tbegin = values["timeloop_tbegin"]
        self.timeloop_tend = values["timeloop_tend"]
        self.setpos = values["setpos"]
        self.setvelmul = values["setvelmul"]
        self.setveladd = values["setveladd"]