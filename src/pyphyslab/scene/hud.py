from pyphyslab.scene.camera import Camera
from pyphyslab.scene.scene import Scene
from pyphyslab.scene.texture import Texture, TextTexture
from pyphyslab.primitive.rectangle import RectanglePrimitive
from pyphyslab.scene.shape import Mesh
from pyphyslab.material.texture import TextureMaterial

class HeadsUpDisplay:
    """Class representing heads up display"""

    def __init__(self, screen_size=(800, 600)):
        self.hud_scene = Scene()
        self.hud_camera = Camera()
        self.hud_camera.set_orthographic(0, screen_size[0], 0, screen_size[1], 1, -1)

        coords_rectangle = RectanglePrimitive(
               width=0.45, height=0.4,
            position=[0, 0],
            alignment=[0, 1]
        )

        coords_texture = Texture(file_name="src/pyphyslab/images/coordinates.png")
        cooreds_texture_material = TextureMaterial(coords_texture)

        coords_image = Mesh(coords_rectangle, cooreds_texture_material)
        coords_image.translate(-2.2, 2.2, -4.0)
        self.hud_scene.add(coords_image)

        legend_text_width = 800
        legend_text_height = 400
        legend_z = -4.0

        self._add_text("Version 1.0", -2.2, 2.25, legend_z, legend_text_width, legend_text_height)

        legend_x = 0.7
        self._add_text("A - Left , D - Right, W - Forward, S - Backward", legend_x, 2.25, legend_z, legend_text_width, legend_text_height)
        self._add_text("R - Move Up , F - Move Down, Q - Rotate Left , E - Rotate Right", legend_x, 2.15,legend_z, legend_text_width, legend_text_height)        
        self._add_text("T - Look Up , G - Look Down", legend_x, 2.05, legend_z, legend_text_width, legend_text_height)
        self._add_text("Hold Mouse Left - Move , Hold Mouse Wheel - Rotate", legend_x, 1.95, legend_z, legend_text_width, legend_text_height, [255, 255, 255])
        self._add_text("SPACE - Activate experiment", legend_x, 1.85, legend_z, legend_text_width, legend_text_height, [255, 255, 0])

    def update(self, renderer):
        renderer.render(
            scene=self.hud_scene,
            camera=self.hud_camera,
            clear_color=False
        )

    def _add_text(self, text, x, y, z, width = 400, height = 400, font_color = [0, 255, 255]):
        
        text_rectangle = RectanglePrimitive(
               width=1.6, height=1.0,
            position=[0, 0],
            alignment=[0, 1]
        )

        text_texture = TextTexture(
            text = text,
            system_font_name = "Impact",
            font_size = 38,
            font_color = font_color,
            background_color = (0, 0, 0),
            image_width = width,
            image_height = height,
            transparent = True
        )

        text_texture_material = TextureMaterial(text_texture)
        text_mesh = Mesh(text_rectangle, text_texture_material)
        text_mesh.translate(x, y, z)
        self.hud_scene.add(text_mesh)