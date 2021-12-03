from os import remove

import random
import time
from pandas import *

from usuarios import inicio_ses as ini, registro as rg
from program import tableros as tb, elecciones as elc, fin_de_partida as fp


# Constantes declaradas
FILA_UNO = 0
COLUMNA_UNO = 1
FILA_DOS = 2
COLUMNA_DOS = 3

RANGO = 4

LETRAS = ["A", "A", "B", "B", "C", "C", "D",
          "D", "E", "E", "F", "F", "G", "G", "H", "H"]

PUNTOS_JUGADOR = 0
MANOS_JUGADAS_JUGADOR = 1

HORAS = 0
MINUTOS = 1
SEGUNDOS = 2
PASAJE_HORAS = 3600
PASAJE_MINUTOS = 60
TIEMPO_JUGADO = 0

TERMINO_TABLERO = 2
TABLERO_OCULTO = 0
TABLERO = 1
TABLERO_RESET = 2

HORA = 1
DIA = 2

# Constantes obtenidas del archivo de configuracion
archivo = open("./Datos/Configuracion.csv", "r")
registro = rg.leer(archivo)
while (registro):

    if registro[0] == "CANTIDAD_FICHAS":
        CANTIDAD_FICHAS = int(registro[1])
    elif registro[0] == "MAXIMO_JUGADORES":
        MAXIMO_JUGADORES = int(registro[1])
    elif registro[0] == "MAXIMO_PARTIDAS":
        MAXIMO_PARTIDAS = int(registro[1])
    elif registro[0] == "REINICIAR_ARCHIV0_PARTIDAS":
        REINICIAR_ARCHIV0_PARTIDAS = bool(registro[1])

    registro = rg.leer(archivo)

archivo.close()

# CREAR NUEVO MAIN


def main() -> None:

    jugadores = ini.jugadores  # A que guncion quiere llamar, jugadores no existe!

    sigue_jugando = True
    contador_partidas = 0
    datos_totales = {}

    while sigue_jugando and contador_partidas <= MAXIMO_PARTIDAS:

        inicio = time.time()

        tableros = tb.crear_y_mezclar_tableros(LETRAS, RANGO, CANTIDAD_FICHAS)

        registro_jugadores = registro_de_jugadores_iniciales(jugadores)

        registro_jugadores_final = empezar_juego(registro_jugadores, tableros)

        horarios = fp.registro_tiempos(inicio, PASAJE_MINUTOS, PASAJE_HORAS)

        fp.fin_de_partida(registro_jugadores_final, horarios[TIEMPO_JUGADO])

        guardado_datos_csv(datos_totales, horarios)

        for jugador in registro_jugadores:
            if jugador not in datos_totales:
                datos_totales[jugador] = registro_jugadores[jugador]
            else:
                datos_totales[jugador][PUNTOS_JUGADOR] += registro_jugadores[jugador][PUNTOS_JUGADOR]
                datos_totales[jugador][MANOS_JUGADAS_JUGADOR] += registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR]

        contador_partidas += 1

    ranking(datos_totales, horarios)


# AGREGAR AUTOR
def registro_de_jugadores_iniciales(jugadores: list) -> dict:

    registro_jugadores = {}

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = [0, 0]

    return registro_jugadores


def empezar_juego(registro_jugadores: dict, tableros: tuple) -> dict:
    # Funcion principal que ayuda a recorrer el programa.

    hay_ganador = False

    while not hay_ganador:

        for jugador in registro_jugadores:

            pasada = elc.jugada(jugador, registro_jugadores[jugador][PUNTOS_JUGADOR],
                                registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR], tableros, TABLERO_OCULTO, TABLERO, CANTIDAD_FICHAS, RANGO, TABLERO_RESET, FILA_UNO, COLUMNA_UNO, FILA_DOS, COLUMNA_DOS)

            registro_jugadores[jugador][PUNTOS_JUGADOR] += pasada[PUNTOS_JUGADOR]
            registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR] += pasada[MANOS_JUGADAS_JUGADOR]

            hay_ganador = pasada[TERMINO_TABLERO]

    return registro_jugadores


def guardado_datos_csv(registro: dict, horarios: tuple) -> None:
    registro_ordenado = fp.diccionario_ordenado(registro)

    if not REINICIAR_ARCHIV0_PARTIDAS:
        archivo = open("./Datos/Configuracion.csv", "r+")
        registro = rg.leer(archivo)
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[DIA]},{horarios[HORA]},{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")
    else:
        remove("./Datos/Configuracion.csv")
        archivo = open("./Datos/Configuracion.csv", "w")
        registro = rg.leer(archivo)
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[DIA]},{horarios[HORA]},{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")

    archivo.close()


def ranking(datos_totales: dict, horario: tuple) -> None:
    datos_ordenados = fp.diccionario_ordenado(datos_totales)


main()

# def tabla_datos_panda():
#    df = pd.read_csv("./Datos/Partida_individual.csv", index_col = "Jugador")
