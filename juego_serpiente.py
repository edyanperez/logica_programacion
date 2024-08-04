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

# Función para mostrar la puntuación
def your_score(score):
    # Crear un rectángulo para la barra superior
    pygame.draw.rect(dis, GREY, [0, 0, WIDTH, TOP_BAR_HEIGHT])  # Color de fondo para el encabezado
    # Renderizar el texto de la puntuación
    value = score_font.render("Tu Puntuación: " + str(score), True, BLACK)  # Texto en negro para mejor visibilidad
    # Mostrar el texto de puntuación en la barra superior
    dis.blit(value, [10, 10])

# Función para dibujar la serpiente
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])  # Dibujar cada bloque de la serpiente

# Función para mostrar mensajes
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)  # Crear el mensaje
    mesg_rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + TOP_BAR_HEIGHT + y_displace))  # Centrando el mensaje
    dis.blit(mesg, mesg_rect)  # Colocar el mensaje en la pantalla

# Función de pantalla de inicio
def game_intro():
    intro = True
    while intro:
        dis.fill(WHITE)  # Fondo blanco

        # Mensaje de bienvenida
        draw_text("Bienvenido al Juego de la Serpiente", score_font, BLUE, dis, WIDTH // 2, HEIGHT // 4)
        draw_text("Selecciona el modo de juego", font_style, BLACK, dis, WIDTH // 2, HEIGHT // 3)
        # Botones para seleccionar modo
        button("Modo Normal", 150, 350, 150, 50, GREEN, BLUE, "mode_normal")
        button("Modo Desafío", 500, 350, 150, 50, GREEN, BLUE, "mode_challenge")

        pygame.display.update()  # Actualizar pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
            # Mensaje de pérdida con fuente ajustada para asegurar que quepa en la pantalla
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
                if event.key == pygame.K_LEFT:  # Movimiento a la izquierda
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:  # Movimiento a la derecha
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:  # Movimiento hacia arriba
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:  # Movimiento hacia abajo
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
        pygame.draw.rect(dis, BLUE, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)  # Añadir la nueva posición de la cabeza

        # Eliminar la parte más antigua de la serpiente si es más larga de lo necesario
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Verificar colisión con el cuerpo de la serpiente
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Dibujar la serpiente
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)  # Mostrar la puntuación

        pygame.display.update()  # Actualizar la pantalla

        # Verificar si la serpiente ha comido la fruta
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            # Generar nueva fruta
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(TOP_BAR_HEIGHT, HEIGHT - snake_block) / snake_block) * snake_block
            Length_of_snake += 1  # Aumentar la longitud de la serpiente
            fruits_eaten += 1  # Incrementar contador de frutas comidas

            # Verificar si se ha completado el desafío
            if mode.startswith('challenge') and fruits_eaten >= challenge_goal:
                challenge_completed = True
                challenge_active = False

        # Mostrar mensaje de desafío completado
        if challenge_completed:
            message("¡Desafío completado! Recibes una recompensa.", GREEN, 20)
            pygame.display.update()
            time.sleep(2)  # Pausa de 2 segundos para mostrar el mensaje
            challenge_completed = False
            game_close = True  # Finalizar juego tras completar el desafío

        clock.tick(snake_speed)  # Controlar la velocidad del juego

    pygame.quit()  # Cerrar pygame
    quit()  # Salir del programa

# Función para crear botones interactivos
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()  # Obtener posición del ratón
    click = pygame.mouse.get_pressed()  # Obtener estado del clic del ratón

    # Dibujar el botón e identificar si se hace clic
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))  # Cambiar color al pasar el ratón

        if click[0] == 1 and action is not None:  # Si se hace clic
            if action == "mode_normal":
                gameLoop()  # Iniciar juego normal
            elif action == "mode_challenge":
                challenge_selection()  # Selección de desafío
            elif action == "challenge1":
                gameLoop("challenge_1")  # Iniciar desafío 1
            elif action == "random_challenge":
                gameLoop("challenge_random")  # Iniciar desafío aleatorio
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))  # Dibujar botón

    # Dibujar el texto del botón
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf = smallText.render(msg, True, BLACK)
    textRect = textSurf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    dis.blit(textSurf, textRect)

# Función para selección de desafío
def challenge_selection():
    selecting = True
    while selecting:
        dis.fill(WHITE)  # Limpiar la pantalla

        # Mensaje de selección de desafío
        draw_text("Seleccione el desafío:", font_style, BLACK, dis, WIDTH // 2, 100)
        button("Desafío 1", 150, 200, 150, 50, RED, BLUE, "challenge1")
        button("Desafío Aleatorio", 500, 200, 150, 50, RED, BLUE, "random_challenge")

        pygame.display.update()  # Actualizar la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)  # Crear objeto de texto
    textrect = textobj.get_rect(center=(x, y))  # Posicionar el texto
    surface.blit(textobj, textrect)  # Dibujar texto en la pantalla

# Función principal
def main():
    game_intro()  # Iniciar pantalla de bienvenida

if __name__ == "__main__":
    main()  # Ejecutar el juego
