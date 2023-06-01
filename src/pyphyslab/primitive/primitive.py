import numpy as np
from pyphyslab.core.shader import Attribute

class Primitive:

    VERTEX_POSITION_ATTRIBUTE = "vertexPosition"
    VERTEX_NORMAL_ATTRIBUTE = "vertexNormal"
    VERTEX_COLOR_ATTRIBUTE = "vertexColor"
    FACE_NORMAL_ATTRIBUTE = "faceNormal"    

    def __init__(self):
        self.attribute_dict = {}
        self.vertex_count = None

    def add_attribute(self, data_type, variable_name, data):
        """ Adds attribute """
        attribute = Attribute(data_type, data)
        self.attribute_dict[variable_name] = attribute
        if variable_name == Primitive.VERTEX_POSITION_ATTRIBUTE:
            self.vertex_count = len(data)

    def apply_matrix(self, matrix):
        """ Transform the data in an attribute using a matrix """
        old_position_data = self.attribute_dict[Primitive.VERTEX_POSITION_ATTRIBUTE].data
        new_position_data = []
        for old_pos in old_position_data:
            new_pos = old_pos.copy()
            new_pos.append(1)
            new_pos = matrix @ new_pos
            new_pos = list(new_pos[0:3])
            new_position_data.append(new_pos)
        self.attribute_dict[Primitive.VERTEX_POSITION_ATTRIBUTE].data = new_position_data

        self.attribute_dict[Primitive.VERTEX_POSITION_ATTRIBUTE].upload()
        self._vertex_count = len(new_position_data)


        rotation_matrix = np.array(
            [matrix[0][0:3],
             matrix[1][0:3],
             matrix[2][0:3]]
        ).astype(float)

        old_vertex_normal_data = self.attribute_dict[Primitive.VERTEX_NORMAL_ATTRIBUTE].data
        new_vertex_normal_data = []
        
        for old_normal in old_vertex_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_vertex_normal_data.append(new_normal)

        self.attribute_dict[Primitive.VERTEX_NORMAL_ATTRIBUTE].data = new_vertex_normal_data
        self.attribute_dict[Primitive.VERTEX_NORMAL_ATTRIBUTE].upload()

        old_face_normal_data = self.attribute_dict[Primitive.FACE_NORMAL_ATTRIBUTE].data
        new_face_normal_data = []
        
        for old_normal in old_face_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_normal_data.append(new_normal)
        
        self.attribute_dict[Primitive.FACE_NORMAL_ATTRIBUTE].data = new_face_normal_data
        self.attribute_dict[Primitive.FACE_NORMAL_ATTRIBUTE].upload()