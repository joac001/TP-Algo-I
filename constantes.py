def leer(archivo):
    # Lee una linea de un archivo .csv
    linea = archivo.readline()
    if (linea):
        linea = linea.rstrip()
        devolver = linea.split(",")
    else:
        devolver = None
    return devolver


# Utilizadas para la lectura del archivo de configuracion
PARAMETRIZACION = 0
VALOR_PARAMETRIZACION = 1
SITIO_OBTENIDO = 0


def leer_y_declarar_constantes() -> dict:
    # Lectura del archivo de configuracion
    parametrizaciones_default = {"CANTIDAD_FICHAS": [0, 16], "MAXIMO_JUGADORES": [
        0, 3], "MAXIMO_PARTIDAS": [0, 4], "REINICIAR_ARCHIV0_PARTIDAS": [0, "False"]}
    archivo = open("archivos/configuracion.csv", "r")
    registro = leer(archivo)
    while (registro):
        if registro[PARAMETRIZACION] == "REINICIAR_ARCHIV0_PARTIDAS":
            if parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] == "True":
                parametrizaciones_default[registro[PARAMETRIZACION]
                                          ][VALOR_PARAMETRIZACION] = True
            else:
                parametrizaciones_default[registro[PARAMETRIZACION]
                                          ][VALOR_PARAMETRIZACION] = False
        elif registro[PARAMETRIZACION] in parametrizaciones_default:
            parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = int(
                registro[VALOR_PARAMETRIZACION])
        parametrizaciones_default[registro[PARAMETRIZACION]
                                  ][SITIO_OBTENIDO] += 1
        registro = leer(archivo)
    archivo.close()

    # Si el primer valor de la lista vale 0, fue obtendio por default, si vale 1 fue obtenido por configuracion.
    for parametro in parametrizaciones_default:
        if parametrizaciones_default[parametro][SITIO_OBTENIDO] == 0:
            print(
                f"{parametro} vale {parametrizaciones_default[parametro][VALOR_PARAMETRIZACION]} y fue establecido por default")
        else:
            print(
                f"{parametro} vale {parametrizaciones_default[parametro][VALOR_PARAMETRIZACION]} y fue establecido por el archivo de configuracion")

    # Desempaquetado de los valores de la parametrizacion
    cantidad_fichas, maximo_jugadores, maximo_partidas, reiniciar_archiv0_partidas = parametrizaciones_default.values()
    CANTIDAD_FICHAS = cantidad_fichas[VALOR_PARAMETRIZACION]
    MAXIMO_JUGADORES = maximo_jugadores[VALOR_PARAMETRIZACION]
    MAXIMO_PARTIDAS = maximo_partidas[VALOR_PARAMETRIZACION]
    REINICIAR_ARCHIV0_PARTIDAS = reiniciar_archiv0_partidas[VALOR_PARAMETRIZACION]

    return CANTIDAD_FICHAS, MAXIMO_JUGADORES, MAXIMO_PARTIDAS, REINICIAR_ARCHIV0_PARTIDAS


# Desempaquetado de datos del archivo de configuracion.csv
parametrizaciones = leer_y_declarar_constantes()
CANTIDAD_FICHAS, MAXIMO_JUGADORES, MAXIMO_PARTIDAS, REINICIAR_ARCHIV0_PARTIDAS = parametrizaciones[
    0], parametrizaciones[1], parametrizaciones[2], parametrizaciones[3]


def continuar():
    # Lectura y desempaquetado del archivo sigue_jugando.csv
    archivo = open("archivos/sigue_jugando.csv", "r")
    registro = leer(archivo)
    if registro[1] == "False":
        continua_jugando = False
    else:
        continua_jugando = True
    archivo.close()
    return continua_jugando


continua_jugando = continuar()
jugadores = []

# Desempaquetado de datos en la funcion fichas_son_iguales
FILA_UNO = 0
COLUMNA_UNO = 1
FILA_DOS = 2
COLUMNA_DOS = 3

# Para la generacion de tableros
DURACION = 4

# Parametro utilizado para obligar a que todos los jugadores jueguen al menos una mano
MAXIMO_MANOS_JUGADAS_PRIMERA_RONDA = (
    CANTIDAD_FICHAS//DURACION)//MAXIMO_JUGADORES

# Letras utilizadas en los tableros
LETRAS = ["A", "A", "B", "B", "C", "C", "D",
          "D", "E", "E", "F", "F", "G", "G", "H", "H"]

# Indices de los registros
PUNTOS_JUGADOR = 0
MANOS_JUGADAS_JUGADOR = 1

# Indices y conversiones del tiempo jugado
HORA = 1
DIA = 2
HORAS = 0
MINUTOS = 1
SEGUNDOS = 2
PASAJE_HORAS = 3600
PASAJE_MINUTOS = 60
TIEMPO_JUGADO = 0

# Indices de tableros
TERMINO_TABLERO = 2
TABLERO_OCULTO = 0
TABLERO = 1
TABLERO_RESET = 2

# Constantes para validaciones de contrasenia
MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
EXCEPCIONES = "_-áéíóú"

# Indice del inicio de sesion y registro
USUARIO = 0
CONTRASENIA = 1


def seteo_sigue_jugando_true():
    # Configura inicialmente el archivo sigue_jugando para comenzar en True
    archivo = open("archivos/sigue_jugando.csv", "w")
    archivo.write("SIGUE_JUGANDO,True")
    archivo.close()


seteo_sigue_jugando_true()
