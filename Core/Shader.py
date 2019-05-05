from OpenGL.GL import *

class Shader:
    def __init__(self, frag_path, vert_path):
        self.id = glCreateProgram()
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

        try:
            with open(frag_path, "r") as vert_file:
                vert_source = vert_file.read()
            with open(vert_path, "r") as frag_file:
                frag_source = frag_file.read()
        except IOError:
            print(".shaders file not found.")

        glShaderSource(vertex_shader, vert_source)
        glShaderSource(fragment_shader, frag_source)

        glCompileShader(vertex_shader)
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            info_log = glGetShaderInfoLog(vertex_shader)
            print ("Compilation Failure for " + vertex_shader + " shader:\n" + info_log)

        glCompileShader(fragment_shader)
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            info_log = glGetShaderInfoLog(fragment_shader)
            print ("Compilation Failure for " + fragment_shader + " shader:\n" + info_log)

        glAttachShader(self.id, vertex_shader)
        glAttachShader(self.id, fragment_shader)

        glLinkProgram(self.id)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def bind(self):
        glUseProgram(self.id)

    def unbind(self):
        glUseProgram(0)

    def add_uniform_matrix_4f(self, name, data):
        self.bind()
        uniform = glGetUniformLocation(self.id, name)
        glUniformMatrix4fv(uniform, 1, GL_FALSE, data)

    def add_uniform_1i(self, name, data):
        self.bind()
        uniform = glGetUniformLocation(self.id, name)
        glUniform1i(uniform, data)

    def add_uniform_3f(self, name, data):
        self.bind()
        uniform = glGetUniformLocation(self.id, name)
        glUniform3f(uniform, data[0], data[1], data[2])