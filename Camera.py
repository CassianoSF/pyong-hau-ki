import pygame, math, numpy

class Camera:
    def __init__(self, window_width, window_height):
        self.view = {
            'position': [0.0, 0.0, 5.0],
            'target':   [0.0, 0.0, 0.0],
            'up':       [0.0, 1.0, 0.0]
        }
        
        self.projection = {
            'fovy':   45.0, 
            'aspect': window_width/window_height,
            'near':   0.1,
            'far':    200.0,
            'dtype':  None 
        }
        self.orthogonal = False
        self.animacao_inicial = True

    def move_up(self, amount):
        self.view['position'][1] += amount

    def move_down(self, amount):
        self.view['position'][1] -= amount

    def move_right(self, amount):
        self.view['position'][0] += amount

    def move_left(self, amount):
        self.view['position'][0] -= amount

    def move_backward(self, amount):
        self.view['position'][2] += amount

    def move_forward(self, amount):
        self.view['position'][2] -= amount

    def move_to(self, x, y, z, speed):
        if (round(self.view['position'][0], 2) < x):
            self.view['position'][0] += 0.01 * speed
        elif(round(self.view['position'][0], 2) > x):
            self.view['position'][0] -= 0.01 * speed

        if (round(self.view['position'][1], 2) < y):
            self.view['position'][1] += 0.01 * speed
        elif(round(self.view['position'][1], 2) > y):
            self.view['position'][1] -= 0.01 * speed

        if (round(self.view['position'][2], 2) < z):
            self.view['position'][2] += 0.01 * speed
        elif(round(self.view['position'][2], 2) > z):
            self.view['position'][2] -= 0.01 * speed

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'p' or event.unicode == 'P':
                self.orthogonal = not self.orthogonal

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.move_forward(0.25)
            elif event.button == 5:
                self.move_backward(0.25)

    def update(self):
        if self.animacao_inicial:
            self.move_to(5, 5, 0, 10)
            if self.view['position'][1] > 4.99 :
                self.animacao_inicial = False
            return
           

        pressed = pygame.key.get_pressed()

        if(pressed[pygame.K_r]):
            self.view = {
                'position': [0.0, 0.0, 6.0],
                'target':   [0.0, 0.0, 0.0],
                'up':       [0.0, 1.0, 0.0]
            }

        if pressed[pygame.K_a]:
            self.move_left(0.10)
        if pressed[pygame.K_d]:
            self.move_right(0.10)

        if pressed[pygame.K_w]:
            self.move_up(0.10)
        if pressed[pygame.K_s]:
            self.move_down(0.10)

        if(pressed[pygame.K_1]):
            self.move_to(1, 4, 4, 10)
        if(pressed[pygame.K_2]):
            self.move_to(1, 4, -4, 10)
        if(pressed[pygame.K_3]):
            self.move_to(3, 5, 0, 10)
