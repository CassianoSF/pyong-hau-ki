from random import randint

class Camera:
    def self.__init__(self):
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

    def random_animate
        self.view = {
            'position': [
                [-.02, .02][randint(0,1)] + self.view['position'][0], 
                [-.02, .02][randint(0,1)] + self.view['position'][1], 
                [-.02, .02][randint(0,1)] + self.view['position'][2]
            ],
            'target':   [0.0, 0.0, 0.0],
            'up':       [0.0, 1.0, 0.0]
        }