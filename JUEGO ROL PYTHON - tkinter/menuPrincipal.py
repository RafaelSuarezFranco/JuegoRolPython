import gestionPartidas as gp
import gestionFicheros as gf
from tkinter import *
import centrarPantalla as cp

ventana = Tk()
ventana.title('JUEGO ROL PYTHON - VERSIÓN TKINTER')
cp.centrarPantalla(350, 500, ventana)
ventana.resizable(False, False)


imagenfondo = PhotoImage(file="./pictures/menuppal.png")
labelfondo = Label(ventana,image=imagenfondo)
labelfondo.place(x=0, y=0)

lbl = Label(ventana, text="MENÚ PRINCIPAL")
lbl.place(x=200, y=0)

def botonnuevaClick():
    ventana.destroy()
    gp.nuevaPartida(None)
    
def botoncargarClick():
    ventana.destroy()
    gp.nuevaPartida(gf.elegirPartidaGuardada())

def salirClick():
    ventana.destroy()

botonnueva = Button(ventana, text="Nueva Partida", command=botonnuevaClick)
botonnueva.place(x=200, y=100)

botoncargar = Button(ventana, text="Cargar Partida", command=botoncargarClick)
botoncargar.place(x=200, y=200)

botonsalir = Button(ventana, text="Salir", command=salirClick)
botonsalir.place(x=200, y=300)

ventana.mainloop()