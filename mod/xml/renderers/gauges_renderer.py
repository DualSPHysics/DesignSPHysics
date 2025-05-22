from mod.constants import LINE_END
from mod.tools.template_tools import get_template_text


class GaugesRenderer:
    """ Renders the gauges of the GenCase XML. """

    BASE_XML = "/templates/gencase/gauges/base.xml"
    COMMON_XML = "/templates/gencase/gauges/common.xml"
    VELOCITY_XML = "/templates/gencase/gauges/velocity.xml"
    SWL_XML = "/templates/gencase/gauges/swl.xml"
    MAXZ_XML = "/templates/gencase/gauges/maxz.xml"
    FORCE_XML = "/templates/gencase/gauges/force.xml"
    MESH_XML = "/templates/gencase/gauges/mesh.xml"
    FLOW_XML = "/templates/gencase/gauges/flow.xml"

    each_template= {
        "velocity" : VELOCITY_XML,
        "swl":SWL_XML,
        "maxz":MAXZ_XML,
        "force":FORCE_XML,
        "mesh":MESH_XML,
        "flow":FLOW_XML
    }


    @classmethod
    def render(cls, data):


        gauges_template_list: list = list()
        for name,gauge in data["gauges"]["gauges_dict"].items():
            if name != "Defaults":
                gauge["common"]=get_template_text(cls.COMMON_XML).format(**gauge)
                if gauge["type"]=="swl":
                    if gauge["mass_limit_coef"]=="true": gauge["mass_limit_coef"]="coef"
                    else: gauge["mass_limit_coef"]="value"
                    if gauge["point_dp_coef_dp"]=="true": gauge["point_dp_coef_dp"]="coefdp"
                    else: gauge["point_dp_coef_dp"]="value"
                if gauge["type"] == "mesh":
                    if gauge["mass_limit_coef"] == "true": gauge["mass_limit_coef"] = "coef"
                    else: gauge["mass_limit_coef"] = "value"
                    if gauge["kclimit_enable"]=="false":gauge["kclimit"]="NONE"
                    if gauge["kc_dummy_enable"]=="false": gauge["kc_dummy"] = "NONE"
                if gauge["type"] == "flow":
                    if gauge["kclimit_enable"]=="false":gauge["kclimit"]="NONE"
                gauges_template_list.append(get_template_text(cls.each_template[gauge["type"]]).format(**gauge))
        formatter: dict = {
            "gauges_each": LINE_END.join(gauges_template_list)
        }
        return get_template_text(cls.BASE_XML).format(**formatter)



