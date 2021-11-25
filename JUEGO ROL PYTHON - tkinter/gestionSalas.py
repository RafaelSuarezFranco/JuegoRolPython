import random
import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionPersonaje as gpj
from tkinter import *
import gestionPantalla as cp
import menuPrincipal as mp
from tkinter.ttk import *
import gestionPartidas as gp

arraysalas = []
arrayambientes = []

def randomizarAmbiente(): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice]#devolvemos la cadena y el código de ambiente también para saber qué imagen mostrar



"""
el codigo de esta función es extraído de la siguiente, la cual es bastante larga.
lo que hacemos aquí es convertir salaactual en entero para poder usarlo como índice y buscar dicha sala en el array
de salas, y así guardar las salidas en el array 'salidas'. Ya de paso, actualizamos el arraysalas y eliminamos las
salas y salidas a las que no tendremos acceso conforme avancemos en el juego.
"""
def actualizarMapa(salaactual, salidas):
    try:
        salaactual = int(salaactual)
        for puerta in range(1, len(arraysalas[salaactual]) ):
            if arraysalas[salaactual][puerta] != "0":
                salidas.append(arraysalas[0][puerta])
                #esta condicion significa que si en la fila de la sala que corresponde a sala actual hay algo que
                #no sea un 0, guardamos en el array de salidas la letra que corresponde, que se encuentra en
                #la primera fila de arraysalas
                
    except ValueError: # si entramos en esta excepción significa que salaactual toma valor que no es entero, cosa que solo
        #debería ocurrir en la sala FIN. En cualquier caso significa que no debemos preocuparnos de las salidas.
        pass
        
    #borramos la sala actual de array de salas para que no se pueda volver
    #básicamente si por ejemplo estamos en la sala 1, borramos todos los 1 y los cambiamos por 0.
    for i in range(len(arraysalas)-1):
        for j in range(len(arraysalas[i])):
            if arraysalas[i][j] == str(salaactual):
                arraysalas[i][j] = '0'
    #de esta forma, en la siguiente sala no se reconocerá como salida la sala anterior ni ninguna en la que hayamos
    # estado, dado que habrá un 0 en su lugar
    return salaactual, salidas

