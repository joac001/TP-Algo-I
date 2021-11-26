# Joaquin Ordonez
raiz = Tk()
raiz.title("Memotest")
raiz.geometry('370x130')
raiz.config(bg="#FF6800")
raiz.iconbitmap("zanahoria.ico")
mi_frame = Frame(raiz, width=1200, height=600)
mi_frame.config(bg="#FF6800")
mi_frame.pack()

entry_jugador_1 = Entry(mi_frame)
entry_jugador_1.grid(row=0, column=1, padx=10, pady=10)

entry_jugador_2 = Entry(mi_frame)
entry_jugador_2.grid(row=1, column=1, padx=10, pady=10)

label_jugador_1 = Label(
    mi_frame, text="Primer participante:", font=("Arial Black", 9))
label_jugador_1.config(bg="#FF6800")
label_jugador_1.grid(row=0, column=0, sticky="e", padx=10, pady=10)

label_jugador_2 = Label(
    mi_frame, text="Segundo participante:", font=("Arial Black", 9))
label_jugador_2.config(bg="#FF6800")
label_jugador_2.grid(row=1, column=0, sticky="e", padx=10, pady=10)


def codigo_boton(entry_jugador_1, entry_jugador_2):
    #  Funcionalidad del boton. Obtiene los nombres de los jugadores

    if entry_jugador_1.get() == "":
        jugador_1 = "Jugador 1"
    else:
        jugador_1 = entry_jugador_1.get()

    if entry_jugador_2.get() == "":
        jugador_2 = "Jugador 2"
    else:
        jugador_2 = entry_jugador_2.get()

    raiz.destroy()
    main(jugador_1, jugador_2)


boton_envio = Button(raiz, text="Enviar", font=("Arial Black", 9), command=partial(
    codigo_boton, entry_jugador_1, entry_jugador_2))

boton_envio.config(bg="#FCA468", relief="solid", bd=1.5)

boton_envio.pack()

raiz.mainloop()
