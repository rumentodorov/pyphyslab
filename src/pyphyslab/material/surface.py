from OpenGL.GL import *

from pyphyslab.material.basic import BasicMaterial

class SurfaceMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code = None, fragment_shader_code = None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)

        self.setting_dict["drawStyle"] = GL_TRIANGLES
        self.setting_dict["doubleSide"] = False
        self.setting_dict["wireframe"] = False
        self.setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    def update_render_settings(self):
        if self.setting_dict["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        if self.setting_dict["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(self.setting_dict["lineWidth"])