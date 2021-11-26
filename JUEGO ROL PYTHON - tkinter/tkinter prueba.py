import csv
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
    print(arrayfinal)
    return arrayfinal

cargarMapa(1)