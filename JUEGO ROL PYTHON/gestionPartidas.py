import random
import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionSalas as gs
import gestionPersonaje as gpj
import csv

#personaje = []
inventario = []


def nuevaPartida(partida): #le pasamos la partida cargada (si es nueva partida, le pasamos None)
    if partida == None:# SI LA PARTIDA ES COMPLETAMENTE NUEVA
        gf.opcion = gf.elegirArchivos() #controla si usamos archivos default o custom
        #inicializamos variables que controlarán el estado actual del juego
        gpj.personaje = gpj.crearPersonaje()
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
        inventario = []
        for i in range(1, int(partida[6])):
            inventario.append(int(partida[6+i]))#añadiendo los objetos guardados al inventario

        salaactual = partida[4]
        resultadosala = []
        monstruopasado = True
        if partida[5] == "False":#el monstruo pasado está guardado como string.
            monstruopasado = False
        input("Pulsa intro para continuar con la partida...")
    
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
        resultadosala = gs.avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario)
        salaactual = resultadosala[1]
        monstruopasado = resultadosala[0]
        if salaactual != "-1" and salaactual != "guardar y salir":
            print("Te encuentras en la sala "+salaactual)
        #si hemos seleccionado guardar partida y salir, salaactual recoge el valor 'guardar y salir'
        #nos indica que debemos salir del juego (romper este bucle)
           
    if salaactual == "FIN":
        print("Has llegado a la sala final")
        resultadosala = gs.avanzarMapa(salaactual, arraysalas, arrayambientes, monstruopasado, inventario)

#nuevaPartida()