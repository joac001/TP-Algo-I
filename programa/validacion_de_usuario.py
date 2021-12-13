from string import ascii_lowercase, ascii_uppercase, digits
from colorama import Fore, Style

from programa import juego as jg
from programa import constantes as ct


def usuario_y_claves_validas(raiz, usuario: str, clave: str) -> bool:  # Julian Rando
    # Valida que el usuario ingresado este registrado y que ingrese correctamente su respectiva contraseña
    try:
        archivo = open("archivos/usuarios.csv")
    except:
        archivo = open("archivos/usuarios.csv", "w")
        archivo.close()
        archivo = open("archivos/usuarios.csv")

    registro = ct.leer(archivo)
    esta_registrado = False
    clave_correcta = False

    if usuario and clave:
        while registro and not esta_registrado:

            if usuario == registro[ct.USUARIO] and clave == registro[ct.CONTRASENIA]:
                esta_registrado = True
                clave_correcta = True

            elif usuario == registro[ct.USUARIO] and clave != registro[ct.CONTRASENIA]:
                esta_registrado = True

            registro = ct.leer(archivo)

    archivo.close()

    if esta_registrado and clave_correcta:
        print(Fore.GREEN +
              f"\nUsuario {usuario} ingresado correctamente" + Style.RESET_ALL)
        suma_de_jugadores(usuario)

        if len(ct.jugadores) == ct.MAXIMO_JUGADORES:
            print("\nMaximo de jugadores alcanzado, comenzará la partida")
            raiz.destroy()
            jg.main()

    elif esta_registrado and not clave_correcta:
        print(Fore.RED + Style.BRIGHT + "\nClave incorrecta" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\nEl usuario {usuario} no se encuentra registrado" + Style.RESET_ALL)


def nombre_es_correcto(nombre: str) -> bool:  # Lucas Nuñez
    # Corrobora que el nombre del usuario sea valido
    es_valido = False

    if len(nombre) >= ct.MINIMO_USUARIO and len(nombre) <= ct.MAXIMO_USUARIO:
        nombre_alnum = nombre.replace("_", "")

        if nombre_alnum.isalnum():
            es_valido = True

    return es_valido


def es_clave_valida(clave: str, clave_alnum: str) -> bool:  # Agustin Baliño
    # Condicional para corroborar que la clave sea valida
    return len(clave) >= ct.MINIMO_CLAVE and len(clave) <= ct.MAXIMO_CLAVE and (clave.find("_") != ct.NO_ESTA or clave.find("-") != ct.NO_ESTA) and clave_alnum.isalnum()


def clave_es_correcta(clave: str) -> bool:  # Agustin Baliño
    # Corrobora que la contraseña del usuario sea valida
    es_valido = False
    contiene_mayuscula = False
    contiene_minuscula = False
    contiene_numero = False
    clave_alnum = clave

    for excepcion in ct.EXCEPCIONES:
        clave_alnum = clave_alnum.replace(excepcion, "")

    if es_clave_valida(clave, clave_alnum):

        for caracter in clave:
            if caracter in ascii_uppercase:
                contiene_mayuscula = True
            elif caracter in ascii_lowercase:
                contiene_minuscula = True
            elif caracter in digits:
                contiene_numero = True

        if contiene_mayuscula and contiene_minuscula and contiene_numero:
            es_valido = True

    return es_valido


def registro_usuario_nuevo(nombre: str, claves: tuple) -> None:  # Agustin Baliño
    # Registra nuevos usuarios, corroborando el ingreso correcto de contraseñas y nombre de usuario
    clave, clave_dos = claves[ct.CLAVE_UNO], claves[ct.CLAVE_DOS]
    usuario_es_valido = nombre_es_correcto(nombre)

    if clave == clave_dos:
        clave_es_valida = clave_es_correcta(clave)

        if usuario_es_valido and clave_es_valida:
            registro(nombre, clave)

        elif not usuario_es_valido:
            print(Fore.RED + Style.BRIGHT +
                  "\n¡Nombre de usuario no valido!" + Style.RESET_ALL)

        else:
            print(Fore.RED + Style.BRIGHT +
                  "\n¡Contraseña no valida!" + Style.RESET_ALL)

    else:
        print(Fore.RED + Style.BRIGHT +
              "\n¡Las contraseñas no son iguales!" + Style.RESET_ALL)


def registro(nombre: str, clave: str) -> None:  # Julian Rando
    # Realiza el registro del usuario
    try:
        archivo = open("archivos/usuarios.csv", "r+")
    except:
        archivo = open("archivos/usuarios.csv", "w")
        archivo.close()
        archivo = open("archivos/usuarios,csv", "r+")

    registro = ct.leer(archivo)
    esta_registrado = False

    while registro and not esta_registrado:
        if nombre == registro[ct.USUARIO]:
            esta_registrado = True
        else:
            registro = ct.leer(archivo)

    if esta_registrado:
        print(Fore.RED + Style.BRIGHT +
              "\nNombre de usuario ya registrado" + Style.RESET_ALL)
    else:
        archivo.write(f"{nombre},{clave}\n")
        print(Fore.GREEN + "\nUsuario registrado con exito" + Style.RESET_ALL)

    archivo.close()


def suma_de_jugadores(usuario: str) -> None:  # Renzo Martin
    # Agrega al usuario ingresado a una lista de jugadores
    ct.jugadores.append(usuario)
    print("\nLos jugadores ingresados son:")
    for jugador in ct.jugadores:
        print(f"-> {jugador}")
