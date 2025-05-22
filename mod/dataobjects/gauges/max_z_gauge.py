from mod.dataobjects.gauges.gauge_base import Gauge


class MaxZGauge(Gauge):
    def __init__(self, save_vtk_part: bool = False, compute_dt: float = 0, compute_time_start: float = 0,
                 compute_time_end: float = 0, output: bool = False, output_dt: float = 0, output_time_start: float = 0,
                 output_time_end: float = 0, name: str = "", point0_x: float = 0, point0_y: float = 0,
                 point0_z: float = 0,height:float=0,dist_limit:float=0):
        super().__init__(save_vtk_part, compute_dt, compute_time_start, compute_time_end, output, output_dt,
                         output_time_start, output_time_end, name)
        self.point0=[point0_x,point0_y,point0_z]
        self.height=height
        self.dist_limit=dist_limit
        self.type="maxz"
