import numpy as np
from pyphyslab.core.shader import Attribute

class Primitive:
    def __init__(self):
        self.attribute_dict = {}
        self.vertex_count = None

    def add_attribute(self, data_type, variable_name, data):
        attribute = Attribute(data_type, data)
        self.attribute_dict[variable_name] = attribute
        # Update the vertex count
        if variable_name == "vertexPosition":
            # Number of vertices may be calculated from
            # the length of any Attribute object's array of data
            self.vertex_count = len(data)

    def apply_matrix(self, matrix):
        """ Transform the data in an attribute using a matrix """
        old_position_data = self.attribute_dict["vertexPosition"].data
        new_position_data = []
        for old_pos in old_position_data:
            # Avoid changing list references
            new_pos = old_pos.copy()
            # Add the homogeneous fourth coordinate
            new_pos.append(1)
            # Multiply by matrix.
            # No need to transform new_pos to np.array.
            new_pos = matrix @ new_pos
            # Remove the homogeneous coordinate
            new_pos = list(new_pos[0:3])
            # Add to the new data list
            new_position_data.append(new_pos)
        self.attribute_dict["vertexPosition"].data = new_position_data
        # New data must be uploaded
        self.attribute_dict["vertexPosition"].upload()
        self._vertex_count = len(new_position_data)

        # Extract the rotation submatrix
        rotation_matrix = np.array(
            [matrix[0][0:3],
             matrix[1][0:3],
             matrix[2][0:3]]
        ).astype(float)

        old_vertex_normal_data = self.attribute_dict["vertexNormal"].data
        new_vertex_normal_data = []
        for old_normal in old_vertex_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_vertex_normal_data.append(new_normal)
        self.attribute_dict["vertexNormal"].data = new_vertex_normal_data
        # New data must be uploaded
        self.attribute_dict["vertexNormal"].upload()

        old_face_normal_data = self.attribute_dict["faceNormal"].data
        new_face_normal_data = []
        for old_normal in old_face_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_normal_data.append(new_normal)
        self.attribute_dict["faceNormal"].data = new_face_normal_data
        # New data must be uploaded
        self.attribute_dict["faceNormal"].upload()