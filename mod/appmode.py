from mod.constants import CASE_3D_MODE

class AppMode:
    _3d_mode = CASE_3D_MODE
    _2d_pos_y = 0.0
    @classmethod
    def set_3d_mode(self, mode: bool):
        self._3d_mode = bool(mode)
    
    @classmethod
    def is_3d(self) -> bool:
        return self._3d_mode

    @classmethod
    def set_2d_pos_y(self,posy:float):
        self._2d_pos_y=posy
    
    @classmethod
    def get_2d_pos_y(self) -> float:
        return self._2d_pos_y