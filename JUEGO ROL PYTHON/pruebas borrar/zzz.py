import csv
from prettytable import PrettyTable

def borrarPartida():
    #basicamente es una copia de cargar partida + guardar partida, recuperarmos las partidas y mapas en unos arrays,
    #borramos una partida y su mapa de los arrays y los reescribimos en los ficheros
    ficheropartidas = open("yyy.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    
    ficheromapas = open("zzz.txt",'r', encoding='utf-8')   
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
        
    partidas = open("yyy.txt",'w', newline='', encoding='utf-8')#rescribir partidas
    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerows(arraypartidas)
    partidas.close()
    
    mapas = open("zzz.txt",'w', newline='', encoding='utf-8')
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ',')
        csvescrito.writerows(arraymapas)
    mapas.close()
    
borrarPartida()