import math

from Core.Shader import Shader
from Core.Texture import Texture

from Object import Object
from Camera import Camera
from Loader import Loader

class Gui:
    def __init__(self, window_width, window_height):
        quad_obj  = Loader("./resources/models/quad.obj")
        shader = Shader("./resources/shaders/VertexShader.shader", "./resources/shaders/FragmentShader.shader")
        jogar_texture = Texture("./resources/textures/jogar.png")
        btn_texture = Texture("./resources/textures/btn_right.png")

        self.start_menu  = Object(quad_obj, shader, jogar_texture)
        self.start_menu.model['rotation'] = [0, math.pi/2, 0]

        self.btn_light_1_x_r = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_x_r.model['rotation'] = [0, math.pi/2, 0]
        self.btn_light_1_x_r.scale(0.15, 1, 0.1)
        self.btn_light_1_x_r.translate(2.7, 0, -5.6)

        self.btn_light_1_x_l = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_x_l.model['rotation'] = [0, 3*math.pi/2, 0]
        self.btn_light_1_x_l.scale(0.15, 1, 0.1)
        self.btn_light_1_x_l.translate(2.7, 0, -5.2)

        self.btn_light_1_y_r = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_y_r.model['rotation'] = [0, math.pi/2, 0]
        self.btn_light_1_y_r.scale(0.15, 1, 0.1)
        self.btn_light_1_y_r.translate(2.4, 0, -5.6)

        self.btn_light_1_y_l = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_y_l.model['rotation'] = [0, 3*math.pi/2, 0]
        self.btn_light_1_y_l.scale(0.15, 1, 0.1)
        self.btn_light_1_y_l.translate(2.4, 0, -5.2)

        self.btn_light_1_z_r = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_z_r.model['rotation'] = [0, math.pi/2, 0]
        self.btn_light_1_z_r.scale(0.15, 1, 0.1)
        self.btn_light_1_z_r.translate(2.1, 0, -5.6)

        self.btn_light_1_z_l = Object(quad_obj, shader, btn_texture)
        self.btn_light_1_z_l.model['rotation'] = [0, 3*math.pi/2, 0]
        self.btn_light_1_z_l.scale(0.15, 1, 0.1)
        self.btn_light_1_z_l.translate(2.1, 0, -5.2)

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
            self.btn_light_1_x_r.render(self.camera)
            self.btn_light_1_x_l.render(self.camera)
            self.btn_light_1_y_r.render(self.camera)
            self.btn_light_1_y_l.render(self.camera)
            self.btn_light_1_z_r.render(self.camera)
            self.btn_light_1_z_l.render(self.camera)