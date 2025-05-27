from mod.constants import LINE_END
from mod.functions import is_key
from mod.tools.template_tools import get_template_text


class FlexStructRenderer:
    BASE_XML = "/templates/gencase/flexstruct/base.xml"
    EACH_XML = "/templates/gencase/flexstruct/each.xml"
    @classmethod
    def render(cls,data):
        flex_structs: dict = dict()
        for mk, mk_prop in data["mkbasedproperties"].items():
            if is_key(mk_prop,"flex_struct") and mk_prop["flex_struct"] and mk_prop["flex_struct"]["enabled"]=="true":
                flex_structs[mk] = mk_prop["flex_struct"]
        if not flex_structs.values():
            return ""

        each_flex_struct_template: list = list()
        for mk, flex_struct in flex_structs.items():
                flex_struct.update({"mk": mk})
                each_flex_struct_template.append(get_template_text(cls.EACH_XML).format(**flex_struct))


        formatter = {
            "each": LINE_END.join(each_flex_struct_template)
        }

        return get_template_text(cls.BASE_XML).format(**formatter)
        