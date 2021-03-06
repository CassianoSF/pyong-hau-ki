import numpy

class Loader():
    def __init__(self, objFileName):
        self.vertices = []
        self.indices = []
        self.tex_map = []
        self.normals = []
        self.loadObj(objFileName)

    def loadObj(self, objFileName):
        try:
            file = open(objFileName)
            temp_vertices = []
            temp_tex_map = []
            temp_normals = []

            for line in file:
                if line[:2] == "v ":
                    temp_vertices.append(
                        list(map(float, line.replace("v ", "").replace("\n", "").split(" ")))
                    )
                if line[:3] == "vt ":
                    temp_tex_map.append(
                        list(map(float, line.replace("vt ", "").replace("\n", "").split(" ")))
                    )
                if line[:3] == "vn ":
                    temp_normals.append(
                        list(map(float, line.replace("vn ", "").replace("\n", "").split(" ")))
                    )
                elif line[:2] == "f ":
                    if("/" in line):
                        face = line.replace("f ", "").replace("\n", "").split(" ")
                        for triangle in face:
                            v_index, t_index, n_index = triangle.split("/")

                            v_index = int(v_index or 1) -1
                            t_index = int(t_index or 1) -1
                            n_index = int(n_index or 1) -1

                            if len(temp_vertices) > v_index:
                                self.vertices.append(temp_vertices[v_index])

                            if len(temp_tex_map) > t_index:
                                self.tex_map.append(temp_tex_map[t_index])

                            if len(temp_normals) > n_index:
                                self.normals.append(temp_normals[n_index])

                            self.indices.append(len(self.indices))
                    else:
                        v_indices = line.replace("f ", "").replace("\n", "").split(" ")
                        for v_index in v_indices:
                            v_index = int(v_index or 1) -1
                            if len(temp_vertices) > v_index:
                                self.vertices.append(temp_vertices[v_index])
                            
                            self.indices.append(len(self.indices))

            file.close()
        except IOError:
            print(".obj file not found.")

        self.vertices = numpy.array(self.vertices, dtype="float32").flatten()
        self.tex_map  = numpy.array(self.tex_map, dtype="float32").flatten()
        self.normals  = numpy.array(self.normals, dtype="float32").flatten()
        self.indices  = numpy.array(self.indices, dtype="int32")