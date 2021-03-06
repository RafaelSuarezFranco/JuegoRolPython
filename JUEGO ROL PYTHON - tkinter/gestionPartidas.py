import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionSalas as gs
import gestionPersonaje as gpj
from tkinter import *
import gestionPantalla as cp

def nuevaPartida(partida): #le pasamos la partida cargada (si es nueva partida, le pasamos None)

    #vaciamos el inventario, si jugamos varias partidas en al misma sesión, es necesario.
    gpj.inventario = []
    
    if partida == None:################################################# SI LA PARTIDA ES COMPLETAMENTE NUEVA
        gf.elegirArchivos() #controla si usamos archivos default o custom
        #inicializamos variables que controlarán el estado actual del juego
        gs.arraysalas = gf.generarArray("mapa")
        gpj.crearPersonaje()#En este caso, se crean ventanas para crear el pj y elegir la dificultad.
        dificultad = elegirDificultad()
        salaactual = "1"
        resultadosala = []
        monstruopasado = False #guardamos si hubo un monstruo en la sala anterior
        
        ######################### esto es una ventana introductoria con una narración.
        sala1 = Tk()
        sala1.title('Empieza el juego')
        cp.centrarPantalla(360, 450, sala1)
        sala1.resizable(False, False)
        cp.deshabilitarX(sala1)
        
        frame = Frame(sala1)
        frame.pack()
        canvas = Canvas(frame, bg="black", width=700, height=400)
        canvas.pack()
        imgfondo = PhotoImage(file="./pictures/castillo.png")
        canvas.create_image(230,180,image=imgfondo)
        
        narracion = canvas.create_text(200,320,text='Da comienzo la aventura, te encuentras \na las puertas de la mazmorra.',
                                        fill='white', font=('freemono', 10, 'bold'))
        
        def avanzarnarracion():
            if btnsiguiente.counter == 0:
                btnsiguiente.counter = 1
                canvas.itemconfigure(narracion, text="La mazmorra a la que vas a entrar es inestable \ny colapsa a medida que la recorres.")
            elif btnsiguiente.counter == 1:
                btnsiguiente.counter = 2
                canvas.itemconfigure(narracion, text="Cada sala por la que pases se derrumbará y no \npodrás volver sobre tus pasos. Elige bien a dónde vas.")
            elif btnsiguiente.counter == 2:
                btnsiguiente.counter = 3
                canvas.itemconfigure(narracion, text="En cada sala puede haber un monstruo aleatorio\nDebes elegir luchar o huir antes de poder avanzar.")
            elif btnsiguiente.counter == 3:
                btnsiguiente.counter = 4
                canvas.itemconfigure(narracion, text="También puede haber hasta 2 objetos en cada sala.\nPuedes optar por recoger uno de ellos.")
            elif btnsiguiente.counter == 4:
                btnsiguiente.counter = 5
                canvas.itemconfigure(narracion, text="Puedes usar un objeto en cada lucha, si ganas,\nte recompensará o perjudicará. Si pierdes, nada.")
                btnsiguiente.configure(text="Empezar")
            else: 
                sala1.destroy()
        
        btnsiguiente = Button(sala1, text="Siguiente", command=avanzarnarracion)
        btnsiguiente.counter = 0
        btnsiguiente.place(x=380, y=300)
        
        sala1.mainloop()

    else: ####################SI LA PARTIDA ES CARGADA, INICILIZAMOS LAS VARIABLES CON LA PARTIDA QUE HEMOS PASADO
        
        gf.opcion = partida[3] # default o custom guardado en partida[3]
        #realmente nos da igual la opción, dado que el mapa se rescata del fichero de mapas guardados.
        #si tuvieramos archivos de monstruos, objetos o ambientes distintos, sí servería.
        gpj.personaje = [partida[0], int(partida[1]), partida[2]]
        
        dificultad = 0
        if partida[4] == "facil":
            dificultad = -1
        elif partida[4] == "dificil":
            dificultad = 1
            
        gpj.inventario = eval(partida[7])#casteamos el inventario guardado a array
          
        salaactual = partida[5]
        resultadosala = []
        monstruopasado = True
        if partida[6] == "False":#el monstruo pasado está guardado como string.
            monstruopasado = False
            
    ######################################################################### UNA VEZ SE HA CREADO O CARGADO PARTIDA
    #cargamos en memoria los elementos del juego.
    #gs.arraysalas = gf.generarMapa()
    gs.arrayambientes = gf.generarArray("ambientes")
    go.arrayobjetos = gf.generarArray("objetos")
    gm.arraymonstruos = gf.generarArray("monstruos")

    #avanzamos por las salas mientras que no llegemos a la sala FIN o la sala actual valga -1, que significa que estamos
    #en un callejón sin salida. guardar y/o salir o morir tambien son condiciones para salir del bucle.
    while salaactual != "FIN" and salaactual != "-1" and salaactual !="guardar y salir" and gpj.personaje[1] > 0:
        resultadosala = gs.avanzarMapa(salaactual, monstruopasado, dificultad)
        salaactual = resultadosala[1]
        monstruopasado = resultadosala[0]
           
    if salaactual == "FIN":
        resultadosala = gs.avanzarMapa(salaactual, monstruopasado, dificultad)


        

