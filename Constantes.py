import pygame
pygame.mixer.init()
pygame.font.init()

COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)

# dimension de la pantalla
ANCHO = 1280
ALTO = 720
PANTALLA = (ANCHO,ALTO)
FPS = 30
FONDO_AJUSTES = pygame.image.load("assets/imagenes/bg_ajustes.jpg")
FONDO_CATEGORIAS = pygame.image.load("assets/imagenes/bg2.jpg")

# duracion del juego
TIEMPO_INICIAL_JUEGO = 180 # en segundos
TIEMPO_ACIERTOS_CONSECUTIVOS = 15

# 
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3
BOTON_DIFICULTAD = 4

# dimensiones
ANCHO_PREGUNTA = 700
ALTO_PREGUNTA = 150
ANCHO_BOTON = 800
ALTO_BOTON = 60
ANCHO_BOTON_MENU = 350
ALTO_BOTON_MENU = 70

# sonidos
CLICK_SONIDO = pygame.mixer.Sound("assets/sonidos/click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("assets/sonidos/error.mp3")

# fuentes
fuente = "assets/fuentes/pixelated.ttf"
FUENTE_PREGUNTA = pygame.font.Font(fuente,20)
FUENTE_RESPUESTA = pygame.font.Font(fuente,18)
FUENTE_TEXTO = pygame.font.Font(fuente,20)
FUENTE_VOLUMEN = pygame.font.Font(fuente,30)
FUENTE_DADO = pygame.font.Font(fuente,16)

# logica del juego
CANTIDAD_VIDAS = 3
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25

# puntero
PUNTERO = "assets/imagenes/puntero.png"

# constantes para los comodines
ANCHO_COMODIN = 120
ALTO_COMODIN = 50
COLOR_COMODIN_DISPONIBLE = (20, 150, 20) # color verde
COLOR_COMODIN_USADO = (80, 80, 80)      # color gris una vez que ya se usaron