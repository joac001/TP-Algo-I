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
JUGADOR_UNO = 0
JUGADOR_DOS = 1
JUGADOR_TRES = 3
JUGADOR_CUATRO = 4
HORAS = 0
MINUTOS = 1
SEGUNDOS = 2


def registro_de_jugadores_iniciales(jugadores: list) -> dict:

    registro_jugadores = {}
    registro_inicial = []
    registro_inicial[PUNTOS_JUGADOR] = 0
    registro_inicial[MANOS_JUGADAS_JUGADOR] = 0

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = registro_inicial

    return registro_jugadores


# Julian Rando
def empezar_juego(registro_jugadores: dict) -> None:
    # Funcion principal que ayuda a recorrer el programa.
    inicio = time.time()

    tableros = crear_y_mezclar_tableros(LETRAS, len(LETRAS))

    hay_ganador = False

    while not hay_ganador:
        datos_p1 = (registro_jugadores[JUGADOR_UNO], tableros, registro_jugadores[JUGADOR_UNO][MANOS_JUGADAS_JUGADOR], registro_jugadores[JUGADOR_UNO][PUNTOS_JUGADOR])
        registro_uno = jugada(datos_p1)

        puntos_p1, manos_jugadas_p1, ganador = registro_uno[0], registro_uno[1], registro_uno[2]
        registro_jugadores[JUGADOR_UNO][PUNTOS_JUGADOR] += puntos_p1
        registro_jugadores[JUGADOR_UNO][MANOS_JUGADAS_JUGADOR] += manos_jugadas_p1

        if not hay_ganador:
            datos_p2 = (registro_jugadores[JUGADOR_DOS], tableros, registro_jugadores[JUGADOR_DOS][MANOS_JUGADAS_JUGADOR], registro_jugadores[JUGADOR_DOS][PUNTOS_JUGADOR])
            registro_dos = jugada(datos_p2)
            puntos_p2, manos_jugadas_p2, ganador = registro_dos[0], registro_dos[1], registro_dos[2]
            registro_jugadores[JUGADOR_DOS][PUNTOS_JUGADOR] += puntos_p2
            registro_jugadores[JUGADOR_DOS][MANOS_JUGADAS_JUGADOR] += manos_jugadas_p2
            
    final = time.time()
    tiempo = tiempo_hms(inicio, final)

    fin_de_partida(registro_jugadores, tiempo)


# Lucas N
def crear_y_mezclar_tableros(letras: list, cantidad_letras: int) -> tuple:
    # Crea los tableros, y luego los mezcla
    tableros_ocultos = crear_tablero_oculto_y_reset()

    tablero_oculto, tablero_reset, contador = tableros_ocultos[0],  tableros_ocultos[1],  tableros_ocultos[2]

    tablero = crear_tablero_original(letras)

    tablero = mezclar(tablero, cantidad_letras)

    tableros = (tablero_oculto, tablero_reset, contador, tablero)

    return tableros


# Lucas N
def crear_tablero_oculto_y_reset() -> tuple:
    # Genera dos tableros, oculto y reset
    contador = 0

    tablero_oculto = []
    tablero_reset = []

    for fila in range(RANGO):
        tablero_oculto.append([])
        tablero_reset.append([])
        for j in range(RANGO):
            tablero_oculto[fila].append(contador)
            tablero_reset[fila].append(contador)
            contador += 1

    tableros = tablero_oculto, tablero_reset, contador

    return tableros


# Lucas N
def crear_tablero_original(letras: list) -> list:
    # Genera tablero

    tablero = []

    fila = 0
    columna = 0

    for i in range(RANGO):
        tablero.append([])

    for i in range(RANGO):
        for letra in letras[columna:columna+RANGO]:
            tablero[fila].append(letra)
        columna += RANGO

    return tablero


# Lucas N
def mezclar(tablero: list, cantidad_letras: int) -> list:
    # Genera un orden aleatorio en las fichas del tablero

    lista = []

    cantidad_letras = cantidad_letras//RANGO

    for fila in range(cantidad_letras):
        for columna in range(cantidad_letras):
            lista.append(tablero[fila][columna])

    random.shuffle(lista)

    for fila in range(cantidad_letras):
        for columna in range(cantidad_letras):
            tablero[fila][columna] = lista[fila * cantidad_letras + columna]

    return tablero


# Renzo Martin
def jugada(datos: tuple) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos
    jugador, tablero_oculto, tablero_reset, contador, tablero, manos_jugadas, puntos = datos[0], datos[1][0], datos[1][1], datos[1][2], datos[1][3], datos[2], datos[3]

    sigue_jugando = True

    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------\n")
        print(f"Turno de {jugador} \n")

        tableros = tablero_oculto, contador, tablero
        filas_y_columnas = recopilar_elecciones(tableros)

        datos_para_comparar = (filas_y_columnas[FILA_UNO], filas_y_columnas[COLUMNA_UNO], filas_y_columnas[FILA_DOS], filas_y_columnas[COLUMNA_DOS], tablero_oculto, tablero_reset)
        
        encontro_par = fichas_son_iguales(datos_para_comparar)
        manos_jugadas += 1

        if encontro_par:
            puntos += 1
        else:
            sigue_jugando = False

        ganador = hay_un_ganador(tablero, tablero_oculto)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

        pasada = (puntos, manos_jugadas, ganador)

    return pasada


