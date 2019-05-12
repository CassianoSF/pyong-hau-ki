import math

from OpenGL.GL import *

from Core.Shader  import Shader
from Core.Texture import Texture
from Core.Text    import Text

from GuiObject import GuiObject
from Object    import Object
from Camera    import Camera
from Loader    import Loader


class Button:
    def __init__(self, caption, font_size, color, position):
        text = Text(caption, "calibrib",color[0], color[1], color[2])
        quad_obj  = Loader("./resources/models/quad.obj")
        shader = Shader("./resources/shaders/SimpleVertex.shader", "./resources/shaders/TransparencyFragment.shader")
        btn_texture = Texture("./resources/textures/button.png")
        self.text = GuiObject(quad_obj, shader, text)
        self.text.model['rotation'] = [0, math.pi/2, 0]
        self.text.scale(font_size*0.04*len(caption)/10, 1, font_size*0.1/10)
        self.text.translate(position[0], position[1], position[2])

        self.btn = GuiObject(quad_obj, shader, btn_texture)
        self.btn.model['rotation'] = [0, math.pi/2, 0]
        self.btn.scale(font_size*0.08*len(caption)/10, 1, font_size*0.2/10)
        self.btn.translate(position[0], position[1], position[2])

    def render(self, camera):
        self.text.render(camera)
        self.btn.render(camera)
        
class Gui:
    def __init__(self, window_width, window_height):
        quad_obj  = Loader("./resources/models/quad.obj")
        shader = Shader("./resources/shaders/SimpleVertex.shader", "./resources/shaders/TransparencyFragment.shader")
        jogar_texture = Texture("./resources/textures/jogar.png")

        self.start_menu  = GuiObject(quad_obj, shader, jogar_texture)
        self.start_menu.model['rotation'] = [0, math.pi/2, 0]

        self.btn_light_1_x_l = Button(" < ",    10, [0,0,0], [2.7, 0, -3.4])
        self.btn_light_1_x   = Button("123.1",  10, [0,0,0], [2.7, 0, -4.4])
        self.btn_light_1_x_r = Button(" > ",    10, [0,0,0], [2.7, 0, -5.4])
        self.btn_light_1_y_l = Button(" < ",    10, [0,0,0], [2.4, 0, -3.4])
        self.btn_light_1_y   = Button("13.1",   10, [0,0,0], [2.4, 0, -4.4])
        self.btn_light_1_y_r = Button(" > ",    10, [0,0,0], [2.4, 0, -5.4])
        self.btn_light_1_z_l = Button(" < ",    10, [0,0,0], [2.1, 0, -3.4])
        self.btn_light_1_z   = Button("-123.2", 10, [0,0,0], [2.1, 0, -4.4])
        self.btn_light_1_z_r = Button(" > ",    10, [0,0,0], [2.1, 0, -5.4])

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
        # transparency
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND)

        if self.menu:
            self.start_menu.render(self.camera)
            self.pump_menu()
        else:
            self.btn_light_1_x_r.render(self.camera)
            self.btn_light_1_x_l.render(self.camera)
            self.btn_light_1_x.render(self.camera)
            self.btn_light_1_y_r.render(self.camera)
            self.btn_light_1_y_l.render(self.camera)
            self.btn_light_1_y.render(self.camera)
            self.btn_light_1_z_r.render(self.camera)
            self.btn_light_1_z_l.render(self.camera)
            self.btn_light_1_z.render(self.camera)
        
        glDisable(GL_BLEND)