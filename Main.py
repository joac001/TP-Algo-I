from os import remove
import random
import time
from pandas import *
import registro as rg
import inicio_ses as ini
import pandas as pd

PARAMETRIZACION = 0
VALOR_PARAMETRIZACION = 1
SITIO_OBTENIDO = 0

# Constantes obtenidas del archivo de configuracion
def leer_y_declarar_constantes() -> dict:
    parametrizaciones_default = {"CANTIDAD_FICHAS": [0,16], "MAXIMO_JUGADORES": [0,3], "MAXIMO_PARTIDAS": [0,4], "REINICIAR_ARCHIV0_PARTIDAS": [0,4]}
    archivo = open("configuracion.csv", "r")
    registro = rg.leer(archivo)
    while (registro):
        if registro[PARAMETRIZACION] == "REINICIAR_ARCHIV0_PARTIDAS":
            parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = bool(registro[VALOR_PARAMETRIZACION])
        elif registro[PARAMETRIZACION] in parametrizaciones_default:
            parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = int(registro[VALOR_PARAMETRIZACION])
        parametrizaciones_default[registro[PARAMETRIZACION]][SITIO_OBTENIDO] += 1
        registro = rg.leer(archivo)
    archivo.close()

    # Si el primer valor de la lista vale 0, fue obtendio por default, si vale 1 fue obtenido por configuracion.
    for parametro in parametrizaciones_default:
        if parametrizaciones_default[parametro][SITIO_OBTENIDO] == 0:
            print(f"{parametro} vale {parametrizaciones_default[parametro][VALOR_PARAMETRIZACION]} y fue establecido por default")
        else:
            print(f"{parametro} vale {parametrizaciones_default[parametro][VALOR_PARAMETRIZACION]} y fue establecido por el archivo de configuracion")    
    return parametrizaciones_default

parametrizaciones = leer_y_declarar_constantes()
cantidad_fichas, maximo_jugadores, maximo_partidas, reiniciar_archiv0_partidas = parametrizaciones.values()
CANTIDAD_FICHAS = cantidad_fichas[VALOR_PARAMETRIZACION]
MAXIMO_JUGADORES = maximo_jugadores[VALOR_PARAMETRIZACION]
MAXIMO_PARTIDAS = maximo_partidas [VALOR_PARAMETRIZACION]
REINICIAR_ARCHIV0_PARTIDAS = reiniciar_archiv0_partidas[VALOR_PARAMETRIZACION]
# Constantes declaradas
FILA_UNO = 0
COLUMNA_UNO = 1
FILA_DOS = 2
COLUMNA_DOS = 3

DURACION = 4 #EX RANGO

#HIPOTESIS
PUNTOS_MAXIMOS_PRIMERA_MANO =(CANTIDAD_FICHAS//DURACION)//MAXIMO_JUGADORES


LETRAS = ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E", "F", "F", "G", "G", "H", "H"]

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
# CREAR NUEVO MAIN


def main() -> None:
    
    jugadores = ["Carlos", "Marta", "Mario"]
    sigue_jugando = True
    contador_partidas = 0
    datos_totales = {}

    while sigue_jugando and contador_partidas <= MAXIMO_PARTIDAS:

        inicio = time.time()

        tableros = crear_y_mezclar_tableros()

        registro_jugadores = registro_de_jugadores_iniciales(jugadores)

        registro_jugadores_final = empezar_juego(registro_jugadores, tableros)

        horarios = registro_tiempos(inicio)

        fin_de_partida(registro_jugadores_final, horarios[TIEMPO_JUGADO])

        guardado_datos_csv(datos_totales, horarios)

        registro_fin_juego = datos_partidas_multiples(registro_jugadores_final, datos_totales)

        contador_partidas += 1

    fin_de_juego(contador_partidas, registro_fin_juego)

# AGREGAR AUTOR
def registro_de_jugadores_iniciales(jugadores) -> dict:
    
    registro_jugadores = {}

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = [0,0]

    return registro_jugadores


def empezar_juego(registro_jugadores: dict, tableros: tuple) -> dict:
    # Funcion principal que ayuda a recorrer el programa.

    hay_ganador = False

    while not hay_ganador:

        for jugador in registro_jugadores:

            pasada = jugada(jugador, registro_jugadores[jugador][PUNTOS_JUGADOR],
                                registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR], tableros)
            registro_jugadores[jugador][PUNTOS_JUGADOR] += pasada[PUNTOS_JUGADOR]
            registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR] += pasada[MANOS_JUGADAS_JUGADOR]

            hay_ganador = pasada[TERMINO_TABLERO]

    return registro_jugadores


