import random
import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionPersonaje as gpj
import csv
from tkinter import *
import gestionPantalla as cp
import menuPrincipal as mp
arraysalas = []
arrayambientes = []


def randomizarAmbiente(arrayambientes): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice]#devolvemos la cadena y el código de ambiente también para saber qué imagen mostrar

def avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario, dificultad):
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala, si hubo o no hubo monstruo, etc.
    nuevosObjetos = []
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
    puertaSala(salaactual, monstruopasado, inventario, dificultad)
    #en este caso todo el tema de guardar y/o salir al menu se maneja desde la ventana.
    
    try:
        salaactual = int(salaactual)
        #digamos que guardaremos la letra de la salida si en su posición no hay un cero.
        for puerta in range( len(arraysalas[salaactual]) -1 ):
            if arraysalas[salaactual][puerta] != "0" and arraysalas[salaactual][puerta] != arraysalas[salaactual][0]:
                salidas.append(arraysalas[0][puerta])
    except ValueError: # si entramos en esta excepción significa que salaactual toma valor que no es entero, cosa que solo
        #debería ocurrir en la sala FIN
        print("")
    
    #mostrar mensaje de ambiente
    ambiente = randomizarAmbiente(arrayambientes)
    #print(ambiente)
    
    ventanasala = Tk()
    ventanasala.title('SALA '+str(salaactual))
    #alto, ancho
    cp.centrarPantalla(500, 500, ventanasala)
    ventanasala.resizable(False, False)
    cp.deshabilitarX(ventanasala)
    frame = Frame(ventanasala)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.pack()
    imgambiente = PhotoImage(file="./pictures/"+ambiente[0]+".png")
    fotoambiente = canvas.create_image(240,200,image=imgambiente)
    imgpj = PhotoImage(file="./pictures/"+gpj.personaje[2]+".png")
    fotopj = canvas.create_image(80,300,image=imgpj)
    
    panelinferior = Frame(ventanasala, height=100, width=450)
    panelinferior.place(x=5, y= 420)
    textosala = Message(panelinferior, text=ambiente[1], width=400)
    textosala.place(x=5, y=5)
    
    def seguiradelante():
        ventanasala.destroy()
    
    btnsiguiente = Button(ventanasala, text="Siguiente", command=seguiradelante)
    btnsiguiente.place(x=425, y=420)
    
    ventanasala.mainloop()
        
    #calculo de objetos
    nuevosObjetos = go.invocarObjeto(dificultad)
    
    # aqui calculamos si hay o no un monstruo
    monstruopasado, monstruoactual= gm.invocarMonstruo(monstruopasado, salaactual, dificultad)
    resultadosala.append(monstruopasado)
    
    if monstruopasado == True or nuevosObjetos != None: #si hay un monstruo u objetos en la sala
        #entonces mostramos el menú, si no, pasaremos directamente a elegir la salida
        menuMapa(inventario, nuevosObjetos, gpj.personaje, monstruoactual, go.arrayobjetos, salaactual, monstruopasado, dificultad)
    
    
    
    if gpj.personaje[1] < 1: #bajar a 0 o menos de vida es condición de derrota.
        print("Tus heridas tras el último encuentro son letales, tu cuerpo no puede aguantar más. Has perdido la partida.")
        resultadosala.append('-1') # hacemos un return para que la función termine aquí.
        return resultadosala

    # una vez que hayamos hecho lo que sea en la sala, vamos a salir. Si no hay salidas disponibles, se acabó el juego.
    if len(salidas) == 0 and salaactual != "FIN": #siempre que no sea la sala FIN
        print("Parece que has llegado a un callejón sin salida. Te quedas atrapado en la sala hasta que se derruba sobre tu cabeza.")
        print("Fin del juego. Has perdido.")
        resultadosala.append('-1') # hacemos un return para que la función termine aquí.
        return resultadosala
    elif salaactual == "FIN":
        print("Has acabado con el monstruo final, ¡enhorabuena!")
        return resultadosala
    else:
        print("Tus salidas son: "+" ".join(salidas))
        opcion = input("Elige por donde quieres salir ").upper()
        while opcion not in salidas:
            opcion = input("Te chocas con una pared. Elige otra ruta. ").upper()
        
    print("Has abandonado la sala "+arraysalas[salaactual][0]+" por la puerta "+opcion+"...")
    #esta función debería devolver cual es la siguiente sala, la cual está almacenada en la posicion de 1 al 4
    #dependiendo de la opcion que escogemos, del subarray que estamos tratando (el de salaactual)
    if opcion == "N":
        resultadosala.append(arraysalas[salaactual][1])
    elif opcion == "S":
        resultadosala.append(arraysalas[salaactual][2])
    elif opcion == "O":
        resultadosala.append(arraysalas[salaactual][3])
    elif opcion == "E":
        resultadosala.append(arraysalas[salaactual][4])
    else:
        print("Este mensaje no debe aparecer nunca.")

    print("La sala "+arraysalas[salaactual][0]+" se derrumba tras cerrar la puerta.")
    print("")
    #borramos la sala actual de array de salas para que no se pueda volver
    #básicamente si por ejemplo estamos en la sala 1, borramos todos los 1 y los cambiamos por 0.
    for i in range(len(arraysalas)-1):
        for j in range(len(arraysalas[i])-1):
            if arraysalas[i][j] == str(salaactual):
                arraysalas[i][j] = '0'
    #de esta forma, en la siguiente sala no se reconocerá como salida la sala anterior ni ninguna en la que hayamos
    # estado, dado que habrá un 0 en su lugar
 
    return resultadosala

    #en resultadosala tenemos: [monstruopasado, salaactual]


