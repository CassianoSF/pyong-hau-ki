import pygame, numpy, pyrr, math, os, string
from OpenGL.GL import *

from Object import Object
from Loader import Loader
from Camera import Camera

WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class App:
    def __init__(self):
        tabuleiro_loader = Loader("./resources/models/tabuleiro.obj","./resources/textures/triangles_blue.png")
        player11_loader  = Loader("./resources/models/player1.obj",  "./resources/textures/triangles_yellow.png")
        player12_loader  = Loader("./resources/models/player1.obj",  "./resources/textures/triangles_yellow.png")
        player21_loader  = Loader("./resources/models/player2.obj",  "./resources/textures/triangles_red.png")
        player22_loader  = Loader("./resources/models/player2.obj",  "./resources/textures/triangles_red.png")
        self.tabuleiro = Object(tabuleiro_loader)
        self.player11  = Object(player11_loader)
        self.player12  = Object(player12_loader)
        self.player21  = Object(player21_loader)
        self.player22  = Object(player22_loader)

        self.player11.translate(0.8,0.2,0.8)
        self.player11.scale(0.2,0.2,0.2)

        self.player12.translate(-0.8,0.2,0.8)
        self.player12.scale(0.2,0.2,0.2)
        
        self.player21.translate(0.8,0.2,-0.8)
        self.player21.scale(0.2,0.2,0.2)
        
        self.player22.translate(-0.8,0.2,-0.8)
        self.player22.scale(0.2,0.2,0.2)

        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.set_render_mode()

    def set_render_mode(self):
        glEnable(GL_BLEND)
        # Transparency
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)

    def handle_event(self, event):
        self.camera.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update()
        self.tabuleiro.render(self.camera)
        self.player11.render(self.camera)
        self.player12.render(self.camera)
        self.player21.render(self.camera)
        self.player22.render(self.camera)

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("APP")
    pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    clock = pygame.time.Clock()
    app = App()

    while True:
        [app.handle_event(event) for event in pygame.event.get()]
        clock.tick(60)
        app.render()
        pygame.display.flip()

if __name__ == "__main__":
    main()