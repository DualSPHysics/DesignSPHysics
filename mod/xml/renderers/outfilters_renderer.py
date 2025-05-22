from mod.constants import LINE_END
from mod.tools.stdout_tools import debug
from mod.tools.template_tools import get_template_text


class OutFiltersRenderer:
    """ Renders the gauges of the GenCase XML. """

    BASE_XML = "/templates/gencase/outfilters/base.xml"
    POS_XML = "/templates/gencase/outfilters/filterpos.xml"
    PLANE_XML = "/templates/gencase/outfilters/filterplane.xml"
    SPHERE_XML = "/templates/gencase/outfilters/filtersphere.xml"
    CYLINDER_XML = "/templates/gencase/outfilters/filtercylinder.xml"
    TYPE_XML = "/templates/gencase/outfilters/filtertype.xml"
    MK_XML = "/templates/gencase/outfilters/filtermk.xml"
    GROUP_XML = "/templates/gencase/outfilters/filtergroup.xml"

    each_template= {
        "pos" :POS_XML,
        "plane":PLANE_XML,
        "sphere":SPHERE_XML,
        "cylinder":CYLINDER_XML,
        "type":TYPE_XML,
        "mk": MK_XML,
        "group": GROUP_XML
    }


    @classmethod
    def render(cls, data):
        if data["outparts"]["active"] == "false":
            return ""
        if data["outparts"]["preselection_all"]=="true":
            data["outparts"]["preselection_str"]="all"
        else:
            data["outparts"]["preselection_str"] = "none"
        filter_templates_list = list()

        filter_dict = data["outparts"]["filts"]

        for filt in filter_dict.values():  # LISTA DE PADRES
            filter_templates_list.append(cls.rec_render_xml(filt))

        formatter: dict = {
            "each": LINE_END.join(filter_templates_list),
            "preselection_str": data["outparts"]["preselection_str"],
            "n_parts":data["outparts"]["ignore_nparts"]
        }

        result = get_template_text(cls.BASE_XML).format(**formatter)
        return result

    @classmethod
    def rec_render_xml(cls,filter):
        children_text=""
        if filter["filt_type"]=="group":
            children = filter['filts']
            for son in children.values():
                children_text = children_text + cls.rec_render_xml(son)
            filter['each']=children_text
        else:
            filter['each'] = ''
        text = get_template_text(cls.each_template[filter["filt_type"]]).format(**filter)
        return text




