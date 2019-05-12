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
out vec3 LightDirection_cameraspace1;
out vec3 LightDirection_cameraspace2;
out vec3 LightDirection_cameraspace3;

// Values that stay constant for the whole mesh.
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;
uniform vec3 LightPosition1;
uniform vec3 LightPosition2;
uniform vec3 LightPosition3;

void main(){

	mat4 MVP = transpose(model * view * projection);
	// Output position of the vertex, in clip space : MVP * position
	gl_Position =  MVP * vec4(vertexPositions,1);
	
	// Position of the vertex, in worldspace : model * position
	triangle_position = (model * vec4(vertexPositions,1)).xyz;
	
	// Vector that goes from the vertex to the camera, in camera space.
	EyeDirection_cameraspace = vec3(1,1,1) - ( view * model * vec4(vertexPositions,1)).xyz;

	// Vector that goes from the vertex to the light, in camera space. model is ommited because it's identity.
	LightDirection_cameraspace1 = ( view * vec4(LightPosition1,1)).xyz - EyeDirection_cameraspace;
	LightDirection_cameraspace2 = ( view * vec4(LightPosition2,1)).xyz - EyeDirection_cameraspace;
	LightDirection_cameraspace3 = ( view * vec4(LightPosition3,1)).xyz - EyeDirection_cameraspace;
	
	// Normal of the the vertex, in camera space
	Normal_cameraspace = ( view * model * vec4(vertexNormals,0)).xyz;
	
	// UV of the vertex. No special space for this one.
	UV = vertexUVs;
}