import pygame, numpy, pyrr, math, os, string
from OpenGL.GL import *

from Object import Object

WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class App:
    def __init__(self):
        self.tabuleiro = Object("./resources/models/tabuleiro.obj", "./resources/textures/triangles_red.png")
        self.player11  = Object("./resources/models/player1.obj",   "./resources/textures/triangles_yellow.png")
        self.player12  = Object("./resources/models/player1.obj",   "./resources/textures/triangles_yellow.png")
        self.player21  = Object("./resources/models/player2.obj",   "./resources/textures/triangles_blue.png")
        self.player22  = Object("./resources/models/player2.obj",   "./resources/textures/triangles_blue.png")

        self.player11.translate(0.8,0.2,0.8)
        self.player11.scale(0.2,0.2,0.2)

        self.player12.translate(-0.8,0.2,0.8)
        self.player12.scale(0.2,0.2,0.2)
        
        self.player21.translate(0.8,0.2,-0.8)
        self.player21.scale(0.2,0.2,0.2)
        
        self.player22.translate(-0.8,0.2,-0.8)
        self.player22.scale(0.2,0.2,0.2)

        self.view = {
            'position': [0.0, 0.0, 6.0],
            'target':   [0.0, 0.0, 0.0],
            'up':       [0.0, 1.0, 0.0]
        }

        self.projection = {
            'fovy':   45.0, 
            'aspect': WINDOW_WIDTH/WINDOW_HEIGHT,
            'near':   0.1,
            'far':    200.0,
            'dtype':  None 
        }

        self.animacao = False

        self.ortho = False

    def mount_mvp(self, model, view, projection):
        trans_matrix = numpy.transpose(pyrr.matrix44.create_from_translation(model['translation']))
        rot_matrix_x = numpy.transpose(pyrr.matrix44.create_from_x_rotation(model['rotation'][0]))
        rot_matrix_y = numpy.transpose(pyrr.matrix44.create_from_y_rotation(model['rotation'][1]))
        rot_matrix_z = numpy.transpose(pyrr.matrix44.create_from_z_rotation(model['rotation'][2]))
        rot_matrix   = numpy.matmul(numpy.matmul(rot_matrix_x, rot_matrix_y),rot_matrix_z)
        scale_matrix = numpy.transpose(pyrr.matrix44.create_from_scale(model['scale'] ))
        model_matrix = numpy.matmul(numpy.matmul(trans_matrix,rot_matrix),scale_matrix)

        view_matrix = numpy.transpose(pyrr.matrix44.create_look_at(
            numpy.array(view['position'], dtype="float32"),
            numpy.array(view['target'],   dtype="float32"),
            numpy.array(view['up'],       dtype="float32")
        ))

        if self.ortho:
            proj_matrix = numpy.transpose(pyrr.matrix44.create_orthogonal_projection_matrix(-6, 6, -3, 3, 0.001, 300, dtype=None))
        
        else:
            proj_matrix = numpy.transpose(pyrr.matrix44.create_perspective_projection(
                projection['fovy'],
                projection['aspect'],
                projection['near'],
                projection['far'],
                projection['dtype']
            ))

        m = numpy.matmul(numpy.matmul(proj_matrix,view_matrix),model_matrix) 
        return numpy.transpose(m)

    def render(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Transparency
        glEnable(GL_BLEND)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

        mvp = self.motion(self.tabuleiro.model, self.view, self.projection)
        self.tabuleiro.render(mvp)

        mvp2 = self.motion(self.player11.model, self.view, self.projection)
        self.player11.render(mvp2)
        mvp2 = self.motion(self.player12.model, self.view, self.projection)
        self.player12.render(mvp2)
        mvp2 = self.motion(self.player21.model, self.view, self.projection)
        self.player21.render(mvp2)
        mvp2 = self.motion(self.player22.model, self.view, self.projection)
        self.player22.render(mvp2)


    def rotate_view(self, view, degrees):
        rotation = [
            [ math.cos(degrees), 0.0, math.sin(degrees)],
            [               0.0, 1.0, 0.0              ],
            [-math.sin(degrees), 1.0, math.cos(degrees)]
        ]
        rotation = numpy.matrix(rotation, dtype='float32')
        new_view = numpy.array(numpy.dot(rotation, view['up'])).flatten()
        view['up'] = new_view


    def motion(self, model, view, projection):
        if not self.animacao:
            pressed = pygame.key.get_pressed()
            if(pressed[pygame.K_4]):
                self.animacao = True

            if(pressed[pygame.K_r]):
                self.view = {
                    'position': [0.0, 0.0, 6.0],
                    'target':   [0.0, 0.0, 0.0],
                    'up':       [0.0, 1.0, 0.0]
                }
            if pressed[pygame.K_UP]:
                view['position'][1] += 0.03
            if pressed[pygame.K_DOWN]:
                view['position'][1] -= 0.03
            if pressed[pygame.K_LEFT]:
                self.rotate_view(view, 0.001)
            if pressed[pygame.K_RIGHT]:
                self.rotate_view(view, -0.001)
            if pressed[pygame.K_a]:
                view['position'][0] -= 0.03
            if pressed[pygame.K_d]:
                view['position'][0] += 0.03
            if pressed[pygame.K_w]:
                view['position'][2] -= 0.02
            if pressed[pygame.K_s]:
                view['position'][2] += 0.02
            if(pressed[pygame.K_1]):
                self.view = {
                    'position': [0.0, 2.0, 5.0],
                    'target':   [0.0, 0.0, 0.0],
                    'up':       [0.0, 1.0, 0.0]
                }
            
            if(pressed[pygame.K_2]):
                self.view = {
                    'position': [0.0, 5.0, 2.0],
                    'target':   [0.0, 0.0, 0.0],
                    'up':       [1.0, 0.0, 0.0]
                }
            
            if(pressed[pygame.K_3]):
                self.view = {
                    'position': [5.0, 2.0, 0.0],
                    'target':   [0.0, 0.0, 0.0],
                    'up':       [0.0, 1.0, 0.0]
                }

            return self.mount_mvp(model, view, projection)
        
        else:
            if not view['position'][2] <= -6:
                view['position'][2] -= 0.01
                if(view['position'][2] > 0):
                    view['position'][1] += 0.01
                    view['position'][0] += 0.01
                else:
                    view['position'][1] -= 0.01
                    view['position'][0] -= 0.01
            else:
                self.animacao = False
            return self.mount_mvp(model, view, projection)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'p':
                self.ortho = not self.ortho

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