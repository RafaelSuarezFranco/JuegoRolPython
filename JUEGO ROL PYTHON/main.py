import random
import gestionFicheros as gf #alias para llamar a las funciones de cada modulo
import gestionMonstruos as gm
import gestionObjetos as go

arraysalas = []
arrayambientes = []
#arrayobjetos = []
#arraymonstruos = []
personaje = []
inventario = []
    
def randomizarAmbiente(arrayambientes): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice][1]   

def avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario):
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala, si hubo o no hubo monstruo, etc.
    # dado que hay ciertos problemas a la hora de devolverlos por separado.
    nuevosObjetos = []
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
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
    print(ambiente)
    input("Pulsa intro para dar un paso adelante.")
    print("")
    
    #calculo de objetos
    nuevosObjetos = go.invocarObjeto()
    
    # aqui calculamos si hay o no un monstruo
    monstruopasado, monstruoactual= gm.invocarMonstruo(monstruopasado, salaactual)
    resultadosala.append(monstruopasado)
    
    if monstruopasado == True or nuevosObjetos != None: #si hay un monstruo u objetos en la sala
        #entonces mostramos el menú, si no, pasaremos directamente a elegir la salida
        menuMapa(inventario, nuevosObjetos, personaje, monstruoactual, go.arrayobjetos, salaactual, monstruopasado)
    
    if personaje[1] < 1: #bajar a 0 o menos de vida es condición de derrota.
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


def menuMapa(inventario, nuevosObjetos, personaje, monstruoactual, arrayobjetos, salaactual, monstruopasado):
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
            mostrarPersonaje()
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
                personaje[1] = gm.lucha(personaje, monstruoactual, inventario, go.arrayobjetos, salaactual)
        elif accion == "5": # si dedicimos escapar
            if monstruopasado == True and salaactual != "FIN":
                print("Has salido ileso del combate, sin embargo, tu orgullo ha sido gravemente herido. Pierdes 50 HP.")
                personaje[1] = personaje[1] - 50
            elif salaactual == "FIN": #si estamos en la sala FIN, no podemos huir del monstruo
                print("Es el monstruo final, no puedes huir de él.")
                accion = ""

                    

def crearPersonaje():
    print("Vamos a crear tu personaje")
    nombre = input("Nombre de tu personaje: ")
    while nombre == "":
        nombre = input("¿Crees que te voy a dejar avanzar sin que escribas un nombre?")

    vidarand = random.randint(0, 100)
    vida = 100 + vidarand
    print("Los dioses te han condedido "+str(vida)+" puntos de vida.")

    habilidad = input("Elige tu habilidad: 1 - Lucha. 2 - Magia. 3 - Astucia")
    while habilidad != "1" and habilidad != "2" and habilidad != "3":
        habilidad = input("No es tan difícil. Escribe 1, 2, o 3.")
    if habilidad == "1":
        habilidad = "LUCHA"
    elif habilidad == "2":
        habilidad = "MAGIA"
    else:
        habilidad = "ASTUCIA"
        
    personaje.extend((nombre, vida, habilidad))
    return personaje

def mostrarPersonaje():
    print("Estado actual de tu personaje:")
    print("Nombre: " + personaje[0])
    print("Vida: " + str(personaje[1]))
    print("Habilidad: " + personaje[2])

def nuevaPartida():   
    #cargamos en memoria los elementos del juego. Los comentados se cargan desde su propio módulo.
    arraysalas = gf.generarMapa()
    arrayambientes = gf.generarAmbientes()
    #arrayobjetos = gf.generarObjetos()
    #arraymonstruos = gf.generarMonstruos()

    """
    Acerca del array de salas: como el tema sobre no volver a una sala anterior queda un poco a criterio del diseñador, lo
    que he dedidido es que cada sala por la que pasemos se vaya borrando de dicho array, como si el mapa se fuera destruyendo
    a medida que avanzamos. Esto implica que si nos encontramos en un callejón sin salida, el juego se da por perdido.
    """
    
    #inicializamos variables que controlarán el estado actual del juego
    personaje = crearPersonaje()
    inventario = []
    salaactual = "1"
    resultadosala = []
    monstruopasado = False #guardamos si hubo un monstruo en la sala anterior
    print("Da comienzo la aventura, te encuentras en la sala "+arraysalas[1][0]+".")
    print("La mazmorra en la que te encuentras es inestable y colapsa a medida que la recorres.")
    print("Cada sala por la que pases se derrumbará y no podrás volver sobre tus pasos. Elige bien a dónde vas.")
    input("Pulsa intro para empezar...")
    #avanzamos por las salas mientras que no llegemos a la sala FIN o la sala actual valga -1, que significa que estamos
    #en un callejón sin salida.
    while salaactual != "FIN" and salaactual != "-1" and personaje[1] > 0:
        resultadosala = avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario)
        salaactual = resultadosala[1]
        monstruopasado = resultadosala[0]
        if salaactual != "-1":
            print("Te encuentras en la sala "+salaactual)
    
    if salaactual == "FIN":
        print("Has llegado a la sala final")
        resultadosala = avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario)

nuevaPartida()