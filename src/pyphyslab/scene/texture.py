import pygame as pg
from OpenGL.GL import *

class Texture:

    def __init__(self, file_name=None, property_dict={}):
        # Pygame object for storing pixel data;
        # can load from image or manipulate directly
        self._surface = None
        # reference of available texture from GPU
        self._texture_ref = glGenTextures(1)
        # default property values
        self._property_dict = {
            "magFilter": GL_LINEAR,
            "minFilter": GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL_REPEAT
        }
        # Overwrite default property values
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
                else:  # unknown property type
                    raise Exception("Texture has no property with name: " + name)

    def upload_data(self):
        """ Upload pixel data to GPU """
        # Store image dimensions
        width = self._surface.get_width()
        height = self._surface.get_height()
        # Convert image data to string buffer
        pixel_data = pg.image.tostring(self._surface, "RGBA", True)
        # Specify texture used by the following functions
        glBindTexture(GL_TEXTURE_2D, self._texture_ref)
        # Send pixel data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)
        # Generate mipmap image from uploaded pixel data
        glGenerateMipmap(GL_TEXTURE_2D)
        # Specify technique for magnifying/minifying textures
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self._property_dict["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self._property_dict["minFilter"])
        # Specify what happens to texture coordinates outside range [0, 1]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self._property_dict["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self._property_dict["wrap"])
        # Set default border color to white; important for rendering shadows
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
        # Set a default font
        font = pg.font.SysFont(system_font_name, font_size)
        # The font can be overrided by loading font file
        if font_file_name is not None:
            font = pg.font.Font(font_file_name, font_size)
        # Render text to (antialiased) surface
        font_surface = font.render(text, True, font_color)
        # Determine size of rendered text for alignment purposes
        (text_width, text_height) = font.size(text)
        # If image dimensions are not specified,
        # use the font surface size as default
        if image_width is None:
            image_width = text_width
        if image_height is None:
            image_height = text_height
        # Create a surface to store the image of text
        # (with the transparency channel by default)
        self._surface = pg.Surface((image_width, image_height),
                                       pg.SRCALPHA)
        # Set a background color used when not transparent
        if not transparent:
            self._surface.fill(background_color)
        # Attributes align_horizontal, align_vertical define percentages,
        # measured from top-left corner
        corner_point = (align_horizontal * (image_width - text_width),
                        align_vertical * (image_height - text_height))
        destination_rectangle = font_surface.get_rect(topleft=corner_point)
        # Add border (optionally)
        if image_border_width > 0:
            pg.draw.rect(self._surface, image_border_color,
                             [0, 0, image_width, image_height], image_border_width)
        # Apply font_surface to a correct position on the final surface
        self._surface.blit(font_surface, destination_rectangle)
        self.upload_data()

