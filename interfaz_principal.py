from tkinter import *
from functools import partial

from interfaz import botones as bt


def interfaz_principal() -> None:  # Joaquin Ordoñez
    # Interfaz principal del juego
    raiz = Tk()
    raiz.title("Memotest")
    raiz.geometry('500x230')
    raiz.config(bg="#FF6800")
    raiz.iconbitmap("archivos/zanahoria.ico")

    raiz_frame = Frame(raiz, width=1200, height=600)
    raiz_frame.config(bg="#FF6800")
    raiz_frame.grid(row=0, column=0)

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
    # entry_contra_ingreso.config(show="*")

    # Botones
    # Ingreso
    boton_ingreso = Button(raiz_frame, text="Ingresar jugador", font=(
        "Arial Black", 9), command=partial(bt.codigo_boton_ingreso, raiz, entry_usuario_ingreso, entry_contra_ingreso))

    boton_ingreso.grid(row=4, column=2, padx=10, pady=10)
    boton_ingreso.config(bg="#FCA468", relief="solid", bd=1.5)

    # Registro
    boton_registro = Button(raiz_frame, text="Registre un jugador", font=(
        "Arial Black", 9), command=partial(bt.codigo_boton_registro))

    boton_registro.grid(row=4, column=0, padx=10, pady=10)
    boton_registro.config(bg="#FCA468", relief="solid", bd=1.5)

    # inicio partida
    boton_jugar = Button(raiz_frame, text="Iniciar Partida", font=(
        "Arial Black", 9), command=partial(bt.codigo_boton_jugar, raiz))
    boton_jugar.grid(row=5, column=2, padx=10, pady=10)
    boton_jugar.config(bg="#FCA468", relief="solid", bd=1.5)

    boton_cerrar = Button(raiz_frame, text="Cerrar juego", font=(
        "arial Black", 9), command=partial(bt.codigo_cerrar_juego, raiz))
    boton_cerrar.grid(row=5, column=0, padx=10, pady=10)
    boton_cerrar.config(bg="#FCA468", relief="solid", bd=1.5)

    raiz.mainloop()


interfaz_principal()
