from OpenGL.GL import *
import pygame as pg

from pyphyslab.scene.shape import Mesh
from pyphyslab.scene.light import Light
from pyphyslab.material.material import Material

class Renderer:

    VIEW_POSTION_RENDER_UNIFORM = "viewPosition"
    
    def __init__(self, clear_color=(0, 0, 0)):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(*clear_color, 1)

        self.window_size = pg.display.get_surface().get_size()

    def render(self, scene, camera, clear_color=True, clear_depth=True):
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

            if not mesh.visible:
                continue
            glUseProgram(mesh.material.program_ref)

            glBindVertexArray(mesh.vao_ref)

            
            mesh.material.uniform_dict[Material.MODEL_MATRIX_UNIFORM].data = mesh.global_matrix
            mesh.material.uniform_dict[Material.VIEW_MATRIX_UNIFORM].data = camera.view_matrix
            mesh.material.uniform_dict[Material.PROJECTION_MATRIX_UNIFORM].data = camera.projection_matrix

            if "light0" in mesh.material.uniform_dict.keys():
                for light_number in range(len(light_list)):
                    light_name = "light" + str(light_number)
                    light_instance = light_list[light_number]
                    mesh.material.uniform_dict[light_name].data = light_instance

            if Renderer.VIEW_POSTION_RENDER_UNIFORM in mesh.material.uniform_dict.keys():
                mesh.material.uniform_dict[Renderer.VIEW_POSTION_RENDER_UNIFORM].data = camera.global_position

            for uniform_object in mesh.material.uniform_dict.values():
                uniform_object.upload()

            mesh.material.update_render_settings()
            glDrawArrays(mesh.material.setting_dict[Material.DRAWING_STYLE_RENDER_SETTING], 0, mesh.geometry.vertex_count)