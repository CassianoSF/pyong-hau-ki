import math
from Object import Object
from Camera import Camera
from Loader import Loader

class Gui:
    def __init__(self, window_width, window_height):
        quad_loader  = Loader("./resources/models/quad.obj",  "./resources/textures/jogar.png")
        self.quad  = Object(quad_loader)
        self.quad.scale(5,5,5)
        self.quad.model['rotation'] = [0, math.pi/2, 0]
        self.camera = Camera(window_width, window_height)
        self.camera.view['position'] = [0.0, 15.0, 0.0]
        self.camera.update()
        self.menu = True

    def game_start(self):
        self.menu = False
        pass

    def render(self):
        if self.menu:
            self.quad.render(self.camera)
        