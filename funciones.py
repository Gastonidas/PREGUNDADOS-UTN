import random
import csv
from Constantes import *
import pygame

def cargar_preguntas_desde_csv(ruta_archivo: str) -> list[dict]:
    """
    Lee preguntas desde un CSV con formato:
    categoria,pregunta,respuesta_correcta,opcion_1,opcion_2,opcion_3
    
    Mezcla las opciones y devuelve la lista de preguntas en el formato
    que el juego necesita.
    """
    preguntas = []
    try:
        # 'utf-8-sig' evita caracteres invisibles
        with open(ruta_archivo, mode='r', encoding='utf-8-sig') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            
            for fila in lector_csv:
                # 1. obtiene la respuesta correcta y las opciones incorrectas
                respuesta_correcta_texto = fila['respuesta_correcta']
                opciones = [
                    respuesta_correcta_texto,
                    fila['opcion_1'],
                    fila['opcion_2'],
                    fila['opcion_3']
                ]
                
                # 2. mezcla de opciones utilizando random.shuffle
                random.shuffle(opciones)
                
                # 3. encuentra la nueva posicion (1, 2, 3 o 4) de la respuesta correcta
                indice_correcto = opciones.index(respuesta_correcta_texto) + 1
                
                # 4. diccionario con el formato esperado
                pregunta_formateada = {
                    'categoria': fila['categoria'], 
                    'pregunta': fila['pregunta'],
                    'respuesta_1': opciones[0],
                    'respuesta_2': opciones[1],
                    'respuesta_3': opciones[2],
                    'respuesta_4': opciones[3],
                    'respuesta_correcta': indice_correcto
                    # 'categoria': fila['categoria'] # descomentar si se quiere usar la categoria para algo
                }
                preguntas.append(pregunta_formateada)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de preguntas en la ruta '{ruta_archivo}'")
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo CSV: {e}")
    
    return preguntas

def obtener_categorias(lista_preguntas: list) -> list:
    """
    Recorre la lista de preguntas y devuelve una lista con los nombres
    de las categorías sin repetir.
    """
    categorias_unicas = []
    for pregunta in lista_preguntas:
        if pregunta['categoria'] not in categorias_unicas:
            categorias_unicas.append(pregunta['categoria'])
    return categorias_unicas

def dibujar_puntero_pixelado(pantalla, imagen_puntero):
    pos = pygame.mouse.get_pos()
    pantalla.blit(imagen_puntero, pos)


