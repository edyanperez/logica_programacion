import pygame  # Importar la librería pygame
import time  # Importar la librería time para pausar
import random  # Importar la librería random para la generación aleatoria de números

# Inicializar Pygame
pygame.init()

# Definición de colores en RGB
WHITE = (255, 255, 255)  # Blanco
BLACK = (0, 0, 0)  # Negro
RED = (213, 50, 80)  # Rojo
GREEN = (0, 255, 0)  # Verde
BLUE = (50, 153, 213)  # Azul
GREY = (169, 169, 169)  # Gris
YELLOW = (255, 255, 0)  # Amarillo para la cabeza de la serpiente

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600  # Aumentar tamaño para una mejor visualización
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego de la Serpiente')

# Altura de la barra superior
TOP_BAR_HEIGHT = 50

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Tamaño y velocidad de la serpiente
snake_block = 15
snake_speed = 15

# Fuentes para texto
font_style = pygame.font.SysFont("bahnschrift", 25)  # Fuente más pequeña para mensajes de pérdida
score_font = pygame.font.SysFont("comicsansms", 35)  # Fuente para la puntuación

# Variables globales
player_name = ""  # Nombre del jugador

# Función para mostrar la puntuación
def your_score(score):
    pygame.draw.rect(dis, GREY, [0, 0, WIDTH, TOP_BAR_HEIGHT])  # Color de fondo para el encabezado
    value = score_font.render(f"Jugador: {player_name}  |  Puntuación: " + str(score), True, BLACK)  # Texto en negro
    dis.blit(value, [10, 10])

# Función para dibujar la serpiente
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Si es la cabeza
            pygame.draw.rect(dis, YELLOW, [x[0], x[1], snake_block, snake_block])  # Cabeza en amarillo
        else:
            pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])  # Cuerpo en verde

# Función para mostrar mensajes
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)  # Crear el mensaje
    mesg_rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + TOP_BAR_HEIGHT + y_displace))  # Centrando el mensaje
    dis.blit(mesg, mesg_rect)  # Colocar el mensaje en la pantalla

