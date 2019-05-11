import pygame, sys, os
import pprint
import importlib
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Text:
    def __init__(self, text):
        self.font = pygame.font.Font('./resources/fonts/calibrib.ttf', 50)
        self.text = text
        self.tex_id = glGenTextures(1)
        textsurface = self.font.render(self.text, False, (1, 1, 1, 1))
        tex = pygame.image.tostring(textsurface, 'RGBA')
        tex_width, tex_height = textsurface.get_size()
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex)
        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.tex_id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
