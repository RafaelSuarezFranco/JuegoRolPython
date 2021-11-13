import random
from tkinter import *
import centrarPantalla as cp

personaje = []
#el personaje se guardará como una lista global a la que hay que llamar desde este módulo.


def crearPersonaje():
    ventanapj = Tk()
    ventanapj.title('CREACIÓN PERSONAJE')
    cp.centrarPantalla(350, 500, ventanapj)
    ventanapj.resizable(False, False)
    
    imagenfondo = PhotoImage(file="./pictures/personajes.png")
    labelfondo = Label(ventanapj,image=imagenfondo)
    labelfondo.place(x=0, y=0)

    lbl = Label(ventanapj, text="CREACIÓN DE PERSONAJE")
    lbl.place(x=200, y=0)

    lblnombre = Label(ventanapj, text="Nombre")
    lblnombre.place(x=200, y=60)

    txtnombre = Entry(ventanapj,width=20)
    txtnombre.place(x=200, y=100)
    txtnombre.focus()
    
    habilidad = IntVar()
    rad1 = Radiobutton(ventanapj,text='LUCHA', value=1, variable=habilidad)
    rad2 = Radiobutton(ventanapj,text='MAGIA', value=2, variable=habilidad)
    rad3 = Radiobutton(ventanapj,text='ASTUCIA', value=3, variable=habilidad)

    def crearpj():
        habil = ""
        if habilidad.get() == 1:
            habil = "LUCHA"
        elif habilidad.get() == 2:
            habil = "MAGIA"
        elif habilidad.get() == 3:
            habil = "ASTUCIA"
        else:
            messagebox.showinfo('Error', 'Por favor, elige una habilidad')
        
        nombre = txtnombre.get()
        if nombre == "":
            messagebox.showinfo('Error', 'Por favor, escribe un nombre')
        
        vida = 100
        if nombre != "" and habil != "":
            vidarand = random.randint(0, 100)
            vida = vida + vidarand
            messagebox.showinfo("Atención","Los dioses te han condedido "+str(vida)+" puntos de vida.")
            personaje.extend((nombre, vida, habil))
            
            ventanapj.destroy()
            

    btncrear = Button(ventanapj, text="Crear personaje", command=crearpj)
    rad1.place(x=120, y=140)
    rad2.place(x=200, y=140)
    rad3.place(x=280, y=140)
    btncrear.place(x=400, y=140)
    
    ventanapj.mainloop()
    return personaje
    

def mostrarPersonaje():
    ventanapj = Tk()
    ventanapj.title('ESTADO DEL PERSONAJE')
    cp.centrarPantalla(200, 200, ventanapj)
    ventanapj.resizable(False, False)
    
    lblnombre = Label(ventanapj, text="Nombre: "+personaje[0])
    lblnombre.place(x=40, y=30)
    lblvida = Label(ventanapj, text="Vida: " + str(personaje[1]))
    lblvida.place(x=40, y=50)
    lblhabilidad = Label(ventanapj, text="Habilidad: " + personaje[2])
    lblhabilidad.place(x=40, y=70)
    
    def salir():
        ventanapj.destroy()
        
    botonsalir = Button(ventanapj, text="Salir", command=salir)
    botonsalir.place(x=40, y=100)
    
    ventanapj.mainloop()
    

