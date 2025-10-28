#version 330 core

// Variáveis de Entrada
layout (location = 0) in vec3 aPos; //Vértice
layout (location = 1) in vec2 aTexCoord; //Coord de text

// Variáveis de Saída
out vec3 vColor;
out vec2 UV;

// Processamento (sem matriz por enquanto)
void main()
{
    gl_Position = vec4(aPos, 1.0);
    vColor = vec3(aTexCoord, 1);
    UV = aTexCoord;
}