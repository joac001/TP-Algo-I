# Archivo hecho por Joaquin Ordonez #
#   #   #   #   #   #   #   #   #   #

# Utilizamos tkinter para generar la interfaz del programa
from tkinter import *
# importamos esta funcion de functools que ayuda a ejecutar "limpiamente" las funciones dentro de las interfazes de tkinter
from functools import partial


def crear_interfaz():
    raiz = Tk()
    raiz.title("Memotest")
    raiz.geometry('370x130')
    raiz.config(bg="#FF6800")
    raiz.iconbitmap("zanahoria.ico")
    mi_frame = Frame(raiz, width=1200, height=600)
    mi_frame.config(bg="#FF6800")
    mi_frame.pack()

    entry_jugador_uno = Entry(mi_frame)
    entry_jugador_uno.grid(row=0, column=1, padx=10, pady=10)

    entry_jugador_dos = Entry(mi_frame)
    entry_jugador_dos.grid(row=1, column=1, padx=10, pady=10)

    label_jugador_uno = Label(
        mi_frame, text="Primer participante:", font=("Arial Black", 9))
    label_jugador_uno.config(bg="#FF6800")
    label_jugador_uno.grid(row=0, column=0, sticky="e", padx=10, pady=10)

    label_jugador_dos = Label(
        mi_frame, text="Segundo participante:", font=("Arial Black", 9))
    label_jugador_dos.config(bg="#FF6800")
    label_jugador_dos.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    dict_de_jugadores = {}

    def codigo_boton(entry_jugador_uno: str, entry_jugador_dos: str, dict_de_jugadores: dict) -> dict:
        #  Funcionalidad del boton. Obtiene los nombres de los jugadores

        if entry_jugador_uno.get() == "":
            dict_de_jugadores["jugador_uno"] = "Jugador 1"
        else:
            dict_de_jugadores["jugador_uno"] = entry_jugador_uno.get()

        if entry_jugador_dos.get() == "":
            dict_de_jugadores["jugador_dos"] = "Jugador 2"
        else:
            dict_de_jugadores["jugador_dos"] = entry_jugador_dos.get()

        raiz.destroy()
        return dict_de_jugadores

    boton_usuarios = Button(raiz, text="Enviar", font=("Arial Black", 9), command=partial(
        codigo_boton, entry_jugador_uno, entry_jugador_dos, dict_de_jugadores))
    boton_usuarios.config(bg="#FCA468", relief="solid", bd=1.5)
    boton_usuarios.pack()

    raiz.mainloop()

    return dict_de_jugadores