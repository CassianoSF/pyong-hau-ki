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
WINDOW_HEIGHT=720

class App:
    def __init__(self):

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("APP")
        pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()

        tabuleiro_loader = Loader("./resources/models/tabuleiro.obj")
        player11_loader  = Loader("./resources/models/player1.obj")
        player12_loader  = Loader("./resources/models/player1.obj")
        player21_loader  = Loader("./resources/models/player2.obj")
        player22_loader  = Loader("./resources/models/player2.obj")
        suzanne_loader  = Loader("./resources/models/suzanne.obj")

        shader = Shader("./resources/shaders/VertexShader.shader", "./resources/shaders/FragmentShader.shader")

        blue_texture = Texture("./resources/textures/triangles_blue.png")
        red_texture = Texture("./resources/textures/triangles_red.png")
        yellow_texture = Texture("./resources/textures/triangles_yellow.png")


        self.tabuleiro = Object(tabuleiro_loader, shader, red_texture)
        self.player11  = Object(player11_loader, shader, blue_texture)
        self.player12  = Object(player12_loader, shader, blue_texture)
        self.player21  = Object(player21_loader, shader, yellow_texture)
        self.player22  = Object(player22_loader, shader, yellow_texture)
        self.suzanne   = Object(suzanne_loader, shader, red_texture)


        self.suzanne.scale(0.5, 0.5, 0.5)
        self.suzanne.translate(0.0, 0.8, 0.0)

        self.player11.translate(0.8,0.2,0.8)
        self.player11.scale(0.2,0.2,0.2)

        self.player12.translate(-0.8,0.2,0.8)
        self.player12.scale(0.2,0.2,0.2)
        
        self.player21.translate(0.8,0.2,-0.8)
        self.player21.scale(0.2,0.2,0.2)
        
        self.player22.translate(-0.8,0.2,-0.8)
        self.player22.scale(0.2,0.2,0.2)

        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gui = Gui(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_render_mode()
        self.menu = True

    def set_render_mode(self):
        glEnable(GL_BLEND)
        # Transparency
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        # glDepthFunc(GL_LESS)
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
            self.suzanne.render(self.camera)

    def run(self):
        while True:
            [self.handle_event(event) for event in pygame.event.get()]
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

if __name__ == "__main__":
    App().run()
