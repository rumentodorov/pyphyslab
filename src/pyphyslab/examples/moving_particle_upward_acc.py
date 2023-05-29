import pathlib
import sys
import math

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from pyphyslab.core.window import Window
from pyphyslab.scene.renderer import Renderer
from pyphyslab.scene.camera import Camera, MovementRig
from pyphyslab.scene.shpe import Mesh
from pyphyslab.scene.scene import Scene
from pyphyslab.scene.grid import Grid
from pyphyslab.primitive.ellipsoid import EllipsoidPrimitive
from pyphyslab.material.surface import SurfaceMaterial
from pyphyslab.physics.particle import Particle
from pyphyslab.physics.world import World

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


        self.sphere = Mesh(EllipsoidPrimitive(width=0.1, height=0.1, depth=0.1), SurfaceMaterial(property_dict={"baseColor": [1, 0.5, 0.0]}))
        self.sphere.translate(-0.6, 0.5, -4.0)
        self.scene.add(self.sphere)

        self.particle =  Particle(
            mass  = 10.0,  
            velocity = [0.0, 0.0, 0.0],
            acceleration=[0.0, 1.0, 0.0],
            damping = 0.60
        )
        
        self.particle.add_force([0.0,0.0,0.0])
        self.particle.position = [-0.6, 0.5, -4.0]

        grid = Grid(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.world = World.single_particle(self.particle)

    def update(self):        
        self.world.run_physics(self.delta_time)

        position = self.particle.position.tolist()           
        self.sphere.set_position(position)        

        self.rig.update(self.key_input, self.mouse_input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=(1024,768)).run()