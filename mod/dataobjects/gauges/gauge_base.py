from __future__ import annotations


class Gauge:

    def __init__(self, save_vtk_part: bool = False, compute_dt: float = 0, compute_time_start: float = 0,
                 compute_time_end: float = 0, output: bool = False, output_dt: float = 0, output_time_start: float = 0,
                 output_time_end: float = 0, name: str = ""):
        self.save_vtk_part = save_vtk_part
        self.compute_dt: float = compute_dt
        self.compute_time_start: float = compute_time_start
        self.compute_time_end: float = compute_time_end
        self.output: bool = output
        self.output_dt: float = output_dt
        self.output_time_start: float = output_time_start
        self.output_time_end: float = output_time_end
        self.name = name
        self.type = "base"
        self.fc_object_name=""


    def load_defaults(self, defaults: Gauge):
        self.save_vtk_part = defaults.save_vtk_part
        self.compute_dt: float = defaults.compute_dt
        self.compute_time_start: float = defaults.compute_time_start
        self.compute_time_end: float = defaults.compute_time_end
        self.output: bool = defaults.output
        self.output_dt: float = defaults.output_dt
        self.output_time_start: float = defaults.output_time_start
        self.output_time_end: float = defaults.output_time_end
