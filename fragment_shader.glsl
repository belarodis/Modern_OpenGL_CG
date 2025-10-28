#version 330 core

// Variáveis de Entrada
in vec3 vColor;
in vec2 UV;

// Variáveis de Saída
out vec4 FragColor;

uniform sampler2D frameColor;

// Processamento
void main()
{
    FragColor = texture2D(frameColor, UV.xy);
}