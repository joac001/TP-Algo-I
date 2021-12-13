from programa import constantes as ct
from colorama import Fore
from colorama import Style


def validar_ingreso(numero_eleccion: int, tipo_coordenada: str) -> int:  # Lucas Capocasa
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero
    if tipo_coordenada == "FILA":
        rango = ct.RANGO_FILAS - 1
    else:
        rango = ct. RANGO_COLUMNAS - 1

    valor_inicial = input(
        f"\nElija la {tipo_coordenada} numero {numero_eleccion} (0 a {rango}): ")

    while not valor_inicial.isdigit():

        print(Fore.RED + Style.BRIGHT +
              "Ingrese un valor valido." + Style.RESET_ALL)
        valor_inicial = input(
            f"\nElija la {tipo_coordenada} numero {numero_eleccion} (0 a {rango}): ")

    return int(valor_inicial)


def ficha_existe(fila: str, columna: str) -> bool:  # Lucas Capocasa
    # valida que las coordenadas existan en el tablero
    return fila >= ct.MINIMO and fila < ct.RANGO_FILAS and columna >= ct.MINIMO and columna < ct.RANGO_COLUMNAS


def eleccion_es_valida(fila: int, columna: int, tablero_oculto: list) -> bool:  # Lucas Capocasa
    # Valida que la coordenada elegida exista en el tablero, y no haya sido elegida previamente.
    es_valido = False

    if ficha_existe(fila, columna):
        ficha = tablero_oculto[fila][columna]

        if type(ficha) == str:
            print(Fore.RED + Style.BRIGHT +
                  "La ficha ya fue elegida anteriormente, seleccione otra." + Style.RESET_ALL)

        else:
            es_valido = True

    else:
        print(Fore.RED + Style.BRIGHT +
              "La ficha esta fuera del tablero, seleccione otra." + Style.RESET_ALL)

    return es_valido


def hay_un_ganador(tableros: tuple) -> bool:  # Lucas Capocasa
    # Verifica si todas las piezas del tablero fueron encontradas
    return tableros[ct.TABLERO] == tableros[ct.TABLERO_OCULTO]


def fichas_son_iguales(fichas: tuple, tableros: tuple) -> bool:  # Joaquin Ordonez
    # Compara las fichas seleccionadas por el jugador y retorna si encontro o no su par
    fila_uno, columna_uno, fila_dos, columna_dos = fichas[ct.FILA_UNO], fichas[
        ct.COLUMNA_UNO], fichas[ct.FILA_DOS], fichas[ct.COLUMNA_DOS]

    tablero_oculto, tablero_reset = tableros[ct.TABLERO_OCULTO], tableros[ct.TABLERO_RESET]

    encontro_par = True

    if tablero_oculto[fila_uno][columna_uno] != tablero_oculto[fila_dos][columna_dos]:
        tablero_oculto[fila_uno][columna_uno], tablero_oculto[fila_dos][
            columna_dos] = tablero_reset[fila_uno][columna_uno], tablero_reset[fila_dos][columna_dos]

        print(Fore.YELLOW +
              "\nLas fichas no son iguales, no suma puntos." + Style.RESET_ALL)

        encontro_par = False

    else:
        print(Fore.GREEN + "\nLas fichas son iguales, suma un punto" + Style.RESET_ALL)

    return encontro_par
