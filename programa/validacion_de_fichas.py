import constantes as ct


def validar_ingreso(numero_eleccion: int, palabra: str) -> int:
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero
    valor_inicial = input(
        f"\nElija la {palabra} numero {numero_eleccion} (0 a {ct.CANTIDAD_FICHAS // ct.DURACION - 1}): ")

    while not valor_inicial.isdigit():

        print("Ingrese un valor valido.")
        valor_inicial = input(
            f"\nElija la {palabra} numero {numero_eleccion} (0 a {ct.CANTIDAD_FICHAS // ct.DURACION - 1}): ")

    return int(valor_inicial)


def eleccion_es_valida(fila: int, columna: int, tablero_oculto: list) -> bool:
    # Valida que la combinacion fila-columna elegida exista en el tablero, y no haya sido elegida previamente.
    es_valido = False

    if fila >= 0 and fila < len(tablero_oculto) and columna >= 0 and columna < len(tablero_oculto):
        ficha = tablero_oculto[fila][columna]

        if type(ficha) == str:
            print("La ficha ya fue elegida anteriormente, seleccione otra.")
        else:
            es_valido = True

    else:
        print("La ficha esta fuera del tablero, seleccione otra.")

    return es_valido


def hay_un_ganador(tableros: tuple) -> bool:
    # Retorna True cuando fueron encontradas todas las piezas del tablero
    tablero, tablero_oculto = tableros[ct.TABLERO], tableros[ct.TABLERO_OCULTO]
    return tablero_oculto == tablero


def fichas_son_iguales(fichas: tuple, tableros: tuple) -> bool:
    # Compara las fichas seleccionadas por el jugador y retorna si encontro o no su par
    fila_uno, columna_uno, fila_dos, columna_dos = fichas[ct.FILA_UNO], fichas[
        ct.COLUMNA_UNO], fichas[ct.FILA_DOS], fichas[ct.COLUMNA_DOS]
    tablero_oculto, tablero_reset = tableros[ct.TABLERO_OCULTO], tableros[ct.TABLERO_RESET]

    encontro_par = True

    if tablero_oculto[fila_uno][columna_uno] != tablero_oculto[fila_dos][columna_dos]:
        tablero_oculto[fila_uno][columna_uno] = tablero_reset[fila_uno][columna_uno]
        tablero_oculto[fila_dos][columna_dos] = tablero_reset[fila_dos][columna_dos]
        print("\nLas fichas no son iguales, no suma puntos.")

        encontro_par = False

    else:
        print("\nLas fichas son iguales, suma un punto")

    return encontro_par
