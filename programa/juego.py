import constantes as ct

import random
import time

import programa.mas_partidas as mp
import programa.mostrar_estadisticas as me
import programa.tableros as tb
import programa.validacion_de_fichas as vdf


def main() -> None:

    contador_partidas = 0
    datos_totales = {}

    while ct.continua_jugando and contador_partidas <= ct.MAXIMO_PARTIDAS:

        tableros = tb.crear_y_mezclar_tableros()

        registro_comienzo = registro_de_jugadores_iniciales(ct.jugadores)

        contador_partidas += 1

        inicio = time.time()

        hay_ganador = False

        while not hay_ganador:

            for jugador in registro_comienzo:

                if not hay_ganador:

                    pasada_individual = empezar_juego(
                        registro_comienzo, tableros, jugador)

                    registro_jugadores, hay_ganador = pasada_individual[0], pasada_individual[1]

        horarios = registro_tiempos(inicio)

        fin_de_partida(registro_jugadores, horarios[ct.TIEMPO_JUGADO])

        registro_fin_juego = datos_partidas_multiples(
            registro_jugadores, datos_totales)

        guardado_datos_csv(datos_totales, horarios)

        mp.mas_partidas()

        ct.continua_jugando = ct.continuar()

    fin_de_juego(contador_partidas, registro_fin_juego)


def suma_de_jugadores(usuario: str) -> None:
    contador = 0
    ct.jugadores.append(usuario)
    contador += 1
    print("Los usuarion ingresados son:")
    for jugador in ct.jugadores:
        print(f"-> {jugador}")


def registro_de_jugadores_iniciales(jugadores) -> dict:

    registro_jugadores = {}

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = [0, 0]

    return registro_jugadores


def empezar_juego(registro_jugadores: dict, tableros: tuple, jugador: str) -> dict:
    # Funcion principal que ayuda a recorrer el programa.
    pasada = jugada(jugador, registro_jugadores[jugador][ct.PUNTOS_JUGADOR],
                    registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR], tableros)
    registro_jugadores[jugador][ct.PUNTOS_JUGADOR] += pasada[ct.PUNTOS_JUGADOR]
    registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR] += pasada[ct.MANOS_JUGADAS_JUGADOR]

    hay_ganador = pasada[ct.TERMINO_TABLERO]

    return registro_jugadores, hay_ganador


def jugada(jugador: str, puntos: int, manos_jugadas: int, tableros: tuple) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos
    sigue_jugando = True

    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------")
        print(f"Turno de {jugador} \n")

        filas_y_columnas = recopilar_elecciones(tableros)

        encontro_par = vdf.fichas_son_iguales(filas_y_columnas, tableros)

        manos_jugadas += 1

        # HIPOTESIS TOMADA : TODOS DEBEN JUGAR AL MENOS UNA MANO

        if encontro_par:
            puntos += 1
            if manos_jugadas == ct.MAXIMO_MANOS_JUGADAS_PRIMERA_RONDA:
                print(
                    f"{jugador} llego a la maxima cantidad de manos jugadas en la primera ronda.")
                sigue_jugando = False
        else:
            sigue_jugando = False

        hay_ganador = vdf.hay_un_ganador(tableros)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return (puntos, manos_jugadas, hay_ganador)


def recopilar_elecciones(tableros: tuple) -> tuple:
    # Se elijen los valores de filas y columnas
    tablero_oculto, tablero = tableros[ct.TABLERO_OCULTO], tableros[ct.TABLERO]

    for fila in tablero_oculto:
        print(fila)

    primera_eleccion = eleccion(tablero_oculto, numero_eleccion=1)
    fila_uno, columna_uno = primera_eleccion[0], primera_eleccion[1]

    print("\nLa primer ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_uno, columna_uno, tablero)

    segunda_eleccion = eleccion(tablero_oculto, numero_eleccion=2)
    fila_dos, columna_dos = segunda_eleccion[0], segunda_eleccion[1]

    print("\nLa segunda ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_dos, columna_dos, tablero)

    return (fila_uno, columna_uno, fila_dos, columna_dos)


def eleccion(tablero_oculto: list, numero_eleccion: int) -> tuple:
    # Se devuelve la combinacion fila-columna
    eleccion_valida = False

    while not eleccion_valida:

        fila = vdf.validar_ingreso(numero_eleccion, palabra="FILA")

        columna = vdf.validar_ingreso(numero_eleccion, palabra="COLUMNA")

        eleccion_valida = vdf.eleccion_es_valida(fila, columna, tablero_oculto)

    return (fila, columna)


def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:
    # Imprime el tablero luego de que se escoje la ficha
    tablero_oculto[fila][columna] = tablero[fila][columna]

    for ficha in tablero_oculto:
        print(ficha)


def guardado_datos_csv(registro: dict, horarios: tuple) -> None:
    registro_ordenado = diccionario_ordenado(registro)

    if not ct.REINICIAR_ARCHIV0_PARTIDAS:
        archivo = open("archivos/partidas.csv", "r+")
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]}\n")
    else:
        archivo = open("archivos/partidas.csv", "w")
        archivo.write("dia,hora,jugador,aciertos,intentos\n")
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]}\n")

    archivo.close()


