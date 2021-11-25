import random
from tkinter import *
import gestionPantalla as cp

personaje = []
#el personaje e inventario se guardarán como una listas globales a las que hay que llamar desde este módulo.
inventario = []

#descripciones de las habilidades de personaje.
descripcionl = """Especialista de armas:\nTu entrenamiento\naumenta tus\nprobabilidades de\nganar en combate."""
descripcionm = """Experto en pociones:\nTus habilidades\nmágicas te permiten\naumentar su salud\ninicial"""
descripciona = """Maestro de los\ncaminos: Tus vastos\nconocimientos te\nayudan a evitar\nenfrentamientos en\ntu viaje."""

def crearPersonaje():
    ventanapj = Tk()
    ventanapj.title('CREACIÓN PERSONAJE')
    cp.centrarPantalla(350, 540, ventanapj)
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

    fotopj1 = canvas.create_image(120,200,image=pjlucha, state='hidden')
    fotopj2 = canvas.create_image(210,200,image=pjmagia, state='hidden')
    fotopj3 = canvas.create_image(320,200,image=pjastucia, state='hidden')
    #las fotos de pj están escondidas, se enseña la que se seleccione.

    #título, introducción de nombre
    canvas.create_text(265,20,text='CREACIÓN DE PERSONAJE', fill='white', font=('freemono', 16, 'bold'))
    canvas.create_text(160,68,text='Nombre', fill='black', font=('freemono', 11, 'bold'))
    canvas.create_text(162,70,text='Nombre', fill='white', font=('freemono', 11, 'bold'))
    txtnombre = Entry(ventanapj,width=20)
    txtnombre.place(x=220, y=60)
    txtnombre.focus()
    
    descripcion2 = canvas.create_text(447,172,text=descripcionl, fill='black', font=('freemono', 10, 'bold'), state='hidden')
    descripcion1 = canvas.create_text(445,170,text=descripcionl, fill='white', font=('freemono', 10, 'bold'), state='hidden')
    
    def verpersonaje():
        pj = habilidad.get()#mostramos la foto y descripción del pj seleccionado.
        canvas.itemconfigure(fotopj1, state='hidden')
        canvas.itemconfigure(fotopj2, state='hidden')
        canvas.itemconfigure(fotopj3, state='hidden')
        canvas.itemconfigure(descripcion2, state='normal')
        canvas.itemconfigure(descripcion1, state='normal')
        if pj == 1:
            canvas.itemconfigure(fotopj1, state='normal')
            canvas.itemconfigure(descripcion1, text=descripcionl)
            canvas.itemconfigure(descripcion2, text=descripcionl)
        elif pj == 2:
            canvas.itemconfigure(fotopj2, state='normal')
            canvas.itemconfigure(descripcion1, text=descripcionm)
            canvas.itemconfigure(descripcion2, text=descripcionm)
        elif pj == 3:
            canvas.itemconfigure(fotopj3, state='normal')
            canvas.itemconfigure(descripcion1, text=descripciona)
            canvas.itemconfigure(descripcion2, text=descripciona)
    
    habilidad = IntVar()
    Radiobutton(ventanapj,text='LUCHA', value=1, variable=habilidad, command=verpersonaje).place(x=50, y=300)
    Radiobutton(ventanapj,text='MAGIA', value=2, variable=habilidad, command=verpersonaje).place(x=170, y=300)
    Radiobutton(ventanapj,text='ASTUCIA', value=3, variable=habilidad, command=verpersonaje).place(x=290, y=300)

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
            
            bonusmagia = 100 if habil == "MAGIA" else 0 #bonus de la habilidad de magia
            #si el pj tiene la habilidad de MAGIA, aumenta su vida inicial

            vidarand = random.randint(0, 100)
            vida = 100 + vidarand + bonusmagia
            
            messagebox.showinfo("Atención","Los dioses te han condedido "+str(vida)+" puntos de vida.")
            #para hacer referencia a una global dentro del mismo archivo:
            global personaje
            personaje = [nombre, vida, habil]
            ventanapj.destroy()
            

    Button(ventanapj, text="Crear personaje", command=crearpjfinal).place(x=400, y=300)
    
    ventanapj.mainloop()
    

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
    canvas.theimage = imgpj
    
    Label(ventanapj, text="Nombre: "+personaje[0]).place(x=240, y=30)
    Label(ventanapj, text="Vida: " + str(personaje[1])).place(x=240, y=50)
    Label(ventanapj, text="Habilidad: " + personaje[2]).place(x=240, y=70)
        
    Button(ventanapj, text="Salir", command=ventanapj.destroy).place(x=240, y=150)
    
    ventanapj.mainloop()
    

