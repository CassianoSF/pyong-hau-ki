import pygame, os

from Core.Texture  import Texture
from Core.Renderer import Renderer

from Object import Object
from Loader import Loader
from Camera import Camera
from Light  import Light
from Gui    import Gui

import threading


class PongHauKi:
    def __init__(self, playerA1, playerA2, playerB1, playerB2, tabuleiro, light):
        self.playerA1 = playerA1
        self.playerA2 = playerA2
        self.playerB1 = playerB1
        self.playerB2 = playerB2
        self.tabuleiro = tabuleiro

        self.light = light


        self.playerA1.model['translation'] = [-0.8, 0.2, 0.8]
        self.playerA2.model['translation'] = [-0.8, 0.2,-0.8]
        self.playerB1.model['translation'] = [ 0.8, 0.2,-0.8]
        self.playerB2.model['translation'] = [ 0.8, 0.2, 0.8]

        self.playerA1.color = [1,1,0.5]
        self.playerA2.color = [1,1,0.5]
        self.playerB1.color = [1,1,0.5]
        self.playerB2.color = [1,1,0.5]

        self.positions = [
            [ 0.8, 0.2,-0.8],
            [-0.8, 0.2, 0.8],
            [ 0.8, 0.2, 0.8],
            [-0.8, 0.2,-0.8],
            [ 0.0, 0.2, 0.0]
        ]
        self.current_player = "playerA"
        self.selected_piece = self.playerA1
        self.light.set_position(self.selected_piece.model['translation'])
        self.free_position = self.positions[4]

        self.can_move_tree = {
            str(self.positions[0]): {
                str(self.positions[0]): False,
                str(self.positions[1]): False,
                str(self.positions[2]): True,
                str(self.positions[3]): True,
                str(self.positions[4]): True
            },
            str(self.positions[1]):{
                str(self.positions[0]): False,
                str(self.positions[1]): False,
                str(self.positions[2]): True,
                str(self.positions[3]): False,
                str(self.positions[4]): True
            },
            str(self.positions[2]):{
                str(self.positions[0]): True,
                str(self.positions[1]): True,
                str(self.positions[2]): False,
                str(self.positions[3]): False,
                str(self.positions[4]): True
            },
            str(self.positions[3]):{
                str(self.positions[0]): True,
                str(self.positions[1]): False,
                str(self.positions[2]): False,
                str(self.positions[3]): False,
                str(self.positions[4]): True
            },
            str(self.positions[4]): {
                str(self.positions[0]): True,
                str(self.positions[1]): True,
                str(self.positions[2]): True,
                str(self.positions[3]): True,
                str(self.positions[4]): False
            }
        }

    def can_move(self, from_position, to_position):
        return self.can_move_tree[str(from_position)][str(to_position)]


    def select_piece(self):
        self.light.color = [1,1,0.5]
        if self.selected_piece == self.playerA1:
            self.selected_piece = self.playerA2

        elif self.selected_piece == self.playerA2:
            self.selected_piece = self.playerA1

        elif self.selected_piece == self.playerB1:
            self.selected_piece = self.playerB2
        
        elif self.selected_piece == self.playerB2:
            self.selected_piece = self.playerB1

    def move_piece(self):
        current_position = self.selected_piece.model['translation'].copy()
        if(self.can_move(current_position, self.free_position)):
            self.selected_piece.target_position = self.free_position
            self.free_position = current_position
            if self.current_player == "playerA":
                self.current_player = "playerB"
                self.selected_piece = self.playerB1
            elif self.current_player == "playerB":
                self.current_player = "playerA"
                self.selected_piece = self.playerA1
        else:
            self.light.color = [1,0,0]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                self.select_piece()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                self.move_piece()

    def update(self, renderer):
        self.light.set_position(self.selected_piece.model['translation'])
        self.playerA1.update()
        self.playerA2.update()
        self.playerB1.update()
        self.playerB2.update()


