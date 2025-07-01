import pygame
import random
from Constantes import *
from funciones import *

# Cargamos las preguntas una sola vez para obtener las categorías
lista_completa_preguntas = cargar_preguntas_desde_csv("data/preguntas.csv")
categorias_disponibles = obtener_categorias(lista_completa_preguntas)

def mostrar_pantalla_categorias(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """
    Muestra la animación del dado girando y selecciona una categoría.
    """
    fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg2.jpg"), PANTALLA)
    pantalla.blit(fondo_pantalla, (0, 0))
    
    retorno = "categorias"

    # Inicializar estado de la animación si no existe
    if "animacion_dado" not in datos_juego:
        datos_juego["animacion_dado"] = {
            "activo": True,
            "tiempo_inicio": pygame.time.get_ticks(),
            "duracion_total": 3000,  # 3 segundos de animación
            "intervalo_cambio": 100, # Cambiar categoría cada 100 ms
            "ultimo_cambio": 0,
            "categoria_mostrada": random.choice(categorias_disponibles),
            "categoria_final": random.choice(categorias_disponibles)
        }

    anim_data = datos_juego["animacion_dado"]
    tiempo_actual = pygame.time.get_ticks()

    if anim_data["activo"]:
        # --- FASE DE ANIMACIÓN ---
        # Mostrar texto informativo
        info_rect = pygame.Rect(0, 150, ANCHO, 50)
        mostrar_texto(pantalla, "Tirando el dado...", FUENTE_TEXTO, COLOR_BLANCO, info_rect, center_align=True)

        # Mientras dure la animación, cambiar la categoría mostrada
        if tiempo_actual - anim_data["tiempo_inicio"] < anim_data["duracion_total"]:
            if tiempo_actual - anim_data["ultimo_cambio"] > anim_data["intervalo_cambio"]:
                anim_data["categoria_mostrada"] = random.choice(categorias_disponibles)
                anim_data["ultimo_cambio"] = tiempo_actual
        else:
            # La animación terminó, mostrar la categoría final
            anim_data["activo"] = False
            anim_data["categoria_mostrada"] = anim_data["categoria_final"]
            datos_juego["categoria_elegida"] = anim_data["categoria_final"] # Guardar categoría

        # Dibujar el "dado" (un cuadro con el nombre de la categoría)
        dado_rect = pygame.Rect((ANCHO - 120) // 2, (ALTO - 150) // 2, 150, 150)
        pygame.draw.rect(pantalla, COLOR_NEGRO, dado_rect)
        pygame.draw.rect(pantalla, COLOR_BLANCO, dado_rect, 4)
        mostrar_texto(pantalla, anim_data["categoria_mostrada"], FUENTE_DADO, COLOR_BLANCO, dado_rect, center_align=True)

    else:
        # --- FASE DE RESULTADO ---
        # Mostrar la categoría que salió
        resultado_rect = pygame.Rect(0, 150, ANCHO, 50)
        mostrar_texto(pantalla, f"Categoría: {datos_juego['categoria_elegida']}", FUENTE_VOLUMEN, COLOR_VERDE, resultado_rect, center_align=True)
        
        # Mostrar instrucción para continuar
        continuar_rect = pygame.Rect(0, ALTO - 150, ANCHO, 50)
        mostrar_texto(pantalla, "Haz clic para comenzar", FUENTE_TEXTO, COLOR_BLANCO, continuar_rect, center_align=True)

        # Esperar clic para pasar a la pantalla de juego
        for evento in cola_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    CLICK_SONIDO.play()
                    retorno = "juego"
            if evento.type == pygame.QUIT:
                retorno = "salir"

    return retorno