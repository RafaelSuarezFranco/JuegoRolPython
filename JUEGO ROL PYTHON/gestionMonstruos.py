import random
import gestionFicheros as gf

#hay que definir este array aqui, si no, las funciones no pueden encontrarlo.
arraymonstruos = gf.generarMonstruos()

def probalilidad(porcentaje):
    #le pasaremos un porcentaje entero entre 0 y 100, devolverá true o false si el resultado cae dentro de esa probabilidad
    numAleatorio = random.randint(1, 100)
    if numAleatorio <= porcentaje:
        return True
    else:
        return False

def randomizarMonstruo(arraymonstruos): #Devuelve un monstruo aleatorio con sus características.
    numAleatorio = random.randint(1, len(arraymonstruos))
    for indice in range( len(arraymonstruos) ):
        if arraymonstruos[indice][0] == str(numAleatorio):
            return arraymonstruos[indice]


def invocarMonstruo(monstruopasado): # una vez estemos en la sala, usamos esta funcion para dedicir si hay o no hay monstruo y generar mensajes etc
    hayMonstruo = False
    if monstruopasado == False: #si no hubo monstruo en la sala anterior
        hayMonstruo = probalilidad(75)
        print("No hubo monstruo en la sala anterior")
    else:
        hayMonstruo = probalilidad(66)
        print("Hubo monstruo en la sala anterior")
        
    monstruoactual = ""
    if hayMonstruo == True:
        monstruopasado = True
        monstruoactual = randomizarMonstruo(arraymonstruos) #en monstruo actual se almacena una línea del fichero de monstruos
        print("¡Un "+monstruoactual[1]+" salvaje apareció!")
        print("¡Ten cuidado! "+monstruoactual[4]+".")# monstramos el nombre del monstruo y una descripción.
    else:
        print("No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
        monstruopasado = False
    return monstruopasado


def lucha(monstruoactual):
    print("Has decidido enfrentarte al "+monstruoactual[1])
    #hacemos 3 tiradas y guardamos las 2 más grandes.
    resultados = []
    for i in range(0,3):
        resultados.append(random.randint(1, 20))
    resultadomax1 = max(resultados)
    resultados.remove(resultadomax1)
    resultadomax2 = max(resultados)
    #print(str(resultadomax1)+" "+str(resultadomax2)+" "+str(resultados))
        
    resultadoenemigo1 = random.randint(1, 25)
    resultadoenemigo2 = random.randint(1, 25)
    
