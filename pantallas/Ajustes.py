import pygame
from Constantes import *
from funciones import *

boton_mute = crear_elemento_juego("assets/imagenes/boton_mute.png", 50, 50, 730, 0)  
boton_suma = crear_elemento_juego("assets/imagenes/boton_mas.png",60,60,500,300)
boton_resta = crear_elemento_juego("assets/imagenes/boton_menos.png",60,60,200,300)
boton_volver = crear_elemento_juego("assets/imagenes/fondo_boton.jpg",200,40,10,10)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg2.jpg"),PANTALLA)
    pantalla.blit(fondo_pantalla,(0,0))

    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] < 1.0:
                        datos_juego["volumen_musica"] += 0.05
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"])
                    CLICK_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0.0:
                        datos_juego["volumen_musica"] -= 0.05
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"])
                    CLICK_SONIDO.play()
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    datos_juego["muteado"] = not datos_juego.get("muteado", False)
                    if datos_juego["muteado"]:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"])
                    CLICK_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    # Actualizar volumen para evitar imprecisiones de flotantes
    datos_juego["volumen_musica"] = round(datos_juego["volumen_musica"], 2)
    if not datos_juego.get("muteado", False):
        pygame.mixer.music.set_volume(datos_juego["volumen_musica"])

    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])

    if datos_juego.get("muteado", False):
        boton_mute["superficie"] = pygame.transform.scale(pygame.image.load("assets/imagenes/boton_mute.png"), (60, 60))
    else:
        boton_mute["superficie"] = pygame.transform.scale(pygame.image.load("assets/imagenes/boton_unmute.png"), (60, 60))
    
    pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])

    # --- LLAMADAS CORREGIDAS ---
    volumen_porcentaje = int(datos_juego["volumen_musica"] * 100)
    mostrar_texto(pantalla, f"{volumen_porcentaje} %", FUENTE_VOLUMEN, COLOR_BLANCO, pygame.Rect(340,310, 100, 50))
    mostrar_texto(boton_volver["superficie"],"VOLVER", FUENTE_RESPUESTA, COLOR_BLANCO, boton_volver['superficie'].get_rect(), center_align=True)

    return retorno