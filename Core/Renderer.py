from OpenGL.GL import *
import pygame

from Core.Shader import Shader

class Renderer:
    def __init__(self, lights):
        self.lights = lights
        self.shader_simple      = Shader("./resources/shaders/SimpleVertex.shader", "./resources/shaders/SimpleFragment.shader")
        self.shader_transparent = Shader("./resources/shaders/SimpleVertex.shader", "./resources/shaders/TransparencyFragment.shader")
        self.shader_solid_color = Shader("./resources/shaders/SolidColorVertex.shader", "./resources/shaders/SolidColorFragment.shader")
        self.shader_with_light  = Shader("./resources/shaders/LightVertex.shader", "./resources/shaders/LightFragment.shader", lights=lights)

    def add_mvp(self, shader, obj):
        shader.add_uniform_matrix_4f("model", obj.model_matrix)
        shader.add_uniform_matrix_4f("view", obj.view_matrix)
        shader.add_uniform_matrix_4f("projection", obj.proj_matrix)

    def simple(self, obj):
        obj.mount_mvp()
        self.add_mvp(self.shader_simple, obj)
        self.shader_simple.bind()
        obj.bind()
        glDrawElements(GL_TRIANGLES, obj.va.size, GL_UNSIGNED_INT, None)


    def with_transparency(self, obj):
        # transparency
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND)
        obj.mount_mvp()
        self.add_mvp(self.shader_transparent, obj)
        self.shader_transparent.bind()
        obj.bind()
        glDrawElements(GL_TRIANGLES, obj.va.size, GL_UNSIGNED_INT, None)
        glDisable(GL_BLEND)


    def solid_color(self, obj):
        obj.mount_mvp()
        self.add_mvp(self.shader_solid_color, obj)
        self.shader_solid_color.bind()
        obj.bind()
        glDrawElements(GL_TRIANGLES, obj.va.size, GL_UNSIGNED_INT, None)


    def render_with_lights(self, obj):
        obj.mount_mvp()
        self.add_mvp(self.shader_with_light, obj)
        for index, light in enumerate(self.lights):
            self.shader_with_light.add_uniform_3f("LightPosition" + str(index), light.position)
            self.shader_with_light.add_uniform_3f("LightColor" + str(index), light.color)
            self.shader_with_light.add_uniform_1i("LightPower" + str(index), light.power)

        self.shader_with_light.bind()
        obj.bind()

        glDrawElements(GL_TRIANGLES, obj.va.size, GL_UNSIGNED_INT, None)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
