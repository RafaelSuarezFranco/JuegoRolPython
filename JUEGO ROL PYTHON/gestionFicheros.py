import csv
from prettytable import PrettyTable

opcion = "default" #variable global para saber si la partida que vamos a jugar usa archivos default o custom
# esta variable se rescribe cada vez que iniciamos partida, a su vez, deben rescribirse todos los arrays (en nueva partida) 
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
def generarMapa(opcion): #con csv es más conciso, por lo que importaré los archivos de esta manera.
    archivoSalas = open('./'+opcion+'/mapa.txt', "r",encoding="utf-8")
    salas = csv.reader(archivoSalas, delimiter = ';')
    arraysalas = list(salas)
    return arraysalas

def generarAmbientes(opcion):
    archivoAmbiente = open('./'+opcion+'/ambientes.txt', "r",encoding="utf-8")
    ambientes = csv.reader(archivoAmbiente, delimiter = ';')
    arrayambientes = list(ambientes)
    return arrayambientes

def generarObjetos(opcion):
    archivoObjeto = open('./'+opcion+'/objetos.txt', "r",encoding="utf-8")
    objetos = csv.reader(archivoObjeto, delimiter = ';')
    arrayobjetos = list(objetos)
    return arrayobjetos

def generarMonstruos(opcion):
    archivoMonstruo = open('./'+opcion+'/monstruos.txt', "r",encoding="utf-8")
    monstruos = csv.reader(archivoMonstruo, delimiter = ';')
    arraymonstruos = list(monstruos)
    return arraymonstruos

#me conviene tener esta función aquí
def guardarPartida(personaje, opcion, salaactual, monstruopasado, inventario):
    partidas = open("partidasGuardadas.txt",'a', newline='', encoding='utf-8')
    #en la partida guardaré la cantidad de objetos también, para saber cuántos hay.
    datosGuardados = [personaje[0], str(personaje[1]), personaje[2], opcion, str(salaactual), str(monstruopasado), str(len(inventario))]
    for objeto in inventario:
        datosGuardados.append(str(objeto))
    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerow(datosGuardados)
    partidas.close()
    print("Partida guardada con éxito.")
    
"""
Nota: soy consciente de que en guardarpartida no hemos guardado el array del mapa, lo que significa que aunque
carguemos partida, se generará el mapa (default o custom) renovado, por lo que se podría utilizar esto para volver a
salas anteriores, lo cual no está permitido normalmente, pero para no complicar mucho el tema de guardado, no voy a
guardar todo el mapa solo para asegurarme de que se cumple esa regla.
"""

def elegirPartidaGuardada():#muestra las partidas guardadas en una tabla
    #permite seleccionar una que se le pasará como parámetro a nuevaPartida.
    ficheropartidas = open("partidasGuardadas.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    tablaPartidas=PrettyTable(["Nº PARTIDA","NOMBRE","VIDA","HABILIDAD","TIPO PARTIDA","SALA ACTUAL"])
    contador = 0
    
    for partida in arraypartidas:
        if contador != 0:
            tablaPartidas.add_row([contador, partida[0], partida[1], partida[2], partida[3], partida[4]])
        contador = contador + 1
    print(tablaPartidas)
    
    partidaseleccionada = 0
    while partidaseleccionada < 1 or partidaseleccionada > contador-1:
        try:
            partidaseleccionada = int(input("Introduce el nº de partida a cargar"))
        except ValueError:
            partidaseleccionada = 0
    
    return arraypartidas[partidaseleccionada]
    
"""
def generarMapa():
    archivoSalas = open('./default/mapa.txt', "r",encoding="utf-8")
    salas = archivoSalas.readlines()
    arraysalas = []
    for i in salas:
        arraysalas.append(i.split(";"))
    #print(arraysalas)
    return arraysalas
    #guardamos toda la información de las salas en un array de dos coordenadas


def generarAmbientes():
    archivoAmbiente = open('./default/ambientes.txt', "r",encoding="utf-8")
    ambientes = archivoAmbiente.readlines()
    arrayambientes = []
    for i in ambientes:
        arrayambientes.append(i.split(";"))
    return arrayambientes

def generarObjetos():
    archivoObjeto = open('./default/objetos.txt', "r",encoding="utf-8")
    objetos = archivoObjeto.readlines()
    arrayobjetos = []
    for i in objetos:
        arrayobjetos.append(i.split(";"))
    return arrayobjetos
    
"""