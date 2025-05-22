from mod.constants import LINE_END, SUPPORTED_TYPES
from mod.enums import BoundNormalsType
from mod.tools.template_tools import get_template_text
from mod.xml.renderers.objects_renderer import ObjectsRenderer
import FreeCAD

class MdbcRenderer:
    GEOMETRY_BASE_XML = "/templates/gencase/mdbc/geometry_for_normals_base.xml"
    GEOMETRY_EACH_XML = "/templates/gencase/mdbc/each.xml"
    RUNLIST_XML = "/templates/gencase/mdbc/mdbc_runlist.xml"

    NORMALS_BASE_XML= "/templates/gencase/mdbc/normals_base.xml"
    NORMALS_GEOMETRY_XML = "/templates/gencase/mdbc/normals_geometry.xml"

    SET_XML = "/templates/gencase/mdbc/boundnormal_set.xml"
    PLANE_XML = "/templates/gencase/mdbc/boundnormal_plane.xml"
    PLANE_POINT_XML = "/templates/gencase/mdbc/boundnormal_plane_point.xml"
    PLANE_POINT_AUTO_XML = "/templates/gencase/mdbc/boundnormal_plane_point_auto.xml"
    SPHERE_XML = "/templates/gencase/mdbc/boundnormal_sphere.xml"
    CYLINDER_XML = "/templates/gencase/mdbc/boundnormal_cylinder.xml"
    PARTS_XML = "/templates/gencase/mdbc/boundnormal_parts.xml"

    @classmethod
    def render_geo(cls, data):
        """ Returns the rendered string. """
        object_xmls = []
        for obj in data["objects"]:
            if obj["use_mdbc"] == "false":
                continue
            fc_object = FreeCAD.ActiveDocument.getObject(obj["name"])
            obj["is_normals_geo"] = "true"
            if fc_object.TypeId in SUPPORTED_TYPES:
                obj["layers"] = obj["mdbc_dist_vdp"]
                object_template: str = ObjectsRenderer.get_regular_objects_template(obj, fc_object)
            elif "FillBox" in fc_object.Name:
                object_template: str = ObjectsRenderer.get_fillbox_object_template(obj, fc_object)
            else:
                object_template: str = ObjectsRenderer.get_complex_object_template(obj, fc_object)
            object_xmls.append(object_template)

        if object_xmls:
            formatter = {"objects_each": LINE_END.join(object_xmls) if object_xmls else ""}
            return get_template_text(cls.GEOMETRY_BASE_XML).format(**formatter)
        else:
            return ""

    @classmethod
    def runlist(cls):
        return get_template_text(cls.RUNLIST_XML)

    @classmethod
    def render_normals_base(cls,data):
        normals_templates = list()
        for x in data["mkbasedproperties"].values():
            if not "bound_normals" in x:
                x["bound_normals"] = None
        
        suitable_mkbasedproperties = filter(lambda x: x["bound_normals"] is not None, data["mkbasedproperties"].values())
        if not suitable_mkbasedproperties and not data["geometry_for_normals_template"]:
            return ""
        else:
            for mkbasedproperty in suitable_mkbasedproperties:
                bound_normals = mkbasedproperty["bound_normals"]
                if bound_normals is not None:
                    
                    if bound_normals["normals_type"] == BoundNormalsType.SET:
                        normals_templates.append(get_template_text(cls.SET_XML).format(**bound_normals))
                    elif bound_normals["normals_type"] == BoundNormalsType.PLANE:
                        bound_plane_key = "bound_normal_point_template"
                        if bound_normals["point_auto"] == "true":
                            bound_normals[bound_plane_key] = get_template_text(cls.PLANE_POINT_AUTO_XML).format(
                                **bound_normals)
                            # normals_templates.append(get_template_text(cls.PLANE_XML).format(**formatter))
                            # plane_point_auto_tmp = get_template_text(cls.PLANE_POINT_AUTO_XML)
                            # plane_xml_tmp=plane_xml_tmp.format(bound_normal_point_template=plane_point_auto_tmp)
                        else:
                            bound_normals[bound_plane_key] = get_template_text(cls.PLANE_POINT_XML).format(
                                **bound_normals)
                            # normals_templates.append(get_template_text(cls.PLANE_XML).format(**formatter))
                            # plane_point_auto_tmp = get_template_text(cls.PLANE_POINT_AUTO_XML)
                            # plane_xml_tmp=plane_xml_tmp.format(bound_normal_point_template=plane_point_auto_tmp)
                            # normals_templates.append(plane_xml_tmp.format(**bound_normals))
                        normals_templates.append(get_template_text(cls.PLANE_XML).format(**bound_normals))
                    elif bound_normals["normals_type"] == BoundNormalsType.SPHERE:
                        normals_templates.append(get_template_text(cls.SPHERE_XML).format(**bound_normals))
                    elif bound_normals["normals_type"] == BoundNormalsType.CYLINDER:
                        normals_templates.append(get_template_text(cls.CYLINDER_XML).format(**bound_normals))
                    elif bound_normals["normals_type"] == BoundNormalsType.PARTS:
                        normals_templates.append(get_template_text(cls.PARTS_XML).format(**bound_normals))
            if data["geometry_for_normals_template"]:
                normals_templates.append(cls.render_normals(data))

            return get_template_text(cls.NORMALS_BASE_XML).format(normals_each=LINE_END.join(normals_templates))
    @classmethod
    def render_normals(cls,data):
        formatter = {"mdbc_disth": data["execution_parameters"]["mdbc_disth"]
                     ,"mdbc_maxsizeh" : data["execution_parameters"]["mdbc_maxsizeh"]}
        return get_template_text(cls.NORMALS_GEOMETRY_XML).format(**formatter)
