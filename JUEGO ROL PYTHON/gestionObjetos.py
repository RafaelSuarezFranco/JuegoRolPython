import random
import gestionFicheros as gf
import gestionMonstruos as gm #necesitamos usar la funcion de probabilidad

arrayobjetos = gf.generarObjetos()

def randomizarObjeto(arrayobjetos): #Devuelve un objeto (solo su número, si queremos checkear su info, la buscamos en el arrayobjetos)
    numAleatorio = random.randint(1, len(arrayobjetos))
    for indice in range( len(arrayobjetos) ):
        if arrayobjetos[indice][0] == str(numAleatorio):
            return arrayobjetos[indice][0]
        
        
def invocarObjeto():# por cada sala, esta función generará 0, 1 o 2 objetos aleatorios.
    objetosNuevos = []
    hayObjeto = gm.probalilidad(75)
    if hayObjeto == True:
        objeto1 = int(randomizarObjeto(arrayobjetos))
        objetosNuevos.append(objeto1)
        print("En la sala hay " + arrayobjetos[objeto1][1]+".")
        hayOtroObjeto = gm.probalilidad(30)
        if hayOtroObjeto == True:
            objeto2 = int(randomizarObjeto(arrayobjetos))
            objetosNuevos.append(objeto2)
            print("Además, hay " + arrayobjetos[objeto2][1]+".")
    
    if len(objetosNuevos) > 0:
        return objetosNuevos
    else:
        return None
    
def consultarInventario(inventario):
    contador = 0
    if len(inventario) > 0:
        print("Estos son tus objetos disponibles")
        for objeto in inventario:
            print(str(contador)+" - "+arrayobjetos[objeto][1])#mostramos un número y el nombre del objeto, el cual consultamos en el array
            contador = contador + 1
    else:
        print("No hay ningún objeto en tu inventario")
        
def recogerObjeto(nuevosObjetos, inventario):
    if nuevosObjetos != None: #si hay objetos en la sala
        if len(nuevosObjetos) == 1:
            inventario.append(nuevosObjetos[0])
            print("Has recogido "+arrayobjetos[nuevosObjetos[0]][1]+".")
        else:
            opcion = ""
            while opcion != "1" and opcion != "2":
                opcion = input("Elige, ¿recoger "+arrayobjetos[nuevosObjetos[0]][1]+"(1) o recoger "+arrayobjetos[nuevosObjetos[1]][1]+"(2)?")
            if opcion == 1:
                inventario.append(nuevosObjetos[0])
                print("Has recogido "+arrayobjetos[nuevosObjetos[0]][1]+".")
            else:
                inventario.append(nuevosObjetos[1])
                print("Has recogido "+arrayobjetos[nuevosObjetos[1]][1]+".")
    return inventario