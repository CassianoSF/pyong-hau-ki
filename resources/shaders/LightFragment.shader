#version 330 core

// Interpolated values from the vertex shaders
in vec2 UV;
in vec3 triangle_position;
in vec3 Normal_cameraspace;
in vec3 EyeDirection_cameraspace;
// LIGHT DIRECTION IN

// Ouput data
out vec3 color;

// Values that stay constant for the whole mesh.
uniform sampler2D TextureSampler;


// LIGHT POSITION

// LIGHT COLOR

// LIGHT POWER

vec3 calcLight(vec3 LightPos, vec3 LightColor, int LightPower, vec3 LightDirection){
    // Material properties
    vec3 MaterialDiffuseColor = texture( TextureSampler, UV ).rgb * vec3(0.8,0.8,0.8);
    vec3 MaterialAmbientColor = vec3(0.05,0.05,0.05) * MaterialDiffuseColor;
    vec3 MaterialSpecularColor = vec3(0.9,0.9,0.9);

    // Distance to the light
    float distance = length( LightPos - triangle_position );

    // Normal of the computed fragment, in camera space
    vec3 n = normalize( Normal_cameraspace );
    // Direction of the light (from the fragment to the light)
    vec3 l = normalize( LightDirection );
    // Cosine of the angle between the normal and the light direction, 
    float cosTheta = clamp(dot( n,l ), 0,1);
    
    // Eye vector (towards the camera)
    vec3 eye = normalize(EyeDirection_cameraspace);
    // Direction in which the triangle reflects the light
    vec3 reflex = reflect(-l,n);
    // Cosine of the angle between the Eye vector and the Reflect vector,
    float cosAlpha = clamp(dot( eye,reflex ), 0,1);
    
    vec3 ambient = MaterialAmbientColor;
    vec3 diffuse = MaterialDiffuseColor * LightColor * LightPower * cosTheta / (distance*distance);
    vec3 specular = MaterialSpecularColor * LightColor * LightPower * cosTheta * pow(cosAlpha,32) / (distance*distance);
    return ambient + diffuse + specular;
}

void main(){
// COLORS
}