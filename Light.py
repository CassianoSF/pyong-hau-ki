from Core.Shader import Shader
from Core.Texture import Texture

from Object import Object
from Loader import Loader

class Light:
    def __init__(self, position, power, color, radius):
        self.position = position
        self.power = power
        self.color = color
        self.radius = radius
        sphere_obj = Loader("./resources/models/sphere.obj")
        red_texture    = Texture("./resources/textures/triangles_red.png")
        shader  = Shader("./resources/shaders/LightVertex.shader", "./resources/shaders/LightFragment.shader")
        self.sphere = Object(sphere_obj, shader, red_texture)
        self.sphere.scale(radius, radius, radius)
        self.sphere.translate(position[0],position[1],position[2])


    def render(self, camera):
        self.sphere.render(camera)