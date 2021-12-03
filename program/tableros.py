# Lucas N
def crear_y_mezclar_tableros(LETRAS: list, RANGO: int, CANTIDAD_FICHAS: int) -> tuple:
    # Crea los tableros, y luego los mezcla

    tablero = crear_tablero_original(LETRAS)

    tableros_ocultos = crear_tablero_oculto_y_reset(RANGO)

    tablero_oculto, tablero_reset = tableros_ocultos[0],  tableros_ocultos[1]

    tablero = mezclar(tablero, RANGO, CANTIDAD_FICHAS)

    return tablero_oculto, tablero, tablero_reset

# Lucas N


def crear_tablero_oculto_y_reset(RANGO: int) -> tuple:
    # Genera dos tableros, oculto y reset
    contador = 0
    tablero_oculto = []
    tablero_reset = []

    for fila in range(RANGO):
        tablero_oculto.append([])
        tablero_reset.append([])
        for columna in range(RANGO):
            tablero_oculto[fila].append(contador)
            tablero_reset[fila].append(contador)
            contador += 1

    tableros = tablero_oculto, tablero_reset

    return tableros


# Lucas N
def crear_tablero_original(letras: list, RANGO: int) -> list:
    # Genera tablero
    tablero = []
    fila = 0
    columna = 0

    for fila in range(RANGO):
        tablero.append([])

    for fila in range(RANGO):
        for letra in letras[columna:columna + RANGO]:
            tablero[fila].append(letra)
        columna += RANGO

    return tablero


# Lucas N
def mezclar(tablero: list, RANGO: int, CANTIDAD_FICHAS: int) -> list:
    # Genera un orden aleatorio en las fichas del tablero
    lista = []

    rango_letras = CANTIDAD_FICHAS//RANGO

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            lista.append(tablero[fila][columna])

    # random.shuffle(lista)

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            tablero[fila][columna] = lista[fila * rango_letras + columna]

    return tablero
