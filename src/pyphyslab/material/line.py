from OpenGL.GL import *

from  pyphyslab.material.basic import BasicMaterial

class LineMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        # Render vertices as continuous line by default
        self.setting_dict["drawStyle"] = GL_LINE_STRIP
        # Set the line thickness
        self.setting_dict["lineWidth"] = 1
        # line type: "connected" | "loop" | "segments"
        self.setting_dict["lineType"] = "connected"
        self.set_properties(property_dict)

    def update_render_settings(self):
        glLineWidth(self.setting_dict["lineWidth"])
        if self.setting_dict["lineType"] == "connected":
            self.setting_dict["drawStyle"] = GL_LINE_STRIP
        elif self.setting_dict["lineType"] == "loop":
            self.setting_dict["drawStyle"] = GL_LINE_LOOP
        elif self.setting_dict["lineType"] == "segments":
            self.setting_dict["drawStyle"] = GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style")