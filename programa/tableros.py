import constantes as ct


def crear_y_mezclar_tableros() -> tuple:
    # Crea los tableros, y luego los mezcla

    tablero = crear_tablero_original()

    tableros_ocultos = crear_tablero_oculto_y_reset()

    tablero_oculto, tablero_reset = tableros_ocultos[0],  tableros_ocultos[1]

    tablero = mezclar(tablero)

    return tablero_oculto, tablero, tablero_reset


def crear_tablero_oculto_y_reset() -> tuple:
    # Genera dos tableros, oculto y reset
    contador = 0
    tablero_oculto = []
    tablero_reset = []

    for fila in range(ct.DURACION):
        tablero_oculto.append([])
        tablero_reset.append([])
        for columna in range(ct.DURACION):
            tablero_oculto[fila].append(contador)
            tablero_reset[fila].append(contador)
            contador += 1

    tableros = tablero_oculto, tablero_reset

    return tableros


def crear_tablero_original() -> list:
    # Genera tablero
    tablero = []
    fila = 0
    columna = 0

    for fila in range(ct.DURACION):
        tablero.append([])

    for fila in range(ct.DURACION):
        for letra in ct.LETRAS[columna:columna + ct.DURACION]:
            tablero[fila].append(letra)
        columna += ct.DURACION

    return tablero


def mezclar(tablero: list) -> list:
    # Genera un orden aleatorio en las fichas del tablero
    lista = []

    rango_letras = ct.CANTIDAD_FICHAS // ct.DURACION

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            lista.append(tablero[fila][columna])

    # random.shuffle(lista)

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            tablero[fila][columna] = lista[fila * rango_letras + columna]

    return tablero
