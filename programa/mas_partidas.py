from tkinter import *
from functools import partial


def mas_partidas():
    # Interfaz deseo de jugar otra partida
    v_continuar = Tk()
    v_continuar.title("Memotest")
    v_continuar.geometry("350x50")
    v_continuar.config(bg="#FF6800")
    v_continuar.iconbitmap("archivos/zanahoria.ico")

    v_continuar_frame = Frame(v_continuar, width=100, height=100)
    v_continuar_frame.config(bg="#FF6800")
    v_continuar_frame.place(relheight=1, relwidth=1)

    label_titulo = Label(
        v_continuar_frame, text="¿Desea seguir jugando?", font=("Arial Black", 12))
    label_titulo.config(bg="#FF6800")
    label_titulo.grid(row=0, column=0, padx=10, pady=10)

    boton_si = Button(v_continuar_frame, text="SI", font=(
        "Arial Black", 9), command=partial(sigue_jugando, v_continuar))
    boton_si.config(bg="#FCA468", relief="solid", bd=1.5)
    boton_si.grid(row=0, column=1, padx=10, pady=10)

    boton_no = Button(v_continuar_frame, text="NO", font=(
        "Arial Black", 9), command=partial(no_sigue_jugando, v_continuar))
    boton_no.config(bg="#FCA468", relief="solid", bd=1.5)
    boton_no.grid(row=0, column=2, padx=10, pady=10)

    v_continuar.mainloop()


def sigue_jugando(v_continuar):
    # Boton si quiere seguir jugando
    v_continuar.destroy()


def no_sigue_jugando(v_continuar):
    # Boton no quiere seguir jugando
    archivo = open("archivos/sigue_jugando.csv", "w")
    archivo.write("SIGUE_JUGANDO,False")
    archivo.close()
    v_continuar.destroy()
