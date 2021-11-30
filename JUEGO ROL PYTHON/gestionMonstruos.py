import random
import gestionFicheros as gf
import gestionObjetos as go
import gestionPersonaje as gpj

arraymonstruos = []

def probalilidad(porcentaje):
    #le pasaremos un porcentaje entero entre 0 y 100, devolverá true o false si el resultado cae dentro de esa probabilidad
    numAleatorio = random.randint(1, 100)
    return True if numAleatorio <= porcentaje else False

def randomizarMonstruo(): #Devuelve un monstruo aleatorio con sus características.
    numAleatorio = random.randint(1, len(arraymonstruos))
    for indice in range( len(arraymonstruos) ):
        if arraymonstruos[indice][0] == str(numAleatorio):
            return arraymonstruos[indice]


def invocarMonstruo(monstruopasado, salaactual, dificultad):
    # una vez estemos en la sala, usamos esta funcion para dedicir si hay o no hay monstruo y generar mensajes etc
    hayMonstruo = False
    if monstruopasado == False: #si no hubo monstruo en la sala anterior
        hayMonstruo = probalilidad(75 + (dificultad * 5))
    else: # la dificultad hace un 5% más o menos probable que hayan monstruos.
        hayMonstruo = probalilidad(66 + (dificultad * 5))
    
    if salaactual == "FIN": #si es la sala final, debe haber monstruo
        hayMonstruo = True
    
    monstruoactual = ""
    if hayMonstruo == True:
        monstruopasado = True
        monstruoactual = randomizarMonstruo() #en monstruo actual se almacena una línea del fichero de monstruos
        print("¡Un "+monstruoactual[1]+" salvaje apareció!")
        print("¡Ten cuidado! "+monstruoactual[4]+".")# monstramos el nombre del monstruo y una descripción.
    else:
        print("No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
        monstruopasado = False
    return monstruopasado, monstruoactual


def lucha(monstruoactual, salaactual, dificultad):
    print("Has decidido enfrentarte al "+monstruoactual[1])
    
    #aquí damos la opción de usar un objeto, si tenemos algo en el inventario
    objetoUsado = None
    objetoLucha = [] #guarda el objeto que se usa para luchar (si elige uno)
    nombreObjeto = ""
    cualidadObjeto = ""
    puntosObjeto = ""
    if len(gpj.inventario) > 0:
        objetoUsado = go.usarObjeto()
    if objetoUsado != None:#si hemos escogido un objeto, lo eliminamos del inventario y guardamos las variables que nos interesan
        objeto1 = gpj.inventario[objetoUsado]#recordamos que en inventario solo guardamos el "código" del objeto. sus cualidades las
        #consultamos en el array de objetos
        objetoLucha = [go.arrayobjetos[objeto1][1], go.arrayobjetos[objeto1][2], go.arrayobjetos[objeto1][3]]
        #contiene nombre, cualidad y puntos del objeto.
        gpj.inventario.pop(objetoUsado)
    
    #tendremos una variable para saber la vida que le queda al pj despues del encuentro.
    vidaresultado = gpj.personaje[1]
    resultado = "empate"
    while resultado == "empate" or (resultado == "perder" and salaactual == "FIN" and vidaresultado > 0):
        # repetimos hasta que una de las partes gane (si no es la sala final)
    
        #hacemos 3 tiradas y las guardamos ordenadas
        r1 = []
        for i in range(0,3):
            r1.append(random.randint(1, 20))
        r1 = sorted(r1, key=int, reverse=True)
    
        r2 = [] #dos tiradas para el enemigo, las guardamos ordenadas.
        for i in range(0,2):    
            r2.append(random.randint(1, 25 + (dificultad * 5)))
            #la dificultad aumenta o disminuye las probabilidades de ganar del monstruo.   
        r2 = sorted(r2, key=int, reverse=True)
        
    
        #posibles resultados:
        #si ambos nº del pj pasan los del enemigo, ganamos, si uno lo sobrepasa y el otro es igual, ganamos
        #si uno lo sobrepasa y el otro queda por debajo, empate. si ambos nº son iguales a los del enemigo, empate
        #si uno de los nº esta por debajo y el otro también o empata, perdemos
        if (r1[0] == r2[0] and r1[1] == r2[1]) or (r1[0] > r2[0] and r1[1] < r2[1]) or (r1[0] < r2[0] and r1[1] > r2[1]):
            resultado = "empate"
        elif (r1[0] > r2[0] and r1[1] > r2[1]) or (r1[0] > r2[0] and r1[1] == r2[1]) or (r1[0] == r2[0] and r1[1] > r2[1]):
            resultado = "ganar"
        else:
            resultado = "perder"
            
        vidaresultado = resultadoLucha(resultado, vidaresultado, monstruoactual, objetoUsado, objetoLucha, salaactual)
    
    return vidaresultado



def resultadoLucha(resultado, vidaresultado, monstruoactual, objetoUsado, objetoLucha, salaactual):
    nombreObjeto = ""
    cualidadObjeto = ""
    puntosObjeto = ""
    if objetoUsado != None:
        nombreObjeto = objetoLucha[0]
        cualidadObjeto = objetoLucha[1]
        puntosObjeto = objetoLucha[2]
    #recalculamos la vida del pj dependiendo del resultado y del objeto
    ########################################################################################## SI GANAMOS
    if resultado == "ganar" and objetoUsado == None:########si ganamos sin objeto
        vidaresultado = vidaresultado + int(monstruoactual[2])
        print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
        return vidaresultado
    
    elif resultado == "ganar" and objetoUsado != None:########si ganamos con objeto
        vidaresultado = vidaresultado + int(monstruoactual[2])
        print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
        
        if cualidadObjeto == monstruoactual[3]: #comparamos sus cualidades, si es la misma
            print("Has usado un "+nombreObjeto+". Ha sido efectivo, ganas "+puntosObjeto+" puntos de vida.")
            vidaresultado = vidaresultado + int(puntosObjeto)
            
            if gpj.personaje[2] == monstruoactual[3]: #si nuestra cualidad también coincide, sumamos 20%
                bonus = 0.2*(int(puntosObjeto)+int(monstruoactual[2]))
                print("Tu cualidad de "+gpj.personaje[2]+" ha sido efectiva, recibes un bonus de "+str(bonus)+" de vida.")
                vidaresultado = vidaresultado + int(bonus)
                    
        else:##########si la cualidad del objeto no coincide
            print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
            vidaresultado = vidaresultado - int(puntosObjeto)
        return vidaresultado
    ################################################################################### SI PERDEMOS
    elif resultado == "perder":
        vidaresultado = vidaresultado - int(monstruoactual[2])
        print("Has perdido contra el " + monstruoactual[1] + ", tu vida se ha reducido a "+ str(vidaresultado))

        if objetoUsado != None:#si hemos usado efecto, ni suma ni resta.
            print("Has usado un "+nombreObjeto+". No ha tenido efecto")
        
        #si estamos en la sala final, supongo que debemos luchar hasta matar al mostruo final, por lo que perder debe
        #iterar el bucle también
        if salaactual == "FIN":
            resultado = "empate"
            if vidaresultado > 0: #mientras tengamos vida, seguimos luchando.
                input("Aún te quedan fuerzas para luchar. Pulsa intro para intentarlo de nuevo.")

        return vidaresultado #si nos quedamos sin vida, también saldremos de la función.
    else:
        input("Ha habido empate en este turno. Pulsa intro para intentarlo de nuevo.")
        return vidaresultado