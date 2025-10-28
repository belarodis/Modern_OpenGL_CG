#version 330 core

// Variáveis de Entrada
in vec3 vColor;
in vec2 UV;

// Variáveis de Saída
out vec4 FragColor;

uniform sampler2D frameColor;
uniform int controller;

// Processamento
void main()
{
    if (controller == 1) {
        FragColor = texture2D(frameColor, UV.xy);
    } else {
        FragColor = vec4(vColor, 1);
    }
}