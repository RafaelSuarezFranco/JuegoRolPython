import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionSalas as gs
import gestionPersonaje as gpj
from tkinter import *
import centrarPantalla as cp

#personaje = []
inventario = []

def nuevaPartida(partida): #le pasamos la partida cargada (si es nueva partida, le pasamos None)
    if partida == None:# SI LA PARTIDA ES COMPLETAMENTE NUEVA
        gf.opcion = "default"
        #gf.opcion = gf.elegirArchivos() #controla si usamos archivos default o custom
        #inicializamos variables que controlarán el estado actual del juego
        gpj.personaje = gpj.crearPersonaje()
        dificultad = elegirDificultad()
        inventario = []
        salaactual = "1"
        resultadosala = []
        monstruopasado = False #guardamos si hubo un monstruo en la sala anterior
        print("Da comienzo la aventura, te encuentras en la sala 1.")
        print("La mazmorra en la que te encuentras es inestable y colapsa a medida que la recorres.")
        print("Cada sala por la que pases se derrumbará y no podrás volver sobre tus pasos. Elige bien a dónde vas.")
        input("Pulsa intro para empezar...")
        
    else: #SI LA PARTIDA ES CARGADA, INICILIZAMOS LAS VARIABLES CON LA PARTIDA QUE HEMOS PASADO
        gf.opcion = partida[3] # default o custom guardado en partida[3]
        gpj.personaje = [partida[0], int(partida[1]), partida[2]]
        
        dificultad = 0
        if partida[4] == "facil":
            dificultad = -1
        elif partida[4] == "dificil":
            dificultad = 1
            
        inventario = []
        for i in range(1, int(partida[7])):
            inventario.append(int(partida[7+i]))#añadiendo los objetos guardados al inventario

        salaactual = partida[5]
        resultadosala = []
        monstruopasado = True
        if partida[6] == "False":#el monstruo pasado está guardado como string.
            monstruopasado = False
        input("Partida cargada con éxito. Pulsa intro para continuar...")
    
    #cargamos en memoria los elementos del juego.
    arraysalas = gf.generarMapa(gf.opcion)
    arrayambientes = gf.generarAmbientes(gf.opcion)
    go.arrayobjetos = gf.generarObjetos(gf.opcion)
    gm.arraymonstruos = gf.generarMonstruos(gf.opcion)

    """
    Acerca del array de salas: como el tema sobre no volver a una sala anterior queda un poco a criterio del diseñador, lo
    que he dedidido es que cada sala por la que pasemos se vaya borrando de dicho array, como si el mapa se fuera destruyendo
    a medida que avanzamos. Esto implica que si nos encontramos en un callejón sin salida, el juego se da por perdido.
    """
    
    
    #avanzamos por las salas mientras que no llegemos a la sala FIN o la sala actual valga -1, que significa que estamos
    #en un callejón sin salida.
    while salaactual != "FIN" and salaactual != "-1" and salaactual !="guardar y salir" and gpj.personaje[1] > 0:
        resultadosala = gs.avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario, dificultad)
        salaactual = resultadosala[1]
        monstruopasado = resultadosala[0]
        if salaactual != "-1" and salaactual != "guardar y salir":
            print("Te encuentras en la sala "+salaactual)
        #si hemos seleccionado guardar partida y salir, salaactual recoge el valor 'guardar y salir'
        #nos indica que debemos salir del juego (romper este bucle)
           
    if salaactual == "FIN":
        print("Has llegado a la sala final")
        resultadosala = gs.avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario, dificultad)

#nuevaPartida()
        

#dificultad afecta a la probabilidad de encontrar objetos, de generar un monstruo, a los dados del monstruo y a la
#penalización por huir de un monstruo.
def elegirDificultad():
    ventanadif = Tk()
    ventanadif.title('DIFICULTAD')
    cp.centrarPantalla(200, 300, ventanadif)
    ventanadif.resizable(False, False)

    imgnormal = PhotoImage(file="./pictures/normal.png")
    imgfacil = PhotoImage(file="./pictures/facil.png")
    imgdificil = PhotoImage(file="./pictures/dificil.png")
    labelimg = Label(ventanadif,image=imgnormal)
    labelimg.place(x=0, y=0)
    
    lbl = Label(ventanadif, text="Elige una dificultad")
    lbl.place(x=100, y=0)
    
    lbldescripcion = Label(ventanadif, text="Dificultad base del juego.")
    lbldescripcion.place(x=10, y=100)
    
    def describirdif():
        dif = dificultad.get()
        if dif == -1:
            lbldescripcion.configure(text="""Menos monstruos. Más objetos.\nMonstruos más débiles. Penalización de huida menor.""")
            labelimg.configure(image=imgfacil)
        elif dif == 1:
            lbldescripcion.configure(text="""Más monstruos. Menos objetos.\nMonstruos más fuertes. Penalización de huida mayor.""")
            labelimg.configure(image=imgdificil)
        elif dif == 0:
            lbldescripcion.configure(text="Dificultad base del juego.")
            labelimg.configure(image=imgnormal)
    
    dificultad = IntVar()
    rad1 = Radiobutton(ventanadif,text='Fácil', value=-1, variable=dificultad, command=describirdif)
    rad2 = Radiobutton(ventanadif,text='Normal', value=0, variable=dificultad, command=describirdif)
    rad3 = Radiobutton(ventanadif,text='Difícil', value=1, variable=dificultad, command=describirdif)

    def elegirdif():
        dif = dificultad.get()
        if dif == 1 or dif == 0 or dif == -1:
            ventanadif.destroy()
            
    btnelegir = Button(ventanadif, text="Aceptar", command=elegirdif)
    rad1.place(x=10, y=50)
    rad2.place(x=120, y=50)
    rad3.place(x=240, y=50)
    btnelegir.place(x=120, y=160)
    
    ventanadif.mainloop()
    return dificultad.get()  