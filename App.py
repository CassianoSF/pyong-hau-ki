import pygame, numpy, pyrr, math, os, string
from OpenGL.GL import *

from Core.Shader import Shader
from Core.Texture import Texture

from Object import Object
from Loader import Loader
from Camera import Camera
from Gui    import Gui

import threading

WINDOW_WIDTH=1280
WINDOW_HEIGHT=620

class App:
    def __init__(self):
        self.config_screen()
        self.load_env()
        self.config_render()

    def config_screen(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("APP")
        pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    def load_env(self):
        tabuleiro_obj = Loader("./resources/models/tabuleiro.obj")
        player11_obj  = Loader("./resources/models/player1.obj")
        player12_obj  = Loader("./resources/models/player1.obj")
        player21_obj  = Loader("./resources/models/player2.obj")
        player22_obj  = Loader("./resources/models/player2.obj")
        suzanne_obj   = Loader("./resources/models/suzanne.obj")

        shader = Shader("./resources/shaders/LightVertex.shader", "./resources/shaders/LightFragment.shader")
        blue_texture = Texture("./resources/textures/triangles_blue.png")
        red_texture = Texture("./resources/textures/triangles_red.png")
        yellow_texture = Texture("./resources/textures/triangles_yellow.png")

        self.tabuleiro = Object(tabuleiro_obj, shader, red_texture)
        self.player11  = Object(player11_obj, shader, blue_texture)
        self.player12  = Object(player12_obj, shader, blue_texture)
        self.player21  = Object(player21_obj, shader, yellow_texture)
        self.player22  = Object(player22_obj, shader, yellow_texture)
        self.suzanne   = Object(suzanne_obj, shader, red_texture)

        self.suzanne.scale(0.5, 0.5, 0.5)
        self.suzanne.translate(0.0, 0.8, 0.0)

        self.player11.translate(0.8,0.2,-0.8)
        self.player11.scale(0.2,0.2,0.2)

        self.player12.translate(-0.8,0.2,0.8)
        self.player12.scale(0.2,0.2,0.2)
        
        self.player21.translate(0.8,0.2,0.8)
        self.player21.scale(0.2,0.2,0.2)
        
        self.player22.translate(-0.8,0.2,-0.8)
        self.player22.scale(0.2,0.2,0.2)

        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gui = Gui(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.menu = True

    def config_render(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def handle_event(self, event):
        self.camera.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                self.menu = False
                self.gui.game_start()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.menu:
            self.gui.render()
        else:
            self.gui.render()
            self.camera.update()
            self.tabuleiro.render(self.camera)
            self.player11.render(self.camera)
            self.player12.render(self.camera)
            self.player21.render(self.camera)
            self.player22.render(self.camera)
            # self.suzanne.render(self.camera)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            [self.handle_event(event) for event in pygame.event.get()]
            self.render()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    App().run()
