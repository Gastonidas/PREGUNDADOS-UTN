import pygame
from Constantes import *
from funciones import *

# Crear el botón para volver al menú
boton_volver = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", 200, 40, 10, 10)

def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg2.jpg"), PANTALLA)
    pantalla.blit(fondo_pantalla, (0, 0))
    
    retorno = "rankings"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    # --- Interfaz de Rankings (con llamadas a mostrar_texto corregidas) ---
    
    # Botón VOLVER
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"], "VOLVER", FUENTE_RESPUESTA, COLOR_BLANCO, boton_volver['superficie'].get_rect(), center_align=True)

    # Título de la pantalla
    titulo_rect = pygame.Rect(0, 100, ANCHO, 50)
    mostrar_texto(pantalla, "MEJORES PUNTAJES", FUENTE_VOLUMEN, COLOR_BLANCO, titulo_rect, center_align=True)

    # Obtener y mostrar el top 10 de puntajes
    top_10 = obtener_top_10()
    
    if not top_10:
        # Mensaje si no hay puntajes guardados
        mensaje_rect = pygame.Rect(0, 250, ANCHO, 50)
        mostrar_texto(pantalla, "Aun no hay puntajes guardados.", FUENTE_TEXTO, COLOR_BLANCO, mensaje_rect, center_align=True)
    else:
        # Mostrar cada puntaje en la lista
        pos_y_inicial = 200
        for i, partida in enumerate(top_10, 1):
            texto_rank = f"{i}. {partida['nombre']} - {partida['puntaje']} pts"
            rank_rect = pygame.Rect(0, pos_y_inicial + (i * 40), ANCHO, 40)
            mostrar_texto(pantalla, texto_rank, FUENTE_TEXTO, COLOR_BLANCO, rank_rect, center_align=True)

    return retorno