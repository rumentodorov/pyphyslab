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

from pyphyslab.primitive.ellipsoid import EllipsoidPrimitive

from pyphyslab.scene.light import AmbientLight, DirectionalLight
from pyphyslab.material.lighted import PhongMaterial, LambertMaterial, FlatMaterial

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

        ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(ambient_light)
        self.directional_light = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, 0])
        self.scene.add(self.directional_light)

        pm1 = PhongMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=2
        )

        fm1 = FlatMaterial(
            property_dict={"baseColor": [0.1, 0.3, 0.0]},
            number_of_light_sources=2
        )

        lmb1 = LambertMaterial(
            property_dict={"baseColor": [0.2, 0.3, 0.5]},
            number_of_light_sources=2
        )

        ellipse = EllipsoidPrimitive(width=0.5, height=0.5, depth=0.5)
        
        sphere1 = Mesh(ellipse, pm1)
        sphere1.set_position([0.0, 2.0, -4.0])
        self.scene.add(sphere1)

        sphere2 = Mesh(ellipse, lmb1)
        sphere2.set_position([-2.0, 2.0, -4.0])
        self.scene.add(sphere2)

        sphere3 = Mesh(ellipse, fm1)
        sphere3.set_position([-2.0, 2.2, -5.0])
        self.scene.add(sphere3)

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