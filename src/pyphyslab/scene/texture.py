import pygame as pg
from OpenGL.GL import *

class Texture:

    def __init__(self, file_name=None, property_dict={}):

        self._surface = None
        self._texture_ref = glGenTextures(1)
        self._property_dict = {
            "magFilter": GL_LINEAR,
            "minFilter": GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL_REPEAT
        }

        self.set_properties(property_dict)
        if file_name is not None:
            self.load_image(file_name)
            self.upload_data()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def texture_ref(self):
        return self._texture_ref

    def load_image(self, file_name):
        """ Load image from file """
        self._surface = pg.image.load(file_name)

    def set_properties(self, property_dict):
        """ Set property values """
        if property_dict:
            for name, value in property_dict.items():
                if name in self._property_dict.keys():
                    self._property_dict[name] = value
                else:  
                    raise Exception("Texture has no property with name: " + name)

    def upload_data(self):
        """ Upload pixel data to GPU """

        width = self._surface.get_width()
        height = self._surface.get_height()

        pixel_data = pg.image.tostring(self._surface, "RGBA", True)

        glBindTexture(GL_TEXTURE_2D, self._texture_ref)
 
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)
   
        glGenerateMipmap(GL_TEXTURE_2D)
   
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self._property_dict["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self._property_dict["minFilter"])
      
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self._property_dict["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self._property_dict["wrap"])
     
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1, 1, 1, 1])

class TextTexture(Texture):
    """
    Define a text texture by using pygame
    """
    def __init__(self, text="Python graphics",
                 system_font_name="Arial",
                 font_file_name=None,
                 font_size=24,
                 font_color=(0, 0, 0),
                 background_color=(255, 255, 255),
                 transparent=False,
                 image_width=None,
                 image_height=None,
                 align_horizontal=0.0,
                 align_vertical=0.0,
                 image_border_width=0,
                 image_border_color=(0, 0, 0)):
        super().__init__()
 
        font = pg.font.SysFont(system_font_name, font_size)

        if font_file_name is not None:
            font = pg.font.Font(font_file_name, font_size)

        font_surface = font.render(text, True, font_color)
   
        (text_width, text_height) = font.size(text)

        if image_width is None:
            image_width = text_width
        if image_height is None:
            image_height = text_height

        self._surface = pg.Surface((image_width, image_height),
                                       pg.SRCALPHA)

        if not transparent:
            self._surface.fill(background_color)

        corner_point = (align_horizontal * (image_width - text_width),
                        align_vertical * (image_height - text_height))
        destination_rectangle = font_surface.get_rect(topleft=corner_point)

        if image_border_width > 0:
            pg.draw.rect(self._surface, image_border_color,
                             [0, 0, image_width, image_height], image_border_width)

        self._surface.blit(font_surface, destination_rectangle)
        self.upload_data()

