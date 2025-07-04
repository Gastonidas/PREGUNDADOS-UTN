import pygame
import random
from Constantes import *
from funciones import *


lista_completa_preguntas = cargar_preguntas_desde_csv("data/preguntas.csv")
preguntas_filtradas = []

caja_pregunta = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_BOTON, ALTO_PREGUNTA, (ANCHO - ANCHO_BOTON) // 2, 70)
pos_x_respuestas = (ANCHO - ANCHO_BOTON) // 2
y_inicial_respuestas = 245
espaciado_vertical_respuestas = 100

botones_respuestas = []
for i in range(4):
    y = y_inicial_respuestas + i * espaciado_vertical_respuestas
    boton = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_BOTON, ALTO_BOTON, pos_x_respuestas, y)
    boton['desactivado'] = False
    botones_respuestas.append(boton)

# botones comodines
comodines_pos_y = ALTO - ALTO_COMODIN - 10
comodines_espaciado_x = ANCHO_COMODIN + 20
comodines_pos_x_inicial = (ANCHO - (4 * ANCHO_COMODIN + 3 * 20)) // 2

boton_comodin_bomba = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_COMODIN, ALTO_COMODIN, comodines_pos_x_inicial, comodines_pos_y)
boton_comodin_x2 = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_COMODIN, ALTO_COMODIN, comodines_pos_x_inicial + comodines_espaciado_x, comodines_pos_y)
boton_comodin_doble = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_COMODIN, ALTO_COMODIN, comodines_pos_x_inicial + (comodines_espaciado_x * 2), comodines_pos_y)
boton_comodin_pasar = crear_elemento_juego("assets/imagenes/fondo_boton.jpg", ANCHO_COMODIN, ALTO_COMODIN, comodines_pos_x_inicial + (comodines_espaciado_x * 3), comodines_pos_y)

reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo, 1000)

def avanzar_pregunta(datos_juego, lista_preguntas):
    """ Función auxiliar para pasar a la siguiente pregunta y reiniciar estados. """
    datos_juego['indice'] += 1
    if datos_juego['indice'] >= len(lista_preguntas):
        datos_juego['indice'] = 0 
    
    # reactiva los botones de respuestas
    for btn in botones_respuestas:
        btn['desactivado'] = False
    
    # desactiva comodines activos de pregunta anterior
    #datos_juego['x2_activo'] = False


def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    global preguntas_filtradas
    
    if not preguntas_filtradas:
        categoria_elegida = datos_juego.get("categoria_elegida", None)
        if categoria_elegida:
            preguntas_filtradas = [preg for preg in lista_completa_preguntas if preg['categoria'] == categoria_elegida]
            mezclar_lista(preguntas_filtradas) 

    fondo_pantalla = pygame.transform.scale(pygame.image.load("assets/imagenes/bg2.jpg"), PANTALLA)
    pantalla.blit(fondo_pantalla, (0, 0))

    #retorno = "juego"
    pregunta_actual = preguntas_filtradas[datos_juego['indice']]

    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] <= 0:
        preguntas_filtradas = []
        return "fin_partida"

    for evento in cola_eventos:
        if evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                pos_clic = evento.pos
                
                # logica clics en respuestas
                for i, boton in enumerate(botones_respuestas):
                    if not boton['desactivado'] and boton["rectangulo"].collidepoint(pos_clic):
                        resultado = verificar_respuesta(datos_juego, pregunta_actual, i)
                        if resultado == "usando_doble_chance":
                            boton['desactivado'] = True # desactiva la opcion incorrecta
                            ERROR_SONIDO.play()
                        else:
                            if resultado:
                                CLICK_SONIDO.play()
                            else:
                                ERROR_SONIDO.play()
                            avanzar_pregunta(datos_juego, preguntas_filtradas)
                        break 

                # logica clics en comodines
                if datos_juego["comodines"]["pasar"] and boton_comodin_pasar["rectangulo"].collidepoint(pos_clic):
                    datos_juego["comodines"]["pasar"] = False
                    CLICK_SONIDO.play()
                    avanzar_pregunta(datos_juego, preguntas_filtradas)

                elif datos_juego["comodines"]["bomba"] and boton_comodin_bomba["rectangulo"].collidepoint(pos_clic):
                    datos_juego["comodines"]["bomba"] = False
                    CLICK_SONIDO.play()
                    
                    opciones_incorrectas = [i for i in range(4) if i != pregunta_actual['respuesta_correcta']]
                    random.shuffle(opciones_incorrectas)
                    
                    botones_respuestas[opciones_incorrectas[0]]['desactivado'] = True
                    botones_respuestas[opciones_incorrectas[1]]['desactivado'] = True
                
                elif datos_juego["comodines"]["x2"] and boton_comodin_x2["rectangulo"].collidepoint(pos_clic):
                    datos_juego["comodines"]["x2"] = False
                    datos_juego["x2_activo"] = True
                    CLICK_SONIDO.play()

                elif datos_juego["comodines"]["doble_chance"] and boton_comodin_doble["rectangulo"].collidepoint(pos_clic):
                    datos_juego["comodines"]["doble_chance"] = False
                    datos_juego["doble_chance_activa"] = True
                    CLICK_SONIDO.play()


    
    pantalla.blit(caja_pregunta["superficie"], caja_pregunta["rectangulo"])
    padding_rect_pregunta = caja_pregunta["rectangulo"].inflate(-40, -40)
    mostrar_texto(pantalla, pregunta_actual["pregunta"], FUENTE_PREGUNTA, COLOR_BLANCO, padding_rect_pregunta)
    
    tiempo_total = datos_juego['tiempo_restante']
    minutos = tiempo_total // 60
    segundos = tiempo_total % 60
    
    texto_tiempo = f"TIEMPO: {minutos}:{segundos:02d}"
    mostrar_texto(pantalla, texto_tiempo, FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(ANCHO - 210, 10, 200, 30))


    for i, boton in enumerate(botones_respuestas):
        if boton['desactivado']:
            pygame.draw.rect(pantalla, COLOR_COMODIN_USADO, boton['rectangulo']) 
        else:
            pantalla.blit(boton["superficie"], boton["rectangulo"])
        
        padding_rect = boton["rectangulo"].inflate(-40, -40)
        mostrar_texto(pantalla, pregunta_actual[f"respuesta_{i+1}"], FUENTE_RESPUESTA, COLOR_BLANCO, padding_rect)

    # dibujo comodines
    lista_comodines_botones = [boton_comodin_bomba, boton_comodin_x2, boton_comodin_doble, boton_comodin_pasar]
    nombres_comodines = ["BOMBA", "X2", "DOBLE", "PASAR"]
    claves_comodines = ["bomba", "x2", "doble_chance", "pasar"]
    
    for i, boton in enumerate(lista_comodines_botones):
        color = COLOR_COMODIN_DISPONIBLE if datos_juego["comodines"][claves_comodines[i]] else COLOR_COMODIN_USADO
        # resalta el comodin 
        if (claves_comodines[i] == 'x2' and datos_juego['x2_activo']) or \
           (claves_comodines[i] == 'doble_chance' and datos_juego['doble_chance_activa']):
            color = COLOR_VERDE

        pygame.draw.rect(pantalla, color, boton['rectangulo'])
        mostrar_texto(pantalla, nombres_comodines[i], FUENTE_RESPUESTA, COLOR_BLANCO, boton['rectangulo'])

    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(10, 10, 200, 30))
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(10, 40, 360, 30))
    #mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo_restante']}", FUENTE_TEXTO, COLOR_BLANCO, pygame.Rect(ANCHO - 210, 10, 200, 30))

    return "juego"