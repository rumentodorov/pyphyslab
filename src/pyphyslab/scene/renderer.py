from OpenGL.GL import *
import pygame as pg

from pyphyslab.scene.shpe import Mesh
from pyphyslab.scene.light import Light


class Renderer:
    
    def __init__(self, clear_color=(0, 0, 0)):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(*clear_color, 1)

        self.window_size = pg.display.get_surface().get_size()

    def render(self, scene, camera, clear_color=True, clear_depth=True, render_target=None):
        descendant_list = scene.descendant_list
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        if clear_color:
            glClear(GL_COLOR_BUFFER_BIT)
        if clear_depth:
            glClear(GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        camera.update_view_matrix()

        descendant_list = scene.descendant_list
        mesh_list = list(filter(lambda x: isinstance(x, Mesh), descendant_list))
        light_list = list(filter(lambda x: isinstance(x, Light), descendant_list))

        for mesh in mesh_list:
            # If this object is not visible, continue to next object in list
            if not mesh.visible:
                continue
            glUseProgram(mesh.material.program_ref)
            # Bind VAO
            glBindVertexArray(mesh.vao_ref)
            # Update uniform values stored outside of material
            mesh.material.uniform_dict["modelMatrix"].data = mesh.global_matrix
            mesh.material.uniform_dict["viewMatrix"].data = camera.view_matrix
            mesh.material.uniform_dict["projectionMatrix"].data = camera.projection_matrix

            if "light0" in mesh.material.uniform_dict.keys():
                for light_number in range(len(light_list)):
                    light_name = "light" + str(light_number)
                    light_instance = light_list[light_number]
                    mesh.material.uniform_dict[light_name].data = light_instance
            # Add camera position if needed (specular lighting)
            if "viewPosition" in mesh.material.uniform_dict.keys():
                mesh.material.uniform_dict["viewPosition"].data = camera.global_position

            for uniform_object in mesh.material.uniform_dict.values():
                uniform_object.upload()

            mesh.material.update_render_settings()
            glDrawArrays(mesh.material.setting_dict["drawStyle"], 0, mesh.geometry.vertex_count)