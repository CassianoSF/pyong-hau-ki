#version 330 core

in vec2 final_text_coord;

out vec4 color;

uniform sampler2D the_texture;

void main() {
    vec4 tex_color = texture(the_texture, final_text_coord);
    if(tex_color.a < 0.1)
        discard;
    color = tex_color;
}