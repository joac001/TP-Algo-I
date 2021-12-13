from programa import parametrizaciones as pt


def leer(archivo) -> list:  # Julian Rando. Fuente: Clase de Algoritmos y Programacion I
    # Lee una linea del archivo
    linea = archivo.readline()
    return linea.rstrip().split(',') if linea else None


# Lista de jugadores y registro general que seran utilizados en la partida
jugadores = []
registro_general = {}


# Desempaquetado de datos del archivo de configuracion.csv
CANTIDAD_FICHAS, MAXIMO_JUGADORES, MAXIMO_PARTIDAS, REINICIAR_ARCHIV0_PARTIDAS = pt.parametros_de_configuracion()


# Parametro utilizado para contiunuar o no jugando
continuar_jugando = True


# Desempaquetado de datos en la funcion "fichas_son_iguales"
FILA_UNO = 0
COLUMNA_UNO = 1
FILA_DOS = 2
COLUMNA_DOS = 3
MINIMO = 0


# Letras utilizadas en los tableros
# Se listan dos veces y se ordenan las letras del diccionario mediante codigo ascii desde la "A" hasta la letra que sea necesaria
LETRAS = 2 * list(map(chr, range(65, 65 + CANTIDAD_FICHAS // 2)))


# Para la generacion de tableros
RANGO_COLUMNAS = 4
RANGO_FILAS = CANTIDAD_FICHAS // RANGO_COLUMNAS
UNIDAD = 1

# Indices de los registros
PUNTOS_JUGADOR = 0
MANOS_JUGADAS = 1


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
TABL_RES = 1


# Para la validacion de la contraseña
EXCEPCIONES = "-áéíóúÁÉÍÓÚ_"
NO_ESTA = -1


# Indice del inicio de sesion y registro
USUARIO = 0
CONTRASENIA = 1
CLAVE_UNO = 0
CLAVE_DOS = 1


# Maximos y minimos para las validaciones de usuario y contraseña
MINIMO_USUARIO = 4
MAXIMO_USUARIO = 15
MINIMO_CLAVE = 8
MAXIMO_CLAVE = 15


# Porcentaje utilizado para obtener efectividad de los jugadores
PORCENTAJE_MAXIMO = 100
