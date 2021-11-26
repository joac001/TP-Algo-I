#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#                                                                                                                   #
# La metodologia elegida para trabajar fue conectarse a Discord en un horario pactado el cual variaba, depende el   #
# dia y disponibilidad de los miembros. (MOB programming)                                                           #
#                                                                                                                   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #


# La libreria "random" fue utilizada para randomizar cual de los dos jugadores comienza la partida
import random
# Utilizamos tkinter para generar la interfaz del programa
from tkinter import *
# importamos esta funcion de functools que ayuda a ejecutar "limpiamente" las funciones dentro de las interfazes de tkinter
from functools import partial
# para tomar el tiempo de la partida utilizamos esta libreria
import time

import interfaz as iz

# Definimos una variable para cronometrar el timepo desde el inicio de la partida
inicio = time.time()


# Julian Rando
def main(jugador_1: str, jugador_2: str) -> None: # pasarle el dict jugadores
    # Funcion principal que ayuda a recorrer el programa.

    eleccion_jugadores = []
    eleccion_jugadores.append(jugador_1)
    eleccion_jugadores.append(jugador_2)
    jugador_1 = random.choice(eleccion_jugadores)
    eleccion_jugadores.remove(jugador_1)
    jugador_2 = eleccion_jugadores[0]

    letras = ["A", "A", "B", "B", "C", "C", "D",
              "D", "E", "E", "F", "F", "G", "G", "H", "H"]

    duracion = len(letras)

    tableros = crear_y_mezclar_tableros(letras, duracion)

    tablero_oculto = tableros[0]
    TABLERO_RESET = tableros[1]
    contador = tableros[2]
    tablero = tableros[3]

    manos_jugadas = 0
    manos_jugadas_p1 = 0
    manos_jugadas_p2 = 0
    puntos_p1 = 0
    puntos_p2 = 0

    ganador = False

    while not ganador:

        registro_1 = jugada(jugador_1, contador, tablero,
                            tablero_oculto, TABLERO_RESET, manos_jugadas_p1, puntos_p1)

        puntos_p1 = registro_1[0]
        manos_jugadas_p1 = registro_1[1]
        ganador = registro_1[2]

        if not ganador:

            registro_2 = jugada(jugador_2, contador, tablero,
                                tablero_oculto, TABLERO_RESET, manos_jugadas_p2, puntos_p2)

            puntos_p2 = registro_2[0]
            manos_jugadas_p2 = registro_2[1]
            ganador = registro_2[2]

    final = time.time()
    tiempo = final - inicio
    tiempo_minutos = tiempo / 60

    fin_de_partida(manos_jugadas_p1, manos_jugadas_p2,
                   jugador_1, jugador_2, puntos_p1, puntos_p2, tiempo_minutos)


# Lucas N
def crear_y_mezclar_tableros(letras: list, duracion: int) -> tuple:
    # Crea los tableros, y luego los mezcla
    tableros_ocultos = crear_tablero_oculto_y_reset()
    tablero_oculto = tableros_ocultos[0]
    TABLERO_RESET = tableros_ocultos[1]
    contador = tableros_ocultos[2]

    tablero = crear_tablero_original(letras)

    tablero = mezclar(tablero, duracion)

    return tablero_oculto, TABLERO_RESET, contador, tablero


# Lucas N
def crear_tablero_oculto_y_reset() -> tuple:
    # Genera dos tableros, oculto y reset
    contador = 0

    tablero_oculto = []
    TABLERO_RESET = []

    for i in range(4):
        tablero_oculto.append([])
        TABLERO_RESET.append([])
        for j in range(4):
            tablero_oculto[i].append(contador)
            TABLERO_RESET[i].append(contador)

            contador += 1

    return tablero_oculto, TABLERO_RESET, contador


# Lucas N
def crear_tablero_original(letras: list) -> list:
    # Genera tablero

    tablero = []

    i = 0
    j = 0

    for i in range(4):
        tablero.append([])

    for i in range(4):
        for letra in letras[j:j+4]:
            tablero[i].append(letra)
        j += 4

    return tablero


# Lucas N
def mezclar(tablero: list, duracion: int) -> list:
    # Genera un orden aleatorio en las fichas del tablero

    lista = []

    duracion = duracion//4

    for i in range(duracion):
        for j in range(duracion):
            lista.append(tablero[i][j])

    random.shuffle(lista)

    for i in range(duracion):
        for j in range(duracion):
            tablero[i][j] = lista[i*duracion+j]

    return tablero


# Renzo Martin
def jugada(jugador: str, contador: int, tablero: list, tablero_oculto: list, TABLERO_RESET: list, manos_jugadas: int, puntos: int) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos

    sigue_jugando = True

    ganador = False

    while sigue_jugando and not ganador:

        print("-----------------------------------------------------------\n")
        print(f"Turno de {jugador} \n")

        filas_y_columnas = recopilar_elecciones(
            tablero_oculto, contador, tablero)

        fila1 = filas_y_columnas[0]
        columna1 = filas_y_columnas[1]
        fila2 = filas_y_columnas[2]
        columna2 = filas_y_columnas[3]

        encontro_par = comparar_tableros(
            tablero_oculto, fila1, columna1, fila2, columna2, TABLERO_RESET)

        manos_jugadas += 1

        if encontro_par:

            puntos += 1

        elif not encontro_par:

            sigue_jugando = False

        ganador = validar_ganador(tablero, tablero_oculto)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return puntos, manos_jugadas, ganador


