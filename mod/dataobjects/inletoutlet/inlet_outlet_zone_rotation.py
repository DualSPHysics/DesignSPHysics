import math

from mod.constants import DIVIDER
from mod.tools.stdout_tools import debug
import FreeCAD

class InletOutletZone3DRotation():

    def __init__(self) -> None:
        self.rotation_type: int = 0 #0 = No rotation 1=rotateaxis 2=rotateadv 3 = manual rotation
        self.rotateaxis_enabled: bool = False
        self.rotateaxis_angle: float = 0.0
        self.rotateaxis_point1: list = [0.0, 0.0, 0.0]
        self.rotateaxis_point2: list = [0.0, 0.0, 0.0]
        # rotateadv
        self.rotateadv_enabled: bool = False
        self.rotateadv_angle: list = [0.0, 0.0, 0.0]  # angle1, angle2,angle3
        self.rotateadv_axes: str = "XYZ"
        self.rotateadv_intrinsic: bool = False
        self.rotateadv_center: list = [0.0, 0.0, 0.0]

        self.last_fc_rotation :tuple = (0,0,0,0)


    def save_values(self, values):
        self.rotation_type=values["rotation_type"]
        #rotate_axis
        self.rotateaxis_enabled = values["rotateaxis_enabled"]
        self.rotateaxis_angle = values["rotateaxis_angle"]
        self.rotateaxis_point1 = values["rotateaxis_point1"]
        self.rotateaxis_point2 = values["rotateaxis_point2"]
        # rotateadv
        self.rotateadv_enabled = values["rotateadv_enabled"]
        self.rotateadv_angle = values["rotateadv_angle"]
        self.rotateadv_axes = values["rotateadv_axes"]
        self.rotateadv_intrinsic = values["rotateadv_intrinsic"]
        self.rotateadv_center = values["rotateadv_center"]

    def rotate_axis_from_freecad_placement(self,plac):
        self.rotateaxis_point1=list(plac.Base / DIVIDER)
        self.rotateaxis_point2=list((plac.Base /DIVIDER) - plac.Rotation.Axis )
        self.rotateaxis_angle = math.degrees(plac.Rotation.Angle)

    def move_rotation_axes(self,displacement:FreeCAD.Vector):
        self.rotateaxis_point1 = list((FreeCAD.Vector(self.rotateaxis_point1)*DIVIDER + displacement)/DIVIDER)
        self.rotateaxis_point2 = list((FreeCAD.Vector(self.rotateaxis_point2)*DIVIDER + displacement)/DIVIDER)
        self.rotateadv_center = list((FreeCAD.Vector(self.rotateadv_center)*DIVIDER + displacement)/DIVIDER)

    def adv_rotation_from_freecad_placement(self,plac):
        self.rotateadv_angle = list(
            plac.Rotation.getYawPitchRoll())
        self.rotateadv_angle.reverse()
        self.rotateadv_center = list(
            plac.Base / DIVIDER)

class InletOutletZone2DRotation():

    def __init__(self) -> None:
        self.manual_rotation:bool = False
        self.rotation_enabled: bool = False
        self.rotation_angle: float = 0.0
        self.rotation_center: list = [0.0,0.0]
        self.last_fc_rotation = (0,0,0,0)

    def save_values(self, values):
        self.manual_rotation = values["manual_rotation"]
        self.rotation_enabled = values["rotation_enabled"]
        self.rotation_angle = values["rotation_angle"]
        self.rotation_center = values["rotation_center"]

    def rotation_from_freecad_placement(self,plac):
        self.rotation_angle=plac.Rotation.getYawPitchRoll()[1]
        self.rotation_center=list(
            plac.Base / DIVIDER)
