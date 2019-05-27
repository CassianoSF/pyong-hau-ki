import math

from Core.Font    import Font

from Object    import Object
from Loader    import Loader

class Label:
    def __init__(self, caption, font, size, color, position, camera):
        quad_obj  = Loader("./resources/models/quad.obj")
        self.font = Font(caption, font, color[0], color[1], color[2])
        self.quad = Object(quad_obj, camera, self.font)
        self.quad.model['rotation'] = [0, math.pi/2, 0]
        self.quad.translate(*position)
        self.quad.scale(size*0.04*len(caption)/10, 1, size*0.1/10)

    def render(self, renderer):
        renderer.render_with_transparency(self.quad)
