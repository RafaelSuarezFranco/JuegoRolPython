import gestionPartidas as gp
import gestionFicheros as gf
from tkinter import *
import gestionPantalla as cp
import sys

def menuPrincipal():
    ventana = Tk()
    ventana.title('JUEGO ROL PYTHON - VERSIÓN TKINTER')
    cp.centrarPantalla(350, 500, ventana)
    cp.deshabilitarX(ventana)
    ventana.resizable(False, False)
    imagenfondo = PhotoImage(file="./pictures/menuppal.png")    
    # crear un canvas para poner la foto de fondo y otras fotos encima.
    frame = Frame(ventana)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(200,180,image=imagenfondo)
    canvas.pack()
    canvas.create_text(238,18,text='MENÚ PRINCIPAL', fill='black', font=('freemono', 20, 'bold'))
    canvas.create_text(240,20,text='MENÚ PRINCIPAL', fill='white', font=('freemono', 20, 'bold'))

    def botonnuevaClick():
        ventana.destroy()
        gp.nuevaPartida(None)
    
    def botoncargarClick():
        ventana.destroy()
        gp.nuevaPartida(gf.elegirPartidaGuardada())

    def salirClick():
        ventana.destroy()
        sys.exit()

    botonnueva = Button(ventana, text="Nueva Partida", command=botonnuevaClick)
    botonnueva.place(x=150, y=300)

    botoncargar = Button(ventana, text="Cargar Partida", command=botoncargarClick)
    botoncargar.place(x=250, y=300)

    botonsalir = Button(ventana, text="Salir", command=salirClick)
    botonsalir.place(x=350, y=300)

    ventana.mainloop()