def tiempo_hms(inicio: float, final: float) -> tuple:
    # Convierte el tiempo de segundos a horas, minutos y segundos.
    segundos = final - inicio
    horas = int(segundos / ct.PASAJE_HORAS)
    segundos -= horas * ct.PASAJE_HORAS
    minutos = int(segundos / ct.PASAJE_MINUTOS)
    segundos -= minutos * ct.PASAJE_MINUTOS

    return (horas, minutos, segundos)


def registro_tiempos(inicio: float) -> tuple:
    final = time.time()
    tiempo_jugado = tiempo_hms(inicio, final)
    hora_fin_partida = time.strftime("%H:%M:%S")
    dia_jugado = time.strftime("%d/%m/%y")

    return tiempo_jugado, hora_fin_partida, dia_jugado


def diccionario_ordenado(diccionario: dict) -> dict:
    valores_ordenados = sorted(diccionario.values(), reverse=True)
    diccionario_ordenado = {}

    for valores in valores_ordenados:
        for clave in diccionario.keys():
            if diccionario[clave] == valores:
                diccionario_ordenado[clave] = diccionario[clave]

    return diccionario_ordenado


def datos_partidas_multiples(registro_jugadores: dict, datos_totales: dict) -> dict:
    for jugador in registro_jugadores:
        if jugador not in datos_totales:
            datos_totales[jugador] = registro_jugadores[jugador]
        else:
            datos_totales[jugador][ct.PUNTOS_JUGADOR] += registro_jugadores[jugador][ct.PUNTOS_JUGADOR]
            datos_totales[jugador][ct.MANOS_JUGADAS_JUGADOR] += registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR]

    return datos_totales


def obtencion_ganadores(registro_ordenado: dict) -> list:
    ganadores = []

    for jugador in registro_ordenado:
        if registro_ordenado[jugador] == sorted(registro_ordenado.values(), key=lambda i: (i[ct.MANOS_JUGADAS_JUGADOR], i[ct.PUNTOS_JUGADOR]))[0]:
            ganadores.append(jugador)

    return ganadores


def fin_de_partida(registro_partida: dict, tiempo: tuple) -> None:
    # nombres de los jugadores, con su respectiva cantidad de aciertos, el total de intentos y la cantidad promedio de intentos.
    registro_ordenado = diccionario_ordenado(registro_partida)
    ganadores = obtencion_ganadores(registro_ordenado)

    print(
        f"El tiempo jugado fue de {tiempo[ct.HORAS]} horas, {tiempo[ct.MINUTOS]} minutos y {round(tiempo[ct.SEGUNDOS],2)} segundos\n")

    archivo = open("archivos/partida_individual.csv", "w")
    archivo.write("jugador,aciertos,intentos,efectividad\n")
    for jugador in registro_ordenado:
        efectividad = round(registro_ordenado[jugador][ct.PUNTOS_JUGADOR]
                            * 100 / registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR], 1)
        if jugador in ganadores:
            archivo.write(
                f"{jugador} ES EL GANADOR,{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{efectividad}%\n")

    archivo.close()

    me.mostrar_estadisticas("archivos/partida_individual.csv")


def fin_de_juego(cantidad_partidas: int, datos_totales: dict) -> None:
    registro_ordenado = diccionario_ordenado(datos_totales)
    mvps = obtencion_ganadores(registro_ordenado)

    print(f"Se han jugado un total de {cantidad_partidas} partidas")

    archivo = open("archivos/partida_total.csv", "w")
    archivo.write(
        "jugador,aciertos_totales,intentos_totales,promedio_aciertos,promedio_intentos,efectividad\n")

    for jugador in registro_ordenado:
        promedio_puntos = round(
            registro_ordenado[jugador][ct.PUNTOS_JUGADOR] / cantidad_partidas, 1)
        promedio_intentos = round(
            registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] / cantidad_partidas, 1)
        efectividad = round((promedio_intentos * 100) / promedio_puntos, 1)
        if jugador in mvps:
            archivo.write(
                f"MVP {jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")
    archivo.close()

    me.mostrar_estadisticas("archivos/partida_total.csv")