#dificultad afecta a la probabilidad de encontrar objetos, de generar un monstruo, a los dados del monstruo y a la
#penalización por huir de un monstruo.
def elegirDificultad():
    ventanadif = Tk()
    ventanadif.title('DIFICULTAD')
    cp.centrarPantalla(200, 300, ventanadif)
    ventanadif.resizable(False, False)
    cp.deshabilitarX(ventanadif)
    
    frame = Frame(ventanadif)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.pack()
    
    imgnormal = PhotoImage(file="./pictures/normal.png")
    imgfacil = PhotoImage(file="./pictures/facil.png")
    imgdificil = PhotoImage(file="./pictures/dificil.png")
    
    fotofacil = canvas.create_image(130,120,image=imgfacil)
    fotonormal = canvas.create_image(130,120,image=imgnormal)
    fotodificil = canvas.create_image(130,120,image=imgdificil)
    
    canvas.itemconfigure(fotofacil, state='hidden')
    canvas.itemconfigure(fotonormal, state='normal')
    canvas.itemconfigure(fotodificil, state='hidden')
    
    canvas.create_text(148,18,text='Elige una dificultad', fill='black', font=('freemono', 14, 'bold'))#sombra
    canvas.create_text(150,20,text='Elige una dificultad', fill='white', font=('freemono', 14, 'bold'))
    
    descripcion2 = canvas.create_text(121,111,text='Dificultad base del juego.', fill='black', font=('freemono', 10, 'bold'))#sombra
    descripcion = canvas.create_text(120,110,text='Dificultad base del juego.', fill='white', font=('freemono', 10, 'bold'))

    def describirdif():
        dif = dificultad.get()
        canvas.itemconfigure(fotofacil, state='hidden')#similar a la elección de pj.
        canvas.itemconfigure(fotonormal, state='hidden')
        canvas.itemconfigure(fotodificil, state='hidden')
        if dif == -1:
            canvas.itemconfigure(fotofacil, state='normal')
            canvas.itemconfigure(descripcion, text="Menos monstruos. Más objetos.\nMonstruos más débiles. \nPenalización de huida menor.")
            canvas.itemconfigure(descripcion2, text="Menos monstruos. Más objetos.\nMonstruos más débiles. \nPenalización de huida menor.")
        elif dif == 1:
            canvas.itemconfigure(fotodificil, state='normal')
            canvas.itemconfigure(descripcion, text="Más monstruos. Menos objetos.\nMonstruos más fuertes. \nPenalización de huida mayor.")
            canvas.itemconfigure(descripcion2, text="Más monstruos. Menos objetos.\nMonstruos más fuertes. \nPenalización de huida mayor.")
        elif dif == 0:
            canvas.itemconfigure(fotonormal, state='normal')
            canvas.itemconfigure(descripcion, text='Dificultad base del juego.')
            canvas.itemconfigure(descripcion2, text='Dificultad base del juego.')

    
    dificultad = IntVar()
    Radiobutton(ventanadif,text='Fácil', value=-1, variable=dificultad, command=describirdif).place(x=10, y=50)
    Radiobutton(ventanadif,text='Normal', value=0, variable=dificultad, command=describirdif).place(x=120, y=50)
    Radiobutton(ventanadif,text='Difícil', value=1, variable=dificultad, command=describirdif).place(x=240, y=50)

    def elegirdif():
        dif = dificultad.get()
        if dif == 1 or dif == 0 or dif == -1:
            ventanadif.destroy()
            
    Button(ventanadif, text="Aceptar", command=elegirdif).place(x=120, y=160)
    
    ventanadif.mainloop()
    return dificultad.get()