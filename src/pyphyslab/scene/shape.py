import numpy as np
import pyphyslab.core.matrix as matrix
from OpenGL.GL import *

class Shape3d:
    """The base class of all shapes. Provides multiple gemotric transformation methods"""

    def __init__(self):
        self._matrix = matrix.make_identity()
        self._parent = None
        self._children_list = []

    def add(self, child):
        self._children_list.append(child)
        child._parent = self

    def remove(self, child):
        self._children_list.remove(child)
        child._parent = None

    @property
    def descendant_list(self):
        descendant_list = []
        nodes_to_process = [self]
        
        while len(nodes_to_process) > 0 :
            node = nodes_to_process.pop(0)
            descendant_list.append(node)
            nodes_to_process = node._children_list + nodes_to_process

        return descendant_list

    @property
    def global_matrix(self):
        if self._parent is None:
            return self._matrix
        else:
            return self._parent.global_matrix @ self._matrix
    
    def apply_matrix(self, matrix, local=True):
        if local:
            self._matrix = self._matrix @ matrix

    def translate(self, x, y, z, local = True):
        m = matrix.make_translation(x, y, z)
        self.apply_matrix(m, local)

    def rotate_x(self, angle, local=True):
        m = matrix.make_rotation_x(angle)
        self.apply_matrix(m, local)

    def rotate_y(self, angle, local=True):
        m = matrix.make_rotation_y(angle)
        self.apply_matrix(m, local)

    def rotate_z(self, angle, local=True):
        m = matrix.make_rotation_z(angle)
        self.apply_matrix(m, local)

    def scale(self, s, local = True):
        m = matrix.make_scale(s)
        self.apply_matrix(m, local)

    @property
    def global_position(self):
        return [self.global_matrix.item((0, 3)),
                self.global_matrix.item((1, 3)),
                self.global_matrix.item((2, 3))]
    
    @property
    def local_position(self):
        return [self._matrix.item((0, 3)),
                self._matrix.item((1, 3)),
                self._matrix.item((2, 3))]
    
    def set_position(self, position):
        self._matrix.itemset((0, 3), position[0])
        self._matrix.itemset((1, 3), position[1])
        self._matrix.itemset((2, 3), position[2])

    @property
    def rotation_matrix(self):
        return np.array(
            [self._matrix[0][0:3],
             self._matrix[1][0:3],
             self._matrix[2][0:3]]
        ).astype(float)
    
    @property
    def direction(self):
        forward = np.array([0, 0, -1]).astype(float)
        return list(self.rotation_matrix @ forward)
    
    def set_direction(self, direction):
        position = self.local_position
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2]
        ]
        self.look_at(target_position)

    def look_at(self, target_position):
        self._matrix = matrix.make_look_at(self.global_position, target_position)


class Mesh(Shape3d):

    def __init__(self, geometry, material):
        super().__init__()

        self.geometry = geometry
        self.material = material
        self.visible = True

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)

        for variable_name, attribute_object in geometry.attribute_dict.items():
            attribute_object.associate_variable(material.program_ref, variable_name)
        
        glBindVertexArray(0)

class Group(Shape3d):

    def __init__(self):
        super().__init__()