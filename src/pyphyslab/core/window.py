import pygame as pg
import sys

from pyphyslab.core.input import KeyboardInput, MouseInput

class Window:
    
    def __init__(self, screen_size=(800, 600)):
        pg.init()

        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_caption("Graphics Window")
        
        display_flags = pg.DOUBLEBUF | pg.OPENGL
        self._screen = pg.display.set_mode(screen_size, display_flags)
        self._running = True
        self._clock = pg.time.Clock()

        self.key_input = KeyboardInput()
        self.mouse_input = MouseInput()

        self.time = 0

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        self.initialize()

        while self._running:

            for event in pg.event.get():
                self.mouse_input.update(event)
                self.key_input.update(event)
            
            if self.key_input.quit:
                self._running = False

            self.delta_time = self._clock.get_time() / 1000            
            self.time += self.delta_time

            self.update()

            pg.display.flip()
            
            self._clock.tick(60)
        
        pg.quit()
        sys.exit()