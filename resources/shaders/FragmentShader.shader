#version 330 core

// Interpolated values from the vertex shaders
in vec2 UV;
in vec3 triangle_position;
in vec3 Normal_cameraspace;
in vec3 EyeDirection_cameraspace;
in vec3 LightDirection_cameraspace;

// Ouput data
out vec3 color;

// Values that stay constant for the whole mesh.
uniform sampler2D TextureSampler;
uniform vec3 LightPosition;

void main(){

	// Light emission properties
	// You probably want to put them as uniforms
	vec3 LightColor = vec3(1,1,1);
	float LightPower = 1000.0f;
	
	// Material properties
	vec3 MaterialDiffuseColor = texture( TextureSampler, UV ).rgb * vec3(1,1,1);
	vec3 MaterialAmbientColor = vec3(0.1,0.1,0.1) * MaterialDiffuseColor;
	vec3 MaterialSpecularColor = vec3(0.9,0.9,0.9);

	// Distance to the light
	float distance = length( LightPosition - triangle_position );

	// Normal of the computed fragment, in camera space
	vec3 n = normalize( Normal_cameraspace );
	// Direction of the light (from the fragment to the light)
	vec3 l = normalize( LightDirection_cameraspace );
	// Cosine of the angle between the normal and the light direction, 
	float cosTheta = max( dot( n,l ), 0.0 );
	
	// Eye vector (towards the camera)
	vec3 eye = normalize(EyeDirection_cameraspace);
	// Direction in which the triangle reflects the light
	vec3 reflex = reflect(-l,n);
	// Cosine of the angle between the Eye vector and the Reflect vector,
	float cosAlpha = max( dot( eye,reflex ), 0.0);
	
	vec3 ambient = MaterialAmbientColor;
	vec3 diffuse = MaterialDiffuseColor * LightColor * LightPower * cosTheta / (distance*distance);
	vec3 specular = MaterialSpecularColor * LightColor * LightPower * pow(cosAlpha,32) / (distance*distance);
	
	color = ambient + diffuse + specular;
}