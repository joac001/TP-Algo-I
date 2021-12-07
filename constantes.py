def leer(usuarios):
    linea = usuarios.readline()
    if (linea):
        linea = linea.rstrip()
        devolver = linea.split(",")
    else:
        devolver = None
    return devolver


PARAMETRIZACION = 0
VALOR_PARAMETRIZACION = 1
SITIO_OBTENIDO = 0

# Constantes obtenidas del archivo de configuracion
def leer_y_declarar_constantes() -> dict:
    parametrizaciones_default = {"CANTIDAD_FICHAS": [0,16], "MAXIMO_JUGADORES": [0,3], "MAXIMO_PARTIDAS": [0,4], "REINICIAR_ARCHIV0_PARTIDAS": [0,4]}
    archivo = open("configuracion.csv", "r")
    registro = leer(archivo)
    while (registro):
        if registro[PARAMETRIZACION] == "REINICIAR_ARCHIV0_PARTIDAS":
            parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = bool(registro[VALOR_PARAMETRIZACION])
        elif registro[PARAMETRIZACION] in parametrizaciones_default:
            parametrizaciones_default[registro[PARAMETRIZACION]][VALOR_PARAMETRIZACION] = int(registro[VALOR_PARAMETRIZACION])
        parametrizaciones_default[registro[PARAMETRIZACION]][SITIO_OBTENIDO] += 1
        registro = leer(archivo)
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


archivo = open("sigue_jugando.csv","w")
archivo.write("SIGUE_JUGANDO,True")
archivo.close()


def continuar():
    archivo = open("sigue_jugando.csv", "r")
    registro = leer(archivo)
    if registro[1] == "False":
        continua_jugando = False
    else:
        continua_jugando = True
    archivo.close()
    return continua_jugando

continua_jugando = continuar()


FILA_UNO = 0
COLUMNA_UNO = 1
FILA_DOS = 2
COLUMNA_DOS = 3

DURACION = 4 #EX RANGO

#HIPOTESIS
MAXIMO_MANOS_JUGADAS_PRIMERA_RONDA = (CANTIDAD_FICHAS//DURACION)//MAXIMO_JUGADORES


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

MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
EXCEPCIONES = "_-áéíóú"
USUARIO = 0
CONTRASENIA = 1