# Agustin Balino
def recopilar_elecciones(tablero_oculto: list, contador: int, tablero: list) -> tuple:
    # Se elijen los valores de filas y columnas

    for i in tablero_oculto:
        print(i)

    primera_eleccion = eleccion(contador, tablero_oculto, numero_eleccion=1)
    fila1 = primera_eleccion[0]
    columna1 = primera_eleccion[1]

    print("\nLa primer ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila1, columna1, tablero)

    segunda_eleccion = eleccion(contador, tablero_oculto, numero_eleccion=2)
    fila2 = segunda_eleccion[0]
    columna2 = segunda_eleccion[1]

    print("\nLa segunda ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila2, columna2, tablero)

    return fila1, columna1, fila2, columna2


# Agustin Balino
def eleccion(contador: int, tablero_oculto: list, numero_eleccion: int) -> tuple:
    # Se devuelve la combinacion fila-columna

    eleccion = False

    while not eleccion:

        fila = validar_ingreso(contador, numero_eleccion, palabra="FILA")

        columna = validar_ingreso(contador, numero_eleccion, palabra="COLUMNA")

        eleccion = validar_eleccion(fila, columna, tablero_oculto)

    return fila, columna


# Agustin Balino
def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:
    # Imprime el tablero luego de que se escoje la ficha

    tablero_oculto[fila][columna] = tablero[fila][columna]

    for i in tablero_oculto:
        print(i)


# Lucas C
def validar_ingreso(contador: int, numero_eleccion: int, palabra: str) -> int:
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero

    valor_inicial = input(
        f"\nElija la {palabra} numero {numero_eleccion} (0 a {contador//4 - 1}): ")

    while not valor_inicial.isdigit():

        print("Ingrese un valor valido.")
        valor_inicial = input(
            f"\nElija la {palabra} numero {numero_eleccion} (0 a {contador//4 - 1}): ")

    return int(valor_inicial)


# Lucas C
def validar_eleccion(fila: int, columna: int, tablero_oculto: list) -> bool:
    # Valida que la combinacion fila-columna elegida exista en el tablero, y no haya sido elegida previamente.

    valido = False  # ya_esta_elegida

    if fila >= 0 and fila < len(tablero_oculto) and columna >= 0 and columna < len(tablero_oculto):

        ficha = tablero_oculto[fila][columna]

        if type(ficha) == str:
            # valido = False
            print("La ficha ya fue elegida anteriormente, seleccione otra.")

        else:
            valido = True

    else:
        print("La ficha esta fuera del tablero, seleccione otra.")

    return valido


# Lucas C
def validar_ganador(tablero: list, tablero_oculto: list) -> bool:
    # Retorna True cuando fueron encontradas todas las piezas del tablero

    ganador = False

    if tablero_oculto == tablero:
        ganador = True

    return ganador

# Joaquin Ordonez


def comparar_tableros(tablero_oculto: list, fila1: int, columna1: int, fila2: int, columna2: int, TABLERO_RESET: list) -> bool:
    # Compara las fichas seleccionadas por el jugador y retorna si encontro o no su par

    encontro_par = True

    if tablero_oculto[fila1][columna1] != tablero_oculto[fila2][columna2]:
        tablero_oculto[fila1][columna1] = TABLERO_RESET[fila1][columna1]
        tablero_oculto[fila2][columna2] = TABLERO_RESET[fila2][columna2]
        print("Las fichas no son iguales, no suma puntos.")

        encontro_par = False

    else:
        print("Las fichas son iguales, suma un punto")

    return encontro_par


# Julian Rando
def fin_de_partida(manos_jugadas_p1: int, manos_jugadas_p2: int, jugador_1: str, jugador_2: str, puntos_p1: int, puntos_p2: int, tiempo_minutos: float) -> None:
    # Imprime estadisticas finales de la partida

    manos_jugadas = manos_jugadas_p1 + manos_jugadas_p2

    print("-----------------------------------------------------------")
    print(f"La partida duro {round(tiempo_minutos, 1)} minutos")
    print(f"\nLa cantidad de manos jugadas totales fueron {manos_jugadas}")

    print(f"\n{jugador_1} acumulo {puntos_p1} puntos y jugo {manos_jugadas_p1} manos")
    print(f"\n{jugador_2} acumulo {puntos_p2} puntos y jugo {manos_jugadas_p2} manos")

    if puntos_p1 > puntos_p2:
        print("\n" + chr(27) + "[1;32m" + f"EL GANADOR ES {jugador_1}")
    elif puntos_p2 > puntos_p1:
        print("\n" + chr(27) + "[1;32m" + f"EL GANADOR ES {jugador_2}")
    elif puntos_p1 == puntos_p2:

        if manos_jugadas_p1 > manos_jugadas_p2:
            print("\n" + chr(27) +
                  "[1;32m" + f"EL GANADOR ES {jugador_2} PORQUE JUGO MENOS MANOS")
        elif manos_jugadas_p1 < manos_jugadas_p2:
            print("\n" + chr(27) +
                  "[1;32m" + f"EL GANADOR ES {jugador_1} PORQUE JUGO MENOS MANOS")
        else:
            print("\n" + chr(27) + "[1;33m" + f"EMPATE!")
    print(chr(27) + "[1;37m")


jugadores = iz.crear_interfaz()
main(jugadores)