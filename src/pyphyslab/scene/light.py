from pyphyslab.scene.shape import Shape3d

class Light(Shape3d):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, light_type=0):
        super().__init__()
        self.light_type = light_type
        self.color = [1, 1, 1]
        self.attenuation = [1, 0, 0]
    
class AmbientLight(Light):
    def __init__(self, color=(1, 1, 1)):
        super().__init__(Light.AMBIENT)
        self._color = color

class DirectionalLight(Light):
    def __init__(self, color=(1, 1, 1), direction=(0, -1, 0)):
        super().__init__(Light.DIRECTIONAL)
        self._color = color
        self.set_direction(direction)

class PointLight(Light):
    def __init__(self,
                 color=(1, 1, 1),
                 position=(0, 0, 0),
                 attenuation=(1, 0, 0.1)
                 ):
        super().__init__(Light.POINT)
        self._color = color
        self._attenuation = attenuation
        self.set_position(position)