import pathlib
import sys

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from OpenGL.GL import *

from pyphyslab.core.window import Window
from pyphyslab.core.shader import Attribute, Uniform
import pyphyslab.core.shader as shader


class Example(Window):

    def initialize(self):
        print("Initializing program...")

        vertex_shader_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """

        fragment_shader_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
 
        self.program_ref = shader.initialize_program(vertex_shader_code, fragment_shader_code)

        glClearColor(0.0, 0.0, 0.0, 1.0)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vetex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, "translation")

        self.base_color = Uniform("vec3", [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, "baseColor")
    
    def update(self):        
        self.translation.data[0] += 0.01

        if self.translation.data[0] > 1.2:
            self.translation.data[0] = -1.2

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program_ref)

        self.translation.upload()
        self.base_color.upload()

        glDrawArrays(GL_TRIANGLES, 0, self.vetex_count)

Example().run()