from programa import constantes as ct

from colorama import Fore, Style

import random
import time

from interfaz import estadisticas as me
from programa import tableros as tb
from programa import validacion_de_fichas as vdf


def main() -> None:  # Lucas Capocasa
    # Funcion principal que maneja el juego

    contador_partidas = 0

    while ct.continuar_jugando and contador_partidas < ct.MAXIMO_PARTIDAS:

        tableros = tb.crear_y_mezclar_tableros()

        registro_jugadores = registro_de_jugadores_iniciales(ct.jugadores)

        inicio = time.time()

        partida_individual(registro_jugadores, tableros)

        horarios = registro_tiempos(inicio)

        contador_partidas += 1

        me.fin_de_partida(registro_jugadores, horarios[ct.TIEMPO_JUGADO])

        guardado_datos_partida(registro_jugadores, horarios)

        datos_partidas_multiples(registro_jugadores)

    me.fin_de_juego(contador_partidas)


def registro_de_jugadores_iniciales(jugadores: list) -> dict:  # Lucas Nuñez
    # Aleatoriza el orden de los jugadores y crea el registro inicial de cada jugador
    registro_jugadores = {}

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = [0, 0]

    return registro_jugadores


def partida_individual(registro_jugadores: dict, tableros: tuple) -> dict:  # Julian Rando
    # Ocurre una partida completa
    hay_ganador = False

    while not hay_ganador:
        for jugador in registro_jugadores:
            if not hay_ganador:
                registro_jugadores[jugador][ct.PUNTOS_JUGADOR], registro_jugadores[jugador][ct.MANOS_JUGADAS], hay_ganador = jugada(
                    jugador, registro_jugadores, tableros)

    return registro_jugadores


def jugada(jugador: str, registro_jugadores: dict, tableros: tuple) -> tuple:  # Renzo Martin
    # Se desarrolla cada mano, sumandose puntos y manos jugadas

    puntos, manos_jugadas = registro_jugadores[jugador][
        ct.PUNTOS_JUGADOR], registro_jugadores[jugador][ct.MANOS_JUGADAS]

    sigue_jugando = True
    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------")
        print(Fore.BLUE + Style.BRIGHT + "Turno de " +
              jugador + "\n" + Style.RESET_ALL)

        filas_y_columnas = recopilar_elecciones(tableros)

        encontro_par = vdf.fichas_son_iguales(filas_y_columnas, tableros)

        manos_jugadas += ct.UNIDAD

        if encontro_par:
            puntos += ct.UNIDAD
        else:
            sigue_jugando = False

        hay_ganador = vdf.hay_un_ganador(tableros)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return puntos, manos_jugadas, hay_ganador


def recopilar_elecciones(tableros: tuple) -> tuple:  # Agustin Baliño
    # Se elijen los valores de filas y columnas
    tablero_oculto, tablero = tableros[ct.TABLERO_OCULTO], tableros[ct.TABLERO]

    contador = 0
    for fila in tablero_oculto:
        print(Fore.CYAN, f"F{contador}", Style.RESET_ALL, fila)
        contador += ct.UNIDAD

    fila_uno, columna_uno = eleccion(tablero_oculto, numero_eleccion=1)

    print('\nLa primer ficha elegida es: " ' + Fore.CYAN + Style.BRIGHT +
          str(tablero[fila_uno][columna_uno]) + Style.RESET_ALL + ' "')

    mostrar_eleccion(tablero_oculto, fila_uno, columna_uno, tablero)

    fila_dos, columna_dos = eleccion(tablero_oculto, numero_eleccion=2)

    print('\nLa segunda ficha elegida es: " ' + Fore.CYAN + Style.BRIGHT +
          str(tablero[fila_dos][columna_dos]) + Style.RESET_ALL + ' "')

    mostrar_eleccion(tablero_oculto, fila_dos, columna_dos, tablero)

    return fila_uno, columna_uno, fila_dos, columna_dos


def eleccion(tablero_oculto: list, numero_eleccion: int) -> tuple:  # Agustin Baliño
    # Se devuelve la coordenada elejida
    eleccion_valida = False

    while not eleccion_valida:

        fila = vdf.validar_ingreso(numero_eleccion, tipo_coordenada="FILA")

        columna = vdf.validar_ingreso(
            numero_eleccion, tipo_coordenada="COLUMNA")

        eleccion_valida = vdf.eleccion_es_valida(fila, columna, tablero_oculto)

    return fila, columna


def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:  # Agustin Baliño
    # Imprime el tablero luego de que se escoje la ficha
    tablero_oculto[fila][columna] = tablero[fila][columna]

    contador = 0
    for fila in tablero_oculto:
        print(Fore.CYAN, f"F{contador}", Style.RESET_ALL, fila)
        contador += ct.UNIDAD


def guardado_datos_partida(registro: dict, horarios: tuple) -> None:  # Lucas Nuñez
    # Guarda los datos de la partida jugada en un .csv
    registro = me.diccionario_ordenado(registro)

    if not ct.REINICIAR_ARCHIV0_PARTIDAS:
        try:
            archivo = open("archivos/partidas.csv", "a")
        except:
            archivo = open("archivos/partidas.csv", "w")
            archivo.write("dia,hora,jugador,aciertos,intentos\n")

        for jugador in registro:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]}\n")
    else:
        archivo = open("archivos/partidas.csv", "w")
        archivo.write("dia,hora,jugador,aciertos,intentos\n")

        for jugador in registro:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]}\n")

    archivo.close()


def tiempo_hms(inicio: float, final: float) -> tuple:  # Agustin Baliño
    # Convierte el tiempo de segundos a horas y minutos
    segundos = final - inicio
    horas = int(segundos / ct.PASAJE_HORAS)
    segundos -= horas * ct.PASAJE_HORAS
    minutos = int(segundos / ct.PASAJE_MINUTOS)
    segundos -= minutos * ct.PASAJE_MINUTOS

    return horas, minutos, segundos


def registro_tiempos(inicio: float) -> tuple:  # Lucas Nuñez
    # Se obtiene el tiempo, la hora y el dia
    final = time.time()
    tiempo_jugado = tiempo_hms(inicio, final)
    hora_fin_partida = time.strftime("%H:%M:%S")
    dia_jugado = time.strftime("%d/%m/%y")

    return tiempo_jugado, hora_fin_partida, dia_jugado


def datos_partidas_multiples(registro_jugadores: dict) -> None:  # Lucas Capocasa
    # Guarda los datos del juego completo, sumandose partida a partida.
    for jugador in registro_jugadores:

        if jugador not in ct.registro_general:
            ct.registro_general[jugador] = registro_jugadores[jugador]
        else:
            ct.registro_general[jugador][ct.PUNTOS_JUGADOR] += registro_jugadores[jugador][ct.PUNTOS_JUGADOR]
            ct.registro_general[jugador][ct.MANOS_JUGADAS] += registro_jugadores[jugador][ct.MANOS_JUGADAS]
