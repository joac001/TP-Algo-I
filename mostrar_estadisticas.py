import pandas as pd

import tkinter as tk
from tkinter import ttk


def mostrar_estadisticas(ruta_archivo: str):
    v_estadisticas = tk.Tk()
    v_estadisticas.title("Estadisticas de la partida")
    v_estadisticas.iconbitmap("zanahoria.ico")
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

    v_estadisticas.mainloop()


mostrar_estadisticas("partidas.csv")
