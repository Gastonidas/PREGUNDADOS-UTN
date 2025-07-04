import pygame
import random
from Constantes import *
from funciones import *

# cargamos las preguntas una sola vez para obtener las categorías
lista_completa_preguntas = cargar_preguntas_desde_csv("data/preguntas.csv")
categorias_disponibles = obtener_categorias(lista_completa_preguntas)

def mostrar_categorias(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """
    muestra la animación del dado girando y selecciona una categoría.
    """
    fondo_pantalla = pygame.transform.scale(FONDO_CATEGORIAS, PANTALLA)
    pantalla.blit(fondo_pantalla, (0, 0))
    
    retorno = "categorias"

    # inicializa el dado
    if "animacion_dado" not in datos_juego:
        datos_juego["animacion_dado"] = {
            "activo": True,
            "tiempo_inicio": pygame.time.get_ticks(),
            "duracion_total": 3000,  # 3 segundos de animación
            "intervalo_cambio": 100, # velocidad en la que cambia las categorias en ms
            "ultimo_cambio": 0,
            "categoria_mostrada": random.choice(categorias_disponibles),
            #"categoria_final": random.choice(categorias_disponibles)
        }

    anim_data = datos_juego["animacion_dado"]
    tiempo_actual = pygame.time.get_ticks()

    # animacion
    if anim_data["activo"]:
        info_rect = pygame.Rect(0, 150, ANCHO, 50)
        mostrar_texto(pantalla, "Tirando el dado...", FUENTE_TEXTO, COLOR_BLANCO, info_rect, center_align=True)

        # mientras dura la animacion cambia la categoria que se muestra
        if tiempo_actual - anim_data["tiempo_inicio"] < anim_data["duracion_total"]:
            if tiempo_actual - anim_data["ultimo_cambio"] > anim_data["intervalo_cambio"]:
                anim_data["categoria_mostrada"] = random.choice(categorias_disponibles)
                anim_data["ultimo_cambio"] = tiempo_actual
        else:
            # termina la animacion y muestra la categoria final a la vez que la guarda
            anim_data["activo"] = False
           # anim_data["categoria_mostrada"] = anim_data["categoria_final"]
            datos_juego["categoria_elegida"] = anim_data["categoria_mostrada"] # guardado

        # dibujar del dado (un cuadro con el nombre de la categoria)
        dado_rect = pygame.Rect((ANCHO - 120) // 2, (ALTO - 150) // 2, 150, 150)
        pygame.draw.rect(pantalla, COLOR_NEGRO, dado_rect)
        pygame.draw.rect(pantalla, COLOR_BLANCO, dado_rect, 4)
        mostrar_texto(pantalla, anim_data["categoria_mostrada"], FUENTE_DADO, COLOR_BLANCO, dado_rect, center_align=True)

    else:
        # muestra la categoria aleatoria que fue guardada anteriormente
        resultado_rect = pygame.Rect(0, 150, ANCHO, 50)
        mostrar_texto(pantalla, f"Categoría: {datos_juego['categoria_elegida']}", FUENTE_VOLUMEN, COLOR_VERDE, resultado_rect, center_align=True)
        
        # insturccion de continuar
        continuar_rect = pygame.Rect(0, ALTO - 150, ANCHO, 50)
        mostrar_texto(pantalla, "Click para comenzar a jugar", FUENTE_TEXTO, COLOR_BLANCO, continuar_rect, center_align=True)

        # si no se hace clic, no avanza
        for evento in cola_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    CLICK_SONIDO.play()
                    retorno = "juego"
            if evento.type == pygame.QUIT:
                retorno = "salir"

    return retorno