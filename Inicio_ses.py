import Main

USUARIO = 0
CONTRASENIA = 1

def leer(usuarios):
    linea = usuarios.readline()
    if (linea):
        linea = linea.rstrip()
        devolver = linea.split(",")
    else:
        devolver = None
    return devolver

def validar_usuario_y_contraseña(usuario: str, contra: str) -> bool:
    archivo = open("Usuarios.txt", "r")
    registro = leer(archivo)
    esta_registrado = False
    clave_correcta = False

    while (registro):
        if usuario == registro[USUARIO] and contra == registro[CONTRASENIA]:
            esta_registrado = True
            clave_correcta = True
            registro = leer(archivo)
        elif usuario == registro[USUARIO] and contra != registro[CONTRASENIA]:
            esta_registrado = True
            registro = leer(archivo)
        else:
            registro = leer(archivo)
    
    if esta_registrado and clave_correcta:
        lista_de_jugadores(usuario)
    elif esta_registrado and not clave_correcta:
        print("Clave incorrecta")
    else: 
        print(f"El usuario {usuario} no esta registrado")


def lista_de_jugadores(usuario: str) -> list:
    contador = 0
    jugadores = []

    jugadores[contador] = usuario

    contador += 1

    return jugadores
