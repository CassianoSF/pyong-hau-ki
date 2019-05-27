import pygame, os

from Core.Texture  import Texture
from Core.Renderer import Renderer

from Components.Label import Label

from Object import Object
from Loader import Loader
from Camera import Camera
from Light  import Light

class PongHauKi:
    def __init__(self, playerA1, playerA2, playerB1, playerB2, tabuleiro, lights):
        self.window_width  = 1280
        self.window_height = 620
        player1_obj   = Loader("./resources/models/drone.obj")
        player2_obj   = Loader("./resources/models/galinha.obj")
        galinha_texture  = Texture("./resources/textures/galinha.png")
        mech_texture     = Texture("./resources/textures/mech.png")
        self.camera = Camera(self.window_width, self.window_height)
        self.camera.view['position'] = [0.0, 1.0, 0.0]
        self.camera.orthogonal = True
        self.camera.update()
        self.nave     = Object(player1_obj,   self.camera, mech_texture)
        self.nave.scale(0.4,0.4,0.4)
        self.galinha  = Object(player2_obj,   self.camera, galinha_texture)
        self.nave.model['rotation'][2] += 5
        self.galinha.model['rotation'][2] += 5

        self.galinha_win = Label("Galinha Wins", "kashima", 40, [1,1,1], [-1.5,0,0], self.camera)
        self.nave_win = Label(      "Nave Wins", "kashima", 40, [1,1,1], [-1.5,0,0], self.camera)



        self.playerA1 = playerA1
        self.playerA2 = playerA2
        self.playerB1 = playerB1
        self.playerB2 = playerB2
        self.tabuleiro = tabuleiro

        self.light = lights[0]

        self.playerA1.model['translation'] = [-0.8, 0.2, 0.8]
        self.playerA2.model['translation'] = [-0.8, 0.2,-0.8]
        self.playerB1.model['translation'] = [ 0.8, 0.2,-0.8]
        self.playerB2.model['translation'] = [ 0.8, 0.2, 0.8]

        self.positions = [
            [ 0.8, 0.2,-0.8],
            [-0.8, 0.2, 0.8],
            [ 0.8, 0.2, 0.8],
            [-0.8, 0.2,-0.8],
            [ 0.0, 0.2, 0.0]
        ]

        self.current_player = "playerA"
        self.selected_piece = self.playerA1
        self.free_position = self.positions[4]
        self.winner = None

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

    def have_winner(self):
        if self.current_player == "playerA":
            return( 
                not self.can_move(self.playerA1.model['translation'], self.free_position) and 
                not self.can_move(self.playerA2.model['translation'], self.free_position)
            )
        elif self.current_player == "playerB":
            return( 
                not self.can_move(self.playerB1.model['translation'], self.free_position) and 
                not self.can_move(self.playerB2.model['translation'], self.free_position)
            )

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
            previous_player = self.current_player
            if self.current_player == "playerA":
                self.current_player = "playerB"
                self.selected_piece = self.playerB1
            elif self.current_player == "playerB":
                self.current_player = "playerA"
                self.selected_piece = self.playerA1
            if self.have_winner():
                self.winner = previous_player
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

        if self.winner == "playerA":
            renderer.render_with_lights(self.nave)
            self.nave.model['rotation'][0] += 0.1
            self.nave_win.render(renderer)
        elif self.winner == "playerB":
            renderer.render_with_lights(self.galinha)
            self.galinha.model['rotation'][0] += 0.1
            self.galinha_win.render(renderer)