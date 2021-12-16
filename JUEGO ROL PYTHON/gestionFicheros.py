import csv
from prettytable import PrettyTable
import gestionPersonaje as gpj
import gestionSalas as gs

opcion = "default" #variable global para saber si la partida que vamos a jugar usa archivos default o custom
#esta variable se rescribe cada vez que iniciamos partida, a su vez deben rescribirse todos los arrays(en nuevaPartida) 
def elegirArchivos():
    opcion = ""
    while opcion != "1" and opcion != "2":
        opcion = input("Introduce 1 para cargar archivos por defecto, Introduce 2 para cargar archivos personalizados.")
    if opcion == "2":
        opcion = "custom"
    else:
        opcion = "default"
    return opcion

# para cargar los elementos del juego en arrays, le pasamos el nombre de los ficheros.
def generarArray(fichero):
    archivo = open('./'+opcion+'/'+fichero+'.txt', "r",encoding="utf-8")
    elementos = csv.reader(archivo, delimiter = ';')
    array = list(elementos)
    return array

#FUNCIONES DE GUARDAR
def guardarPartida(salaactual, monstruopasado, dificultad):
    partidas = open("partidasGuardadas.txt",'a', newline='', encoding='utf-8')
    if dificultad == 0:
        dificultad = "normal"
    elif dificultad == 1:
        dificultad = "dificil"
    elif dificultad == -1:
        dificultad = "facil"  
    #el inventario lo guardaremos casteando el array a string
    inventarioguardado = str(gpj.inventario)
    #el personaje prefiero guardarlo por separado porque quiero visualizarlo a la hora de mostrar partidas guardadas (para cargar una de ellas)
    datosGuardados = [gpj.personaje[0], str(gpj.personaje[1]), gpj.personaje[2], opcion, str(dificultad),
                      str(salaactual), str(monstruopasado), inventarioguardado]

    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerow(datosGuardados)
    partidas.close()
    print("Partida guardada con éxito.")
    
def guardarMapa():
    mapas = open("mapasGuardados.txt",'a', newline='', encoding='utf-8')
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ',')
        csvescrito.writerow(gs.arraysalas)
    mapas.close()
    print("Estado del mapa guardado con éxito.")
    
#FUNCIONES DE CARGAR PARTIDA GUARDADA
def elegirPartidaGuardada():#muestra las partidas guardadas en una tabla
    #permite seleccionar una que se le pasará como parámetro a nuevaPartida.
    ficheropartidas = open("partidasGuardadas.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    
    if len(arraypartidas) == 1:#si no hay partidas guardadas
        print("No tienes partidas guardadas. Se creará una nueva.")
        return None
    
    tablaPartidas=PrettyTable(["Nº PARTIDA","NOMBRE","VIDA","HABILIDAD","TIPO PARTIDA","DIFICULTAD","SALA ACTUAL"])
    contador = 0

        
    for partida in arraypartidas:
        if contador != 0:
            tablaPartidas.add_row([contador, partida[0], partida[1], partida[2], partida[3], partida[4], partida[5]])
        contador = contador + 1
    print(tablaPartidas)
    
    partidaseleccionada = 0
    while partidaseleccionada < 1 or partidaseleccionada > contador-1:
        try:
            partidaseleccionada = int(input("Introduce el nº de partida a cargar"))
        except ValueError:
            partidaseleccionada = 0
    gs.arraysalas = cargarMapa(partidaseleccionada) #carga el estado guardado del mapa
    return arraypartidas[partidaseleccionada]


def cargarMapa(indice):#carga el mapa guardado en la misma posicion de la partida.
    ficheromapas = open("mapasGuardados.txt",'r', encoding='utf-8')   
    mapasguardados = csv.reader(ficheromapas, delimiter = ',')
    arraymapas = list(mapasguardados)
    arrayfinal = []
    #tal como guardo los mapas (el mapa entero en una linea) cada subarray se guarda como cadena, por lo tanto
    #al recuperarlo aqui, tengo que hacerle un eval a cada string para convertirlo en array.
    for i in range(0, len(arraymapas[indice])):
        array = eval(arraymapas[indice][i])
        arrayfinal.append(array)
    #print(arrayfinal)
    return arrayfinal

#FUNCIÓN DE BORRAR PARTIDA
def borrarPartida():
    #basicamente es una copia de cargar partida + guardar partida, recuperarmos las partidas y mapas en unos arrays,
    #borramos una partida y su mapa de los arrays y los reescribimos en los ficheros
    ficheropartidas = open("partidasGuardadas.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    
    ficheromapas = open("mapasGuardados.txt",'r', encoding='utf-8')   
    mapasguardados = csv.reader(ficheromapas, delimiter = ',')
    arraymapas = list(mapasguardados)
    
    if len(arraypartidas) == 1:#si no hay partidas guardadas
        print("No tienes partidas guardadas.")
    
    tablaPartidas=PrettyTable(["Nº PARTIDA","NOMBRE","VIDA","HABILIDAD","TIPO PARTIDA","DIFICULTAD","SALA ACTUAL"])
    contador = 0

        
    for partida in arraypartidas:
        if contador != 0:
            tablaPartidas.add_row([contador, partida[0], partida[1], partida[2], partida[3], partida[4], partida[5]])
        contador = contador + 1
    print(tablaPartidas)
    
    partidaseleccionada = -1
    while (partidaseleccionada < 0 or partidaseleccionada > contador-1):
        try:
            partidaseleccionada = int(input("Introduce el nº de partida a borrar (pulsa intro si no quieres borrar nada)"))
        except ValueError:
            partidaseleccionada = 0

    if partidaseleccionada != 0:
        arraypartidas.pop(partidaseleccionada) #borramos la línea en partidas y mapas guardados.
        arraymapas.pop(partidaseleccionada)
        print("Partida borrada con éxito")
        #print(arraypartidas)
        
    partidas = open("partidasGuardadas.txt",'w', newline='', encoding='utf-8')#rescribir partidas
    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerows(arraypartidas)
    partidas.close()
    
    mapas = open("mapasGuardados.txt",'w', newline='', encoding='utf-8')
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ',')
        csvescrito.writerows(arraymapas)
    mapas.close()
    

