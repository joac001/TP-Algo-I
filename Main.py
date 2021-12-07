import random
import time
import mas_partidas as mp
import constantes as ct
import mostrar_estadisticas as me


def main() -> None:

    contador_partidas = 0
    datos_totales = {}

    while ct.continua_jugando and contador_partidas <= ct.MAXIMO_PARTIDAS:

        tableros = crear_y_mezclar_tableros()

        registro_comienzo = registro_de_jugadores_iniciales(jugadores)

        contador_partidas += 1

        inicio = time.time()

        hay_ganador = False

        while not hay_ganador:

            for jugador in registro_comienzo:

                if not hay_ganador:

                    pasada_individual = empezar_juego(
                        registro_comienzo, tableros, jugador)

                    registro_jugadores, hay_ganador = pasada_individual[0], pasada_individual[1]

        horarios = registro_tiempos(inicio)

        fin_de_partida(registro_jugadores, horarios[ct.TIEMPO_JUGADO])

        registro_fin_juego = datos_partidas_multiples(
            registro_jugadores, datos_totales)

        guardado_datos_csv(datos_totales, horarios)

        mp.mas_partidas()

        ct.continua_jugando = ct.continuar()

    fin_de_juego(contador_partidas, registro_fin_juego)


jugadores = ["Messi", "Carlos", "Pedro"]


def suma_de_jugadores(usuario: str):
    contador = 0
    jugadores.append(usuario)
    contador += 1
    print("Los usuarion ingresados son:")
    for jugador in jugadores:
        print(f"-> {jugador}")

# AGREGAR AUTOR


def registro_de_jugadores_iniciales(jugadores) -> dict:
    registro_jugadores = {}

    random.shuffle(jugadores)

    for jugador in jugadores:
        registro_jugadores[jugador] = [0, 0]

    return registro_jugadores


def empezar_juego(registro_jugadores: dict, tableros: tuple, jugador: str) -> dict:
    # Funcion principal que ayuda a recorrer el programa.
    pasada = jugada(jugador, registro_jugadores[jugador][ct.PUNTOS_JUGADOR],
                    registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR], tableros)
    registro_jugadores[jugador][ct.PUNTOS_JUGADOR] += pasada[ct.PUNTOS_JUGADOR]
    registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR] += pasada[ct.MANOS_JUGADAS_JUGADOR]

    hay_ganador = pasada[ct.TERMINO_TABLERO]

    return registro_jugadores, hay_ganador

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

    for fila in range(ct.DURACION):
        tablero_oculto.append([])
        tablero_reset.append([])
        for columna in range(ct.DURACION):
            tablero_oculto[fila].append(contador)
            tablero_reset[fila].append(contador)
            contador += 1

    tableros = tablero_oculto, tablero_reset

    return tableros

# Lucas N


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

# Lucas N


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

# Renzo Martin


def jugada(jugador: str, puntos: int, manos_jugadas: int, tableros: tuple) -> None:
    # Se desarrolla cada jugada, sumandose puntos y manos
    sigue_jugando = True

    hay_ganador = False

    while sigue_jugando and not hay_ganador:

        print("-----------------------------------------------------------")
        print(f"Turno de {jugador} \n")

        filas_y_columnas = recopilar_elecciones(tableros)

        encontro_par = fichas_son_iguales(filas_y_columnas, tableros)

        manos_jugadas += 1

        # HIPOTESIS TOMADA : TODOS DEBEN JUGAR AL MENOS UNA MANO

        if encontro_par:
            puntos += 1
            if manos_jugadas == ct.MAXIMO_MANOS_JUGADAS_PRIMERA_RONDA:
                print(
                    f"{jugador} llego a la maxima cantidad de manos jugadas en la primera ronda.")
                sigue_jugando = False
        else:
            sigue_jugando = False

        hay_ganador = hay_un_ganador(tableros)

        print(f"\nEl jugador {jugador} hasta ahora lleva {puntos} puntos. ")

    return (puntos, manos_jugadas, hay_ganador)

# Lucas C


def validar_ingreso(numero_eleccion: int, palabra: str) -> int:
    # Valida que el valor ingresado sea si o si un numero unico y lo convierte a entero
    valor_inicial = input(
        f"\nElija la {palabra} numero {numero_eleccion} (0 a {ct.CANTIDAD_FICHAS // ct.DURACION - 1}): ")

    while not valor_inicial.isdigit():

        print("Ingrese un valor valido.")
        valor_inicial = input(
            f"\nElija la {palabra} numero {numero_eleccion} (0 a {ct.CANTIDAD_FICHAS // ct.DURACION - 1}): ")

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
    tablero, tablero_oculto = tableros[ct.TABLERO], tableros[ct.TABLERO_OCULTO]
    return tablero_oculto == tablero

# Joaquin Ordonez


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

# Agustin Balino


def recopilar_elecciones(tableros) -> tuple:
    # Se elijen los valores de filas y columnas
    tablero_oculto, tablero = tableros[ct.TABLERO_OCULTO], tableros[ct.TABLERO]

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