def mostrar_texto(surface, text, font, color, rect, center_align=True):
    """
    Dibuja texto dentro de un rectángulo, ajustando líneas y centrando
    el bloque de texto completo tanto vertical como horizontalmente.
    """
    lines = []
    words = text.split(' ')
    current_line = ""

    # 1. dividir el texto en líneas que quepan en el ancho del rectángulo
    for word in words:
        if font.size(current_line + " " + word)[0] < rect.width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())

    # 2. calcular el alto total del bloque de texto
    font_height = font.size("Tg")[1]
    total_height = len(lines) * font_height

    # 3. dibujar cada línea centrada
    y_start = rect.centery - (total_height / 2)
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        # posicionar cada línea en el centro del rectángulo
        line_rect = line_surface.get_rect(center=(rect.centerx, y_start + i * font_height + font_height // 2))
        surface.blit(line_surface, line_rect)

def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)

def reiniciar_estadisticas(datos_juego:dict) -> None:
    """ Reinicia todas las estadísticas y comodines para una nueva partida. """

    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["tiempo_restante"] = TIEMPO_INICIAL_JUEGO
    datos_juego["indice"] = 0
    datos_juego["aciertos_consecutivos"] = 0
    
    # reiniciar comodines
    datos_juego["comodines"] = {
        "bomba": True,
        "x2": True,
        "doble_chance": True,
        "pasar": True
    }
    datos_juego["x2_activo"] = False
    datos_juego["doble_chance_activa"] = False
    
    # limpia pantallas 
    if "animacion_dado" in datos_juego:
        del datos_juego["animacion_dado"]
    if "categoria_elegida" in datos_juego:
        del datos_juego["categoria_elegida"]


def verificar_respuesta(datos_juego:dict,pregunta:dict,respuesta:int) -> bool:
    """ Verifica la respuesta, aplicando la lógica de comodines X2 y Doble Chance. """

    acerto = (respuesta == pregunta["respuesta_correcta"]) # verifica que la respuesta sea correcta
    
    if acerto:
        # si la respuesta es correcta, suma los puntos correspondientes
        puntos_ganados = PUNTUACION_ACIERTO
        if datos_juego.get("x2_activo", False): 
            puntos_ganados *= 2
            datos_juego["x2_activo"] = False # el x2 se consume
            
        datos_juego["puntuacion"] += puntos_ganados
        datos_juego["aciertos_consecutivos"] += 1
        
        if datos_juego["aciertos_consecutivos"] >= 5:
            datos_juego["vidas"] += 1
            datos_juego["aciertos_consecutivos"] = 0
        
        datos_juego["doble_chance_activa"] = False # se desactiva la doble chance si se acierta
        return True
    else:
        # respuesta incorrecta
        if datos_juego.get("doble_chance_activa", False):
            # uso la doble chance
            datos_juego["doble_chance_activa"] = False
            return "usando_doble_chance" # devuelve estado que permite usar la doble chance
        else:
            # Error normal
            datos_juego["vidas"] -= 1
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            datos_juego["aciertos_consecutivos"] = 0
            datos_juego["x2_activo"] = False # El X2 se pierde si se erra
            return False

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = elemento_juego["superficie"].get_rect()
    elemento_juego["rectangulo"].x = pos_x
    elemento_juego["rectangulo"].y = pos_y
    
    return elemento_juego

# def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int) -> None:
#     elemento_juego["superficie"] =  pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    
# def obtener_respuesta_click(boton_respuesta_uno:dict,boton_respuesta_dos:dict,boton_respuesta_tres:dict,boton_respuesta_cuatro:dict,pos_click:tuple):
#     lista_aux = [boton_respuesta_uno["rectangulo"],boton_respuesta_dos["rectangulo"],boton_respuesta_tres["rectangulo"], boton_respuesta_cuatro["rectangulo"]]
#     respuesta = None
    
#     for i in range(len(lista_aux)):
#         if lista_aux[i].collidepoint(pos_click):
#             respuesta = i + 1
    
#     return respuesta

# def cambiar_pregunta(lista_preguntas:list,indice:int,caja_pregunta:dict,boton_respuesta_uno:dict,boton_respuesta_dos:dict,boton_respuesta_tres:dict, boton_respuesta_cuatro:dict) -> dict:
#     pregunta_actual = lista_preguntas[indice]
#     limpiar_superficie(caja_pregunta,"assets/imagenes/fondo_boton.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
#     limpiar_superficie(boton_respuesta_uno,"assets/imagenes/fondo_boton.jpg",ANCHO_BOTON,ALTO_BOTON)
#     limpiar_superficie(boton_respuesta_dos,"assets/imagenes/fondo_boton.jpg",ANCHO_BOTON,ALTO_BOTON)
#     limpiar_superficie(boton_respuesta_tres,"assets/imagenes/fondo_boton.jpg",ANCHO_BOTON,ALTO_BOTON)
#     limpiar_superficie(boton_respuesta_cuatro,"assets/imagenes/fondo_boton.jpg",ANCHO_BOTON,ALTO_BOTON)
    
#     return pregunta_actual


def crear_botones_menu() -> list:
    lista_botones = []
    pos_x_menu = (ANCHO - ANCHO_BOTON_MENU) // 2 
    pos_y = 250
    espaciado_menu = 85 # espaciado entre botones del menu

    for i in range(4):
        # dimensiones
        boton = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_BOTON_MENU, ALTO_BOTON_MENU, pos_x_menu, pos_y)
        pos_y += espaciado_menu
        lista_botones.append(boton)
        
    return lista_botones

def guardar_partida(nombre_jugador:int, puntaje_final:int) -> None:
    """
    Guarda los datos de la partida en un archivo JSON. Primero lee el archivo existente,
    agrega la nueva partida y luego guarda todo de nuevo
    """
    from datetime import datetime
    import json
    try:
        with open("data/partidas.json", "r", encoding="utf-8") as file:
            partidas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        partidas = []


    partida = {
        "nombre": nombre_jugador,
        "puntaje": puntaje_final,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # agregar y guarda
    partidas.append(partida)
    with open("data/partidas.json", "w", encoding="utf-8") as f:
        json.dump(partidas, f, indent=4, ensure_ascii=False)

def obtener_top_10():
    """
    Obtiene las 10 mejores partidas ordenadas por puntaje.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    import json
    try:
        with open("data/partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    # ordenar las partidas por puntaje de forma descendente
    partidas.sort(key=lambda x: x["puntaje"], reverse=True)
    return partidas[:10]