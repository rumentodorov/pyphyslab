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

from pyphyslab.material.surface import SurfaceMaterial

from pyphyslab.physics.particle import Particle
from pyphyslab.physics.collision import ParticleCollisionDetector

class Example(Window):
     
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1024/768)
        self.camera.set_position([0.0, 1.0, -2.0])
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.0, 0.0, 0.0])
        self.scene.add(self.rig)    

        self.sphere1 = Mesh(EllipsoidPrimitive(width=0.1, height=0.1, depth=0.1), SurfaceMaterial(property_dict={"baseColor": [0, 1, 1]}))
        self.sphere1.set_position([0.6, 0.5, -4.0])
        self.scene.add(self.sphere1)


        self.sphere2 = Mesh(EllipsoidPrimitive(width=0.1, height=0.1, depth=0.1), SurfaceMaterial(property_dict={"baseColor": [1, 1, 0]}))
        self.sphere2.set_position([0.3, 0.5, -4.0])
        self.scene.add(self.sphere2)

        self.p1 =  Particle(
            mass  = 100.0,  
            velocity = [0.0, 0.0, 0.0],
            acceleration=[0.0, 0.0, 0.0],
            damping = 0.85
        )
        
        self.p1.position = [0.6, 0.5, -4.0]
        self.p1.add_force([0.0,0.0,0.0])
        
        self.p2 =  Particle(
            mass  = 0.5,  
            velocity = [0.0, 0.0, 0.0],
            acceleration=[0.0, 0.0, 0.0],
            damping = 0.85 
        )
        
        self.p2.position = [0.3, 0.5, -4.0]
        self.p2.add_force([20.0, 0.08, 3.8])

        grid = Grid(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)
        self._collision_detector = ParticleCollisionDetector()
        

    def update(self):
        if (self.rig.activated == True):
            resolver = self._collision_detector.detect(self.p1,self.p2)
            resolver.resolve(self.delta_time)

            self.p1.resolve(self.delta_time)
            self.p2.resolve(self.delta_time)

            position = self.p1.position.tolist() 
            self.sphere1.set_position(position)

            position = self.p2.position.tolist()     
            self.sphere2.set_position(position)

        self.rig.update(self.key_input, self.mouse_input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=(1024,768)).run()