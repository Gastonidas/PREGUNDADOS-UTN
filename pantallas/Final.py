import pygame
from datetime import datetime
from Constantes import * 
from funciones import *

fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg_final.jpg"), PANTALLA)
input_caja_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 60, 300, 40)
boton_guardar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 160, 200, 50)

def mostrar_fin_partida(pantalla: pygame.Surface, cola_eventos: list[pygame.event.
Event], datos_juego: dict) -> str:
    """
     pantalla final. gestiona el input del nombre del jugador que se almacena en partidas.json y luego, si entra en el top 10, se puede visualizar en la pantalla de rankings
    """
    pantalla.blit(fondo_pantalla,(0,0))
    
    retorno = "fin_partida" 
    

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if input_caja_rect.collidepoint(evento.pos):
                datos_juego["input_active"] = not datos_juego["input_active"] 
            else:
                datos_juego["input_active"] = False 

            if boton_guardar_rect.collidepoint(evento.pos):
                nombre_jugador = datos_juego["nombre_jugador_input"].strip()
                if nombre_jugador:
                    guardar_partida(nombre_jugador, datos_juego["puntuacion"])
                    datos_juego["nombre_jugador_input"] = "" 
                    datos_juego["input_active"] = False 
                    retorno = "menu" 
        
        elif evento.type == pygame.KEYDOWN:
            if datos_juego["input_active"]:
                if evento.key == pygame.K_BACKSPACE:
                    datos_juego["nombre_jugador_input"] = datos_juego["nombre_jugador_input"][:-1]
                else:
                    if len(datos_juego["nombre_jugador_input"]) < 15 and evento.unicode.isprintable():
                        datos_juego["nombre_jugador_input"] += evento.unicode

    mostrar_texto(pantalla, "PARTIDA FINALIZADA", FUENTE_PREGUNTA, COLOR_ROJO, pygame.Rect(0, ALTO // 2 - 150, ANCHO, 50), center_align=True)
    mostrar_texto(pantalla, f"Puntaje Final: {datos_juego['puntuacion']}", FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(0, ALTO // 2 - 80, ANCHO, 50), center_align=True)
    mostrar_texto(pantalla, "Ingresa tu nombre:", FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(input_caja_rect.x, input_caja_rect.y - 50, 300, 50))
    
    # dibujo caja input
    pygame.draw.rect(pantalla, COLOR_BLANCO, input_caja_rect, 2) # borde
    pygame.draw.rect(pantalla, COLOR_NEGRO, input_caja_rect) # fondo
    input_texto = FUENTE_TEXTO.render(datos_juego["nombre_jugador_input"], True, COLOR_BLANCO)
    pantalla.blit(input_texto, (input_caja_rect.x + 5, input_caja_rect.y + 5))

    # dibujo boton de guardado
    pygame.draw.rect(pantalla, COLOR_VERDE, boton_guardar_rect)
    mostrar_texto(pantalla, "GUARDAR PUNTAJE", FUENTE_RESPUESTA, COLOR_BLANCO, boton_guardar_rect, center_align=True)

    return retorno