def menuMapa(inventario, nuevosObjetos, personaje, monstruoactual, arrayobjetos, salaactual, monstruopasado, dificultad):
    # si hay monstruo o objeto, damos a elegir las acciones.
    accion = ""
    
    while accion != "4" and accion != "5":
        #este es el menu que se mostrará si hay monstruo y/o objeto, si no hay nada, vamos directamente a la elección
        #del siguiente camino. Algunas acciones no nos sacarán de este menú, como mostrar el estado actual o recoger un
        #objeto. otras acciones son definitivas, si elegimos luchar por ejemplo, ya no hay posibilidad de huir o recoger objeto
        print("\nElige una acción")
        print("1 - Estado del personaje")
        print("2 - Mostrar tu inventario")
        print("3 - Recoger Objeto")
        if monstruopasado == True: #si hay objetos pero no hay monstruo, no queremos enseñar esto
            print("4 - Luchar con el monstruo")
            print("5 - Huir del monstruo")
        else:
            print("4, 5 - Salir de la sala")
                
        accion = input("")

        if accion == "1":
            gpj.mostrarPersonaje()
        elif accion == "2":
            go.consultarInventario(inventario)
        elif accion == "3":
            if nuevosObjetos != None:
                inventario = go.recogerObjeto(nuevosObjetos, inventario)
                nuevosObjetos = None
            else:
                print("No puedes recoger más objetos de esta sala.")
        elif accion == "4": #si decidimos luchar
            if monstruopasado == True:
                gpj.personaje[1] = gm.lucha(gpj.personaje, monstruoactual, inventario, go.arrayobjetos, salaactual, dificultad)
        elif accion == "5": # si dedicimos escapar
            if monstruopasado == True and salaactual != "FIN":
                penalizacion = 50 + dificultad * 10
                gpj.personaje[1] = gpj.personaje[1] - penalizacion
                print("Has salido ileso del combate, sin embargo, tu orgullo ha sido gravemente herido. Pierdes "+str(penalizacion)+" HP.")
                
            elif salaactual == "FIN": #si estamos en la sala FIN, no podemos huir del monstruo
                print("Es el monstruo final, no puedes huir de él.")
                accion = ""
 
 
def puertaSala(salaactual, monstruopasado, inventario, dificultad):
    ventanasala = Tk()
    ventanasala.title('PUERTA DE LA SALA '+salaactual)
    cp.centrarPantalla(400, 480, ventanasala)
    ventanasala.resizable(False, False)
    cp.deshabilitarX(ventanasala)
    frame = Frame(ventanasala)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.pack()
    
    imgpuerta1 = PhotoImage(file="./pictures/puerta.png")
    imgpuerta2 = PhotoImage(file="./pictures/puertaabierta.png")
    imgpj = PhotoImage(file="./pictures/"+gpj.personaje[2]+".png")
    
    puertacerrada = canvas.create_image(240,220,image=imgpuerta1)
    puertaabierta = canvas.create_image(240,220,image=imgpuerta2)
    canvas.itemconfigure(puertaabierta, state='hidden')
    fotopj = canvas.create_image(80,300,image=imgpj)

    textosala = canvas.create_text(240,20,text='Te encuentras a las puertas de la sala '+salaactual,
                       fill='white', font=('freemono', 10, 'bold'))

    def moverpj():#animacion
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
        canvas.create_text(240,180,text='Entrando en la sala '+salaactual+'...',
                       fill='white', font=('freemono', 10, 'bold'))
        for i in range(1, 75):#animacion
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
    
    ventanasala.mainloop()
