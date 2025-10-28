#version 330 core

// Variáveis de Entrada
layout (location = 0) in vec3 aPos; //Vértice
layout (location = 1) in vec2 aTexCoord; //Coord de text
layout (location = 2) in vec3 aColor; //Cor vinda dos vértices

// Variáveis de Saída
out vec2 UV;
out vec3 vColor;

// Processamento (sem matriz por enquanto)
void main()
{
    gl_Position = vec4(aPos, 1.0);
    UV = aTexCoord;
    vColor = aColor;
}