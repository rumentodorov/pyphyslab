from OpenGL.GL import *
from pyphyslab.material.material import Material

_GLSL_LIGHT_TYPE_STRUCT = """
    struct Light
    {
        int lightType;  // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
        vec3 color;  // used by all lights
        vec3 direction; // used by directional lights
        vec3 position;  // used by point lights
        vec3 attenuation;  // used by all lights
    };
"""

_GLSL_CALC_LIGHT_FUNCTION = """
    vec3 calculateLight(Light light, vec3 pointPosition, vec3 pointNormal)
    {
        float ambient = 0;
        float diffuse = 0;
        float specular = 0;
        float attenuation = 1;
        vec3 lightDirection = vec3(0, 0, 0);
                
        if (light.lightType == 1)  // ambient light
        {
            ambient = 1;
        }
        else if (light.lightType == 2)  // directional light 
        {
            lightDirection = normalize(light.direction);
        }
        else if (light.lightType == 3)  // point light 
        {
            lightDirection = normalize(pointPosition - light.position);
            float distance = length(light.position - pointPosition);
            attenuation = 1.0 / (light.attenuation[0] 
                + light.attenuation[1] * distance 
                + light.attenuation[2] * distance * distance);
        }
                
        if (light.lightType > 1)  // directional or point light
        {
            pointNormal = normalize(pointNormal);
            diffuse = max(dot(pointNormal, -lightDirection), 0.0);
            diffuse *= attenuation;
        }
        
        return light.color * (ambient + diffuse + specular);
    }
""" 

class LightedMaterial(Material):
    
    def __init__(self, number_of_light_sources=1):
        self._number_of_light_sources = number_of_light_sources
        super().__init__(self.vertex_shader_code, self.fragment_shader_code)

        for i in range(self._number_of_light_sources):
            self.add_uniform("Light", f"light{i}", None)

    @property
    def declaring_light_uniforms_in_shader_code(self):
        """ Create a text line with light uniforms to be inserted into a shader code """
        return "\n" + "\n".join(f"\t\t\tuniform Light light{i};"
                                for i in range(self._number_of_light_sources)) + "\n"

    @property
    def adding_lights_in_shader_code(self):
        return "\n" + "\n".join(f"\t\t\t\tlight += calculateLight(light{i}, position, calcNormal);"
                                for i in range(self._number_of_light_sources))

    @property
    def vertex_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")

    @property
    def fragment_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")

class FlatMaterial(LightedMaterial):
    """
    Flat material with at least one light source (or more)
    """
    def __init__(self, property_dict=None, number_of_light_sources=1):
        super().__init__(number_of_light_sources)
        self.add_uniform("vec3", LightedMaterial.BASE_COLLOR_UNIFORM, [1.0, 1.0, 1.0])
        self.locate_uniforms()
        self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING] = True
        self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING] = False
        self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING] = 1
        self.set_properties(property_dict)

    @property
    def vertex_shader_code(self):
        return _GLSL_LIGHT_TYPE_STRUCT + self.declaring_light_uniforms_in_shader_code + _GLSL_CALC_LIGHT_FUNCTION + \
    """        
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec3 faceNormal;
            out vec3 light;
            
            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                vec3 position = vec3(modelMatrix * vec4(vertexPosition, 1));
                vec3 calcNormal = normalize(mat3(modelMatrix) * faceNormal);
                light = vec3(0, 0, 0);""" + self.adding_lights_in_shader_code + """
            }
        """

    @property
    def fragment_shader_code(self):
        return """
            uniform vec3 baseColor;
            uniform bool useTexture;
            uniform sampler2D textureSampler;
            in vec3 light;
            out vec4 fragColor;
            void main()
            {
                vec4 color = vec4(baseColor, 1.0);
                color *= vec4(light, 1);
                fragColor = color;
            }
        """

    def update_render_settings(self):
        if self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        if self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING])


