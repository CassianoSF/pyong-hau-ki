from Core.Shader import Shader
from Core.Texture import Texture

from Object import Object
from Loader import Loader

class Light:
    def __init__(self, position, power, color, radius, camera):
        self.position = position
        self.power = power
        self.color = color
        self.radius = radius
        sphere_obj = Loader("./resources/models/sphere.obj")
        red_texture    = Texture("./resources/textures/triangles_red.png")

        self.sphere = Object(sphere_obj, camera, red_texture, color=color)
        self.sphere.scale(radius, radius, radius)
        self.sphere.translate(position[0],position[1],position[2])

    def render(self, renderer):
        renderer.render_solid_color(self.sphere)