import pygame
from Constantes import *
from funciones import *

lista_botones = crear_botones_menu()
fondo_pantalla = pygame.transform.scale(FONDO_MENU,PANTALLA)

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    """
    esta pantalla gestiona lo que visualizamos en el menu principal del juego
    """
    pantalla.blit(fondo_pantalla,(0,0))
    
    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for i in range(len(lista_botones)):
                    if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                        CLICK_SONIDO.play() 
                        if i == BOTON_JUGAR:
                            retorno = "categorias"
                        elif i == BOTON_PUNTUACIONES:
                            retorno = "rankings"
                        elif i == BOTON_CONFIG:
                            retorno = "ajustes"
                        else:
                            retorno = "salir"
        
    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
    

    mostrar_texto(lista_botones[BOTON_JUGAR]["superficie"],"JUGAR", FUENTE_TEXTO, COLOR_BLANCO, lista_botones[BOTON_JUGAR]["superficie"].get_rect(), center_align=True)
    mostrar_texto(lista_botones[BOTON_PUNTUACIONES]["superficie"],"RANKINGS", FUENTE_TEXTO, COLOR_BLANCO, lista_botones[BOTON_PUNTUACIONES]["superficie"].get_rect(), center_align=True)
    mostrar_texto(lista_botones[BOTON_CONFIG]["superficie"],"AJUSTES", FUENTE_TEXTO, COLOR_BLANCO, lista_botones[BOTON_CONFIG]["superficie"].get_rect(), center_align=True)
    mostrar_texto(lista_botones[BOTON_SALIR]["superficie"],"SALIR", FUENTE_TEXTO, COLOR_BLANCO, lista_botones[BOTON_SALIR]["superficie"].get_rect(), center_align=True)
    
    
    return retorno