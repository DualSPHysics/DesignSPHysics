from mod.dataobjects.gauges.gauge_base import Gauge


class SWLGauge(Gauge):
    def __init__(self, save_vtk_part: bool = False, compute_dt: float = 0, compute_time_start: float = 0,
                 compute_time_end: float = 0, output: bool = False, output_dt: float = 0, output_time_start: float = 0,
                 output_time_end: float = 0, name: str = "", point0_x: float = 0, point0_y: float = 0,
                 point0_z: float = 0, point1_x: float = 0, point1_y: float = 0, point1_z: float = 0,
                 point_dp: float = 0, point_dp_coef_dp: bool = False, mass_limit: float = 0.5,
                 mass_limit_coef: bool = True):
        super().__init__(save_vtk_part, compute_dt, compute_time_start, compute_time_end, output, output_dt,
                         output_time_start, output_time_end, name)
        self.point0 = [point0_x, point0_y, point0_z]
        self.point1 = [point1_x, point1_y, point1_z]
        self.point_dp = point_dp
        self.point_dp_coef_dp = point_dp_coef_dp
        self.mass_limit = mass_limit
        self.mass_limit_coef = mass_limit_coef
        self.type="swl"
