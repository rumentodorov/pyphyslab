import math

import pyphyslab.core.matrix as matrix
from pyphyslab.primitive.parametric import ParametricPrimitive

class EllipsoidPrimitive(ParametricPrimitive):
    def __init__(self, width=1, height=1, depth=1, theta_segments=16, phi_segments=32):
        def surface_function(u, v):
            phi = 2 * math.pi * u
            theta = (1 - v) * math.pi
            return [width / 2 * math.sin(theta) * math.cos(phi),
                    height / 2 * math.sin(theta) * math.sin(phi),
                    depth / 2 * math.cos(theta)]

        super().__init__(u_start=0,
                         u_end=1,
                         u_resolution=phi_segments,
                         v_start=0,
                         v_end=1,
                         v_resolution=theta_segments,
                         surface_function=surface_function)
        self.apply_matrix(matrix.make_rotation_x(-math.pi/2))