# Función de pantalla de inicio
def game_intro():
    global player_name
    intro = True
    name_entered = False  # Variable para controlar si el nombre fue ingresado

    while intro:
        dis.fill(WHITE)  # Fondo blanco

        if not name_entered:
            # Campo para ingresar el nombre del jugador
            player_name = input_name()
            name_entered = True  # Marcar que el nombre fue ingresado

        # Mensaje de bienvenida
        draw_text("Bienvenido al Juego de la Serpiente", score_font, BLUE, dis, WIDTH // 2, HEIGHT // 4)
        draw_text("Selecciona el modo de juego", font_style, BLACK, dis, WIDTH // 2, HEIGHT // 3)

        # Botones para seleccionar modo
        button("Modo Normal", 150, 400, 150, 50, GREEN, BLUE, "mode_normal")
        button("Modo Desafío", 500, 400, 150, 50, GREEN, BLUE, "mode_challenge")

        pygame.display.update()  # Actualizar pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Función para ingresar el nombre del jugador
def input_name():
    name = ""
    input_active = True
    while input_active:
        dis.fill(WHITE)
        draw_text("Ingresa tu nombre:", font_style, BLACK, dis, WIDTH // 2, HEIGHT // 2)
        draw_text(name, font_style, BLUE, dis, WIDTH // 2, HEIGHT // 2 + 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter para confirmar
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Borrar el último carácter
                    name = name[:-1]
                else:
                    name += event.unicode  # Agregar el carácter a la cadena

    return name

# Función principal del juego
def gameLoop(mode='normal'):
    game_over = False  # Indica si el juego ha terminado
    game_close = False  # Indica si el jugador ha perdido

    # Variables de posición de la serpiente
    x1 = WIDTH / 2
    y1 = (HEIGHT / 2) + (TOP_BAR_HEIGHT / 2)  # Ajustar posición inicial debajo de la barra

    # Cambios en la posición
    x1_change = 0
    y1_change = 0

    snake_List = []  # Lista para las partes de la serpiente
    Length_of_snake = 1  # Longitud inicial de la serpiente

    # Generación de la fruta en una posición aleatoria
    foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(TOP_BAR_HEIGHT, HEIGHT - snake_block) / snake_block) * snake_block

    # Variables de modo de juego
    challenge_selected = False

    # Desafío diario
    challenge_active = False
    challenge_goal = 5  # Número de frutas para completar el desafío
    fruits_eaten = 0  # Frutas comidas
    challenge_completed = False  # Estado del desafío

    # Desafíos específicos
    if mode == 'challenge_1':
        challenge_goal = 10  # Ejemplo: meta del desafío 1
    elif mode == 'challenge_random':
        challenge_goal = random.randint(5, 15)  # Ejemplo: meta aleatoria

    while not game_over:  # Bucle principal del juego

        while game_close:  # Cuando el jugador pierde
            dis.fill(WHITE)  # Limpiar la pantalla
            your_score(Length_of_snake - 1)  # Mostrar puntuación final
            message("¡Has perdido! Presiona C para reiniciar", RED, -50)
            message("Q para salir o M para menú", RED, 0)
            pygame.display.update()  # Actualizar la pantalla

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Opción de salir
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # Reiniciar el juego
                        gameLoop(mode)
                    if event.key == pygame.K_m:  # Volver al menú principal
                        game_intro()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:  # Detectar teclas presionadas
                if event.key == pygame.K_LEFT and x1_change == 0:  # Movimiento a la izquierda
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:  # Movimiento a la derecha
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:  # Movimiento hacia arriba
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:  # Movimiento hacia abajo
                    y1_change = snake_block
                    x1_change = 0

        # Verificación de colisiones con los bordes
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < TOP_BAR_HEIGHT:
            game_close = True

        # Actualizar la posición de la serpiente
        x1 += x1_change
        y1 += y1_change
        dis.fill(WHITE)  # Limpiar la pantalla

        # Dibujar el borde del área de juego
        pygame.draw.rect(dis, BLACK, [0, TOP_BAR_HEIGHT, WIDTH, HEIGHT - TOP_BAR_HEIGHT], 2)

        # Dibujar la fruta
        pygame.draw.rect(dis, RED, [foodx, foody, snake_block, snake_block])

        # Actualizar la lista de la serpiente
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # Mantener la longitud de la serpiente
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Verificar colisión con el cuerpo de la serpiente
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Dibujar la serpiente
        our_snake(snake_block, snake_List)

        # Mostrar la puntuación
        your_score(Length_of_snake - 1)

        pygame.display.update()  # Actualizar la pantalla

        # Verificar si la serpiente ha comido la fruta
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(TOP_BAR_HEIGHT, HEIGHT - snake_block) / snake_block) * snake_block
            Length_of_snake += 1  # Aumentar la longitud de la serpiente
            fruits_eaten += 1  # Aumentar el contador de frutas comidas

            # Verificar si se ha completado un desafío
            if fruits_eaten >= challenge_goal:
                challenge_completed = True  # Marcar el desafío como completado

        # Terminar el juego si el desafío está completo y la serpiente ha chocado
        if challenge_completed and game_close:
            game_close = True
            game_over = True

        clock.tick(snake_speed)  # Controlar la velocidad del juego

    pygame.quit()  # Salir de pygame
    quit()  # Salir del script

# Función para dibujar texto centrado
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Función para los botones del menú
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "mode_normal":
                gameLoop('normal')
            elif action == "mode_challenge":
                gameLoop('challenge')
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    textSurf = font_style.render(msg, True, BLACK)
    textRect = textSurf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    dis.blit(textSurf, textRect)

# Iniciar la pantalla de introducción
game_intro()
