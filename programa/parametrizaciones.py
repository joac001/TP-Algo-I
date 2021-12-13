def leer(archivo) -> list:  # Julian Rando. Fuente: Clase de Algoritmos y Programacion I
    # Lee una linea del archivo
    linea = archivo.readline()
    return linea.rstrip().split(',') if linea else None


# Utilizadas para la lectura del archivo de configuracion
PARAMETRIZACION = 0
VALOR_PARAMETRIZACION = 1
SITIO_OBTENIDO = 0

RANGO_COLUMNAS = 4
UNIDAD = 1


def parametros_de_configuracion() -> tuple:  # Julian Rando
    # Lectura del archivo de configuracion
    parametrizaciones = {"CANTIDAD_FICHAS": [True, 16], "MAXIMO_JUGADORES": [
        True, 3], "MAXIMO_PARTIDAS": [True, 4], "REINICIAR_ARCHIV0_PARTIDAS": [True, "False"]}

    try:
        archivo = open("archivos/configuracion.csv")
    except:
        archivo = open("archivos/configuracion.csv", "w")
        archivo.close()
        archivo = open("archivos/configuracion.csv")

    registro = leer(archivo)

    while registro:

        if registro[PARAMETRIZACION] == "REINICIAR_ARCHIV0_PARTIDAS":

            if registro[VALOR_PARAMETRIZACION] == "True":
                parametrizaciones[registro[PARAMETRIZACION]
                                  ][VALOR_PARAMETRIZACION] = True
            else:
                parametrizaciones[registro[PARAMETRIZACION]
                                  ][VALOR_PARAMETRIZACION] = False

        elif registro[PARAMETRIZACION] in parametrizaciones:
            parametrizaciones[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = int(
                registro[VALOR_PARAMETRIZACION])

        parametrizaciones[registro[PARAMETRIZACION]][SITIO_OBTENIDO] = False
        registro = leer(archivo)

    archivo.close()

    if parametrizaciones["CANTIDAD_FICHAS"][VALOR_PARAMETRIZACION] % RANGO_COLUMNAS != 0:
        parametrizaciones["CANTIDAD_FICHAS"][VALOR_PARAMETRIZACION] = acomodar_cantidad_fichas(
            parametrizaciones["CANTIDAD_FICHAS"][VALOR_PARAMETRIZACION])

    mostrar_parametrizaciones(parametrizaciones)

    cantidad_fichas, maximo_jugadores, maximo_partidas, reiniciar_archiv0_partidas = parametrizaciones.values()

    return cantidad_fichas[VALOR_PARAMETRIZACION], maximo_jugadores[VALOR_PARAMETRIZACION], maximo_partidas[VALOR_PARAMETRIZACION], reiniciar_archiv0_partidas[VALOR_PARAMETRIZACION]


def acomodar_cantidad_fichas(cantidad_fichas: int) -> int:  # Julian Rando
    # se sumara una ficha hasta que todas tengan su par y que la creacion de tableros sea correcta
    fichas_sumadas = 0

    while cantidad_fichas % RANGO_COLUMNAS != 0:

        cantidad_fichas += 1
        fichas_sumadas += 1

    print(
        f'\nAl parametro "Cantidad de fichas" se le han sumado {fichas_sumadas} fichas para la correcta creacion del tablero')

    return cantidad_fichas


def mostrar_parametrizaciones(parametrizaciones: dict) -> None:  # Julian Rando
    # Muestra el valor de las parametrizaciones y de donde fue obtenida
    for parametro in parametrizaciones:

        if parametrizaciones[parametro][SITIO_OBTENIDO]:
            print(
                f"\n{parametro} vale {parametrizaciones[parametro][VALOR_PARAMETRIZACION]} y fue establecido por default")

        else:
            print(
                f"\n{parametro} vale {parametrizaciones[parametro][VALOR_PARAMETRIZACION]} y fue establecido por el archivo de configuracion")
