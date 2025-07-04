import pygame 

pygame.init()
pygame.mixer.init()
from Constantes import *
from pantallas.Menu import *
from pantallas.Juego import *
from pantallas.Ajustes import *
from pantallas.Rankings import *
from pantallas.Final import *
from pantallas.Categorias import * 
from funciones import *

pantalla = pygame.display.set_mode(PANTALLA)
puntero_img = pygame.transform.scale(pygame.image.load(PUNTERO).convert_alpha(), (32, 32))
pygame.display.set_caption("PREGUNDADOS")
icono = pygame.image.load("assets/imagenes/pregmi.png")
pygame.display.set_icon(icono)
pygame.mouse.set_visible(False)

datos_juego = {"puntuacion": 0,
                "vidas": CANTIDAD_VIDAS,
                "tiempo_restante": TIEMPO_INICIAL_JUEGO,
                "indice": 0, 
                "volumen_musica": 100, 
                "muteado": False, 
                "input_active": False,
                "nombre_jugador_input": "",
                "comodines": {"bomba": True,"x2": True,"doble_chance": True,"pasar": True},
                "x2_activo": False,
                "doble_chance_activa": False
                }

pygame.mixer.music.load("assets/sonidos/musica.mp3")
pygame.mixer.music.set_volume(datos_juego["volumen_musica"])
pygame.mixer.music.play(-1)

corriendo = True
reloj = pygame.time.Clock()
ventana_actual = "menu"

while corriendo:
    """
    el main gestiona la navegacion entre las pantallas
    """
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            corriendo = False

    if ventana_actual == "menu":
        reiniciar_estadisticas(datos_juego)
        resultado_menu = mostrar_menu(pantalla, cola_eventos)
        if resultado_menu == "juego":
            ventana_actual = "categorias"
        else:
            ventana_actual = resultado_menu
    
    elif ventana_actual == "categorias":
        ventana_actual = mostrar_categorias(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "juego":
        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "fin_partida":
        ventana_actual = mostrar_fin_partida(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "salir":
        corriendo = False

    if not corriendo:
        break
    
    dibujar_puntero_pixelado(pantalla, puntero_img)
    pygame.display.flip()

pygame.quit()