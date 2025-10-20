import glfw
from OpenGL.GL import *
import numpy as np


def main():
    # 1. Initialize GLFW
    if not glfw.init():
        print("Erro: Não foi possível inicializar o GLFW.")
        return

    # Request OpenGL Core Profile 3.3
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # Uncomment if needed (MacOS)

    # 2. Criação da Janela de Aplicação
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (2D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)

    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    # Triângulo (posição + cor)
    triangle_vertices = np.array([
        -0.5, -0.5, 0.0,    1.0, 0.0, 0.0, # vermelho
         0.0,  0.5, 0.0,    0.0, 1.0, 0.0, # verde
         0.5, -0.5, 0.0,    0.0, 0.0, 1.0 # azul
    ], dtype=np.float32)

    # Linha (posição + cor)
    line_vertices = np.array([
        -0.8, 0.8, 0.0,     1.0, 1.0, 0.0, # amarelo
         0.8, 0.8, 0.0,     1.0, 0.0, 1.0 # magenta
    ], dtype=np.float32)

    VAO_tri, VBO_tri = setup_geometry(triangle_vertices, [3, 3]) #x, y, z = 3 e R, G, B = 3
    VAO_line, VBO_line = setup_geometry(line_vertices, [3, 3]) #x, y, z = 3 e R, G, B = 3

    # 3.1 VAO/VBO
    # 3.2 Shaders
    # 3.3 Programa (shaders)

    #Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        #Definicao da matriz de projeção
        """ proj = np.identity(4, dtype=np.float32)
        model = translation @ rotation @ scale
        transf_matrix = proj @ model
        glUniformMatrix4fv(location, 1, GL_FALSE, model) """
        # Vincular o programa (shaders) que fará as operações
        # Envia a matriz de projeção para o shader

        # >>> Espaço para o seu código de desenho aqui (Core) <<<
            # Vincular VAOs/VBOs dos seus desenhos
        # Desenha triângulo
        glBindVertexArray(VAO_tri)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        # Desenha linha
        glBindVertexArray(VAO_line)
        glDrawArrays(GL_LINES, 0, 2)
        glBindVertexArray(0)

        # Chamadas de desenho das primitivas (usando programa/shader vinculado)

        # Desvincular VAOs/VBOs
        # Desvincular o programa (shaders)


        # Verifica e processa eventos da janela
        glfw.poll_events()

        # Troca os buffers front e back para exibir a imagem renderizada
        glfw.swap_buffers(window)


    # 5. Finalização
    glfw.terminate()

    #Também será necessário limpar os VAOs/VBOs e Program/Shaders
        #VAO
    glDeleteVertexArrays(1, VAO_tri)
    glDeleteVertexArrays(1, VAO_line)

        #VBO
    glDeleteBuffers(1, VBO_tri)
    glDeleteBuffers(1, VBO_line)

def setup_geometry(vertices, attributes):
    #VBO
    vbo = glGenBuffers(1) #cria
    glBindBuffer(GL_ARRAY_BUFFER, vbo) #vincula
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) #envia

    #VAO
    vao = glGenVertexArrays(1) #cria
    glBindVertexArray(vao) #vincula

    stride = sum(attributes) * vertices.itemsize  # total por vértice
    offset = 0
    for index, size in enumerate(attributes):
        glEnableVertexAttribArray(index)#habilita VAO
        glVertexAttribPointer(
        index, #índice do atributo
        size, #número de componentes por vértice
        GL_FLOAT, #tipo dos dados
        GL_FALSE, #normalização
        stride, #sride (tam. de cada vértice em byes)
        ctypes.c_void_p(offset) #offset (onde começa o primeiro valor)
        ) #configura
        offset += size * vertices.itemsize

    #UNBINDING
    glBindBuffer(GL_ARRAY_BUFFER, 0) #desvincula o VBO
    glBindVertexArray(0) #desvincula o VAO
    return vao, vbo

if __name__ == "__main__":
    main()