# Lucas N
def crear_y_mezclar_tableros() -> tuple:
    # Crea los tableros, y luego los mezcla

    tablero = crear_tablero_original()

    tableros_ocultos = crear_tablero_oculto_y_reset()

    tablero_oculto, tablero_reset = tableros_ocultos[0],  tableros_ocultos[1]

    tablero = mezclar(tablero)

    return tablero_oculto, tablero, tablero_reset


# Lucas N
def crear_tablero_oculto_y_reset() -> tuple:
    # Genera dos tableros, oculto y reset
    contador = 0
    tablero_oculto = []
    tablero_reset = []

    for fila in range(DURACION):
        tablero_oculto.append([])
        tablero_reset.append([])
        for columna in range(DURACION):
            tablero_oculto[fila].append(contador)
            tablero_reset[fila].append(contador)
            contador += 1

    tableros = tablero_oculto, tablero_reset

    return tableros


# Lucas N
def crear_tablero_original(letras: list) -> list:
    # Genera tablero
    tablero = []
    fila = 0
    columna = 0

    for fila in range(DURACION):
        tablero.append([])

    for fila in range(DURACION):
        for letra in letras[columna:columna + DURACION]:
            tablero[fila].append(letra)
        columna += DURACION

    return tablero


# Lucas N
def mezclar(tablero: list) -> list:
    # Genera un orden aleatorio en las fichas del tablero
    lista = []

    rango_letras = CANTIDAD_FICHAS//DURACION

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            lista.append(tablero[fila][columna])

    # random.shuffle(lista)

    for fila in range(rango_letras):
        for columna in range(rango_letras):
            tablero[fila][columna] = lista[fila * rango_letras + columna]

    return tablero


# Renzo Martin
def jugada(jugador: str, puntos: int, manos_jugadas: int, tableros: tuple) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos
    sigue_jugando = True

    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------\n")
        print(f"Turno de {jugador} \n")

        filas_y_columnas = recopilar_elecciones(tableros)

        encontro_par = fichas_son_iguales(filas_y_columnas, tableros)

        manos_jugadas += 1

        if encontro_par:
            puntos += 1
        else:
            sigue_jugando = False

        hay_ganador = hay_un_ganador(tableros)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return (puntos, manos_jugadas, hay_ganador)


# Lucas C
def validar_ingreso(numero_eleccion: int, palabra: str) -> int:
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero
    valor_inicial = input(
        f"\nElija la {palabra} numero {numero_eleccion} (0 a {CANTIDAD_FICHAS//DURACION - 1}): ")

    while not valor_inicial.isdigit():

        print("Ingrese un valor valido.")
        valor_inicial = input(
            f"\nElija la {palabra} numero {numero_eleccion} (0 a {CANTIDAD_FICHAS//DURACION - 1}): ")

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
def hay_un_ganador(tableros: tuple) -> bool:
    # Retorna True cuando fueron encontradas todas las piezas del tablero
    tablero, tablero_oculto = tableros[TABLERO], tableros[TABLERO_OCULTO]
    return tablero_oculto == tablero


# Joaquin Ordonez
def fichas_son_iguales(fichas: tuple, tableros: tuple) -> bool:
    # Compara las fichas seleccionadas por el jugador y retorna si encontro o no su par
    fila_uno, columna_uno, fila_dos, columna_dos = fichas[FILA_UNO], fichas[COLUMNA_UNO], fichas[FILA_DOS], fichas[COLUMNA_DOS]
    tablero_oculto, tablero_reset = tableros[TABLERO_OCULTO], tableros[TABLERO_RESET]

    encontro_par = True

    if tablero_oculto[fila_uno][columna_uno] != tablero_oculto[fila_dos][columna_dos]:
        tablero_oculto[fila_uno][columna_uno] = tablero_reset[fila_uno][columna_uno]
        tablero_oculto[fila_dos][columna_dos] = tablero_reset[fila_dos][columna_dos]
        print("Las fichas no son iguales, no suma puntos.")

        encontro_par = False

    else:
        print("Las fichas son iguales, suma un punto")

    return encontro_par


