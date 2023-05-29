import pygame as pg

class MouseInput:
    
    def __init__(self):
        self._left_drag = False
        self._middle_drag = False
        self._mouse_drag_rel = (0,0)        
        self._wheel_pos = 0 

    def is_left_drag(self):
        return self._left_drag
    
    def is_middle_drag(self):
        return self._middle_drag

    def mouse_drag_rel(self):
        return self._mouse_drag_rel
    
    def is_mouse_wheel(self, direction):      
        return direction == self._wheel_pos
    
    def reset_wheel(self):
        self._wheel_pos = 0
    
    def update(self, event):   
        if event.type == pg.MOUSEBUTTONDOWN:
            left, middle, _ = pg.mouse.get_pressed()            
            if left == True:
                self._left_drag = True
            else:
                self._left_drag = False

            if middle == True:
                self._middle_drag = True
            else:
                self._middle_drag = False

        if event.type == pg.MOUSEBUTTONUP:   
            self._left_drag = False
            self._middle_drag = False
            self._wheel_pos = 0
        if event.type == pg.MOUSEMOTION and (self._left_drag or self._middle_drag):
            self._mouse_drag_rel = pg.mouse.get_rel()
        if event.type == pg.MOUSEWHEEL:        
            self._wheel_pos = event.y

class KeyboardInput:

    def __init__(self):
        self.quit = False
        self._key_down_list = []
        self._key_pressed_list = []
        self._key_up_list = []
      
    
    def is_key_down(self, key_code):
        return key_code in self._key_down_list

    def is_key_pressed(self, key_code):
        return key_code in self._key_pressed_list

    def is_key_up(self, key_code):
        return key_code in self._key_up_list

    def update(self, event):

        self._key_down_list = []
        self._key_up_list = []

        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            key_name = pg.key.name(event.key)
            self._key_down_list.append(key_name)
            self._key_pressed_list.append(key_name)
        if event.type == pg.KEYUP:
            key_name = pg.key.name(event.key)
            self._key_pressed_list.remove(key_name)
            self._key_up_list.append(key_name) 
