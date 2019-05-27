#version 330 core

// Input vertex data, different for all executions of this shader.
layout(location = 0) in vec3 vertexPositions;
layout(location = 1) in vec2 vertexUVs;
layout(location = 2) in vec3 vertexNormals;

// Output data ; will be interpolated for each fragment.
out vec2 UV;
out vec3 triangle_position;
out vec3 Normal_cameraspace;
out vec3 EyeDirection_cameraspace;
// LIGHT DIRECTION OUT

// Values that stay constant for the whole mesh.
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

// LIGHT POSITIONS

void main(){

    mat4 MVP = transpose(model * view * projection);
    // Output position of the vertex, in clip space : MVP * position
    gl_Position =  MVP * vec4(vertexPositions,1);
    
    // Position of the vertex, in worldspace : model * position
    triangle_position = (vec4(vertexPositions,1) * model).xyz;
    
    // Vector that goes from the vertex to the camera, in camera space.
    EyeDirection_cameraspace = - ( view * (vec4(vertexPositions,1) * model) ).xyz;

    // Vector that goes from the vertex to the light, in camera space. model is ommited because it's identity.
// LIGHT DIRECTION
    
    // Normal of the the vertex, in camera space
    Normal_cameraspace = ( view * vec4(vertexNormals,0)).xyz;
    // Normal_cameraspace = mat3(transpose(inverse(model))) * vertexNormals;
    
    // UV of the vertex. No special space for this one.
    UV = vertexUVs;
}