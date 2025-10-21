#version 330 core

// Variáveis de Entrada
layout (location = 0) in vec3 aPos; //Vértice
layout (location = 1) in vec3 aColor; //Cor

// Variáveis de Saída
out vec3 vColor;

// Processamento (sem matriz por enquanto)
void main()
{
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
}