# Julian Rando


def guardado_datos_csv(registro: dict, horarios: tuple) -> None:
    registro_ordenado = diccionario_ordenado(registro)

    if not ct.REINICIAR_ARCHIV0_PARTIDAS:
        archivo = open("partidas.csv", "r+")
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]}\n")
    else:
        archivo = open("partidas.csv", "w")
        archivo.write("dia,hora,jugador,aciertos,intentos\n")
        for jugador in registro_ordenado:
            archivo.write(
                f"{horarios[ct.DIA]},{horarios[ct.HORA]},{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]}\n")

    archivo.close()

# AGREGAR AUTOR


def tiempo_hms(inicio: float, final: float) -> tuple:
    # Convierte el tiempo de segundos a horas, minutos y segundos.
    segundos = final - inicio
    horas = int(segundos / ct.PASAJE_HORAS)
    segundos -= horas * ct.PASAJE_HORAS
    minutos = int(segundos / ct.PASAJE_MINUTOS)
    segundos -= minutos * ct.PASAJE_MINUTOS

    return (horas, minutos, segundos)


def registro_tiempos(inicio: float) -> tuple:
    final = time.time()
    tiempo_jugado = tiempo_hms(inicio, final)
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


def datos_partidas_multiples(registro_jugadores: dict, datos_totales: dict):
    for jugador in registro_jugadores:
        if jugador not in datos_totales:
            datos_totales[jugador] = registro_jugadores[jugador]
        else:
            datos_totales[jugador][ct.PUNTOS_JUGADOR] += registro_jugadores[jugador][ct.PUNTOS_JUGADOR]
            datos_totales[jugador][ct.MANOS_JUGADAS_JUGADOR] += registro_jugadores[jugador][ct.MANOS_JUGADAS_JUGADOR]

    return datos_totales

# Julian Rando


def fin_de_partida(registro_partida: dict, tiempo: tuple) -> None:
    # nombres de los jugadores, con su respectiva cantidad de aciertos, el total de intentos y la cantidad promedio de intentos.
    registro_ordenado = diccionario_ordenado(registro_partida)
    ganador = list(registro_ordenado.keys())[0]

    for jugador in registro_ordenado:
        if registro_ordenado[jugador][ct.PUNTOS_JUGADOR] == registro_ordenado[ganador][ct.PUNTOS_JUGADOR]:
            if registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] > registro_ordenado[ganador][ct.MANOS_JUGADAS_JUGADOR]:
                ganador = jugador
            elif registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] == registro_ordenado[ganador][ct.MANOS_JUGADAS_JUGADOR]:
                ganador_dos = jugador

    print(
        f"El tiempo jugado fue de {tiempo[ct.HORAS]} horas, {tiempo[ct.MINUTOS]} minutos y {round(tiempo[ct.SEGUNDOS],2)} segundos\n")

    archivo = open("partida_individual.csv", "w")
    archivo.write("jugador,aciertos,intentos,efectividad\n")
    for jugador in registro_ordenado:
        efectividad = round(registro_ordenado[jugador][ct.PUNTOS_JUGADOR]
                            * 100 / registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR], 1)
        if jugador == ganador or jugador == ganador_dos:
            archivo.write(
                f"{jugador} ES EL GANADOR,{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{efectividad}%\n")

    archivo.close()

    me.mostrar_estadisticas("partida_individual.csv")

# Julian Rando


def fin_de_juego(cantidad_partidas: int, datos_totales: dict) -> None:

    registro_ordenado = diccionario_ordenado(datos_totales)
    mvp = list(registro_ordenado.keys())[0]

    for jugador in registro_ordenado:
        if registro_ordenado[jugador][ct.PUNTOS_JUGADOR] == registro_ordenado[mvp][ct.PUNTOS_JUGADOR]:
            if registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] > registro_ordenado[mvp][ct.MANOS_JUGADAS_JUGADOR]:
                mvp = jugador
            elif registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] == registro_ordenado[mvp][ct.MANOS_JUGADAS_JUGADOR]:
                mvp_dos = jugador

    print(f"Se han jugado un total de {cantidad_partidas} partidas")

    archivo = open("partida_total.csv", "w")
    archivo.write(
        "jugador,aciertos_totales,intentos_totales,promedio_aciertos,promedio_intentos,efectividad\n")

    for jugador in registro_ordenado:
        promedio_puntos = round(
            registro_ordenado[jugador][ct.PUNTOS_JUGADOR] / cantidad_partidas, 1)
        promedio_intentos = round(
            registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR] / cantidad_partidas, 1)
        efectividad = round((promedio_intentos * 100) / promedio_puntos, 1)
        if jugador == mvp or jugador == mvp_dos:
            archivo.write(
                f"MVP {jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro_ordenado[jugador][ct.PUNTOS_JUGADOR]},{registro_ordenado[jugador][ct.MANOS_JUGADAS_JUGADOR]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")
    archivo.close()

    me.mostrar_estadisticas("partida_total.csv")


main()
