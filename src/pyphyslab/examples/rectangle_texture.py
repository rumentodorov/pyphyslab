import pathlib
import sys
import math

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from pyphyslab.core.window import Window
from pyphyslab.scene.renderer import Renderer
from pyphyslab.scene.camera import Camera, MovementRig
from pyphyslab.scene.shape import Mesh
from pyphyslab.scene.scene import Scene
from pyphyslab.scene.grid import Grid
from pyphyslab.scene.texture import Texture

from pyphyslab.material.texture import TextureMaterial
from pyphyslab.primitive.rectangle import RectanglePrimitive

class Example(Window):
     
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1024/768)
        self.camera.set_position([0.0, 1.0, 0.0])
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.0, 0.0, 0.0])
        self.scene.add(self.rig)

        #self.camera.set_position([0, 4, 4])
        retangle = RectanglePrimitive()
        grid_texture = Texture(file_name="src/pyphyslab/images/grid.jpg")
        texture_material = TextureMaterial(texture=grid_texture)

        self.sphere = Mesh(retangle, texture_material)
        self.sphere.translate(-0.6, 2.0, -4.0)
        self.scene.add(self.sphere)

        grid = Grid(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

    def update(self):        
        self.rig.update(self.key_input, self.mouse_input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=(1024,768)).run()