from OpenGL.GL import *

class Shader:
    def __init__(self, frag_path, vert_path, lights=[]):
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


        if(lights):
            for index, light in enumerate(lights):
                lines = vert_source.splitlines()
                i = lines.index("// LIGHT DIRECTION OUT")
                lines.insert(i, "out vec3 LightDirection_cameraspace" + str(index) + ";")
                i = lines.index("// LIGHT POSITIONS")
                lines.insert(i, "uniform vec3 LightPosition" + str(index) + ";")
                i = lines.index("// LIGHT DIRECTION")
                lines.insert(i,"LightDirection_cameraspace"+str(index)+" = ( view * vec4(LightPosition"+str(index)+",1)).xyz - EyeDirection_cameraspace;")
                vert_source = "\n".join(lines)

                lines = frag_source.splitlines()
                i = lines.index("// LIGHT DIRECTION IN")
                lines.insert(i, "in vec3 LightDirection_cameraspace"+str(index)+";")
                i = lines.index("// LIGHT POSITION")
                lines.insert(i, "uniform vec3 LightPosition"+str(index)+";")
                i = lines.index("// LIGHT COLOR")
                lines.insert(i, "uniform vec3 LightColor"+str(index)+";")
                i = lines.index("// LIGHT POWER")
                lines.insert(i, "uniform int LightPower"+str(index)+";")
                i = lines.index("// COLORS")
                lines.insert(i, "color += calcLight(LightPosition"+str(index)+", LightColor"+str(index)+", LightPower"+str(index)+", LightDirection_cameraspace"+str(index)+");")
                frag_source = "\n".join(lines)

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