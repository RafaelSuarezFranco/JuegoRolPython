import random
import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionPersonaje as gpj
import csv
from tkinter import *
import gestionPantalla as cp
import menuPrincipal as mp
from tkinter.ttk import *
import gestionPartidas as gp

arraysalas = []
arrayambientes = []
luchar = False

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
    
    # aqui calculamos si hay o no un monstruo
    monstruopasado, monstruoactual= gm.invocarMonstruo(monstruopasado, salaactual, dificultad)
    resultadosala.append(monstruopasado)
    
    fotomonstruo = ""
    if monstruopasado == True:#si hay monstruo, creamos su imagen y la escondemos
        imgmonstruo = PhotoImage(file="./pictures/monstruo"+str(monstruoactual[0])+".png")
        fotomonstruo = canvas.create_image(550,320,image=imgmonstruo)
        canvas.itemconfigure(fotomonstruo, state='hidden')
    
    #calculo de objetos
    nuevosObjetos = go.invocarObjeto(dificultad)
    
    """
    A partir de aquí, vamos creando nuevos botones y elementos para ir controlando lo que pasa en la sala. los botones
    usados normalmente se quedarán escondidos una vez los pulsemos (normalmente surgirá otro botón o un panel de botones
    que lo reemplace)
    """
    
    def movermonstruo():#animacion entrada de monstruo
        canvas.move(fotomonstruo, -5, 0)
        ventanasala.update()
        
    def animacionmonstruo():
        for i in range(1, 35):
            canvas.after(10, None)
            movermonstruo()
    
    def siguentemonstruo(): #al pulsar el boton btnsiguiente, se enseña el monstruo y el mensaje
        btnsiguiente.place_forget()
        btnsiguiente2.place(x=425, y=420)
        if monstruopasado == True:
            canvas.itemconfigure(fotomonstruo, state='normal')
            textosala.configure(text="Un "+monstruoactual[1]+" salvaje apareció!"+
                                "¡Ten cuidado! "+monstruoactual[4]+".")
            animacionmonstruo()
        else:
            textosala.configure(text="No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
    
    btnsiguiente = Button(ventanasala, text="Siguiente", command=siguentemonstruo)#boton introduce al monstruo, si lo hay
    btnsiguiente.place(x=425, y=420)
    
    
    def siguienteobjetos(): #lógica similar, si hay objetos, los monstramos en mensajes.
        btnsiguiente2.place_forget()
        btnsiguiente3.place(x=425, y=420)
        if nuevosObjetos != None:#si hay 1 objeto
            cadenaobjeto = "En la sala hay " + go.arrayobjetos[nuevosObjetos[0]][1]+"."
            textosala.configure(text=cadenaobjeto)
            if len(nuevosObjetos) > 1:#si hay 2 objetos
                textosala.configure(text=cadenaobjeto + " Además, hay " + go.arrayobjetos[nuevosObjetos[1]][1]+".")
        else:
            textosala.configure(text="No parece haber ningún objeto en la sala.")
            
    btnsiguiente2 = Button(ventanasala, text="Siguiente", command=siguienteobjetos)#al pulsar este boton salen los objetos.
    """
    una vez hemos determinado el monstruo y los objetos, enseñamos un menu que será el 'panelinferior', el cual tendrá
    las mismas fuciones o equivalentes al menu de la versión de texto (por ejemplo no hay una opcion de monstrar inventario
    porque mostraremos los objetos en un combobox) por tanto al pulsar el boton, se crea dicho panel con los controles
    que llaman a las funciones necesarias, algunas son de otros módulos, otras son creadas dentro de la misma función del
    panel. de nuevo solo saldremos de ese panel de controles una vez elijamos luchar o huir (o salir si no hay monstruo)
    por lo que el resultado de la sala se determinará en la función del panel inferior, la cual se llama 'crearMenu'.
    """
    indiceinventario = ""
    resultadolucha = "empate"
    def mostrarmenu(indiceinventario, resultadolucha):
        btnsiguiente3.place_forget()
        panelinferior, indiceinventario, resultadolucha = crearMenu(ventanasala,canvas, textosala,fotopj, fotomonstruo, inventario, nuevosObjetos,
                                                       monstruoactual, salaactual, monstruopasado, dificultad)
        panelinferior.place(x=5, y= 420)
        btnsiguiente4.place(x=425, y=420)#nuevo botón, será visible cuando quitemos el panel de controles.
        
    btnsiguiente3 = Button(ventanasala, text="Ver Menú", command=lambda: mostrarmenu(indiceinventario, resultadolucha))#al pulsar este boton sale el menú.
    
    """
    la siguiente función controla lo que pasa una vez hemos luchado, huido o salido. analiza si nos queda vida para continuar
    las salidas que hay a continuación, si estamos en un callejón sin salida o en la sala FIN, etc.
    crearemos un botón más que nos permite salir al menú si hemos perdido la partida al finalizar la sala (btnsiguiente5)
    """
    objetobueno = False #si el objeto ha sido eficaz o no
    def lucharhuirsalir():
        if monstruopasado == True and resultadolucha != "empate":
            canvas.itemconfigure(fotomonstruo, state='hidden')
        if gpj.personaje[1] < 1: #bajar a 0 o menos de vida es condición de derrota.
            textosala.configure(text="Tus heridas tras el último encuentro son letales, tu cuerpo no puede aguantar más. Has perdido la partida.")
            btnsiguiente5.place(x=425, y=420)
            resultadosala.append("-1")
        else:
            textosala.configure(text="Procede a elegir una salida.")
            encontrarSalida(salidas, norte, sur, este, oeste)
            if len(salidas) == 0 and salaactual != "FIN":
                textosala.configure(text="""Parece ser que estás en un callejón sin salida. Esperas cruzado de brazos hasta que la sala se derrumba sobre tu cabeza. Fin del juego.""")
                btnsiguiente5.place(x=425, y=420)
                resultadosala.append("-1")
            elif len(salidas) == 0 and salaactual == "FIN":
                #textosala.configure(text="""¡Enhorabuena!¡Has derrotado al jefe final!""")
                btnsiguiente5.place(x=425, y=420)
            btnsiguiente4.place_forget()
    
    def saliralmenu():
        ventanasala.destroy()
        mp.menuPrincipal()
    
    btnsiguiente4 = Button(ventanasala, text="Siguiente", command=lucharhuirsalir)#una vez terminemos con el menú, tendremos
    #este botón para seguir avanzando.
    btnsiguiente5 = Button(ventanasala, text="Salir", command=saliralmenu)#botón para salir al menu si es game over.
    """
    a continuación tenemos un par de funciones para hacer una animación de salida del personaje, además de controlar
    los botones de salida (N S O E) que mostraremos.
    """
    def salirsala(puerta):
        textosala.configure(text="Saliendo de la sala por la puerta "+puerta+"...")
        canvas.after(200, None)
        ventanasala.destroy()
        return resultadosala #retornamos resultado sala para acabar con esta maldita funcion interminable
    
    def pjsaliranimacion(salida, s):
        norte.place_forget()
        sur.place_forget()
        este.place_forget()
        oeste.place_forget()
        resultadosala.append(arraysalas[salaactual][s])
        animacionSalir(ventanasala, canvas, fotopj, salida)
        salirsala(salida)
    
    def irnorte():
        salida = "norte"
        s = 1
        pjsaliranimacion(salida, s)
        
    def irsur():
        salida = "sur"
        s = 2
        pjsaliranimacion(salida, s)
        
    def iroeste():
        salida = "oeste"
        s = 3
        pjsaliranimacion(salida, s)
        
    def ireste():
        salida = "este"
        s = 4
        pjsaliranimacion(salida, s)
    
    #borramos la sala actual de array de salas para que no se pueda volver
    #básicamente si por ejemplo estamos en la sala 1, borramos todos los 1 y los cambiamos por 0.
    for i in range(len(arraysalas)-1):
        for j in range(len(arraysalas[i])-1):
            if arraysalas[i][j] == str(salaactual):
                arraysalas[i][j] = '0'
    #de esta forma, en la siguiente sala no se reconocerá como salida la sala anterior ni ninguna en la que hayamos
    # estado, dado que habrá un 0 en su lugar
    
    norte = Button(ventanasala, text="Norte", command=irnorte)
    sur = Button(ventanasala, text="Sur", command=irsur)
    este = Button(ventanasala, text="Este", command=ireste)
    oeste = Button(ventanasala, text="Oeste", command=iroeste)
    ventanasala.mainloop()
    
 
    return resultadosala

    #en resultadosala tenemos: [monstruopasado, salaactual]

def encontrarSalida(salidas, norte, sur, este, oeste):
    if 'N' in salidas:
        norte.place(x=200, y= 20)
    if 'S' in salidas:
        sur.place(x=200, y= 380)
    if 'E' in salidas:
        este.place(x=400, y= 190)
    if 'O' in salidas:
        oeste.place(x=20, y= 190)
    
    


#se crea un panel con unos botones, sustituye al menu de la otra version. Por tanto debemos pasarle casi los mismos parámetros.
def crearMenu(window, canvas, textosala,fotopj, fotomonstruo, inventario, nuevosObjetos, monstruoactual, salaactual, monstruopasado, dificultad):
    panelinferior = Frame(window, height=100, width=500)
    resultadolucha = "empate"
    def mostrarpj():
        gpj.mostrarPersonaje()
    
    btnpj = Button(panelinferior, text="Mostrar Personaje", command=mostrarpj)
    btnpj.place(x=10,y=0)
    
    lblinventario = Label(panelinferior, text="Tu inventario:")
    lblinventario.place(x=30,y=50)
        
    comboobjeto = go.crearInventario(panelinferior, inventario)
    comboobjeto.place(x=150,y=50)
    
    # para recoger objetos, monstrare tantos botones como objetos hayan en la sala, al pulsar uno, se recoge
    # y se desactivan los botones, a la vez que se actualiza el combo del inventario
    btnobjeto1 = ""
    btnobjeto2 = ""
    o1 = ""
    o2 = ""
   
    def recoger1():
        go.recogerObjeto(o1,comboobjeto, inventario, nuevosObjetos, btnobjeto1, btnobjeto2)
        
    def recoger2():
        go.recogerObjeto(o2,comboobjeto, inventario, nuevosObjetos, btnobjeto1, btnobjeto2)
        
    if nuevosObjetos != None:
        o1 = int(nuevosObjetos[0])
        btnobjeto1 = Button(panelinferior, text="Recoger "+go.arrayobjetos[o1][1], command=recoger1)
        btnobjeto1.place(x=150,y=0)
        if len(nuevosObjetos) > 1:
            o2 = int(nuevosObjetos[1])
            btnobjeto2 = Button(panelinferior, text="Recoger "+go.arrayobjetos[o2][1], command=recoger2)
            btnobjeto2.place(x=150,y=25)
    ################ FIN BOTONES RECOGER OBJETO.
    btnluchar = ""
    btnhuir = ""
    btnsalir = ""
    
    def huir():
        penalizacion = 50 + dificultad * 10
        gpj.personaje[1] = gpj.personaje[1] - penalizacion
        textosala.configure(text="Has salido ileso del combate, sin embargo, tu orgullo ha sido gravemente herido. Pierdes "+str(penalizacion)+" HP.")
        panelinferior.place_forget()
        return panelinferior, indiceinventario, resultadolucha
    
    #la función de luchar (o que llama a la función lucha de gestionMonstruos) es un poco más extensa
    #dado que hay que recoger si hay un objeto seleccionado y pasarselo a lucha(). esta lucha se repetirá
    #si hay empate o no hemos ganado en la sala FIN, lo cual se verá reflejado en las animaciones.
    objetousado = "" #el objeto que se utilizará en la lucha
    indiceinventario = ""
    objetobueno = False
    def luchar2(objetousado,indiceinventario, objetobueno):
        luchar = True
        if comboobjeto.get() != "Ninguno":
            objetousado = " utilizando "+comboobjeto.get()
            indiceinventario = comboobjeto.current()
            
        resultadolucha = "empate"
        while resultadolucha == "empate" or (salaactual == "FIN" and resultadolucha != "ganar"):
            #repetimos la lucha y la animación hasta que no sea empate
            gpj.personaje[1], resultadolucha, objetobueno = gm.lucha(monstruoactual, inventario,indiceinventario, salaactual, dificultad)
            gm.animacionLucha(window, canvas, resultadolucha, fotopj, fotomonstruo, textosala, monstruoactual, objetobueno, indiceinventario)

        if resultadolucha != "empate" or (salaactual == "FIN" and resultadolucha != "ganar"):
            panelinferior.place_forget()
        return panelinferior,  indiceinventario,resultadolucha
    
    def salir(): #simplemente quitamos el panel y procedemos a elegir la salida
        panelinferior.place_forget()
        textosala.configure(text="Recorres la sala sin pena ni gloria.")
        return panelinferior, indiceinventario, resultadolucha
    
    if monstruopasado == True:#si hay monstruo, monstramos boton para luchar y huir
        btnluchar = Button(panelinferior, text="Luchar", command=lambda: luchar2(objetousado,indiceinventario,objetobueno))
        btnluchar.place(x=340,y=0)
    
        btnhuir = Button(panelinferior, text="Huir", command=huir)
        btnhuir.place(x=340,y=50)
    else:#si no, solo un botón de salir.
        btnsalir = Button(panelinferior, text="Salir", command=salir)
        btnsalir.place(x=340,y=0)
    
    return panelinferior, indiceinventario, resultadolucha

 
# es la introducción de la sala, equivalente a la pequeña etapa de la version de texto donde damos la opcion de guardar
# y salir.
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
    btnguardar.place(x=200,y=360)
    
    btnsalir = Button(ventanasala, text="Salir", command=salir)
    btnsalir.place(x=350,y=360)
    
    ventanasala.mainloop()

#una vez acaba la sala, animamos la salida del personaje.
def animacionSalir(window, canvas, fotopj, salida):

    def moverfoto(fotopj,x,y):
        canvas.move(fotopj, x,y)
        window.update()
    
    x = 0
    y = 0
    if salida == "norte":
        y = -10
    elif salida == "sur":
        y = 2
    elif salida == "oeste":
        x = -2
    else:
        x = 10
    
    def animacion():
        for i in range(1, 130):
            canvas.after(10, None)
            moverfoto(fotopj,x,y)
    animacion()