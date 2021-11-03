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
        #print("No hubo monstruo en la sala anterior")
    else:
        hayMonstruo = probalilidad(66)
        #print("Hubo monstruo en la sala anterior")
        
    monstruoactual = ""
    if hayMonstruo == True:
        monstruopasado = True
        monstruoactual = randomizarMonstruo(arraymonstruos) #en monstruo actual se almacena una línea del fichero de monstruos
        print("¡Un "+monstruoactual[1]+" salvaje apareció!")
        print("¡Ten cuidado! "+monstruoactual[4]+".")# monstramos el nombre del monstruo y una descripción.
    else:
        print("No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
        monstruopasado = False
    return monstruopasado, monstruoactual


def lucha(personaje, monstruoactual):
    print("Has decidido enfrentarte al "+monstruoactual[1])
    resultado = "empate"
    while resultado == "empate":
    
        #hacemos 3 tiradas y guardamos las 2 más grandes.
        resultados = []
        for i in range(0,3):
            resultados.append(random.randint(1, 20))
        pjmax1 = max(resultados)
        resultados.remove(pjmax1)
        pjmax2 = max(resultados)
        #print(str(resultadomax1)+" "+str(resultadomax2)+" "+str(resultados))
    
        resultadosenemigo = [] #dos tiradas para el enemigo, las guardamos ordenadas.
        for i in range(0,2):    
            resultadosenemigo.append(random.randint(1, 25))
        enemax1 = max(resultadosenemigo)
        resultadosenemigo.remove(enemax1)
        enemax2 = max(resultadosenemigo)   
    
        #posibles resultados:
        #si ambos nº del pj pasan los del enemigo, ganamos, si uno lo sobrepasa y el otro es igual, ganamos
        #si uno lo sobrepasa y el otro queda por debajo, empate. si ambos nº son iguales a los del enemigo, empate
        #si uno de los nº esta por debajo y el otro también o empata, perdemos
    
        if (pjmax1 == enemax1 and pjmax2 == enemax2) or (pjmax1 > enemax1 and pjmax2 < enemax2) or (pjmax1 < enemax1 and pjmax2 > enemax2):
            resultado = "empate"
        elif (pjmax1 > enemax1 and pjmax2 > enemax2) or (pjmax1 > enemax1 and pjmax2 == enemax2) or (pjmax1 == enemax1 and pjmax2 > enemax2):
            resultado = "ganar"
        else:
            resultado = "perder"
        
        vidaresultado = personaje[1]
        if resultado == "ganar":
            vidaresultado = vidaresultado + int(monstruoactual[2])
            print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
            return vidaresultado
        elif resultado == "perder":
            vidaresultado = vidaresultado - int(monstruoactual[2])
            print("Has perdido contra el " + monstruoactual[1] + ", tu vida se ha reducido a "+ str(vidaresultado))
            return vidaresultado
        else:
            print("Ha habido empate en este turno.")