from OpenGL.GL import *

from  pyphyslab.material.basic import BasicMaterial

class LineMaterial(BasicMaterial):

    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        
        self.setting_dict[BasicMaterial.DRAWING_STYLE_RENDER_SETTING] = GL_LINE_STRIP
        self.setting_dict[BasicMaterial.LINE_WIDTH_RENDER_SETTING] = 1        
        self.setting_dict[BasicMaterial.LINE_TYPE_RENDER_SETTING] = "connected"
        self.set_properties(property_dict)

    def update_render_settings(self):

        glLineWidth(self.setting_dict[BasicMaterial.LINE_WIDTH_RENDER_SETTING])
        if self.setting_dict[BasicMaterial.LINE_TYPE_RENDER_SETTING] == "connected":
            self.setting_dict[BasicMaterial.DRAWING_STYLE_RENDER_SETTING] = GL_LINE_STRIP
        elif self.setting_dict[BasicMaterial.LINE_TYPE_RENDER_SETTING] == "loop":
            self.setting_dict[BasicMaterial.DRAWING_STYLE_RENDER_SETTING] = GL_LINE_LOOP
        elif self.setting_dict[BasicMaterial.LINE_TYPE_RENDER_SETTING] == "segments":
            self.setting_dict[BasicMaterial.DRAWING_STYLE_RENDER_SETTING] = GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style")