from tkinter import *
import gestionPantalla as cp
from tkinter.ttk import *
import gestionObjetos as go
def puertaSala():
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala, si hubo o no hubo monstruo, etc.
    nuevosObjetos = []
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    salaactual = "1"
    ventanasala = Tk()
    ventanasala.title('SALA '+salaactual)
    cp.centrarPantalla(400, 480, ventanasala)
    ventanasala.resizable(False, False)
    cp.deshabilitarX(ventanasala)
    frame = Frame(ventanasala)
    frame.pack()
    #panelinferior = Frame(ventanasala, height=100, width=450)
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.pack()
    
    imgpuerta1 = PhotoImage(file="./pictures/puerta.png")
    imgpuerta2 = PhotoImage(file="./pictures/puertaabierta.png")
    
    puertacerrada = canvas.create_image(240,220,image=imgpuerta1)
    puertaabierta = canvas.create_image(240,220,image=imgpuerta2)

    canvas.itemconfigure(puertacerrada, state='normal')
    canvas.itemconfigure(puertaabierta, state='hidden')
    imgpj = PhotoImage(file="./pictures/ASTUCIA.png")
    fotopj = canvas.create_image(80,300,image=imgpj)

    textosala = canvas.create_text(240,20,text='Te encuentras a las puertas de la sala '+salaactual,
                       fill='white', font=('freemono', 10, 'bold'))
    def moverpj():
        canvas.move(fotopj, 2, 0)
        ventanasala.update()
    
    def cerrarventana():
        ventanasala.destroy()
        
    def entrar():
        btnentrar.place_forget()
        btnguardar.place_forget()
        btnsalir.place_forget()
        canvas.itemconfigure(textosala, state='hidden')
        canvas.itemconfigure(puertacerrada, state='hidden')
        canvas.itemconfigure(puertaabierta, state='normal')
        canvas.after(1500, cerrarventana)
        canvas.create_text(240,220,text='Entrando en la sala '+salaactual+'...',
                       fill='white', font=('freemono', 10, 'bold'))
        for i in range(1, 75):
            canvas.after(10, None)
            moverpj()
    def guardar():
        gf.guardarPartida(gpj.personaje, gf.opcion, salaactual, monstruopasado, inventario, dificultad)
        ventanasala.destroy()
        mp.menuPrincipal()
        
    def salir():
        ventanasala.destroy()
        mp.menuPrincipal()
        
    btnentrar = Button(ventanasala, text="Entrar", command=entrar)
    btnentrar.place(x=70,y=360)
    
    btnguardar = Button(ventanasala, text="Guardar y Salir", command=guardar)
    btnguardar.place(x=190,y=360)
    
    btnsalir = Button(ventanasala, text="Salir", command=salir)
    btnsalir.place(x=350,y=360)
    
    canvas.create_text(240,20,text='Te encuentras a las puertas de la sala '+salaactual,
                       fill='white', font=('freemono', 10, 'bold'))
    panelinferior = crearMenu(ventanasala)
    panelinferior.place(x=5, y= 5)
    ventanasala.mainloop()
    
def crearMenu(window):
    panelinferior = Frame(window, height=100, width=450)
    #panelinferior.place(x=5, y= 420)
    
    btnentrar = Button(panelinferior, text="Mostrar Personaje", command=None)
    btnentrar.place(x=10,y=10)
    
    btnguardar = Button(panelinferior, text="Mostrar Inventario", command=None)
    btnguardar.place(x=10,y=50)
    
    combo = crearInventario(panelinferior, ["1", "3", "4", "4", "4", "4"])
    combo.place(x=150,y=50)
    
    btnsalir = Button(panelinferior, text="Recoger Objeto", command=None)
    btnsalir.place(x=150,y=10)
    return panelinferior

def crearInventario(panelinferior, inventario):
    
    combo = Combobox(panelinferior)
    nombres = ['Ninguno']
    for objeto in inventario:
        nombres.append(go.arrayobjetos[int(objeto)][1])
    combo['values']= nombres
    combo.current(0)
    return combo
    #combo.place(x=150,y=50)
    
puertaSala()