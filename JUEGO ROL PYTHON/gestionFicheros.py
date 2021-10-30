import csv


def generarMapa(): #con csv es más conciso, por lo que importaré los archivos de esta manera.
    archivoSalas = open('./default/mapa.txt', "r",encoding="utf-8")
    salas = csv.reader(archivoSalas, delimiter = ';')
    arraysalas = list(salas)
    return arraysalas

def generarAmbientes():
    archivoAmbiente = open('./default/ambientes.txt', "r",encoding="utf-8")
    ambientes = csv.reader(archivoAmbiente, delimiter = ';')
    arrayambientes = list(ambientes)
    return arrayambientes

def generarObjetos():
    archivoObjeto = open('./default/objetos.txt', "r",encoding="utf-8")
    objetos = csv.reader(archivoObjeto, delimiter = ';')
    arrayobjetos = list(objetos)
    return arrayobjetos

def generarMonstruos():
    archivoMonstruo = open('./default/monstruos.txt', "r",encoding="utf-8")
    monstruos = csv.reader(archivoMonstruo, delimiter = ';')
    arraymonstruos = list(monstruos)
    return arraymonstruos


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