import pygame
from Constantes import *
from funciones import *

pygame.init()

boton_mute = crear_elemento_juego("assets/imagenes/boton_mute.png", 50, 50, 1200, 0)  
boton_unmute = crear_elemento_juego("assets/imagenes/boton_unmute.png", 50, 50, 730, 0)
boton_suma = crear_elemento_juego("assets/imagenes/boton_mas.png",60,60,750,350)
boton_resta = crear_elemento_juego("assets/imagenes/boton_menos.png",60,60,470,350)
boton_volver = crear_elemento_juego("assets/imagenes/fondo_boton.jpg",200,40,10,10)
fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg_ajustes.jpg"),PANTALLA)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    pantalla.blit(fondo_pantalla,(0,0))
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                    if not datos_juego["muteado"]:
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                    if not datos_juego["muteado"]:
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    datos_juego["muteado"] = not datos_juego["muteado"]
                    if datos_juego["muteado"]:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    CLICK_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])

    if datos_juego["muteado"]:
        imagen_mute = pygame.transform.scale(boton_mute["superficie"], (50, 50))
    else:
        imagen_mute = pygame.transform.scale(boton_unmute["superficie"], (50, 50))
    pantalla.blit(imagen_mute, boton_mute["rectangulo"])

    mostrar_texto(
        pantalla,f"{datos_juego['volumen_musica']} %",FUENTE_VOLUMEN, COLOR_BLANCO,pygame.Rect(550, 350, 200, 60) )
    mostrar_texto(boton_volver["superficie"],
    "VOLVER", FUENTE_RESPUESTA,COLOR_BLANCO,boton_volver["superficie"].get_rect())

    return retorno
    