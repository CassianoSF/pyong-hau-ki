import math

from Core.Shader import Shader
from Core.Texture import Texture

from Object import Object
from Camera import Camera
from Loader import Loader

class Gui:
    def __init__(self, window_width, window_height):
        start_menu_obj  = Loader("./resources/models/quad.obj")

        shader = Shader("./resources/shaders/VertexShader.shader", "./resources/shaders/FragmentShader.shader")
        blue_texture = Texture("./resources/textures/jogar.png")

        self.start_menu  = Object(start_menu_obj, shader, blue_texture)
        self.start_menu.model['rotation'] = [0, math.pi/2, 0]
        
        self.camera = Camera(window_width, window_height)
        self.camera.view['position'] = [0.0, 1.0, 0.0]
        self.camera.orthogonal = True
        self.camera.update()
        self.resize = 0
        self.menu = True

    def game_start(self):
        self.menu = False

    def pump_menu(self):
        if self.start_menu.model['scale'][0] > 1.5:
            self.resize = -0.01
        if self.start_menu.model['scale'][0] <= 1:
            self.resize = 0.01
        self.start_menu.model['scale'] = [
            self.start_menu.model['scale'][0]+self.resize,
            self.start_menu.model['scale'][1]+self.resize,
            self.start_menu.model['scale'][2]+self.resize
        ]

    def render(self):
        if self.menu:
            self.start_menu.render(self.camera)
            self.pump_menu()
        else:
            pass