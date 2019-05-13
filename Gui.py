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
    def __init__(self, caption, font, size, color, position, camera):
        quad_obj  = Loader("./resources/models/quad.obj")
        self.font = Font(caption, font, color[0], color[1], color[2])
        self.quad = Object(quad_obj, camera, self.font)
        self.quad.model['rotation'] = [0, math.pi/2, 0]
        self.quad.translate(*position)
        self.quad.scale(size*0.04*len(caption)/10, 1, size*0.1/10)

    def render(self, renderer):
        renderer.render_with_transparency(self.quad)

        
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

        self.start_menu  = Label("Press enter to play", "kashima", 30,  [1,1,1], [0,0,0],    self.camera)
        self.logo        = Label("Pong Hau Ki",         "kashima", 100, [1,1,1], [-1.5,0,0], self.camera)


        lx = str(round(app.lights[0].position[0], 2))
        ly = str(round(app.lights[0].position[1], 2))
        lz = str(round(app.lights[0].position[2], 2))

        lr = str(round(app.lights[0].color[0]*255, 2))
        lg = str(round(app.lights[0].color[1]*255, 2))
        lb = str(round(app.lights[0].color[2]*255, 2))

        self.btn_light_1_x_l = Button(" < ",     10, [0,0,0], [2.7, 0, -3.4], self.camera)
        self.btn_light_1_x   = Button(lx,        10, [0,0,0], [2.7, 0, -4.4], self.camera)
        self.btn_light_1_x_r = Button(" > ",     10, [0,0,0], [2.7, 0, -5.4], self.camera)
        self.btn_light_1_y_l = Button(" < ",     10, [0,0,0], [2.4, 0, -3.4], self.camera)
        self.btn_light_1_y   = Button(ly,        10, [0,0,0], [2.4, 0, -4.4], self.camera)
        self.btn_light_1_y_r = Button(" > ",     10, [0,0,0], [2.4, 0, -5.4], self.camera)
        self.btn_light_1_z_l = Button(" < ",     10, [0,0,0], [2.1, 0, -3.4], self.camera)
        self.btn_light_1_z   = Button(lz,        10, [0,0,0], [2.1, 0, -4.4], self.camera)
        self.btn_light_1_z_r = Button(" > ",     10, [0,0,0], [2.1, 0, -5.4], self.camera)

        self.btn_light_1_x_r_down = False
        self.btn_light_1_y_r_down = False
        self.btn_light_1_z_r_down = False
        self.btn_light_1_x_l_down = False
        self.btn_light_1_y_l_down = False
        self.btn_light_1_z_l_down = False

        self.btn_light_1_r_l = Button(" < ",     10, [0,0,0], [2.7-2, 0, -3.4], self.camera)
        self.btn_light_1_r   = Button(lr,        10, [0,0,0], [2.7-2, 0, -4.4], self.camera)
        self.btn_light_1_r_r = Button(" > ",     10, [0,0,0], [2.7-2, 0, -5.4], self.camera)
        self.btn_light_1_g_l = Button(" < ",     10, [0,0,0], [2.4-2, 0, -3.4], self.camera)
        self.btn_light_1_g   = Button(lg,        10, [0,0,0], [2.4-2, 0, -4.4], self.camera)
        self.btn_light_1_g_r = Button(" > ",     10, [0,0,0], [2.4-2, 0, -5.4], self.camera)
        self.btn_light_1_b_l = Button(" < ",     10, [0,0,0], [2.1-2, 0, -3.4], self.camera)
        self.btn_light_1_b   = Button(lb,        10, [0,0,0], [2.1-2, 0, -4.4], self.camera)
        self.btn_light_1_b_r = Button(" > ",     10, [0,0,0], [2.1-2, 0, -5.4], self.camera)

        self.btn_light_1_r_l_down = False
        self.btn_light_1_r_r_down = False
        self.btn_light_1_g_l_down = False
        self.btn_light_1_g_r_down = False
        self.btn_light_1_b_l_down = False
        self.btn_light_1_b_r_down = False


    def game_start(self):
        self.menu = False

    def pump_menu(self):
        if self.start_menu.quad.model['scale'][0] > 2:
            self.resize = -0.001
        if self.start_menu.quad.model['scale'][0] <= 1.5:
            self.resize = 0.001
        self.start_menu.quad.model['scale'] = [
            self.start_menu.quad.model['scale'][0]+self.resize*7,
            self.start_menu.quad.model['scale'][1],
            self.start_menu.quad.model['scale'][2]+self.resize
        ]

    def handle_event(self, event):
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



            if self.btn_light_1_r_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_r_r.position[0]+0.15 and self.btn_light_1_r_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_r_r.position[2]+0.4:
                self.btn_light_1_r_r_down = True

            if self.btn_light_1_g_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_g_r.position[0]+0.15 and self.btn_light_1_g_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_g_r.position[2]+0.4:
                self.btn_light_1_g_r_down = True

            if self.btn_light_1_b_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_b_r.position[0]+0.15 and self.btn_light_1_b_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_b_r.position[2]+0.4:
                self.btn_light_1_b_r_down = True


            if self.btn_light_1_r_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_r_l.position[0]+0.15 and self.btn_light_1_r_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_r_l.position[2]+0.4:
                self.btn_light_1_r_l_down = True

            if self.btn_light_1_g_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_g_l.position[0]+0.15 and self.btn_light_1_g_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_g_l.position[2]+0.4:
                self.btn_light_1_g_l_down = True

            if self.btn_light_1_b_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_b_l.position[0]+0.15 and self.btn_light_1_b_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_b_l.position[2]+0.4:
                self.btn_light_1_b_l_down = True

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



            if self.btn_light_1_r_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_r_r.position[0]+0.15 and self.btn_light_1_r_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_r_r.position[2]+0.4:
                self.btn_light_1_r_r_down = False

            if self.btn_light_1_g_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_g_r.position[0]+0.15 and self.btn_light_1_g_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_g_r.position[2]+0.4:
                self.btn_light_1_g_r_down = False

            if self.btn_light_1_b_r.position[0]-0.15 <= -pos_y <= self.btn_light_1_b_r.position[0]+0.15 and self.btn_light_1_b_r.position[2]-0.4 <= -pos_x <= self.btn_light_1_b_r.position[2]+0.4:
                self.btn_light_1_b_r_down = False


            if self.btn_light_1_r_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_r_l.position[0]+0.15 and self.btn_light_1_r_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_r_l.position[2]+0.4:
                self.btn_light_1_r_l_down = False

            if self.btn_light_1_g_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_g_l.position[0]+0.15 and self.btn_light_1_g_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_g_l.position[2]+0.4:
                self.btn_light_1_g_l_down = False

            if self.btn_light_1_b_l.position[0]-0.15 <= -pos_y <= self.btn_light_1_b_l.position[0]+0.15 and self.btn_light_1_b_l.position[2]-0.4 <= -pos_x <= self.btn_light_1_b_l.position[2]+0.4:
                self.btn_light_1_b_l_down = False


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

        if self.btn_light_1_r_r_down:
            self.btn_light_1_r.set_caption(str(round(self.app.lights[0].color[0]*255, 2)))
            self.app.lights[0].color[0] += 0.01
            self.app.lights[0].sphere.color[0] += 0.01
        if self.btn_light_1_g_r_down:
            self.btn_light_1_g.set_caption(str(round(self.app.lights[0].color[1]*255, 2)))
            self.app.lights[0].color[1] += 0.01
            self.app.lights[0].sphere.color[1] += 0.01
        if self.btn_light_1_b_r_down:
            self.btn_light_1_b.set_caption(str(round(self.app.lights[0].color[2]*255, 2)))
            self.app.lights[0].color[2] += 0.01
            self.app.lights[0].sphere.color[2] += 0.01
        if self.btn_light_1_r_l_down:
            self.btn_light_1_r.set_caption(str(round(self.app.lights[0].color[0]*255, 2)))
            self.app.lights[0].color[0] += -0.01
            self.app.lights[0].sphere.color[0] += -0.01
        if self.btn_light_1_g_l_down:
            self.btn_light_1_g.set_caption(str(round(self.app.lights[0].color[1]*255, 2)))
            self.app.lights[0].color[1] += -0.01
            self.app.lights[0].sphere.color[1] += -0.01
        if self.btn_light_1_b_l_down:
            self.btn_light_1_b.set_caption(str(round(self.app.lights[0].color[2]*255, 2)))
            self.app.lights[0].color[2] += -0.01
            self.app.lights[0].sphere.color[2] += -0.01


    def render(self, renderer):
        self.update_lights()
        if self.menu:
            self.logo.render(renderer)
            self.start_menu.render(renderer)
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

            self.btn_light_1_r_l.render(renderer)
            self.btn_light_1_r.render(renderer)
            self.btn_light_1_r_r.render(renderer)
            self.btn_light_1_g_l.render(renderer)
            self.btn_light_1_g.render(renderer)
            self.btn_light_1_g_r.render(renderer)
            self.btn_light_1_b_l.render(renderer)
            self.btn_light_1_b.render(renderer)
            self.btn_light_1_b_r.render(renderer)