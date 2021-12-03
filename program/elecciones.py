from . import validaciones as val

# Renzo Martin


def jugada(jugador: str, puntos: int, manos_jugadas: int, tableros: tuple, TABLERO_OCULTO, TABLERO, CANTIDAD_FICHAS, RANGO, TABLERO_RESET, FILA_UNO, COLUMNA_UNO, FILA_DOS, COLUMNA_DOS) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos
    sigue_jugando = True

    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------\n")
        print(f"Turno de {jugador} \n")

        filas_y_columnas = recopilar_elecciones(
            tableros, TABLERO_OCULTO, TABLERO, CANTIDAD_FICHAS, RANGO)

        encontro_par = val.fichas_son_iguales(
            filas_y_columnas, tableros, TABLERO_OCULTO, TABLERO_RESET, FILA_UNO, COLUMNA_UNO, FILA_DOS, COLUMNA_DOS)

        manos_jugadas += 1

        if encontro_par:
            puntos += 1
        else:
            sigue_jugando = False

        hay_ganador = val.hay_un_ganador(tableros, TABLERO_OCULTO, TABLERO)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return (puntos, manos_jugadas, hay_ganador)


# Agustin Balino
def recopilar_elecciones(tableros, TABLERO_OCULTO, TABLERO, CANTIDAD_FICHAS, RANGO) -> tuple:
    # Se elijen los valores de filas y columnas
    tablero_oculto, tablero = tableros[TABLERO_OCULTO], tableros[TABLERO]

    for fila in tablero_oculto:
        print(fila)

    primera_eleccion = eleccion(
        tablero_oculto, CANTIDAD_FICHAS, RANGO, numero_eleccion=1)
    fila_uno, columna_uno = primera_eleccion[0], primera_eleccion[1]

    print("\nLa primer ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_uno, columna_uno, tablero)

    segunda_eleccion = eleccion(tablero_oculto, numero_eleccion=2)
    fila_dos, columna_dos = segunda_eleccion[0], segunda_eleccion[1]

    print("\nLa segunda ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_dos, columna_dos, tablero)

    return (fila_uno, columna_uno, fila_dos, columna_dos)


# Agustin Balino
def eleccion(tablero_oculto: list, CANTIDAD_FICHAS, RANGO, numero_eleccion: int) -> tuple:
    # Se devuelve la combinacion fila-columna
    eleccion_valida = False

    while not eleccion_valida:

        fila = val.validar_ingreso(
            numero_eleccion, CANTIDAD_FICHAS, RANGO, palabra="FILA")

        columna = val.validar_ingreso(
            numero_eleccion, CANTIDAD_FICHAS, RANGO, palabra="COLUMNA")

        eleccion_valida = val.eleccion_es_valida(fila, columna, tablero_oculto)

    return (fila, columna)


# Agustin Balino
def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:
    # Imprime el tablero luego de que se escoje la ficha
    tablero_oculto[fila][columna] = tablero[fila][columna]

    for ficha in tablero_oculto:
        print(ficha)
