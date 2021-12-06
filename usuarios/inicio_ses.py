import main as mn
import registro as rg

USUARIO = 0
CONTRASENIA = 1

def validar_usuario_y_contrasenia(usuario: str, contra: str) -> bool:
    archivo = open("usuarios.csv", "r")
    registro = rg.leer(archivo)
    esta_registrado = False
    clave_correcta = False

    while (registro):
        if usuario == registro[USUARIO] and contra == registro[CONTRASENIA]:
            esta_registrado = True
            clave_correcta = True
            registro = rg.leer(archivo)
        elif usuario == registro[USUARIO] and contra != registro[CONTRASENIA]:
            esta_registrado = True
            registro = rg.leer(archivo)
        else:
            registro = rg.leer(archivo)

    archivo.close()

    if esta_registrado and clave_correcta:
        suma_de_jugadores(usuario)
        print(f"Usuario {usuario} ingresado correctamente")
        if len(jugadores) == mn.MAXIMO_JUGADORES:
            print("Maximo de jugadores alcanzado, comenzará la partida")
            mn.main()
    elif esta_registrado and not clave_correcta:
        print("Clave incorrecta")

    else:
        print(f"El usuario {usuario} no esta registrado")

jugadores = []
def suma_de_jugadores(usuario: str):
    contador = 0
    jugadores.append(usuario)
    contador += 1
    print ("Los usuarion ingresados son:")
    for jugador in jugadores:
        print(f"-> {jugador}")

        return jugadores