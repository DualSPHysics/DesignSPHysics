from mod.dataobjects.gauges.gauge_base import Gauge


class FlowGauge(Gauge):
    def __init__(self, save_vtk_part: bool = False, compute_dt: float = 0, compute_time_start: float = 0,
                 compute_time_end: float = 0, output: bool = False, output_dt: float = 0, output_time_start: float = 0,
                 output_time_end: float = 0, name: str = "", point_x: float = 0, point_y: float = 0,
                 point_z: float = 0, vec1_x: float = 1, vec1_y: float = 0, vec1_z: float = 0, vec2_x: float = 0,
                 vec2_y: float = 1, vec2_z: float = 0, size1_length: float = 0, size1_distpt: float = 0,
                 size2_length: float = 0, size2_distpt: float = 0, dirdat_x: float = 0, dirdat_y: float = 0,
                 dirdat_z: float = 0, buffersize: float = 30 , kclimit: float = 0.5,
                 kclimit_enable: bool = False):

        super().__init__(save_vtk_part, compute_dt, compute_time_start, compute_time_end, output, output_dt,
                         output_time_start, output_time_end, name)
        self.point0 = [point_x, point_y, point_z]
        self.vec1 = [vec1_x, vec1_y, vec1_z]
        self.vec2 = [vec2_x, vec2_y, vec2_z]
        self.size1_length = size1_length
        self.size1_distpt = size1_distpt
        self.size2_length = size2_length
        self.size2_distpt = size2_distpt
        self.dirdat = [dirdat_x, dirdat_y, dirdat_z]
        self.buffersize = buffersize
        self.kclimit = kclimit
        self.kclimit_enable = kclimit_enable
        self.type="flow"