def avanzarMapa(salaactual, monstruopasado, dificultad):
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala y si hubo o no hubo monstruo
    nuevosObjetos = []
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
    salaactual, salidas = actualizarMapa(salaactual, salidas)
    
    #en este caso todo el tema de guardar y/o salir al menu se maneja desde esta ventana.
    puertaSala(salaactual, monstruopasado, dificultad)
    
    #cogemos un ambiente aleatorio. en esta versión guardamos su código también para asociarlo a una imagen.
    ambiente = randomizarAmbiente()
    
    ventanasala = Tk()
    ventanasala.title('SALA '+str(salaactual))
    cp.centrarPantalla(500, 500, ventanasala)
    ventanasala.resizable(False, False)
    cp.deshabilitarX(ventanasala)
    frame = Frame(ventanasala)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.pack()
    imgambiente = PhotoImage(file="./pictures/ambiente"+ambiente[0]+".png")
    fotoambiente = canvas.create_image(240,200,image=imgambiente)
    imgpj = PhotoImage(file="./pictures/"+str(gpj.personaje[2])+".png")
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
        
    def animacionmonstruo():#animacion entrada de monstruo
        for i in range(1, 35):
            canvas.after(10, None)
            canvas.move(fotomonstruo, -5, 0)
            ventanasala.update()
    
    def siguentemonstruo(): #al pulsar el boton btnsiguiente, se enseña el monstruo y el mensaje
        btnsiguiente.place_forget()
        btnsiguiente2.place(x=415, y=420)
        if monstruopasado == True:
            canvas.itemconfigure(fotomonstruo, state='normal')
            textosala.configure(text="Un "+monstruoactual[1]+" salvaje apareció!"+
                                " ¡Ten cuidado! "+monstruoactual[4]+".")
            animacionmonstruo()
        else:
            textosala.configure(text="No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
    
    btnsiguiente = Button(ventanasala, text="Siguiente", command=siguentemonstruo)#boton introduce al monstruo, si lo hay
    btnsiguiente.place(x=415, y=420)
    
    
    def siguienteobjetos(): #lógica similar, si hay objetos, los monstramos en mensajes.
        btnsiguiente2.place_forget()
        btnsiguiente3.place(x=415, y=420)
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
    indiceinventario = ""#controla el indice del inventario segun el objeto que hemos seleccionado en el menu.
    def mostrarmenu():
        btnsiguiente3.place_forget()
        elementosVentana = [ventanasala, canvas, textosala, fotopj, fotomonstruo]
        #para hacer animaciones y cambiar texto, etc, debo pasar estos elementos de un sitio a otro.
        panelinferior, indiceinventario = crearMenu(elementosVentana, nuevosObjetos, monstruoactual,
                                                                    salaactual, monstruopasado, dificultad)
        panelinferior.place(x=5, y= 420)
        btnsiguiente4.place(x=415, y=420)#nuevo botón, será visible cuando quitemos el panel de controles.
    
    btnsiguiente3 = Button(ventanasala, text="Ver Menú", command=mostrarmenu)    
    #al pulsar este boton sale el menú con los controles..
    
    """
    la siguiente función controla lo que pasa una vez hemos luchado, huido o salido. analiza si nos queda vida para continuar
    las salidas que hay a continuación, si estamos en un callejón sin salida o en la sala FIN, etc.
    crearemos un botón más que nos permite salir al menú si hemos perdido la partida al finalizar la sala (btnsiguiente5)
    """
    
    def lucharhuirsalir():
        if gpj.personaje[1] < 1: #bajar a 0 o menos de vida es condición de derrota.
            textosala.configure(text="Tus heridas tras el último encuentro son letales, tu cuerpo no puede aguantar más. Has perdido la partida.")
            btnsiguiente5.place(x=415, y=420)
            resultadosala.append("-1")
        elif salaactual == "FIN":#si estamos aqui significa que hemos salido vivos de la lucha final y hemos ganado el juego
            textosala.configure(text="""¡Enhorabuena! ¡Has derrotado al jefe final!""")
            btnsiguiente4.place_forget()
            btnsiguiente5.place(x=415, y=420)
        else: #si no hemos muerto, mostramos los botones con salidas
            textosala.configure(text="Procede a elegir una salida.")
            encontrarSalida(salidas, norte, sur, este, oeste)
            if len(salidas) == 0 and salaactual != "FIN":#si no hay salida posible
                textosala.configure(text="""Parece ser que estás en un callejón sin salida. Esperas cruzado de brazos hasta que la sala se derrumba sobre tu cabeza. Fin del juego.""")
                btnsiguiente5.place(x=415, y=420)
                resultadosala.append("-1")
            
            btnsiguiente4.place_forget()
    
    def saliralmenu():
        ventanasala.destroy()
        mp.menuPrincipal()
    
    btnsiguiente4 = Button(ventanasala, text="Siguiente", command=lucharhuirsalir)#una vez terminemos con el menú, tendremos
    #este botón para seguir avanzando.
    btnsiguiente5 = Button(ventanasala, text="Salir al menú", command=saliralmenu)#botón para salir al menu si es game over.
    """
    a continuación tenemos un par de funciones para hacer una animación de salida del personaje, además de controlar
    los botones de salida (N S O E) que mostraremos.
    """
    
    def pjsaliranimacion(salida, s):
        norte.place_forget()
        sur.place_forget()
        este.place_forget()
        oeste.place_forget()
        resultadosala.append(arraysalas[salaactual][s])#guardamos en el resultado la salaactual nueva.
        textosala.configure(text="Saliendo de la sala por la puerta "+salida+"...")
        animacionSalir(ventanasala, canvas, fotopj, salida)
        canvas.after(200, None)
        ventanasala.destroy()
        return resultadosala #retornamos resultado sala para acabar con esta funcion interminable


    
    norte = Button(ventanasala, text="Norte", command=lambda: pjsaliranimacion("norte", 1))
    sur = Button(ventanasala, text="Sur", command=lambda: pjsaliranimacion("sur", 2))
    oeste = Button(ventanasala, text="Oeste", command=lambda: pjsaliranimacion("oeste", 3))
    este = Button(ventanasala, text="Este", command=lambda: pjsaliranimacion("este", 4))
    ventanasala.mainloop()
    
 
    return resultadosala

    #en resultadosala tenemos: [monstruopasado, salaactual]

def encontrarSalida(salidas, norte, sur, este, oeste):
    if 'N' in salidas: #muestra los botones de las salidas disponibles.
        norte.place(x=200, y= 20)
    if 'S' in salidas:
        sur.place(x=200, y= 380)
    if 'E' in salidas:
        este.place(x=400, y= 190)
    if 'O' in salidas:
        oeste.place(x=20, y= 190)
    
    

"""
Se crea un panel con unos botones, sustituye al menu de la otra versión. Por tanto debemos pasarle casi los mismos
parámetros. Además hay que pasarle la ventana, el canvas, las fotos, etc. porque queremos manipular todo eso
desde este menú.
"""
def crearMenu(elementosVentana, nuevosObjetos, monstruoactual, salaactual, monstruopasado, dificultad):
    window, canvas, textosala, fotopj, fotomonstruo = elementosVentana #desempaquetamos los elementos.
    
    panelinferior = Frame(window, height=100, width=500)

    btnpj = Button(panelinferior, text="Mostrar Personaje", command=gpj.mostrarPersonaje)
    btnpj.place(x=10,y=0)
    
    lblinventario = Label(panelinferior, text="Tu inventario:")
    lblinventario.place(x=30,y=50)
        
    comboobjeto = go.crearInventario(panelinferior)
    comboobjeto.place(x=150,y=50)
    
    # para recoger objetos, monstrare tantos botones como objetos hayan en la sala, al pulsar uno, se recoge
    # y se desactivan los botones, a la vez que se actualiza el combo del inventario
    btnobjeto1 = ""
    btnobjeto2 = ""
    o1 = ""
    o2 = ""
   
    if nuevosObjetos != None:#si hay objetos, mostraremos botones para elegir uno de ellos.
        o1 = int(nuevosObjetos[0])
        btnobjeto1 = Button(panelinferior, text="Recoger "+go.arrayobjetos[o1][1],
                            command=lambda: go.recogerObjeto(o1,comboobjeto, nuevosObjetos, btnobjeto1, btnobjeto2))
        btnobjeto1.place(x=150,y=0)
        if len(nuevosObjetos) > 1:
            o2 = int(nuevosObjetos[1])
            btnobjeto2 = Button(panelinferior, text="Recoger "+go.arrayobjetos[o2][1],
                            command=lambda: go.recogerObjeto(o2,comboobjeto, nuevosObjetos, btnobjeto1, btnobjeto2))
            btnobjeto2.place(x=150,y=25)
    ################
            
    btnluchar = ""
    btnhuir = ""
    btnsalir = ""
    
    def huir():
        penalizacion = 50 + dificultad * 10
        gpj.personaje[1] = gpj.personaje[1] - penalizacion
        textosala.configure(text="Has salido ileso del combate, sin embargo, tu orgullo ha sido gravemente herido. Pierdes "+str(penalizacion)+" HP.")
        panelinferior.place_forget()
        return panelinferior, indiceinventario
    
    #la función de luchar2 (o que llama a la función lucha de gestionMonstruos) es un poco más extensa
    #dado que hay que recoger si hay un objeto seleccionado y pasarselo a lucha(). esta lucha se repetirá
    #si hay empate o no hemos ganado en la sala FIN, lo cual se verá reflejado en las animaciones.
    objetousado = "" #el objeto que se utilizará en la lucha
    indiceinventario = ""
    
    def luchar2(objetousado,indiceinventario):
        panelinferior.place_forget()
        
        if comboobjeto.get() != "Ninguno":
            objetousado = " utilizando "+comboobjeto.get()
            indiceinventario = comboobjeto.current()
        #este texto no llega a mostrarse :/   
        textosala.configure(text="Te enfrentas al " + monstruoactual[1] + objetousado + ".")
        
        gm.lucha(elementosVentana, monstruoactual, indiceinventario, salaactual, dificultad)

        return panelinferior, indiceinventario
    
    def salir(): #simplemente quitamos el panel y procedemos a elegir la salida
        panelinferior.place_forget()
        textosala.configure(text="Recorres la sala sin pena ni gloria.")
        return panelinferior, indiceinventario
    
    if monstruopasado == True:#si hay monstruo, monstramos boton para luchar y huir
        btnluchar = Button(panelinferior, text="Luchar", command=lambda: luchar2(objetousado,indiceinventario))
        btnluchar.place(x=340,y=0)
        
        btnhuir = Button(panelinferior, text="Huir", command=huir)
        if salaactual != "FIN":#solo enseñamos el botón huir si no es el monstruo final.
            btnhuir.place(x=340,y=50)
    else:#si no, solo un botón de salir.
        btnsalir = Button(panelinferior, text="Salir", command=salir)
        btnsalir.place(x=340,y=0)
    
    return panelinferior, indiceinventario

 
# es la introducción de la sala, equivalente a la pequeña etapa de la version de texto donde damos la opcion de guardar
# y salir.
def puertaSala(salaactual, monstruopasado, dificultad):
    salaactual = str(salaactual)
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
    
        
    def entrar():
        btnentrar.place_forget()
        btnguardar.place_forget()
        btnsalir.place_forget()
        canvas.itemconfigure(textosala, state='hidden')
        canvas.itemconfigure(puertacerrada, state='hidden')
        canvas.itemconfigure(puertaabierta, state='normal')
        canvas.after(1500, ventanasala.destroy)
        canvas.create_text(240,180,text='Entrando en la sala '+salaactual+'...',
                       fill='white', font=('freemono', 10, 'bold'))
        for i in range(1, 75):#animación
            canvas.after(10, None)
            canvas.move(fotopj, 2, 0)
            ventanasala.update()

        
    def salir():
        ventanasala.destroy()
        mp.menuPrincipal()
        
    def guardar():
        gf.guardarPartida(salaactual, monstruopasado, dificultad)
        gf.guardarMapa()
        salir()
        
    btnentrar = Button(ventanasala, text="Entrar", command=entrar)
    btnentrar.place(x=70,y=360)
    
    btnguardar = Button(ventanasala, text="Guardar y Salir", command=guardar)
    btnguardar.place(x=200,y=360)
    
    btnsalir = Button(ventanasala, text="Salir", command=salir)
    btnsalir.place(x=350,y=360)
    
    ventanasala.mainloop()

#una vez acaba la sala, animamos la salida del personaje.
def animacionSalir(window, canvas, fotopj, salida): 
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
            canvas.move(fotopj, x,y)
            window.update()
            
    animacion()