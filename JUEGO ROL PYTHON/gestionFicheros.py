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


#funciones de carga de partida
def generarMapa(): 
    archivoSalas = open('./'+opcion+'/mapa.txt', "r",encoding="utf-8")
    salas = csv.reader(archivoSalas, delimiter = ';')
    arraysalas = list(salas)
    return arraysalas

def generarAmbientes():
    archivoAmbiente = open('./'+opcion+'/ambientes.txt', "r",encoding="utf-8")
    ambientes = csv.reader(archivoAmbiente, delimiter = ';')
    arrayambientes = list(ambientes)
    return arrayambientes

def generarObjetos():
    archivoObjeto = open('./'+opcion+'/objetos.txt', "r",encoding="utf-8")
    objetos = csv.reader(archivoObjeto, delimiter = ';')
    arrayobjetos = list(objetos)
    return arrayobjetos

def generarMonstruos():
    archivoMonstruo = open('./'+opcion+'/monstruos.txt', "r",encoding="utf-8")
    monstruos = csv.reader(archivoMonstruo, delimiter = ';')
    arraymonstruos = list(monstruos)
    return arraymonstruos

#me conviene tener esta función aquí
def guardarPartida(salaactual, monstruopasado, dificultad):
    partidas = open("partidasGuardadas.txt",'a', newline='', encoding='utf-8')
    if dificultad == 0:
        dificultad = "normal"
    elif dificultad == 1:
        dificultad = "dificil"
    elif dificultad == -1:
        dificultad = "facil"  
    #en la partida guardaré la cantidad de objetos también, para saber cuántos hay.
    datosGuardados = [gpj.personaje[0], str(gpj.personaje[1]), gpj.personaje[2], opcion, str(dificultad),
                      str(salaactual), str(monstruopasado), str(len(gpj.inventario))]
    for objeto in gpj.inventario:
        datosGuardados.append(str(objeto))
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


