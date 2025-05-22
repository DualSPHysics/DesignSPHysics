from mod.dataobjects.flow_tool_xml_box import FlowToolXmlBox
from mod.enums import FlowUnits


class PostProcessingSettings():

    def __init__(self):
        self.measuretool_points: list = []
        self.measuretool_grid: list = []
        self.flowtool_units: FlowUnits = FlowUnits.LITERSSECOND
        self.flowtool_xml_boxes: list[FlowToolXmlBox] = list()  # [FlowToolBox]