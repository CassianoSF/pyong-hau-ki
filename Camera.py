import pygame

class Camera:
    def __init__(self, window_width, window_height):
        self.view = {
            'position': [0.0, 0.0, 6.0],
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
        self.animacao = False


    def spin(self, degrees):
        rotation = [
            [ math.cos(degrees), 0.0, math.sin(degrees)],
            [               0.0, 1.0, 0.0              ],
            [-math.sin(degrees), 1.0, math.cos(degrees)]
        ]
        rotation = numpy.matrix(rotation, dtype='float32')
        new_view = numpy.array(numpy.dot(rotation, self.view['up'])).flatten()
        self.view['up'] = new_view

    def move_up(self, amount):
        self.view['position'][1] += amount

    def move_down(self, amount):
        self.view['position'][1] -= amount

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'p':
                self.orthogonal = not self.orthogonal

    def update(self):
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
                self.move_up(0.03)
            if pressed[pygame.K_DOWN]:
                self.move_down(0.03)
            if pressed[pygame.K_LEFT]:
                self.spin(0.001)
            if pressed[pygame.K_RIGHT]:
                self.spin(-0.001)
            if pressed[pygame.K_a]:
                self.view['position'][0] -= 0.03
            if pressed[pygame.K_d]:
                self.view['position'][0] += 0.03
            if pressed[pygame.K_w]:
                self.view['position'][2] -= 0.02
            if pressed[pygame.K_s]:
                self.view['position'][2] += 0.02
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
        else:
            if not self.view['position'][2] <= -6:
                self.view['position'][2] -= 0.01
                if(self.view['position'][2] > 0):
                    self.view['position'][1] += 0.01
                    self.view['position'][0] += 0.01
                else:
                    self.view['position'][1] -= 0.01
                    self.view['position'][0] -= 0.01
            else:
                self.animacao = False