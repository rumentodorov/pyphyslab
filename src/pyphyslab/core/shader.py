from OpenGL.GL import *
import numpy as np

#Generic constants
UTF8_ENCODING = "utf-8"
GLSL_INT = "int"
GLSL_BOOL = "bool"
GLSL_FLOAT = "float"
GLSL_VECTOR2 = "vec2"
GLSL_VECTOR3 = "vec3"
GLSL_VECTOR4 = "vec4"
GLSL_MATRIX4 = "mat4"
GLSL_SAMPLER_2D = "sampler2D"
GLSL_CUSTOM_LIGHT_STRUCT = "Light"

def initialize_program(vertex_shader_code, fragment_shader_code):
    """ 
    Compiles the vertex and fragment shaders on the GPU and provides a program_ref for
    further access to the program runtume
        Parameters: 
            shader_code (string): The code of the shader program
            shader_type (C type): OpenGL C type mapping for a shader
        Returns:
            program_ref: Reference to shader program
    """
    vertex_shader_ref = _initialize_shader(vertex_shader_code, GL_VERTEX_SHADER)
    fragment_shader_ref = _initialize_shader(fragment_shader_code, GL_FRAGMENT_SHADER)

    program_ref = glCreateProgram()
 
    glAttachShader(program_ref, vertex_shader_ref)
    glAttachShader(program_ref, fragment_shader_ref)
    

    glLinkProgram(program_ref)
    link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)
    
    if not link_success:
        
        error_message = glGetProgramInfoLog(program_ref)            
        glDeleteProgram(program_ref)
        
        error_message = '\n' + error_message.decode(UTF8_ENCODING)        
        raise Exception(error_message)
        
    return program_ref

def _initialize_shader(shader_code, shader_type):
    """ 
    Internal helper function used to initialize a shader
        Parameters: 
            shader_code (string): The code of the shader program
            shader_type (C type): OpenGL C type mapping for a shader
    """
    shader_code = '#version 330\n' + shader_code
    shader_ref = glCreateShader(shader_type)
    glShaderSource(shader_ref, shader_code)
    glCompileShader(shader_ref)
    compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
    
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_ref)
        glDeleteShader(shader_ref)
        error_message = '\n' + error_message.decode(UTF8_ENCODING)
        raise Exception(error_message)
    return shader_ref

class Uniform:

    LIGHT_TYPE_PARAM = "lightType"
    COLOR_PARAM = "color"
    DIRECTION_PARAM = "direction"
    POSITION_PARAM = "position"
    ATTENUATION_PARAM = "attenuation"

    def __init__(self, data_type, data):
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
        if self._data_type == GLSL_CUSTOM_LIGHT_STRUCT:
            self._variable_ref = {
                Uniform.LIGHT_TYPE_PARAM :  glGetUniformLocation(program_ref, variable_name + f".{Uniform.LIGHT_TYPE_PARAM}"),
                Uniform.COLOR_PARAM:        glGetUniformLocation(program_ref, variable_name + f".{Uniform.COLOR_PARAM}"),
                Uniform.DIRECTION_PARAM:    glGetUniformLocation(program_ref, variable_name + f".{Uniform.DIRECTION_PARAM}"),
                Uniform.POSITION_PARAM:     glGetUniformLocation(program_ref, variable_name + f".{Uniform.POSITION_PARAM}"),
                Uniform.ATTENUATION_PARAM : glGetUniformLocation(program_ref, variable_name + f".{Uniform.ATTENUATION_PARAM}"),
            }
        else:
            self._variable_ref = glGetUniformLocation(program_ref, variable_name)

    def upload(self):
        """ Store data in uniform variable previously located """
        if (self._variable_ref == -1):
            return
        
        if self._data_type == GLSL_INT:
            glUniform1i(self._variable_ref, self._data)
        elif self._data_type == GLSL_BOOL:
            glUniform1i(self._variable_ref, self._data)
        elif self._data_type == GLSL_FLOAT:
            glUniform1f(self._variable_ref, self._data)
        elif self._data_type == GLSL_VECTOR2:
            glUniform2f(self._variable_ref, *self._data)
        elif self._data_type == GLSL_VECTOR3:
            glUniform3f(self._variable_ref, *self._data)
        elif self._data_type == GLSL_VECTOR4:
            glUniform4f(self._variable_ref, *self._data)
        elif self._data_type == GLSL_MATRIX4:
            glUniformMatrix4fv(self._variable_ref, 1, GL_TRUE, self._data)
        elif self._data_type == GLSL_SAMPLER_2D:
            texture_object_ref, texture_unit_ref = self._data
            glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
            glBindTexture(GL_TEXTURE_2D, texture_object_ref)
            glUniform1i(self._variable_ref, texture_unit_ref)
        elif self._data_type == GLSL_CUSTOM_LIGHT_STRUCT:
            glUniform1i(self._variable_ref[Uniform.LIGHT_TYPE_PARAM], self._data.light_type)
            glUniform3f(self._variable_ref[Uniform.COLOR_PARAM], *self._data.color)
            glUniform3f(self._variable_ref[Uniform.DIRECTION_PARAM], *self._data.direction)
            glUniform3f(self._variable_ref[Uniform.POSITION_PARAM], *self._data.local_position)
            glUniform3f(self._variable_ref[Uniform.ATTENUATION_PARAM], *self._data.attenuation)

class Attribute: 
    
    def __init__(self, data_type, data):        
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

            if self._data_type == GLSL_INT:
                glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
            elif self._data_type == GLSL_FLOAT:
                glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
            elif self._data_type == GLSL_VECTOR2:
                glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
            elif self._data_type == GLSL_VECTOR3:
                glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
            elif self._data_type == GLSL_VECTOR4:
                glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
            else:
                raise Exception(f'Attribute {variable_name} has unknown type {self._data_type}')
            
            glEnableVertexAttribArray(variable_ref)