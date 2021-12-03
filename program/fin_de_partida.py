from os import remove

import time

from usuarios import registro as rg

# Julian Rando


def fin_de_partida(registro_partida: dict, tiempo: tuple, PUNTOS_JUGADOR, MANOS_JUGADAS_JUGADOR) -> None:
    # nombres de los jugadores, con su respectiva cantidad de aciertos, el total de intentos y la cantidad promedio de intentos.
    registro_ordenado = diccionario_ordenado(registro_partida)

    archivo = open("./Datos/Partida_individual.csv", "w")
    registro = rg.leer(archivo)
    archivo.write("Jugador,Aciertos,Intentos")
    for jugador in registro_ordenado:
        if registro_ordenado[0] == jugador:
            archivo.write(
                f"{jugador} ES EL GANADOR,{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][PUNTOS_JUGADOR]},{registro_ordenado[jugador][MANOS_JUGADAS_JUGADOR]}\n")

    # tabla_datos_panda()

    archivo.close()

    remove("./Datos/Partida_individual.csv")


# AGREGAR AUTOR
def tiempo_hms(inicio: float, final: float, PASAJE_MINUTOS, PASAJE_HORAS) -> tuple:
    # Convierte el tiempo de segundos a horas, minutos y segundos.
    segundos = final - inicio
    horas = int(segundos / PASAJE_HORAS)
    segundos -= horas * PASAJE_HORAS
    minutos = int(segundos / PASAJE_MINUTOS)
    segundos -= minutos * PASAJE_MINUTOS

    return (horas, minutos, segundos)


def registro_tiempos(inicio: float, PASAJE_MINUTOS, PASAJE_HORAS) -> tuple:
    final = time.time()
    tiempo_jugado = tiempo_hms(final, PASAJE_MINUTOS, PASAJE_HORAS)
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
