import math, pygame

from OpenGL.GL import *

from Core.Texture import Texture
from Core.Font    import Font

from Object    import Object
from Camera    import Camera
from Loader    import Loader


class Button:
    def __init__(self, caption, font_size, color, position, camera):
        self.color = color
        self.font_size = font_size
        self.position = position
        text = Font(caption, "calibrib",color[0], color[1], color[2])
        quad_obj  = Loader("./resources/models/quad.obj")
        btn_texture = Texture("./resources/textures/button.png")
        self.text = Object(quad_obj, camera, text)
        self.text.model['rotation'] = [0, math.pi/2, 0]
        self.text.scale(self.font_size*0.04*len(caption)/10, 1, self.font_size*0.1/10)
        self.text.translate(self.position[0], self.position[1], self.position[2])

        self.btn = Object(quad_obj, camera, btn_texture)
        self.btn.model['rotation'] = [0, math.pi/2, 0]
        self.btn.scale(self.font_size*0.1*len(caption)/10, 1, self.font_size*0.2/10)
        self.btn.translate(self.position[0], self.position[1], self.position[2])

    def set_caption(self, caption):
        text = Font(caption, "calibrib", self.color[0], self.color[1], self.color[2])
        self.text.scale(self.font_size*0.04*len(caption)/10, 1, self.font_size*0.1/10)
        self.btn.scale(self.font_size*0.1*len(caption)/10, 1, self.font_size*0.2/10)
        self.text.texture.delete
        self.text.texture = text

    def render(self, renderer):
        renderer.render_with_transparency(self.text)
        renderer.render_with_transparency(self.btn)

class Label:
    def __init__(self, caption, font, size, color):
        quad_obj  = Loader("./resources/models/quad.obj")
        self.font = Font(caption, font, color[0], color[1], color[2])
        self.quad = Object(quad_obj, self.camera, self.font)
        self.quad.model['rotation'] = [0, math.pi/2, 0]
        self.quad.scale(size*0.04*len(caption)/10, 1, size*0.1/10)

    def render(renderer):
        renderer.render_with_transparency(self.start_menu)

        
