import random
import gestionFicheros as gf
import gestionObjetos as go

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


def invocarMonstruo(monstruopasado, salaactual): # una vez estemos en la sala, usamos esta funcion para dedicir si hay o no hay monstruo y generar mensajes etc
    hayMonstruo = False
    if monstruopasado == False: #si no hubo monstruo en la sala anterior
        hayMonstruo = probalilidad(75)
        #print("No hubo monstruo en la sala anterior")
    else:
        hayMonstruo = probalilidad(66)
        #print("Hubo monstruo en la sala anterior")
    
    if salaactual == "FIN": #si es la sala final, debe haber monstruo
        hayMonstruo = True
    
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


def lucha(personaje, monstruoactual, inventario, arrayobjetos, salaactual):
    print("Has decidido enfrentarte al "+monstruoactual[1])
    
    #aquí damos la opción de usar un objeto, si tenemos algo en el inventario
    objetoUsado = None
    nombreObjeto = ""
    cualidadObjeto = ""
    puntosObjeto = ""
    if len(inventario) > 0:
        objetoUsado = go.usarObjeto(inventario)
    if objetoUsado != None:#si hemos escogido un objeto, lo eliminamos del inventario y guardamos las variables que nos interesan
        objeto1 = inventario[objetoUsado]#recordamos que en inventario solo guardamos el "código" del objeto. sus cualidades las
        #consultamos en el array de objetos
        nombreObjeto = arrayobjetos[objeto1][1]
        cualidadObjeto = arrayobjetos[objeto1][2]
        puntosObjeto = arrayobjetos[objeto1][3]
        inventario.pop(objetoUsado)
    
    #tendremos una variable para saber la vida que le queda al pj despues del encuentro.
    vidaresultado = personaje[1]
    resultado = "empate"
    while resultado == "empate" or (resultado == "perder" and salaactual == "FIN" and vidaresultado > 0):
        # repetimos hasta que una de las partes gane (si no es la sala final)
    
        #hacemos 3 tiradas y guardamos las 2 más grandes.
        resultados = []
        for i in range(0,3):
            resultados.append(random.randint(1, 20))
        pjmax1 = max(resultados)
        resultados.remove(pjmax1)
        pjmax2 = max(resultados)
    
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
            
        vidaresultado = resultadoLucha(personaje, resultado, vidaresultado, monstruoactual, objetoUsado, cualidadObjeto, puntosObjeto, nombreObjeto, salaactual)
    
    return vidaresultado
    """
        #recalculamos la vida del pj dependiendo del resultado y del objeto
        ########################################################################################## SI GANAMOS
        if resultado == "ganar":
            vidaresultado = vidaresultado + int(monstruoactual[2])
            print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
            if objetoUsado != None: #si hemos usado objeto
                if cualidadObjeto == monstruoactual[3]: #comparamos sus cualidades, si es la misma
                    print("Has usado un "+nombreObjeto+". Ha sido efectivo, ganas "+puntosObjeto+" puntos de vida.")
                    vidaresultado = vidaresultado + int(puntosObjeto)
                    if personaje[2] == monstruoactual[3]: #si nuestra cualidad también coincide, sumamos 20%
                        bonus = 0.2*(int(puntosObjeto)+int(monstruoactual[2]))
                        print("Tu cualidad de "+personaje[2]+" ha sido efectiva, recibes un bonus de "+str(bonus)+" de vida.")
                        vidaresultado = vidaresultado + bonus
                else:# si no es la misma
                    print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
                    vidaresultado = vidaresultado - int(puntosObjeto)
            return vidaresultado
        ################################################################################### SI PERDEMOS
        elif resultado == "perder":
            vidaresultado = vidaresultado - int(monstruoactual[2])
            print("Has perdido contra el " + monstruoactual[1] + ", tu vida se ha reducido a "+ str(vidaresultado))
            # de momento voy a restar el objeto, sea de la cualidad que sea.
            if objetoUsado != None: #si hemos usado objeto, considero que no ha sido beneficioso en ningún caso.
                print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
                vidaresultado = vidaresultado - int(puntosObjeto)
            
            #si estamos en la sala final, supongo que debemos luchar hasta matar al mostruo final, por lo que perder debe
            #iterar el bucle también
            if salaactual == "FIN":
                resultado = "empate"
                if vidaresultado > 0: #mientras tengamos vida, seguimos luchando.
                    input("Aún te quedan fuerzas para luchar. Pulsa intro para intentarlo de nuevo.")
                else:
                    return vidaresultado #si nos quedamos sin vida, salimos de la función.
            else:
                return vidaresultado
        else:
            print("Ha habido empate en este turno.")
        """

def resultadoLucha(personaje, resultado, vidaresultado, monstruoactual, objetoUsado, cualidadObjeto, puntosObjeto, nombreObjeto, salaactual):
    #recalculamos la vida del pj dependiendo del resultado y del objeto
    ########################################################################################## SI GANAMOS
    if resultado == "ganar":
        vidaresultado = vidaresultado + int(monstruoactual[2])
        print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
        if objetoUsado != None: #si hemos usado objeto
            if cualidadObjeto == monstruoactual[3]: #comparamos sus cualidades, si es la misma
                print("Has usado un "+nombreObjeto+". Ha sido efectivo, ganas "+puntosObjeto+" puntos de vida.")
                vidaresultado = vidaresultado + int(puntosObjeto)
                if personaje[2] == monstruoactual[3]: #si nuestra cualidad también coincide, sumamos 20%
                    bonus = 0.2*(int(puntosObjeto)+int(monstruoactual[2]))
                    print("Tu cualidad de "+personaje[2]+" ha sido efectiva, recibes un bonus de "+str(bonus)+" de vida.")
                    vidaresultado = vidaresultado + bonus
            else:# si no es la misma
                print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
                vidaresultado = vidaresultado - int(puntosObjeto)
        return vidaresultado
    ################################################################################### SI PERDEMOS
    elif resultado == "perder":
        vidaresultado = vidaresultado - int(monstruoactual[2])
        print("Has perdido contra el " + monstruoactual[1] + ", tu vida se ha reducido a "+ str(vidaresultado))
        # de momento voy a restar el objeto, sea de la cualidad que sea.
        if objetoUsado != None: #si hemos usado objeto, considero que no ha sido beneficioso en ningún caso.
            print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
            vidaresultado = vidaresultado - int(puntosObjeto)
        
        #si estamos en la sala final, supongo que debemos luchar hasta matar al mostruo final, por lo que perder debe
        #iterar el bucle también
        if salaactual == "FIN":
            resultado = "empate"
            if vidaresultado > 0: #mientras tengamos vida, seguimos luchando.
                input("Aún te quedan fuerzas para luchar. Pulsa intro para intentarlo de nuevo.")
                return vidaresultado
            else:
                return vidaresultado #si nos quedamos sin vida, salimos de la función.
        else:
            return vidaresultado
    else:
        input("Ha habido empate en este turno. Pulsa intro para intentarlo de nuevo.")
    return vidaresultado