class App:
    def __init__(self):
        self.config_screen()
        self.load_env()
        self.load_sound()

    def load_sound(self):
        self.sound = {}
        self.sound['next'] = pygame.mixer.Sound('./resources/sounds/whoosh1.wav')
        pygame.mixer.music.load('./resources/sounds/musica_menu.wav')
        pygame.mixer.music.play()

    def config_screen(self):
        self.window_width  = 1280
        self.window_height = 620
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Pong hau ki")
        pygame.display.set_mode((self.window_width,self.window_height), pygame.DOUBLEBUF | pygame.OPENGL)

    def load_env(self):
        sphere_obj = Loader("./resources/models/sphere2.obj")
        tabuleiro_obj = Loader("./resources/models/tabuleiro.obj")
        player1_obj   = Loader("./resources/models/drone.obj")
        player2_obj   = Loader("./resources/models/galinha.obj")
        # suzanne_obj   = Loader("./resources/models/suzanne.obj")
        # sphere_obj    = Loader("./resources/models/sphere.obj")

        space_texture    = Texture("./resources/textures/space.png")
        galinha_texture  = Texture("./resources/textures/galinha.png")
        wood_texture     = Texture("./resources/textures/wood.png")
        mech_texture     = Texture("./resources/textures/mech.png")
        # blue_texture     = Texture("./resources/textures/triangles_blue.png")
        # red_texture      = Texture("./resources/textures/triangles_red.png")
        # yellow_texture   = Texture("./resources/textures/triangles_yellow.png")

        self.camera = Camera(self.window_width, self.window_height)

        self.background = Object(sphere_obj,      self.camera, space_texture)
        self.tabuleiro = Object(tabuleiro_obj, self.camera, wood_texture)
        self.player11  = Object(player1_obj,   self.camera, mech_texture)
        self.player12  = Object(player1_obj,   self.camera, mech_texture)
        self.player21  = Object(player2_obj,   self.camera, galinha_texture)
        self.player22  = Object(player2_obj,   self.camera, galinha_texture)
        # self.suzanne   = Object(suzanne_obj,   self.camera, red_texture)
        # self.sphere    = Object(sphere_obj,    self.camera, red_texture)


        self.background.scale(5, 5, 5)
        # self.sphere.scale(0.5, 0.5, 0.5)
        # self.sphere.translate(0, -4, 0)

        # self.suzanne.scale(0.5, 0.5, 0.5)
        # self.suzanne.translate(0.0, -2, 0.0)

        self.player11.translate(0.8,0.1,-0.8)
        self.player11.scale(0.1,0.1,0.1)

        self.player12.translate(-0.8,0.1,0.8)
        self.player12.scale(0.1,0.1,0.1)
        
        self.player21.translate(0.8,0.2,0.8)
        self.player21.scale(0.4,0.4,0.4)
        
        self.player22.translate(-0.8,0.2,-0.8)
        self.player22.scale(0.4,0.4,0.4)

        self.menu = True

        self.light_1  = Light([ 0,  2,  1], 2,  [1.0, 1.0, 0.5], 0.01, self.camera)
        self.light_2  = Light([ 1, -1,  1], 5,  [0.5, 0.8, 0.3], 0.1,  self.camera)
        self.light_3  = Light([ 1,  1, -2], 5,  [1.0, 1.0, 1.0], 0.1,  self.camera)
        self.light_4  = Light([ 2,  1,  2], 5,  [0.7, 0.2, 0.2], 0.1,  self.camera)
        self.light_5  = Light([ 2,  2, -1], 5,  [0.0, 0.2, 0.8], 0.1,  self.camera)

        self.lights = [
            self.light_1,
            self.light_2,
            self.light_3,
            self.light_4,
            self.light_5
        ]

        self.gui = Gui(self.window_width, self.window_height, self)
        self.renderer = Renderer(self.lights)

        self.pong_hau_ki = PongHauKi(self.player11,self.player12,self.player21,self.player22,self.tabuleiro, self.light_1)

    def handle_event(self, event):
        self.camera.handle_event(event)
        self.gui.handle_event(event)
        self.pong_hau_ki.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                pygame.mixer.music.load('./resources/sounds/musica_tema.wav')
                pygame.mixer.music.play()
                self.menu = False
                self.gui.game_start()

    def render(self):
        self.renderer.clear()
        self.gui.render(self.renderer)
        if not self.menu:
            self.camera.update()
            self.renderer.render_with_lights(self.tabuleiro)
            self.renderer.render_with_lights(self.player11)
            self.renderer.render_with_lights(self.player12)
            self.renderer.render_with_lights(self.player21)
            self.renderer.render_with_lights(self.player22)
            self.renderer.render_with_lights(self.background)
            # self.renderer.render_with_lights(self.sphere)
            # self.renderer.render_with_lights(self.suzanne)
            self.light_1.render(self.renderer)
            self.light_2.render(self.renderer)
            self.light_3.render(self.renderer)
            self.light_4.render(self.renderer)
            self.light_5.render(self.renderer)
            self.pong_hau_ki.update(self.renderer)



    def run(self):
        clock = pygame.time.Clock()
        while True:
            [self.handle_event(event) for event in pygame.event.get()]
            self.render()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    App().run()
