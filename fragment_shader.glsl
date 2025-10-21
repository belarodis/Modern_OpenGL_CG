#version 330 core

// Variáveis de Entrada
in vec3 vColor;

// Variáveis de Saída
out vec4 FragColor;

// Processamento
void main()
{
    FragColor = vec4(vColor, 1.0);
}