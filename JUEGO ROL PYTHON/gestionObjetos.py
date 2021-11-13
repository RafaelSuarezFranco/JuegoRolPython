import random
import gestionFicheros as gf
import gestionMonstruos as gm #necesitamos usar la funcion de probabilidad


arrayobjetos = gf.generarObjetos(gf.opcion)

def esEntero(num):
    try:
        entero = int(num)
        num = entero
        return True
    except ValueError:
        return False
    
def randomizarObjeto(arrayobjetos): #Devuelve un objeto (solo su número, si queremos checkear su info, la buscamos en el arrayobjetos)
    numAleatorio = random.randint(1, len(arrayobjetos))
    for indice in range( len(arrayobjetos) ):
        if arrayobjetos[indice][0] == str(numAleatorio):
            return arrayobjetos[indice][0]
            
        
def invocarObjeto(dificultad):# por cada sala, esta función generará 0, 1 o 2 objetos aleatorios.
    #la dificultad hace más o menos probable que hayan objetos. si es fácil, será 85 y 40, si es difícil, será 65 y 20.
    objetosNuevos = []
    hayObjeto = gm.probalilidad(75 - (dificultad * 10))
    if hayObjeto == True:
        objeto1 = int(randomizarObjeto(arrayobjetos))-1
        objetosNuevos.append(objeto1)
        print("En la sala hay " + arrayobjetos[objeto1][1]+".")
        hayOtroObjeto = gm.probalilidad(30 - (dificultad * 10))
        if hayOtroObjeto == True:
            objeto2 = objeto1
            while objeto2 == objeto1: #no permitimos que un segundo objeto sea igual al primero
                objeto2 = int(randomizarObjeto(arrayobjetos))-1
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


def usarObjeto(inventario): #en la funcion de lucha, llamamos a esta función para dar la opción de escoger un objeto.
    usarObjeto = ""
    while usarObjeto != "si" and usarObjeto != "no":
        usarObjeto = input("¿Quieres utilizar un objeto? (si/no)").lower()
    if usarObjeto == "si":
        consultarInventario(inventario)
        objetoUsado = ""
        while esEntero(objetoUsado) == False or objetoUsado == "":
            objetoUsado = input("Introduce el número a la izquierda del objeto que quieres usar")
            try: # queremos que el usuario meta un número desde 0 hasta el contador máximo de objeto
                # ej: tenemos 4 objetos, el usuario puede elegir del 0 al 3
                objetoUsado = int(objetoUsado)
                if objetoUsado >= 0 and objetoUsado < len(inventario):
                    return objetoUsado #lo que estamos devolviendo es el INDICE del inventario que tenemos que usar y quitar
                else:
                    objetoUsado = ""
            except ValueError:
                objetoUsado = "" # iterar el bucle
    else:#si elige no usar objeto
        return None