class LambertMaterial(LightedMaterial):
    """
    Lambert material with at least one light source (or more)
    """
    def __init__(self,
                 texture=None,
                 property_dict=None,
                 number_of_light_sources=1,
                 bump_texture=None,
                 use_shadow=False):
        super().__init__(number_of_light_sources)
        self.add_uniform("vec3", LightedMaterial.BASE_COLLOR_UNIFORM, [1.0, 1.0, 1.0])
        self.locate_uniforms()

        # Render both sides?
        self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING] = True
        # Render triangles as wireframe?
        self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING] = False
        # Set line thickness for wireframe rendering
        self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING] = 1
        self.set_properties(property_dict)

    @property
    def vertex_shader_code(self):
        return """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec3 vertexNormal;
            out vec3 position;
            out vec3 normal;
        

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                position = vec3(modelMatrix * vec4(vertexPosition, 1));
                normal = normalize(mat3(modelMatrix) * vertexNormal);          
            }
        """

    @property
    def fragment_shader_code(self):
        return _GLSL_LIGHT_TYPE_STRUCT + "\n\n""" \
            + self.declaring_light_uniforms_in_shader_code + _GLSL_CALC_LIGHT_FUNCTION + \
        """
            uniform vec3 baseColor;
            in vec3 position;
            in vec3 normal;
            out vec4 fragColor;
            

            void main()
            {
                vec4 color = vec4(baseColor, 1.0);
                vec3 calcNormal = normal;
                // Calculate total effect of lights on color
                vec3 light = vec3(0, 0, 0);""" + self.adding_lights_in_shader_code + """
                color *= vec4(light, 1);              
                fragColor = color;
            }
        """

    def update_render_settings(self):
        if self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        if self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING])


class PhongMaterial(LightedMaterial):
    """
    Phong material with at least one light source (or more)
    """
    def __init__(self,
                 property_dict=None,
                 number_of_light_sources=1):
        super().__init__(number_of_light_sources)
        self.add_uniform("vec3", LightedMaterial.BASE_COLLOR_UNIFORM, [1.0, 1.0, 1.0])

        self.add_uniform("vec3", "viewPosition", [0, 0, 0])
        self.add_uniform("float", "specularStrength", 1.0)
        self.add_uniform("float", "shininess", 32.0)

        self.locate_uniforms()

        # Render both sides?
        self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING] = True
        self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING] = False
        self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING] = 1
        self.set_properties(property_dict)

    @property
    def vertex_shader_code(self):
        return """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec3 vertexNormal;
            out vec3 position;
            out vec3 normal;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                position = vec3(modelMatrix * vec4(vertexPosition, 1));
                normal = normalize(mat3(modelMatrix) * vertexNormal);
            }
        """

    @property
    def fragment_shader_code(self):
        return _GLSL_LIGHT_TYPE_STRUCT + """\n\n""" \
            + self.declaring_light_uniforms_in_shader_code + """
            uniform vec3 viewPosition;
            uniform float specularStrength;
            uniform float shininess;

            vec3 calculateLight(Light light, vec3 pointPosition, vec3 pointNormal)
            {
                float ambient = 0;
                float diffuse = 0;
                float specular = 0;
                float attenuation = 1;
                vec3 lightDirection = vec3(0, 0, 0);
                
                if (light.lightType == 1)  // ambient light
                {
                    ambient = 1;
                }
                else if (light.lightType == 2)  // directional light
                {
                    lightDirection = normalize(light.direction);
                }
                else if (light.lightType == 3)  // point light
                {
                    lightDirection = normalize(pointPosition - light.position);
                    float distance = length(light.position - pointPosition);
                    attenuation = 1.0 / (light.attenuation[0] 
                                       + light.attenuation[1] * distance 
                                       + light.attenuation[2] * distance * distance);
                }
                
                if (light.lightType > 1)  // directional or point light
                {
                    pointNormal = normalize(pointNormal);
                    diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                    diffuse *= attenuation;
                    if (diffuse > 0)
                    {
                        vec3 viewDirection = normalize(viewPosition - pointPosition);
                        vec3 reflectDirection = reflect(lightDirection, pointNormal);
                        specular = max(dot(viewDirection, reflectDirection), 0.0);
                        specular = specularStrength * pow(specular, shininess);
                    }
                }
                return light.color * (ambient + diffuse + specular);
            }

            uniform vec3 baseColor;
            in vec3 position;
            in vec3 normal;
            out vec4 fragColor;

            void main()
            {
                vec4 color = vec4(baseColor, 1.0);
                vec3 calcNormal = normal;
                vec3 light = vec3(0, 0, 0);""" + self.adding_lights_in_shader_code + """
                color *= vec4(light, 1);
                fragColor = color;
            }
        """

    def update_render_settings(self):
        if self.setting_dict[LightedMaterial.DOUBLE_SIDE_RENDER_SETTING]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        if self.setting_dict[LightedMaterial.WIREFRAME_RENDER_STTING]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.setting_dict[LightedMaterial.LINE_WIDTH_RENDER_SETTING])