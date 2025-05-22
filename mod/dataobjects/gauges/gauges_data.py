from mod.dataobjects.gauges.gauge_base import Gauge


class GaugesData:

    def __init__(self):
        self.gauges_dict:dict= {"Defaults": Gauge(name="Defaults")}

    def add_gauge(self,gauge :Gauge):
        name=gauge.name
        self.gauges_dict[name] = gauge

    def remove_gauge(self,name:str):
        self.gauges_dict.pop(name)