# Agustin Balino
def recopilar_elecciones(tableros) -> tuple:
    # Se elijen los valores de filas y columnas
    tablero_oculto, tablero = tableros[TABLERO_OCULTO], tableros[TABLERO]

    for fila in tablero_oculto:
        print(fila)

    primera_eleccion = eleccion(tablero_oculto, numero_eleccion=1)
    fila_uno, columna_uno = primera_eleccion[0], primera_eleccion[1]

    print("\nLa primer ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_uno, columna_uno, tablero)

    segunda_eleccion = eleccion(tablero_oculto, numero_eleccion=2)
    fila_dos, columna_dos = segunda_eleccion[0], segunda_eleccion[1]

    print("\nLa segunda ficha elegida es: ")

    mostrar_eleccion(tablero_oculto, fila_dos, columna_dos, tablero)

    return (fila_uno, columna_uno, fila_dos, columna_dos)


# Agustin Balino
def eleccion(tablero_oculto: list, numero_eleccion: int) -> tuple:
    # Se devuelve la combinacion fila-columna
    eleccion_valida = False

    while not eleccion_valida:

        fila = validar_ingreso(numero_eleccion, palabra="FILA")

        columna = validar_ingreso(numero_eleccion, palabra="COLUMNA")

        eleccion_valida = eleccion_es_valida(fila, columna, tablero_oculto)

    return (fila, columna)


# Agustin Balino
def mostrar_eleccion(tablero_oculto: list, fila: int, columna: int, tablero: int) -> None:
    # Imprime el tablero luego de que se escoje la ficha
    tablero_oculto[fila][columna] = tablero[fila][columna]

    for ficha in tablero_oculto:
        print(ficha)


def guardado_datos_csv(registro: dict, horarios: tuple) -> None:
    registro_ordenado = diccionario_ordenado(registro)

    if not REINICIAR_ARCHIV0_PARTIDAS:
        archivo = open("partidas.csv", "r+")
        registro = rg.leer(archivo)
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[DIA]},{horarios[HORA]},{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")
    else:
        remove("partidas.csv")
        archivo = open("partidas.csv", "w")
        registro = rg.leer(archivo)
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[DIA]},{horarios[HORA]},{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")

    archivo.close()


# Julian Rando
def fin_de_partida(registro_partida: dict, tiempo: tuple) -> None:
    # nombres de los jugadores, con su respectiva cantidad de aciertos, el total de intentos y la cantidad promedio de intentos.
    registro_ordenado = diccionario_ordenado(registro_partida)

    archivo = open("partida_individual.csv", "w")
    archivo.write("jugador,aciertos,intentos\n")
    for jugador in registro_ordenado:
        if registro_ordenado[0] == jugador:
            archivo.write(
                f"{jugador} ES EL GANADOR,{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")

    tabla_datos_panda("partida_individual.csv")

    archivo.close()
    remove("partida_individual.csv")


# AGREGAR AUTOR
def tiempo_hms(inicio: float, final: float) -> tuple:
    # Convierte el tiempo de segundos a horas, minutos y segundos.
    segundos = final - inicio
    horas = int(segundos / PASAJE_HORAS)
    segundos -= horas * PASAJE_HORAS
    minutos = int(segundos / PASAJE_MINUTOS)
    segundos -= minutos * PASAJE_MINUTOS

    return (horas, minutos, segundos)



def registro_tiempos() -> tuple:
    final = time.time()
    tiempo_jugado = tiempo_hms(final)
    hora_fin_partida = time.strftime("%H:%M:%S")
    dia_jugado = time.strftime("%d/%m/%y")

    return tiempo_jugado, hora_fin_partida, dia_jugado



def diccionario_ordenado(diccionario: dict) -> dict:
    valores_ordenados = sorted(diccionario.values(), reverse=True)
    diccionario_ordenado = {}

    for valores in valores_ordenados:
        for clave in diccionario.keys():
            if diccionario[clave] == valores:
                diccionario_ordenado[clave] = diccionario[clave]

    return diccionario_ordenado



def tabla_datos_panda(ruta_archivo: str):
    df = pd.read_csv(ruta_archivo, index_col="jugador")
    print(df)



def datos_partidas_multiples(registro_jugadores: dict, datos_totales: dict):
    for jugador in registro_jugadores:
        if jugador not in datos_totales:
            datos_totales[jugador] = registro_jugadores[jugador]
        else:
            datos_totales[jugador][PUNTOS_JUGADOR] += registro_jugadores[jugador][PUNTOS_JUGADOR]
            datos_totales[jugador][MANOS_JUGADAS_JUGADOR] += registro_jugadores[jugador][MANOS_JUGADAS_JUGADOR]
    
    return datos_totales



def fin_de_juego(cantidad_partidas: int, datos_totales: dict) -> None:
    registro_ordenado = diccionario_ordenado(datos_totales)

    archivo = open("partida_total.csv", "w")
    archivo.write("jugador,aciertos_totales,intentos_totales,promedio_aciertos,promedio_intentos\n")

    for jugador in registro_ordenado:
        promedio_puntos = round(registro_ordenado[jugador][PUNTOS_JUGADOR] / cantidad_partidas, 2)
        promedio_intentos = round(registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR] / cantidad_partidas, 2)
        if registro_ordenado[0] == jugador:
            archivo.write(
                f"{jugador} ES EL GANADOR GENERAL,{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos}\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos}\n")

    tabla_datos_panda("partida_total.csv")

    archivo.close()
    remove("partida_total.csv")

main()