from tkinter import *
from functools import partial
import constantes as ct
import main as mn

# Interfaz raíz
def interfaz_principal():
    raiz = Tk()
    raiz.title("Memotest")
    raiz.geometry('500x230')
    raiz.config(bg="#FF6800")
    raiz.iconbitmap("zanahoria.ico")

    raiz_frame = Frame(raiz, width=1200, height=600)
    raiz_frame.config(bg="#FF6800")

    # labels
    label_titulo_ingreso = Label(
        raiz_frame, text="Iniciar sesion", font=("Arial Black", 12))
    label_titulo_ingreso.config(bg="#FF6800")
    label_titulo_ingreso.grid(row=0, column=1, padx=10, pady=10)

    label_usuario_ingreso = Label(
        raiz_frame, text="USUARIO", font=("Arial Black", 9))
    label_usuario_ingreso.config(bg="#FF6800")
    label_usuario_ingreso.grid(row=1, column=0, padx=10, pady=10)

    label_contra_ingreso = Label(
        raiz_frame, text="CONTRASEÑA", font=("Arial Black", 9))
    label_contra_ingreso.config(bg="#FF6800")
    label_contra_ingreso.grid(row=2, column=0, padx=10, pady=10)

    # Entry - Ingreso
    # Usuario
    entry_usuario_ingreso = Entry(raiz_frame)
    entry_usuario_ingreso.grid(row=1, column=1, padx=10, pady=10)

    # Contrasenia
    entry_contra_ingreso = Entry(raiz_frame)
    entry_contra_ingreso.grid(row=2, column=1, padx=10, pady=10)
    entry_contra_ingreso.config(show="*")

    # Botones
    # Ingreso
    boton_ingreso = Button(raiz_frame, text="Ingresar jugador", font=(
        "Arial Black", 9), command=partial(codigo_boton_ingreso, raiz, entry_usuario_ingreso, entry_contra_ingreso))

    boton_ingreso.grid(row=4, column=2, padx=10, pady=10)
    boton_ingreso.config(bg="#FCA468", relief="solid", bd=1.5)

    # Registro
    boton_registro = Button(raiz_frame, text="Registre un jugador", font=(
        "Arial Black", 9), command=partial(codigo_boton_registro))

    boton_registro.grid(row=4, column=0, padx=10, pady=10)
    boton_registro.config(bg="#FCA468", relief="solid", bd=1.5)

    # inicio partida
    boton_jugar = Button(raiz_frame, text="Iniciar Partida", font=(
        "Arial Black", 9), command=partial(codigo_boton_jugar, raiz))

    boton_jugar.grid(row=5, column=1, padx=10, pady=10)
    boton_jugar.config(bg="#FCA468", relief="solid", bd=1.5)

    raiz.mainloop()


def codigo_boton_jugar(raiz):
    raiz.destroy()
    mn.main()

# Registro
def codigo_boton_envio_registro(v_registro, entry_usuario, entry_contra_uno, entry_contra_dos):
    # Recopilacion de datos de usuario
    usuario = entry_usuario.get()
    entry_usuario.delete(0, "end")
    lista_contras = [entry_contra_uno.get(),
                     entry_contra_dos.get()]
    entry_contra_uno.delete(0, "end")
    entry_contra_dos.delete(0, "end")

    v_registro.destroy()

    registro_usuario_nuevo(usuario, lista_contras)


def codigo_boton_registro():

    v_registro = Tk()
    v_registro.title("Registro")
    v_registro.geometry('500x230')
    v_registro.config(bg="#FF6800")
    v_registro.iconbitmap("zanahoria.ico")

    v_registro_frame = Frame(v_registro, width=1200, height=600)
    v_registro_frame.config(bg="#FF6800")

    # Labels - Registro
    # TITULO
    label_titulo_registro = Label(
        v_registro_frame, text="Registre un usuario", font=("Arial Black", 10))

    label_titulo_registro.config(bg="#FF6800")
    label_titulo_registro.grid(row=0, column=1, padx=10, pady=10)

    # USUARIO
    label_usuario_registro = Label(
        v_registro_frame, text="USUARIO", font=("Arial Black", 9))

    label_usuario_registro.config(bg="#FF6800")
    label_usuario_registro.grid(row=1, column=0, padx=10, pady=10)

    # CONTRASEÑA 1
    label_contra_uno_registro = Label(
        v_registro_frame, text="CONTRASEÑA", font=("Arial Black", 9))
    label_contra_uno_registro.config(bg="#FF6800")
    label_contra_uno_registro.grid(row=2, column=0, padx=10, pady=10)

    # CONTRASEÑA 2
    label_contra_dos_registro = Label(
        v_registro_frame, text="REPITA LA CONTRASEÑA", font=("Arial Black", 9))

    label_contra_dos_registro.config(bg="#FF6800")
    label_contra_dos_registro.grid(row=3, column=0, padx=10, pady=10)

    # Entry - Registro
    # Usuario
    entry_usuario_registro = Entry(v_registro_frame)
    entry_usuario_registro.grid(row=1, column=1, padx=10, pady=10)

    # CONTRASEÑA
    # 1
    entry_contra_uno_registro = Entry(v_registro_frame)
    entry_contra_uno_registro.grid(row=2, column=1, padx=10, pady=10)
    entry_contra_uno_registro.config(show="*")
    # 2
    entry_contra_dos_registro = Entry(v_registro_frame)
    entry_contra_dos_registro.grid(row=3, column=1, padx=10, pady=10)
    entry_contra_dos_registro.config(show="*")

    boton_envio_registro = Button(v_registro_frame, text="Registrarse", font=(
        "Arial Black", 9), command=partial(codigo_boton_envio_registro, v_registro, entry_usuario_registro, entry_contra_uno_registro, entry_contra_dos_registro))

    boton_envio_registro.grid(row=4, column=1, padx=10, pady=10)
    boton_envio_registro.config(bg="#FCA468", relief="solid", bd=1.5)

# Inicio sesion
def codigo_boton_ingreso(raiz, entry_usuario, entry_contra_uno):
    # Recopilacion de datos de usuario
    usuario = entry_usuario.get()
    entry_usuario.delete(0, "end")
    # En caso de ingreso
    contra = entry_contra_uno.get()
    entry_contra_uno.delete(0, "end")
    validar_usuario_y_contrasenia(raiz, usuario, contra)


def validar_usuario_y_contrasenia(raiz, usuario: str, contra: str) -> bool:
    archivo = open("usuarios.csv", "r")
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
        mn.suma_de_jugadores(usuario)
        if len(mn.jugadores) == ct.MAXIMO_JUGADORES:
            print("Maximo de jugadores alcanzado, comenzará la partida")
            raiz.destroy()
            mn.main()
    elif esta_registrado and not clave_correcta:
        print("Clave incorrecta")

    else:
        print(f"El usuario {usuario} no esta registrado")


def leer(usuarios):
    linea = usuarios.readline()
    if (linea):
        linea = linea.rstrip()
        devolver = linea.split(",")
    else:
        devolver = None
    return devolver


def registro(nombre: str, contra: str):
    archivo = open("usuarios.csv", "r+")
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
