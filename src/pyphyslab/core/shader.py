from OpenGL.GL import *
from collections import namedtuple
import numpy as np

#TODO Remove
def pring_gl_info():

    vendor = glGetString(GL_VENDOR).decode('utf-8')
    renderer = glGetString(GL_RENDERER).decode('utf-8')
    opengl = glGetString(GL_VERSION).decode('utf-8')
    glsl = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
    Result = namedtuple('SystemInfo', ['vendor', 'renderer', 'opengl', 'glsl'])
    return Result(vendor, renderer, opengl, glsl)

def initialize_shader(shader_code, shader_type):

    shader_code = '#version 330\n' + shader_code
    shader_ref = glCreateShader(shader_type)
    glShaderSource(shader_ref, shader_code)
    glCompileShader(shader_ref)
    compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
    
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_ref)
        glDeleteShader(shader_ref)
        error_message = '\n' + error_message.decode('utf-8')
        raise Exception(error_message)
    return shader_ref


def initialize_program(vertex_shader_code, fragment_shader_code):
    
    vertex_shader_ref = initialize_shader(vertex_shader_code, GL_VERTEX_SHADER)
    fragment_shader_ref = initialize_shader(fragment_shader_code, GL_FRAGMENT_SHADER)

    program_ref = glCreateProgram()
 
    glAttachShader(program_ref, vertex_shader_ref)
    glAttachShader(program_ref, fragment_shader_ref)
    

    glLinkProgram(program_ref)
    link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)
    
    if not link_success:
        
        error_message = glGetProgramInfoLog(program_ref)            
        glDeleteProgram(program_ref)
        
        error_message = '\n' + error_message.decode('utf-8')        
        raise Exception(error_message)
        
    return program_ref

class Uniform:

    def __init__(self, data_type, data):
        # type of data:
        # int | bool | float | vec2 | vec3 | vec4
        self._data_type = data_type
        self._data = data
        self._variable_ref = None
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data

    def locate_variable(self, program_ref, variable_name):
        """ Get and store reference for program variable with given name """
        if self._data_type == 'Light':
            self._variable_ref = {
                "lightType":    glGetUniformLocation(program_ref, variable_name + ".lightType"),
                "color":        glGetUniformLocation(program_ref, variable_name + ".color"),
                "direction":    glGetUniformLocation(program_ref, variable_name + ".direction"),
                "position":     glGetUniformLocation(program_ref, variable_name + ".position"),
                "attenuation":  glGetUniformLocation(program_ref, variable_name + ".attenuation"),
            }
        else:
            self._variable_ref = glGetUniformLocation(program_ref, variable_name)

    def upload(self):
        """ Store data in uniform variable previously located """
        if (self._variable_ref == -1):
            return
        
        if self._data_type == 'int':
            glUniform1i(self._variable_ref, self._data)
        elif self._data_type == 'bool':
            glUniform1i(self._variable_ref, self._data)
        elif self._data_type == 'float':
            glUniform1f(self._variable_ref, self._data)
        elif self._data_type == 'vec2':
            glUniform2f(self._variable_ref, *self._data)
        elif self._data_type == 'vec3':
            glUniform3f(self._variable_ref, *self._data)
        elif self._data_type == 'vec4':
            glUniform4f(self._variable_ref, *self._data)
        elif self._data_type == 'mat4':
            glUniformMatrix4fv(self._variable_ref, 1, GL_TRUE, self._data)
        elif self._data_type == "sampler2D":
            texture_object_ref, texture_unit_ref = self._data
            glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
            glBindTexture(GL_TEXTURE_2D, texture_object_ref)
            glUniform1i(self._variable_ref, texture_unit_ref)
        elif self._data_type == "Light":
            glUniform1i(self._variable_ref["lightType"], self._data.light_type)
            glUniform3f(self._variable_ref["color"], *self._data.color)
            glUniform3f(self._variable_ref["direction"], *self._data.direction)
            glUniform3f(self._variable_ref["position"], *self._data.local_position)
            glUniform3f(self._variable_ref["attenuation"], *self._data.attenuation)

class Attribute: 
    
    def __init__(self, data_type, data):
        # type of elements in data array: int | float | vec2 | vec3 | vec4
        self._data_type = data_type        
        self._data = data    
        self._buffer_ref = glGenBuffers(1)    
        self.upload()

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data

    def upload(self):
        """ Upload the data to a GPU buffer """
        # Convert data to numpy array format; convert numbers to 32-bit floats
        data = np.array(self._data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer_ref)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    
    def associate_variable(self, program_ref, variable_name):
        """ Associate variable in program with the buffer """
        variable_ref = glGetAttribLocation(program_ref, variable_name)
        
        if variable_ref != -1:
            glBindBuffer(GL_ARRAY_BUFFER, self._buffer_ref)

            if self._data_type == "int":
                glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
            elif self._data_type == "float":
                glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
            elif self._data_type == "vec2":
                glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
            elif self._data_type == "vec3":
                glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
            elif self._data_type == "vec4":
                glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
            else:
                raise Exception(f'Attribute {variable_name} has unknown type {self._data_type}')
            
            glEnableVertexAttribArray(variable_ref)