class Gui:
    def __init__(self, window_width, window_height, app):
        self.app = app

        self.camera = Camera(window_width, window_height)
        self.camera.view['position'] = [0.0, 1.0, 0.0]
        self.camera.orthogonal = True
        self.camera.update()

        self.resize = 0
        self.menu = True

        text = "Press  Enter  to  Play"
        quad_obj  = Loader("./resources/models/quad.obj")
        press_to_play = Font(text, "boston_traffic", 1, 1, 1)
        self.start_menu  = Object(quad_obj, self.camera, press_to_play)
        self.start_menu.model['rotation'] = [0, math.pi/2, 0]
        self.start_menu.scale(35*0.04*len(text)/10, 1, 35*0.1/10)


        lx = str(app.lights[0].position[0])
        ly = str(app.lights[0].position[1])
        lz = str(app.lights[0].position[2])

        self.btn_light_1_x_l = Button(" < ",    10, [0,0,0], [2.7, 0, -3.4], self.camera)
        self.btn_light_1_x   = Button(lx,  10, [0,0,0], [2.7, 0, -4.4], self.camera)
        self.btn_light_1_x_r = Button(" > ",    10, [0,0,0], [2.7, 0, -5.4], self.camera)
        self.btn_light_1_y_l = Button(" < ",    10, [0,0,0], [2.4, 0, -3.4], self.camera)
        self.btn_light_1_y   = Button(ly,   10, [0,0,0], [2.4, 0, -4.4], self.camera)
        self.btn_light_1_y_r = Button(" > ",    10, [0,0,0], [2.4, 0, -5.4], self.camera)
        self.btn_light_1_z_l = Button(" < ",    10, [0,0,0], [2.1, 0, -3.4], self.camera)
        self.btn_light_1_z   = Button(lz, 10, [0,0,0], [2.1, 0, -4.4], self.camera)
        self.btn_light_1_z_r = Button(" > ",    10, [0,0,0], [2.1, 0, -5.4], self.camera)

        self.btn_light_1_x_r_down = False
        self.btn_light_1_y_r_down = False
        self.btn_light_1_z_r_down = False
        self.btn_light_1_x_l_down = False
        self.btn_light_1_y_l_down = False
        self.btn_light_1_z_l_down = False

    def game_start(self):
        self.menu = False

    def pump_menu(self):
        if self.start_menu.model['scale'][0] > 3:
            self.resize = -0.003
        if self.start_menu.model['scale'][0] <= 2.5:
            self.resize = 0.003
        self.start_menu.model['scale'] = [
            self.start_menu.model['scale'][0]+self.resize*7,
            self.start_menu.model['scale'][1],
            self.start_menu.model['scale'][2]+self.resize
        ]

    def handle_event(self, event):
        if(event.type == pygame.MOUSEMOTION):
            pos_x = 6*(event.pos[0]/self.app.window_width*2 -1)
            pos_y = 3*(-(event.pos[1]/self.app.window_height*2 -1))

        # COISA LINDA
        if(event.type == pygame.MOUSEBUTTONDOWN):
            pos_x = 6*(event.pos[0]/self.app.window_width*2 -1)
            pos_y = 3*(-(event.pos[1]/self.app.window_height*2 -1))
            if self.btn_light_1_x_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_x_r.position[0]+0.15 and self.btn_light_1_x_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_x_r.position[2]+0.4:
                self.btn_light_1_x_r_down = True

            if self.btn_light_1_y_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_y_r.position[0]+0.15 and self.btn_light_1_y_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_y_r.position[2]+0.4:
                self.btn_light_1_y_r_down = True

            if self.btn_light_1_z_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_z_r.position[0]+0.15 and self.btn_light_1_z_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_z_r.position[2]+0.4:
                self.btn_light_1_z_r_down = True


            if self.btn_light_1_x_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_x_l.position[0]+0.15 and self.btn_light_1_x_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_x_l.position[2]+0.4:
                self.btn_light_1_x_l_down = True

            if self.btn_light_1_y_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_y_l.position[0]+0.15 and self.btn_light_1_y_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_y_l.position[2]+0.4:
                self.btn_light_1_y_l_down = True

            if self.btn_light_1_z_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_z_l.position[0]+0.15 and self.btn_light_1_z_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_z_l.position[2]+0.4:
                self.btn_light_1_z_l_down = True

        if(event.type == pygame.MOUSEBUTTONUP):
            pos_x = 6*(event.pos[0]/self.app.window_width*2 -1)
            pos_y = 3*(-(event.pos[1]/self.app.window_height*2 -1))
            if self.btn_light_1_x_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_x_r.position[0]+0.15 and self.btn_light_1_x_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_x_r.position[2]+0.4:
                self.btn_light_1_x_r_down = False

            if self.btn_light_1_y_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_y_r.position[0]+0.15 and self.btn_light_1_y_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_y_r.position[2]+0.4:
                self.btn_light_1_y_r_down = False

            if self.btn_light_1_z_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_z_r.position[0]+0.15 and self.btn_light_1_z_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_z_r.position[2]+0.4:
                self.btn_light_1_z_r_down = False


            if self.btn_light_1_x_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_x_l.position[0]+0.15 and self.btn_light_1_x_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_x_l.position[2]+0.4:
                self.btn_light_1_x_l_down = False

            if self.btn_light_1_y_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_y_l.position[0]+0.15 and self.btn_light_1_y_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_y_l.position[2]+0.4:
                self.btn_light_1_y_l_down = False

            if self.btn_light_1_z_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_z_l.position[0]+0.15 and self.btn_light_1_z_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_z_l.position[2]+0.4:
                self.btn_light_1_z_l_down = False


    def update_lights(self):
        if self.btn_light_1_x_r_down:
            self.btn_light_1_x.set_caption(str(round(self.app.lights[0].position[0], 2)))
            self.app.lights[0].position[0] += 0.1
            self.app.lights[0].sphere.model['translation'][0] += 0.1

        if self.btn_light_1_y_r_down:
            self.btn_light_1_y.set_caption(str(round(self.app.lights[0].position[1], 2)))
            self.app.lights[0].position[1] += 0.1
            self.app.lights[0].sphere.model['translation'][1] += 0.1

        if self.btn_light_1_z_r_down:
            self.btn_light_1_z.set_caption(str(round(self.app.lights[0].position[2], 2)))
            self.app.lights[0].position[2] += 0.1
            self.app.lights[0].sphere.model['translation'][2] += 0.1

        if self.btn_light_1_x_l_down:
            self.btn_light_1_x.set_caption(str(round(self.app.lights[0].position[0], 2)))
            self.app.lights[0].position[0] += -0.1
            self.app.lights[0].sphere.model['translation'][0] += -0.1

        if self.btn_light_1_y_l_down:
            self.btn_light_1_y.set_caption(str(round(self.app.lights[0].position[1], 2)))
            self.app.lights[0].position[1] += -0.1
            self.app.lights[0].sphere.model['translation'][1] += -0.1

        if self.btn_light_1_z_l_down:
            self.btn_light_1_z.set_caption(str(round(self.app.lights[0].position[2], 2)))
            self.app.lights[0].position[2] += -0.1
            self.app.lights[0].sphere.model['translation'][2] += -0.1



    def render(self, renderer):
        self.update_lights()
        if self.menu:
            renderer.render_with_transparency(self.start_menu)
            self.pump_menu()
        else:
            self.btn_light_1_x_l.render(renderer)
            self.btn_light_1_x.render(renderer)
            self.btn_light_1_x_r.render(renderer)
            self.btn_light_1_y_l.render(renderer)
            self.btn_light_1_y.render(renderer)
            self.btn_light_1_y_r.render(renderer)
            self.btn_light_1_z_l.render(renderer)
            self.btn_light_1_z.render(renderer)
            self.btn_light_1_z_r.render(renderer)