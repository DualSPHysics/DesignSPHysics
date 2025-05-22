from mod.constants import LINE_END
from mod.tools.stdout_tools import debug
from mod.tools.template_tools import get_template_text


class VResRenderer:
    """ Renders the gauges of the GenCase XML. """

    BASE_XML = "/templates/gencase/vres/base.xml"
    EACH_XML = "/templates/gencase/vres/each.xml"
    TRACKING_XML = "/templates/gencase/vres/tracking.xml"
    TRANSFORM_XML = "/templates/gencase/vres/transform.xml"
    DOMAIN_XML = "/templates/gencase/vres/simulation_domain.xml"
    DOMAIN_POS_XML = "/templates/gencase/vres/simulation_domain_pos.xml"

    @classmethod
    def render(cls, data):

        if data["vres"]["active"]=="false":
            return ""
        vres_render_list : list = list()
        bufferbox_templates_list = list()
        buff_list = data["vres"]["bufferbox_list"].copy()
        delete_list = []
        for bbox in buff_list:
            if bbox["parent"] is not None:
                delete_list.append(bbox)
        for bbox in delete_list:
            buff_list.remove(bbox)

        for buf in buff_list: #LISTA DE PADRES
            bufferbox_templates_list.append(cls.rec_render_xml(buf,data))

        formatter: dict = {
            "vres_each": LINE_END.join(bufferbox_templates_list),
            "vres_buffer_size_h" : data["vres"]["vres_buffer_size_h"]
        }
        result = get_template_text(cls.BASE_XML).format(**formatter)
        return result

    @classmethod
    def rec_render_xml(cls,bbox,data):
        text = ""
        sons_text = ""
        sons = cls.get_bbox_children(bbox,data["vres"]["bufferbox_list"])
        if bbox["tracking_active"] == "true":
            bbox["tracking"] = get_template_text(cls.TRACKING_XML).format(**bbox)
        else:
            bbox["tracking"] = ""
        if bbox["transform_enabled"]:
            if bbox["transform_rotate_radians"] == "false":
                bbox["transform_rotate_units"] = "degrees"
            else:
                bbox["transform_rotate_units"] = "radians"
            bbox["transform"] = get_template_text(cls.TRANSFORM_XML).format(**bbox)
        else:
            bbox["transform"] = ""
        if bbox["domain"]["enabled"] == "true":
            if bbox["domain"]["useparent"] == "false":
                formatter = {}
                for key in ["posmin_x", "posmin_y", "posmin_z"]:
                    value = bbox["domain"][key]["value"]
                    symbol = "-"
                    modes = {
                        0: "default",
                        1: str(value),
                        2: "default{}{}".format(symbol, str(abs(value))),
                        3: "default{}{}%".format(symbol, str(abs(value)))
                    }
                    formatter[key] = modes[bbox["domain"][key]["type"]]
                for key in ["posmax_x", "posmax_y", "posmax_z"]:
                    value = bbox["domain"][key]["value"]
                    symbol = "+"
                    modes = {
                        0: "default",
                        1: str(value),
                        2: "default{}{}".format(symbol, str(abs(value))),
                        3: "default{}{}%".format(symbol, str(abs(value)))
                    }
                    formatter[key] = modes[bbox["domain"][key]["type"]]
                bbox["domain"]["pos"] = get_template_text(cls.DOMAIN_POS_XML).format(**formatter)
            else:
                bbox["domain"]["pos"] = ""
            bbox["simulation_domain"] = get_template_text(cls.DOMAIN_XML).format(**bbox["domain"])
        else:
            bbox["simulation_domain"] = ""
        if not sons:
            bbox['vres_each'] = ''
            text= get_template_text(cls.EACH_XML).format(**bbox)
        else:
            for son in sons:
                sons_text = sons_text + cls.rec_render_xml(son,data)
            bbox['vres_each'] = sons_text
            text = get_template_text(cls.EACH_XML).format(**bbox)
        return text

    @classmethod
    def get_bbox_children(cls,bbox, dict):
        children = []
        for cand in dict:
            if cand['parent'] is not None:
                if cand['parent']['id'] == bbox['id']:
                    children.append(cand)
        return children