# Agustin Balino
def recopilar_elecciones(tableros: tuple) -> tuple:
    # Se elijen los valores de filas y columnas
    tablero_oculto, contador, tablero = tableros[0], tableros[1], tableros[2]

    for ficha in tablero_oculto:
        print(ficha)

    primera_eleccion = eleccion(contador, tablero_oculto, numero_eleccion=1)
    fila_uno, columna_uno = primera_eleccion[0], primera_eleccion[1]

    print("\nLa primer ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_uno, columna_uno, tablero)

    segunda_eleccion = eleccion(contador, tablero_oculto, numero_eleccion=2)
    fila_dos, columna_dos = segunda_eleccion[0], segunda_eleccion[1]

    print("\nLa segunda ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_dos, columna_dos, tablero)

    fichas_elegidas = (fila_uno, columna_uno, fila_dos, columna_dos)

    return fichas_elegidas


# Agustin Balino
def eleccion(contador: int, tablero_oculto: list, numero_eleccion: int) -> tuple:
    # Se devuelve la combinacion fila-columna

    eleccion_valida = False

    while not eleccion_valida :

        fila = validar_ingreso(contador, numero_eleccion, palabra="FILA")

        columna = validar_ingreso(contador, numero_eleccion, palabra="COLUMNA")

        eleccion = eleccion_es_valida(fila, columna, tablero_oculto)

    return fila, columna


# Agustin Balino
def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:
    # Imprime el tablero luego de que se escoje la ficha

    tablero_oculto[fila][columna] = tablero[fila][columna]

    for ficha in tablero_oculto:
        print(ficha)


# Lucas C
def validar_ingreso(contador: int, numero_eleccion: int, palabra: str) -> int:
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero

    valor_inicial = input(
        f"\nElija la {palabra} numero {numero_eleccion} (0 a {contador//RANGO - 1}): ")

    while not valor_inicial.isdigit():

        print("Ingrese un valor valido.")
        valor_inicial = input(
            f"\nElija la {palabra} numero {numero_eleccion} (0 a {contador//RANGO - 1}): ")

    return int(valor_inicial)


# Lucas C
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


# Lucas C
def hay_un_ganador(tablero: list, tablero_oculto: list) -> bool:
    # Retorna True cuando fueron encontradas todas las piezas del tablero

    return tablero_oculto == tablero


# Joaquin Ordonez
def fichas_son_iguales(datos: tuple) -> bool:
    # Compara las fichas seleccionadas por el jugador y retorna si encontro o no su par
    fila_uno, columna_uno, fila_dos, columna_dos, tablero_oculto, tablero_reset = datos[0], datos[1], datos[2], datos[3], datos[RANGO], datos[5]

    encontro_par = True

    if tablero_oculto[fila_uno][columna_uno] != tablero_oculto[fila_dos][columna_dos]:
        tablero_oculto[fila_uno][columna_uno] = tablero_reset[fila_uno][columna_uno]
        tablero_oculto[fila_dos][columna_dos] = tablero_reset[fila_dos][columna_dos]
        print("Las fichas no son iguales, no suma puntos.")

        encontro_par = False

    else:
        print("Las fichas son iguales, suma un punto")

    return encontro_par


def tiempo_hms(inicio:float, final:float):
    HORAS = 3600
    MINUTOS = 60

    tiempo = (final - inicio)
    horas = tiempo // HORAS
    resto = tiempo % HORAS
    tiempo = tiempo - resto
    minutos = tiempo // MINUTOS
    segundos = tiempo % MINUTOS

    return (horas, minutos, round(segundos, 2))


# Julian Rando
def fin_de_partida(registro: dict, tiempo: tuple) -> None:
    # Imprime estadisticas finales de la partida

    manos_jugadas = 0
    puntos_ganador = 0

    print("-----------------------------------------------------------")
    print(f"La partida duro {tiempo[HORAS]}:{tiempo[MINUTOS]}:{tiempo[SEGUNDOS]}.")
    
    for jugador in registro:
        print(f"\n{jugador} acumulo {registro[jugador][PUNTOS_JUGADOR]} puntos y jugo {registro[jugador][MANOS_JUGADAS_JUGADOR]} manos")
        manos_jugadas += registro[jugador][MANOS_JUGADAS_JUGADOR]

    print(f"\nLa cantidad de manos jugadas totales fueron {manos_jugadas}")

    # sorted(registro.values(), key = lambda i:i[1])
  
    # if puntos_p1 > puntos_p2:
    #     print("\n" + chr(27) + "[1;32m" + f"EL GANADOR ES {jugador_uno}")
    # elif puntos_p2 > puntos_p1:
    #     print("\n" + chr(27) + "[1;32m" + f"EL GANADOR ES {jugador_dos}")
    # else:

    #     if manos_jugadas_p1 > manos_jugadas_p2:
    #         print("\n" + chr(27) +
    #               "[1;32m" + f"EL GANADOR ES {jugador_dos} PORQUE JUGO MENOS MANOS")
    #     elif manos_jugadas_p1 < manos_jugadas_p2:
    #         print("\n" + chr(27) +
    #               "[1;32m" + f"EL GANADOR ES {jugador_uno} PORQUE JUGO MENOS MANOS")
    #     else:
    #         print("\n" + chr(27) + "[1;33m" + f"EMPATE!")
    # print(chr(27) + "[1;30m")