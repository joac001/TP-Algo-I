import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import *
from functools import partial

from programa import constantes as ct


def diccionario_ordenado(diccionario: dict) -> dict:  # Joaquin Ordoñez
    # Recibe un diccionario y lo ordena por sus values de mayor a menor

    valores_ordenados = sorted(diccionario.values(), reverse=True)
    diccionario_ordenado = {}

    for valores in valores_ordenados:

        for clave in diccionario.keys():

            if diccionario[clave] == valores:
                diccionario_ordenado[clave] = diccionario[clave]

    return diccionario_ordenado


def obtencion_ganadores(registro: dict) -> list:  # Lucas Capocasa
    # Obtiene los ganadores del juego con dos criterios, primero mayor cantidad de puntos y en
    # caso de igualdad menor cantidad de manos jugadas
    posibles_ganadores = {}
    ganadores = []
    max_punto = max(registro.values(), key=lambda i: i[ct.PUNTOS_JUGADOR])[
        ct.PUNTOS_JUGADOR]

    for jugador in registro:

        if registro[jugador][ct.PUNTOS_JUGADOR] == max_punto:
            posibles_ganadores[jugador] = registro[jugador]

    menor_manos = min(posibles_ganadores.values(),
                      key=lambda i: i[ct.MANOS_JUGADAS])[ct.MANOS_JUGADAS]

    for jugador in posibles_ganadores:

        if posibles_ganadores[jugador][ct.MANOS_JUGADAS] == menor_manos:
            ganadores.append(jugador)

    return ganadores


def fin_de_partida(registro_partida: dict, tiempo: tuple) -> None:  # Julian Rando
    # Crea archivo csv con las estadisticas de la partida individual para luego imprimirlo por interfaz grafica
    ganadores = obtencion_ganadores(registro_partida)
    registro = diccionario_ordenado(registro_partida)

    print("-----------------------------------------------------------\n")
    print(
        f"El tiempo jugado fue de {tiempo[ct.HORAS]} horas, {tiempo[ct.MINUTOS]} minutos y {round(tiempo[ct.SEGUNDOS],2)} segundos\n")

    archivo = open("archivos/partida_individual.csv", "w")
    archivo.write("jugador,aciertos,intentos,efectividad\n")

    for jugador in registro:

        try:
            efectividad = round(registro[jugador][ct.PUNTOS_JUGADOR] *
                                ct.PORCENTAJE_MAXIMO / registro[jugador][ct.MANOS_JUGADAS], 1)
        except:
            efectividad = 0

        if jugador in ganadores:
            archivo.write(
                f"{jugador} ES EL GANADOR,{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]},{efectividad}%\n")

    archivo.close()

    mostrar_estadisticas("archivos/partida_individual.csv")


def fin_de_juego(cantidad_partidas: int) -> None:  # Julian Rando
    # Crea archivo csv con las estadisticas del juego total para luego imprimirlo por interfaz grafica
    registro = diccionario_ordenado(ct.registro_general)
    mvps = obtencion_ganadores(registro)

    print(f"Se han jugado un total de {cantidad_partidas} partidas")

    archivo = open("archivos/partida_total.csv", "w")
    archivo.write(
        "jugador,aciertos_totales,intentos_totales,promedio_aciertos,promedio_intentos,efectividad\n")

    for jugador in registro:

        promedio_puntos = round(
            registro[jugador][ct.PUNTOS_JUGADOR] / cantidad_partidas, 1)
        promedio_intentos = round(
            registro[jugador][ct.MANOS_JUGADAS] / cantidad_partidas, 1)

        try:
            efectividad = round(registro[jugador][ct.PUNTOS_JUGADOR] *
                                ct.PORCENTAJE_MAXIMO / registro[jugador][ct.MANOS_JUGADAS], 1)
        except:
            efectividad = 0

        if jugador in mvps:
            archivo.write(
                f"MVP {jugador},{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")
        else:
            archivo.write(
                f"{jugador},{registro[jugador][ct.PUNTOS_JUGADOR]},{registro[jugador][ct.MANOS_JUGADAS]},{promedio_puntos},{promedio_intentos},{efectividad}%\n")

    archivo.close()

    mostrar_estadisticas("archivos/partida_total.csv")


# Joaquin Ordonez: Williams, R.(2020, 25 de julio). How to view Excel File or Pandas DataFrame in Tkinter (Python GUI)[Video]. YouTube. https//www.youtube.com/watch?v=PgLjwl6Br0k
def mostrar_estadisticas(ruta_archivo: str) -> None:
    # Interfaz grafica para mostrar estadisticas de la partida
    v_estadisticas = tk.Tk()

    if ruta_archivo == "archivos/partida_individual.csv":
        v_estadisticas.title("Estadisticas de la ultima partida")
    else:
        v_estadisticas.title("Estadisticas totales de las partidas")

    v_estadisticas.iconbitmap("archivos/zanahoria.ico")
    v_estadisticas.geometry("1200x350")
    v_estadisticas.pack_propagate(False)

    vista = tk.LabelFrame(v_estadisticas)
    vista.place(relheight=1, relwidth=1)
    vista.config(bg="#FCA468")

    v_datos = ttk.Treeview(vista)
    v_datos.place(relheight=1, relwidth=1)

    style = ttk.Style(v_datos)
    style.theme_use("clam")
    style.configure("Treeview", background="#FCA468",
                    fieldbackground="#FCA468")

    scroll_y = tk.Scrollbar(
        vista, orient="vertical", command=v_datos.yview)
    v_datos.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(
        vista, orient="horizontal", command=v_datos.xview)
    v_datos.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side="bottom", fill="x")

    data_frame = pd.read_csv(ruta_archivo)

    v_datos["column"] = list(data_frame.columns)
    v_datos["show"] = "headings"

    for column in v_datos["columns"]:
        v_datos.heading(column, text=column)

    data_frame_rows = data_frame.to_numpy().tolist()

    for row in data_frame_rows:
        v_datos.insert("", "end", values=row)

    if ruta_archivo == "archivos/partida_individual.csv":
        v_estadisticas.attributes('-disabled', True)

        def sigue_jugando(v_continuar, v_estadisticas) -> None:
            # Boton seguir jugando
            ct.continuar_jugando = True
            v_continuar.destroy()
            v_estadisticas.destroy()

        def no_sigue_jugando(v_continuar, v_estadisticas) -> None:
            # Boton no quiere seguir jugando
            ct.continuar_jugando = False
            v_continuar.destroy()
            v_estadisticas.destroy()

        # Interfaz que permite jugar otra partida
        v_continuar = Tk()
        v_continuar.title("")
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
            "Arial Black", 9), command=partial(sigue_jugando, v_continuar, v_estadisticas))
        boton_si.config(bg="#FCA468", relief="solid", bd=1.5)
        boton_si.grid(row=0, column=1, padx=10, pady=10)

        boton_no = Button(v_continuar_frame, text="NO", font=(
            "Arial Black", 9), command=partial(no_sigue_jugando, v_continuar, v_estadisticas))
        boton_no.config(bg="#FCA468", relief="solid", bd=1.5)
        boton_no.grid(row=0, column=2, padx=10, pady=10)

        v_continuar.mainloop()

    v_estadisticas.mainloop()
