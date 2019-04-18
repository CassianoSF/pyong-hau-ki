import pygame, numpy, pyrr, math, os, string
from OpenGL.GL import *

from Object import Object
from Loader import Loader
from Camera import Camera

WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class App:
    def __init__(self):
        sol_loader  = Loader("./resources/models/sphere.obj",  "./resources/textures/triangles_yellow.png")
        terra_loader  = Loader("./resources/models/sphere.obj",  "./resources/textures/triangles_yellow.png")
        self.sol  = Object(sol_loader)
        self.terra  = Object(terra_loader)

        self.sol.scale(2,2,2)

        self.terra.translate(0,0,0)
        self.terra.scale(0.2,0.2,0.2)

        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.set_render_mode()

        self.counter = 0
        self.frame = 0

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
        self.counter += 1
        self.terra.model['translation'][0] = math.sin(self.counter/360 * math.pi) * 10
        self.terra.model['translation'][2] = math.cos(self.counter/360 * math.pi) * 10
        self.frame += 1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update()
        self.sol.render(self.camera)
        self.terra.render(self.camera)

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("APP")
    pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    clock = pygame.time.Clock()
    app = App()

    while True:
        [app.handle_event(event) for event in pygame.event.get()]
        clock.tick(180)
        app.render()
        pygame.display.flip()

if __name__ == "__main__":
    main()