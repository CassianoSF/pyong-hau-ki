import math

from Core.Texture import Texture
from Core.Font    import Font

from Object    import Object
from Loader    import Loader

class Button:
    def __init__(self, caption, font_size, color, position, camera):
        self.color = color
        self.font_size = font_size
        self.position = position
        text = Font(caption, "calibrib",color[0], color[1], color[2])
        quad_obj  = Loader("./resources/models/quad.obj")
        btn_texture = Texture("./resources/textures/button.png")
        self.text = Object(quad_obj, camera, text)
        self.text.model['rotation'] = [0, math.pi/2, 0]
        self.text.scale(self.font_size*0.04*len(caption)/10, 1, self.font_size*0.1/10)
        self.text.translate(self.position[0], self.position[1], self.position[2])

        self.btn = Object(quad_obj, camera, btn_texture)
        self.btn.model['rotation'] = [0, math.pi/2, 0]
        self.btn.scale(self.font_size*0.1*len(caption)/10, 1, self.font_size*0.2/10)
        self.btn.translate(self.position[0], self.position[1], self.position[2])

    def set_caption(self, caption):
        text = Font(caption, "calibrib", self.color[0], self.color[1], self.color[2])
        self.text.scale(self.font_size*0.04*len(caption)/10, 1, self.font_size*0.1/10)
        self.btn.scale(self.font_size*0.1*len(caption)/10, 1, self.font_size*0.2/10)
        self.text.texture.delete
        self.text.texture = text

    def click(self, event, app):
        pos_x = 6*(event.pos[0]/app.window_width*2 -1)
        pos_y = 3*(-(event.pos[1]/app.window_height*2 -1))
        return (
            self.position[0]-0.15 <= -pos_y <= self.position[0]+0.15 and 
            self.position[2]-0.4  <= -pos_x <= self.position[2]+0.4
        )

    def render(self, renderer):
        renderer.render_with_transparency(self.text)
        renderer.render_with_transparency(self.btn)
