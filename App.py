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

        mouse_pointer_loader  = Loader("./resources/models/square.obj",  "./resources/textures/triangles_red.png")

        self.mouse_pointer = Object(mouse_pointer_loader)
        self.mouse_pointer.scale(1,0,1)
        
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


        self.mouse_pointer_positions = [0,0,0]

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

        if event.type == pygame.MOUSEMOTION:

            p1 = numpy.array(self.camera.view['position'])
            p2 = numpy.array(self.camera.view['target'])
            squared_dist = numpy.sum(p1**2 + p2**2, axis=0)
            dist = numpy.sqrt(squared_dist)


            x, y = pygame.mouse.get_pos()
            x = (x - WINDOW_WIDTH/2)/(WINDOW_WIDTH/2) * dist
            y = (WINDOW_HEIGHT/2 - y)/(WINDOW_HEIGHT/2) * dist
            self.mouse_pointer_positions = [x, 0, -y]
            print(x, y)
            # print(self.camera.view['target'])


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update()
        self.tabuleiro.render(self.camera)
        self.player11.render(self.camera)
        self.player12.render(self.camera)
        self.player21.render(self.camera)
        self.player22.render(self.camera)
        self.mouse_pointer.render(self.camera)
        self.mouse_pointer.move_to(self.mouse_pointer_positions)

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