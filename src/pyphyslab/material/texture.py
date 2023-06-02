from OpenGL.GL import *
from pyphyslab.material.material import Material

class TextureMaterial(Material):

    TEXTURE_SAMPLER_UNIFORM = "textureSampler"
    TEXTURE_REPEAT_UV_UNIFORM = "repeatUV"
    TEXTURE_OFFSET_UV_UNIFORM = "offsetUV"

    def __init__(self, texture, property_dict=None):
        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            uniform vec2 repeatUV;
            uniform vec2 offsetUV;
            out vec2 UV;
            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV * repeatUV + offsetUV;
            }
        """

        fragment_shader_code = """
            uniform vec3 baseColor;
            uniform sampler2D textureSampler;
            in vec2 UV;
            out vec4 fragColor;
            void main()
            {
                vec4 color = vec4(baseColor, 1.0) * texture(textureSampler, UV);
                if (color.a < 0.1)
                    discard;                    
                fragColor = color;
            }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("sampler2D", TextureMaterial.TEXTURE_SAMPLER_UNIFORM, [texture.texture_ref, 1])
        self.add_uniform("vec2", TextureMaterial.TEXTURE_REPEAT_UV_UNIFORM, [1.0, 1.0])
        self.add_uniform("vec2", TextureMaterial.TEXTURE_OFFSET_UV_UNIFORM, [0.0, 0.0])
        self.locate_uniforms()
 
        self.setting_dict[Material.DOUBLE_SIDE_RENDER_SETTING] = True
        self.setting_dict[Material.WIREFRAME_RENDER_STTING] = False
        self.setting_dict[Material.LINE_WIDTH_RENDER_SETTING] = 1
        self.set_properties(property_dict)

    def update_render_settings(self):
        if self.setting_dict[Material.DOUBLE_SIDE_RENDER_SETTING]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        if self.setting_dict[Material.WIREFRAME_RENDER_STTING]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(self.setting_dict[Material.LINE_WIDTH_RENDER_SETTING])