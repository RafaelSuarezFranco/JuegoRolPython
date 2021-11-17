import random
import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionPersonaje as gpj
import csv

arraysalas = []
arrayambientes = []


def randomizarAmbiente(arrayambientes): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice][1]

def avanzarMapa(salaactual, monstruopasado, dificultad):
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala, si hubo o no hubo monstruo, etc.
    nuevosObjetos = []
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
    try:
        salaactual = int(salaactual)
        for puerta in range(1, len(arraysalas[salaactual]) ):
            if arraysalas[salaactual][puerta] != "0":
                salidas.append(arraysalas[0][puerta])
                #esta condicion significa que si en la fila de la sala que corresponde a sala actual hay algo que
                #no sea un 0, guardamos en el array de salidas la letra que corresponde, que se encuentra en
                #la primera fila de arraysalas
                
    except ValueError: # si entramos en esta excepción significa que salaactual toma valor que no es entero, cosa que solo
        #debería ocurrir en la sala FIN
        print("")
    
    #aquí damos la opción de salir (guardando o sin guardar).Si elegimos una de esas opciones, hacemos un return de
    #resultado sala para salir de la función, pero debemos introducir algo en ese return para que no se vuelva a iterar esta
    #función. Para ello, simplemente introduzco la cadena 'guardar y salir' en ese return, la cual indicará al bucle de
    #de nuevaPartida que no se debe seguir iterando, por lo tanto salimos directamente al menú principal.
    salirPartida = input("Pulsa intro para entrar en la sala.\nIntroduce G para Guardar y salir o S para Salir sin guardar.").lower()
    
    if salirPartida == "g":
        gf.guardarPartida(salaactual, monstruopasado, dificultad)
        print("Saliendo de la partida.")
        resultadosala.append(monstruopasado)
        resultadosala.append('guardar y salir')
        return resultadosala
    elif salirPartida == "s":
        print("Saliendo de la partida.")
        resultadosala.append(monstruopasado)
        resultadosala.append('guardar y salir')
        return resultadosala
    
    print("")
    #mostrar mensaje de ambiente
    ambiente = randomizarAmbiente(arrayambientes)
    print(ambiente)
    
    #calculo de objetos
    nuevosObjetos = go.invocarObjeto(dificultad)
    
    # aqui calculamos si hay o no un monstruo
    monstruopasado, monstruoactual= gm.invocarMonstruo(monstruopasado, salaactual, dificultad)
    resultadosala.append(monstruopasado)
    
    if monstruopasado == True or nuevosObjetos != None: #si hay un monstruo u objetos en la sala
        #entonces mostramos el menú, si no, pasaremos directamente a elegir la salida
        menuMapa(nuevosObjetos, monstruoactual, salaactual, monstruopasado, dificultad)
    
    
    
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
        
    print("Has abandonado la sala "+str(salaactual)+" por la puerta "+opcion+"...")
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


def menuMapa(nuevosObjetos, monstruoactual, salaactual, monstruopasado, dificultad):
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
            go.consultarInventario()
        elif accion == "3":
            if nuevosObjetos != None:
                go.recogerObjeto(nuevosObjetos)
                nuevosObjetos = None
            else:
                print("No puedes recoger más objetos de esta sala.")
        elif accion == "4": #si decidimos luchar
            if monstruopasado == True:
                gpj.personaje[1] = gm.lucha(monstruoactual, salaactual, dificultad)
        elif accion == "5": # si dedicimos escapar
            if monstruopasado == True and salaactual != "FIN":
                penalizacion = 50 + dificultad * 10
                gpj.personaje[1] = gpj.personaje[1] - penalizacion
                print("Has salido ileso del combate, sin embargo, tu orgullo ha sido gravemente herido. Pierdes "+str(penalizacion)+" HP.")
                
            elif salaactual == "FIN": #si estamos en la sala FIN, no podemos huir del monstruo
                print("Es el monstruo final, no puedes huir de él.")
                accion = ""
 


