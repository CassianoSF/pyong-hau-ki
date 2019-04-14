import pygame, numpy, pyrr, math, os, string
from OpenGL.GL import *

from Core.Shader        import Shader
from Core.VertexBuffer  import VertexBuffer
from Core.VertexArray   import VertexArray
from Core.IndexBuffer   import IndexBuffer
from Core.Texture       import Texture

class Object():
    def __init__(self, loader):
        self.vertices = loader.vertices
        self.indices = loader.indices
        self.tex_map = loader.tex_map
        self.normals = loader.normals
        self.texture = loader.texture
        self.shader = loader.shader
        
        self.va = VertexArray()
        self.vb_positions = VertexBuffer(self.vertices)
        self.va.add_buffer(0, 3, self.vb_positions)
        self.vb_texture = VertexBuffer(self.tex_map)
        self.va.add_buffer(1, 2, self.vb_texture)
        self.ib = IndexBuffer(self.indices)
        self.model = {
            'translation': [0.0, 0.0, 0.0],
            'rotation':    [0.0, 0.0, 0.0],
            'scale':       [1.0, 1.0, 1.0]
        }

    def translate(self, x, y, z):
        self.model['translation'] = [
            self.model['translation'][0] + x,
            self.model['translation'][1] + y,
            self.model['translation'][2] + z
        ]

    def scale(self, x, y, z):
        self.model['scale'] = [x,y,z]

    def mount_mvp(self, camera):
            trans_matrix = numpy.transpose(pyrr.matrix44.create_from_translation(self.model['translation']))
            rot_matrix_x = numpy.transpose(pyrr.matrix44.create_from_x_rotation(self.model['rotation'][0]))
            rot_matrix_y = numpy.transpose(pyrr.matrix44.create_from_y_rotation(self.model['rotation'][1]))
            rot_matrix_z = numpy.transpose(pyrr.matrix44.create_from_z_rotation(self.model['rotation'][2]))
            rot_matrix   = numpy.matmul(numpy.matmul(rot_matrix_x, rot_matrix_y),rot_matrix_z)
            scale_matrix = numpy.transpose(pyrr.matrix44.create_from_scale(self.model['scale'] ))
            model_matrix = numpy.matmul(numpy.matmul(trans_matrix,rot_matrix),scale_matrix)

            view_matrix = numpy.transpose(pyrr.matrix44.create_look_at(
                numpy.array(camera.view['position'], dtype="float32"),
                numpy.array(camera.view['target'],   dtype="float32"),
                numpy.array(camera.view['up'],       dtype="float32")
            ))

            if camera.orthogonal:
                proj_matrix = numpy.transpose(pyrr.matrix44.create_orthogonal_projection_matrix(-6, 6, -3, 3, 0.001, 300, dtype=None))
            
            else:
                proj_matrix = numpy.transpose(pyrr.matrix44.create_perspective_projection(
                    camera.projection['fovy'],
                    camera.projection['aspect'],
                    camera.projection['near'],
                    camera.projection['far'],
                    camera.projection['dtype']
                ))

            m = numpy.matmul(numpy.matmul(proj_matrix,view_matrix),model_matrix) 
            return numpy.transpose(m)


    def render(self, camera):

        mvp = self.mount_mvp(camera)

        self.texture.bind()
        self.shader.add_uniform_1i("the_texture", 0)
        self.shader.add_uniform_matrix_4f("mvp", mvp)
        self.shader.bind()
        self.va.bind()
        self.ib.bind()
        glDrawElements(GL_TRIANGLES, self.va.size, GL_UNSIGNED_INT, None)