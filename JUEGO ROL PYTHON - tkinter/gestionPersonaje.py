import random
from tkinter import *
import gestionPantalla as cp

personaje = []
#el personaje e inventario se guardarán como una listas globales a las que hay que llamar desde este módulo.
inventario = []

def crearPersonaje():
    ventanapj = Tk()
    ventanapj.title('CREACIÓN PERSONAJE')
    cp.centrarPantalla(350, 500, ventanapj)
    ventanapj.resizable(False, False)
    cp.deshabilitarX(ventanapj)
    imagenfondo = PhotoImage(file="./pictures/personajes.png")
    # crear un canvas para poner la foto de fondo y otras fotos encima.
    frame = Frame(ventanapj)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(350,200,image=imagenfondo)
    canvas.pack()
    
    pjlucha = PhotoImage(file="./pictures/LUCHA.png")
    pjmagia = PhotoImage(file="./pictures/MAGIA.png")
    pjastucia = PhotoImage(file="./pictures/ASTUCIA.png")

    fotopj1 = canvas.create_image(120,200,image=pjlucha)
    fotopj2 = canvas.create_image(210,200,image=pjmagia)
    fotopj3 = canvas.create_image(320,200,image=pjastucia)
    #las fotos de pj están escondidas, se enseña la que se seleccione.
    canvas.itemconfigure(fotopj1, state='hidden')
    canvas.itemconfigure(fotopj2, state='hidden')
    canvas.itemconfigure(fotopj3, state='hidden')
    #título, introducción de nombre
    canvas.create_text(240,20,text='CREACIÓN DE PERSONAJE', fill='white', font=('freemono', 16, 'bold'))
    canvas.create_text(140,68,text='Nombre', fill='black', font=('freemono', 11, 'bold'))
    canvas.create_text(140,70,text='Nombre', fill='white', font=('freemono', 11, 'bold'))
    txtnombre = Entry(ventanapj,width=20)
    txtnombre.place(x=200, y=60)
    txtnombre.focus()
    
    def verpersonaje():
        pj = habilidad.get()#mostramos la foto del pj seleccionado.
        canvas.itemconfigure(fotopj1, state='hidden')
        canvas.itemconfigure(fotopj2, state='hidden')
        canvas.itemconfigure(fotopj3, state='hidden')
        if pj == 1:
            canvas.itemconfigure(fotopj1, state='normal')
        elif pj == 2:
            canvas.itemconfigure(fotopj2, state='normal')
        elif pj == 3:
            canvas.itemconfigure(fotopj3, state='normal')
    
    habilidad = IntVar()
    rad1 = Radiobutton(ventanapj,text='LUCHA', value=1, variable=habilidad, command=verpersonaje)
    rad2 = Radiobutton(ventanapj,text='MAGIA', value=2, variable=habilidad, command=verpersonaje)
    rad3 = Radiobutton(ventanapj,text='ASTUCIA', value=3, variable=habilidad, command=verpersonaje)

    
    def crearpjfinal():
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

        if nombre != "" and habil != "":
            vidarand = random.randint(0, 100)
            vida = 100 + vidarand
            messagebox.showinfo("Atención","Los dioses te han condedido "+str(vida)+" puntos de vida.")
            #para hacer referencia a una global dentro del mismo archivo:
            global personaje
            personaje = [nombre, vida, habil]
            ventanapj.destroy()
            

    btncrear = Button(ventanapj, text="Crear personaje", command=crearpjfinal)
    rad1.place(x=50, y=300)
    rad2.place(x=170, y=300)
    rad3.place(x=290, y=300)
    btncrear.place(x=400, y=300)
    
    ventanapj.mainloop()
    #return personaje
    

def mostrarPersonaje():
    ventanapj = Tk()
    ventanapj.title('ESTADO DEL PERSONAJE')
    cp.centrarPantalla(220, 400, ventanapj)
    ventanapj.resizable(False, False)

    frame = Frame(ventanapj)
    frame.pack()
    canvas = Canvas(frame, width=700, height=400)
    canvas.pack()
    imgpj = PhotoImage(master = canvas, file="./pictures/"+personaje[2]+".png")
    fotopj1 = canvas.create_image(120,100,image=imgpj)
    #PARA PODER ABRIR UNA NUEVA VENTANA CON IMAGEN SIN DESTRUIR LA ANTERIOR
    #DEBE UTILIZARSE UNA LINEA COMO LA SIGUIENTE PARA GUARDAR UNA REFERENCIA. SI NO, NO FUNCIONA
    canvas.theimage = imgpj
    
    
    lblnombre = Label(ventanapj, text="Nombre: "+personaje[0])
    lblnombre.place(x=240, y=30)
    lblvida = Label(ventanapj, text="Vida: " + str(personaje[1]))
    lblvida.place(x=240, y=50)
    lblhabilidad = Label(ventanapj, text="Habilidad: " + personaje[2])
    lblhabilidad.place(x=240, y=70)
        
    botonsalir = Button(ventanapj, text="Salir", command=ventanapj.destroy)
    botonsalir.place(x=240, y=150)
    
    ventanapj.mainloop()
    

