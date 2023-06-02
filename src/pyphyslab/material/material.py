from OpenGL.GL import *

import pyphyslab.core.shader as shader
from pyphyslab.core.shader import Uniform

class Material:

    MODEL_MATRIX_UNIFORM = "modelMatrix"
    VIEW_MATRIX_UNIFORM = "viewMatrix"
    PROJECTION_MATRIX_UNIFORM = "projectionMatrix"
    BASE_COLLOR_UNIFORM = "baseColor"
    USE_VERTEX_COLOR_UNIFORM = "useVertexColors"


    DRAWING_STYLE_RENDER_SETTING = "drawStyle"
    DOUBLE_SIDE_RENDER_SETTING = "doubleSide"
    WIREFRAME_RENDER_STTING = "wireframe"    
    LINE_WIDTH_RENDER_SETTING = "lineWidth"
    LINE_TYPE_RENDER_SETTING = "lineType"

    def __init__(self, vertex_shader_code, fragment_shader_code):
        self.program_ref = shader.initialize_program(vertex_shader_code,  fragment_shader_code)
        self.uniform_dict = {
            Material.MODEL_MATRIX_UNIFORM:      Uniform("mat4", None),
            Material.VIEW_MATRIX_UNIFORM:       Uniform("mat4", None),
            Material.PROJECTION_MATRIX_UNIFORM: Uniform("mat4", None), 
        }

        self.setting_dict = {
           Material.DRAWING_STYLE_RENDER_SETTING: GL_TRIANGLES                 
        }

    def add_uniform(self, data_type, variable_name, data):
        self.uniform_dict[variable_name] = Uniform(data_type, data)

    def locate_uniforms(self):
        """ Initialize all uniform variable references """
        for variable_name, uniform_object in self.uniform_dict.items():
            uniform_object.locate_variable(self.program_ref, variable_name)
    
    def update_render_settings(self):
        """ Configure OpenGL with render settings """
        pass

    def set_properties(self, property_dict):
        """
        Method for setting multiple material "properties"
        """
        if property_dict:
            for name, data in property_dict.items():
                if name in self.uniform_dict.keys():
                    self.uniform_dict[name].data = data
                elif name in self.setting_dict.keys():
                    self.setting_dict[name] = data
                else:
                    raise Exception("Material has no property named: " + name)