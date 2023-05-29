from OpenGL.GL import *

import pyphyslab.core.shader as shader
from pyphyslab.core.shader import Uniform

class Material:

    def __init__(self, vertex_shader_code, fragment_shader_code):
        self.program_ref = shader.initialize_program(vertex_shader_code,  fragment_shader_code)
        self.uniform_dict = {
            "modelMatrix":      Uniform("mat4", None),
            "viewMatrix":       Uniform("mat4", None),
            "projectionMatrix": Uniform("mat4", None), 
        }

        self.setting_dict = {
           "drawStyle": GL_TRIANGLES                 
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
        Convenience method for setting multiple material "properties"
        (uniform and render setting values) from a dictionary
        """
        if property_dict:
            for name, data in property_dict.items():
                # Update uniforms
                if name in self.uniform_dict.keys():
                    self.uniform_dict[name].data = data
                # Update render settings
                elif name in self.setting_dict.keys():
                    self.setting_dict[name] = data
                # Unknown property type
                else:
                    raise Exception("Material has no property named: " + name)