from mod.constants import LINE_END
from mod.tools.stdout_tools import debug
from mod.tools.template_tools import get_template_text


class ParametersRenderer:
    """ Renders the gauges of the GenCase XML. """

    BASE_XML = "/templates/gencase/parameters.xml"


    @classmethod
    def render(cls, data):
        if data["execution_parameters"]["shifting"]==4:
            pass
        else:
            pass
        result = get_template_text(cls.BASE_XML).format(**data)
        return result