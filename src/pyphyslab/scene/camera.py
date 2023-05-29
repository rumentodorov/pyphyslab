import math
from numpy.linalg import inv

import pyphyslab.core.matrix as matrix
from pyphyslab.scene.shpe import Shape3d

class Camera(Shape3d):

    def __init__(self, angle_of_view =  60, aspect_ratio = 1, near = 0.1, far = 1000):
        super().__init__()

        self.projection_matrix = matrix.make_perspective(angle_of_view, aspect_ratio, near, far)
        self.view_matrix = matrix.make_identity()

    def update_view_matrix(self):
        # Computers multiplicative inverse matrix - TODO Check details
        self.view_matrix = inv(self.global_matrix)

    def set_orthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self._projection_matrix = matrix.make_orthographic(left, right, bottom, top, near, far)
    

class MovementRig(Shape3d):
    """
    Add moving forwards and backwards, left and right, up and down (all local translations),
    as well as turning left and right, and looking up and down
    """
    def __init__(self, units_per_second=1, degrees_per_second=60):
        # Initialize base Object3D.
        # Controls movement and turn left/right.
        super().__init__()
        # Initialize attached Object3D; controls look up/down
        self._look_attachment = Shape3d()
        self.children_list = [self._look_attachment]
        self._look_attachment.parent = self
        # Control rate of movement
        self._units_per_second = units_per_second
        self._degrees_per_second = degrees_per_second
        self.activated = False

        # Customizable key mappings.
        # Defaults: W, A, S, D, R, F (move), Q, E (turn), T, G (look)
        self.KEY_MOVE_FORWARDS = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"
        self.KEY_MOVE_UP = "r"
        self.KEY_MOVE_DOWN = "f"
        self.KEY_TURN_LEFT = "q"
        self.KEY_TURN_RIGHT = "e"
        self.KEY_LOOK_UP = "t"
        self.KEY_LOOK_DOWN = "g"
        self.KEY_SPACE = "space"
        self.MOUSE_WEEL_UP = 1
        self.MOUSE_WEEL_DOWN = -1

    # Adding and removing objects applies to look attachment.
    # Override functions from the Object3D class.
    def add(self, child):
        self._look_attachment.add(child)

    def remove(self, child):
        self._look_attachment.remove(child)

    def update(self, key_input, mouse_input, delta_time):
        self._update_key_input(key_input, delta_time)
        self._update_mouse_input(mouse_input, delta_time)


    def _update_key_input(self, key_input, delta_time):
        move_amount = self._units_per_second * delta_time
        rotate_amount = self._degrees_per_second * (math.pi / 180) * delta_time
        if key_input.is_key_pressed(self.KEY_MOVE_FORWARDS):
            self._look_attachment.translate(0, 0, -move_amount)
        if key_input.is_key_pressed(self.KEY_MOVE_BACKWARDS):
            self._look_attachment.translate(0, 0, move_amount)
        if key_input.is_key_pressed(self.KEY_MOVE_LEFT):
            self._look_attachment.translate(-move_amount, 0, 0)
        if key_input.is_key_pressed(self.KEY_MOVE_RIGHT):
            self._look_attachment.translate(move_amount, 0, 0)
        if key_input.is_key_pressed(self.KEY_MOVE_UP):
            self._look_attachment.translate(0, move_amount, 0)
        if key_input.is_key_pressed(self.KEY_MOVE_DOWN):
            self._look_attachment.translate(0, -move_amount, 0)
        if key_input.is_key_pressed(self.KEY_TURN_RIGHT):
            self._look_attachment.rotate_y(-rotate_amount)
        if key_input.is_key_pressed(self.KEY_TURN_LEFT):
            self._look_attachment.rotate_y(rotate_amount)
        if key_input.is_key_pressed(self.KEY_LOOK_UP):
            self._look_attachment.rotate_x(rotate_amount)
        if key_input.is_key_pressed(self.KEY_LOOK_DOWN):
            self._look_attachment.rotate_x(-rotate_amount)
        if key_input.is_key_pressed(self.KEY_SPACE):
            self.activated = True

    def _update_mouse_input(self, mouse_input, delta_time):
        move_amount = self._units_per_second * delta_time * 2 
        rotate_amount = self._degrees_per_second * (math.pi / 180) * delta_time / 2
        
        if mouse_input.is_middle_drag():
            x,y = mouse_input.mouse_drag_rel()
            
            if x > 0:
                self._look_attachment.rotate_y(rotate_amount)
            if x < 0:
                self._look_attachment.rotate_y(-rotate_amount)
            
            if y > 0:
                self._look_attachment.rotate_x(rotate_amount)
            if y < 0:
                self._look_attachment.rotate_x(-rotate_amount)
        
        if mouse_input.is_left_drag():
            x,y = mouse_input.mouse_drag_rel()
            
            if x > 0:
                self._look_attachment.translate(move_amount, 0, 0)
            if x < 0:
                self._look_attachment.translate(-move_amount, 0, 0)

            if y > 0:
                self._look_attachment.translate(0, move_amount, 0)
            if y < 0:
                self._look_attachment.translate(0, -move_amount, 0)

        if mouse_input.is_mouse_wheel(self.MOUSE_WEEL_UP):
            self._look_attachment.translate(0, 0, -move_amount)
        
        if mouse_input.is_mouse_wheel(self.MOUSE_WEEL_DOWN):
            self._look_attachment.translate(0, 0, move_amount)
        
        mouse_input.reset_wheel()