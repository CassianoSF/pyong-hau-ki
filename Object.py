import numpy, pyrr

from Core.VertexArray   import VertexArray
from Core.VertexBuffer  import VertexBuffer
from Core.IndexBuffer   import IndexBuffer

class Object():
    def __init__(self, obj, camera, texture, color=[1,1,1]):
        self.color = color

        self.indices = obj.indices
        self.vertices = obj.vertices
        self.tex_map = obj.tex_map
        self.normals = obj.normals

        self.texture = texture
        self.camera = camera
        
        self.va = VertexArray()
        
        self.vb_positions = VertexBuffer(self.vertices)
        self.va.add_buffer(0, 3, self.vb_positions)
        
        self.vb_texture = VertexBuffer(self.tex_map)
        self.va.add_buffer(1, 2, self.vb_texture)
        
        self.vb_normals = VertexBuffer(self.normals)
        self.va.add_buffer(2, 3, self.vb_normals)
        
        self.ib = IndexBuffer(self.indices)

        self.model = {
            'translation': [0.0, 0.0, 0.0],
            'rotation':    [0.0, 0.0, 0.0],
            'scale':       [1.0, 1.0, 1.0]
        }
        self.model_matrix = []
        self.view_matrix = []   
        self.proj_matrix = []   

    def translate(self, x, y, z):
        self.model['translation'] = [
            self.model['translation'][0] + x,
            self.model['translation'][1] + y,
            self.model['translation'][2] + z
        ]

    def scale(self, x, y, z):
        self.model['scale'] = [x,y,z]

    def mount_mvp(self):
        trans_matrix = numpy.transpose(pyrr.matrix44.create_from_translation(self.model['translation']))
        rot_matrix_x = numpy.transpose(pyrr.matrix44.create_from_x_rotation(self.model['rotation'][0]))
        rot_matrix_y = numpy.transpose(pyrr.matrix44.create_from_y_rotation(self.model['rotation'][1]))
        rot_matrix_z = numpy.transpose(pyrr.matrix44.create_from_z_rotation(self.model['rotation'][2]))
        rot_matrix   = numpy.matmul(numpy.matmul(rot_matrix_x, rot_matrix_y),rot_matrix_z)
        scale_matrix = numpy.transpose(pyrr.matrix44.create_from_scale(self.model['scale'] ))
        self.model_matrix = numpy.matmul(numpy.matmul(trans_matrix,rot_matrix),scale_matrix)

        self.view_matrix = numpy.transpose(pyrr.matrix44.create_look_at(
            numpy.array(self.camera.view['position'], dtype="float32"),
            numpy.array(self.camera.view['target'],   dtype="float32"),
            numpy.array(self.camera.view['up'],       dtype="float32")
        ))

        if self.camera.orthogonal:
            self.proj_matrix = numpy.transpose(
                pyrr.matrix44.create_orthogonal_projection_matrix(
                    -6, 6, -3, 3, 0.001, 300, dtype=None))
        
        else:
            self.proj_matrix = numpy.transpose(pyrr.matrix44.create_perspective_projection(
                self.camera.projection['fovy'],
                self.camera.projection['aspect'],
                self.camera.projection['near'],
                self.camera.projection['far'],
                self.camera.projection['dtype']
            ))

    def bind(self):
        self.texture.bind()
        self.va.bind()
        self.ib.bind()