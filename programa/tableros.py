import random

from programa import constantes as ct


def crear_y_mezclar_tableros() -> tuple:  # Lucas Nuñez
    # Crea los tableros, y luego los mezcla

    tablero = crear_tablero_original()

    tablero_oculto, tablero_reset = crear_tablero_oculto_y_reset()

    mezclar(tablero)

    return tablero_oculto, tablero, tablero_reset


def crear_tablero_oculto_y_reset() -> tuple:  # Lucas Nuñez
    # Genera dos tableros, oculto y reset
    tablero_oculto = []
    tablero_reset = []

    for fila in range(ct.RANGO_FILAS):
        tablero_oculto.append([])
        tablero_reset.append([])
        for columna in range(ct.RANGO_COLUMNAS):
            tablero_oculto[fila].append(columna)
            tablero_reset[fila].append(columna)

    return tablero_oculto, tablero_reset


def crear_tablero_original() -> list:  # Lucas Nuñez
    # Genera tablero con letras ordenadas y visibles
    tablero = []
    fila = 0
    columna = 0

    for fila in range(ct.RANGO_FILAS):
        tablero.append([])

    for fila in range(ct.RANGO_FILAS):
        for letra in ct.LETRAS[columna:columna + ct.RANGO_COLUMNAS]:
            tablero[fila].append(letra)
        columna += ct.RANGO_COLUMNAS

    return tablero


def mezclar(tablero: list) -> list:  # Lucas Nuñez
    # Genera un orden aleatorio en las fichas del tablero
    lista = []

    for fila in range(ct.RANGO_FILAS):
        for columna in range(ct.RANGO_COLUMNAS):
            lista.append(tablero[fila][columna])

    random.shuffle(lista)

    for fila in range(ct.RANGO_FILAS):
        for columna in range(ct.RANGO_COLUMNAS):
            tablero[fila][columna] = lista[fila * ct.RANGO_COLUMNAS + columna]

    return tablero
