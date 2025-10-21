import glfw, math, ctypes
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

    # 2. Criação da Janela de Aplicação
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (2D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)

    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    scale = np.array([
        [2.0, 0.0, 0.0, 0.0],
        [0.0, 1.5, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    angle = math.radians(45)
    rotation = np.array([
        [ math.cos(angle), -math.sin(angle), 0.0, 0.0],
        [ math.sin(angle),  math.cos(angle), 0.0, 0.0],
        [ 0.0,              0.0,             1.0, 0.0],
        [ 0.0,              0.0,             0.0, 1.0]
    ])

    translation = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0], 
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    # Triângulo (posição + cor)
    triangle_vertices = np.array([
        -0.7, -0.5, 0.0, 1.0, 0.0, 0.0, # V1
         0.0, -0.5, 0.0, 0.0, 1.0, 0.0, # V2
        -0.35, 0.5, 0.0, 0.0, 0.0, 1.0 # V3
    ], dtype=np.float32)

    # Linha (posição + cor)
    square_vertices = np.array([
        0.2, -0.5, 0.0, 1.0, 0.5, 0.2, # T1 V1
        0.7, -0.5, 0.0, 1.0, 0.5, 0.2, # T1 V2
        0.7,  0.5, 0.0, 1.0, 0.5, 0.2, # T1 V3
        0.2, -0.5, 0.0, 1.0, 0.5, 0.2, # T2 V1
        0.7,  0.5, 0.0, 1.0, 0.5, 0.2, # T2 V2
        0.2,  0.5, 0.0, 1.0, 0.5, 0.2 # T2 V3
    ], dtype=np.float32)

    VAO_tri, VBO_tri = setup_geometry(triangle_vertices, [3, 3]) #x, y, z = 3 e R, G, B = 3
    VAO_sqr, VBO_sqr = setup_geometry(square_vertices, [3, 3]) #x, y, z = 3 e R, G, B = 3

    # 3.1 VAO/VBO
    # 3.2 Shaders
    # 3.3 Programa (shaders)

    #Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)

    # Vincular o programa (shaders) que fará as operações
    with open('vertex_shader.glsl', 'r') as file:
        vshader = create_shader(GL_VERTEX_SHADER, file.read())
    with open('fragment_shader.glsl', 'r') as file:
        fshader = create_shader(GL_FRAGMENT_SHADER, file.read())

    program = glCreateProgram()
    glAttachShader(program, vshader) #vincula o shader ao programa (1 por 1)
    glAttachShader(program, fshader) #vincula o shader ao programa (1 por 1)
    glLinkProgram(program) #linka todos os shaders para poderem conversar entre si dentro do programa

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Definicao da matriz de projeção
        #transf_matrix = translation @ rotation @ scale
        

        # Matriz de transformação
        # mtx_loc = glGetUniformLocation(program, "uModel")
        # glUniformMatrix4fv(mtx_loc, 1, GL_FALSE, identity_matrix)

        # >>> Espaço para o seu código de desenho aqui (Core) <<<
            # Vincular VAOs/VBOs dos seus desenhos
        # Desenha triângulo
        glUseProgram(program)
        glBindVertexArray(VAO_tri)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        # Desenha quadrado
        glBindVertexArray(VAO_sqr)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        glUseProgram(0)

        # Verifica e processa eventos da janela
        glfw.poll_events()

        # Troca os buffers front e back para exibir a imagem renderizada
        glfw.swap_buffers(window)

    #Também será necessário limpar os VAOs/VBOs e Program/Shaders
        #VAO
    glDeleteVertexArrays(1, [VAO_tri])
    glDeleteVertexArrays(1, [VAO_sqr])

        #VBO
    glDeleteBuffers(1, [VBO_tri])
    glDeleteBuffers(1, [VBO_sqr])

        #SHADER PROGRAM
    glDeleteProgram(program)

    # 5. Finalização
    glfw.terminate()

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

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type) #cria o shader dependendo do tipo enviado no parametro -> GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
    glShaderSource(shader, source) #vincula o código .glsl ao shader criado
    glCompileShader(shader) #complila o shader
    
    return shader

if __name__ == "__main__":
    main()