from programa import juego as jg
import constantes as ct


def validar_usuario_y_contrasenia(raiz, usuario: str, contra: str) -> bool:
    archivo = open("archivos/usuarios.csv", "r")
    registro = leer(archivo)
    esta_registrado = False
    clave_correcta = False

    while (registro):
        if usuario == registro[ct.USUARIO] and contra == registro[ct.CONTRASENIA]:
            esta_registrado = True
            clave_correcta = True
        elif usuario == registro[ct.USUARIO] and contra != registro[ct.CONTRASENIA]:
            esta_registrado = True
        registro = leer(archivo)

    archivo.close()

    if esta_registrado and clave_correcta:
        print(f"Usuario {usuario} ingresado correctamente")
        jg.suma_de_jugadores(usuario)
        if len(ct.jugadores) == ct.MAXIMO_JUGADORES:
            print("Maximo de jugadores alcanzado, comenzará la partida")
            raiz.destroy()
            jg.main()
    elif esta_registrado and not clave_correcta:
        print("Clave incorrecta")

    else:
        print(f"El usuario {usuario} no esta registrado")


def validar_nombre_usuario(nombre: str) -> bool:
    es_valido = False

    if len(nombre) >= 4 and len(nombre) <= 15:
        nombre_alnum = nombre.replace("_", "")

        if nombre_alnum.isalnum():
            es_valido = True

    return es_valido


def validar_contrasenia(contra: str) -> bool:

    es_valido = False

    for excepcion in ct.EXCEPCIONES:
        if excepcion in contra:
            contra_alnum = contra.replace(excepcion, "")

    if len(contra) >= 8 and len(contra) <= 12 and (contra.find("_") != -1 or contra.find("-") != -1) and contra_alnum.isalnum():

        contiene_mayuscula = False
        contiene_minuscula = False
        contiene_numero = False

        for caracter in contra:
            if caracter in ct.MAYUSCULAS:
                contiene_mayuscula = True
            elif caracter in ct.MINUSCULAS:
                contiene_minuscula = True
            elif caracter in ct.NUMEROS:
                contiene_numero = True

        if contiene_mayuscula and contiene_minuscula and contiene_numero:
            es_valido = True

    return es_valido


def registro_usuario_nuevo(nombre: str, lista_contras: list):
    contra_uno, contra_dos = lista_contras[0], lista_contras[1]
    usuario = validar_nombre_usuario(nombre)

    if contra_uno == contra_dos:
        contrasenia = validar_contrasenia(contra_uno)

        if usuario and contrasenia:
            registro(nombre, contra_uno)
        elif not usuario:
            print("¡Nombre de usuario no valido!")
        elif not contrasenia:
            print("¡Contrasenia no valida!")

    else:
        print("¡Las contrasenias no son iguales!")


def registro(nombre: str, contra: str):
    archivo = open("archivos/usuarios.csv", "r+")
    registro = leer(archivo)
    esta_registrado = False

    while (registro):
        if nombre == registro[ct.USUARIO]:
            esta_registrado = True
        registro = leer(archivo)

    if esta_registrado:
        print("Nombre de usuario ya registrado")
    else:
        archivo.write(f"\n{nombre},{contra}")
        print("Usuario registrado con exito")

    archivo.close()


def leer(archivo):
    # Lee una linea de un archivo .csv
    linea = archivo.readline()
    if (linea):
        linea = linea.rstrip()
        devolver = linea.split(",")
    else:
        devolver = None
    return devolver
