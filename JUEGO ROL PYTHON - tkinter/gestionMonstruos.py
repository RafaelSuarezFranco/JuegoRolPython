import random
import gestionFicheros as gf
import gestionObjetos as go
import gestionPersonaje as gpj

#hay que definir este array aqui, si no, las funciones no pueden encontrarlo.
arraymonstruos = gf.generarMonstruos(gf.opcion)

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
        monstruoactual = randomizarMonstruo(arraymonstruos) #en monstruo actual se almacena una línea del fichero de monstruos
        print("¡Un "+monstruoactual[1]+" salvaje apareció!\n")
        print("¡Ten cuidado! "+monstruoactual[4]+".")# monstramos el nombre del monstruo y una descripción.
    else:
        print("No parece haber ninguna amenaza en la sala. Suspiras de alivio.")
        monstruopasado = False
    return monstruopasado, monstruoactual


def lucha(personaje, monstruoactual, inventario, indiceinventario, salaactual, dificultad):
    print("Has decidido enfrentarte al "+monstruoactual[1])
    
    #aquí damos la opción de usar un objeto, si tenemos algo en el inventario
    objetoUsado = None
    nombreObjeto = ""
    cualidadObjeto = ""
    puntosObjeto = ""
    if indiceinventario != "":
        index = int(indiceinventario)-1 # estos unos son para reajustar el índice y objeto escogido, dado que en el combobox se usa fórmula distinta
        objetoUsado = inventario[index]-1
        nombreObjeto = go.arrayobjetos[objetoUsado][1]
        cualidadObjeto = go.arrayobjetos[objetoUsado][2]
        puntosObjeto = go.arrayobjetos[objetoUsado][3]
        inventario.pop(index)
    
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
            resultadosenemigo.append(random.randint(1, 25 + (dificultad * 5)))
            #la dificultad aumenta o disminuye las probabilidades de ganar del monstruo.
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
        objetobueno = False
        vidaresultado, objetobueno = resultadoLucha(personaje, resultado, vidaresultado, monstruoactual, objetoUsado, cualidadObjeto, puntosObjeto, nombreObjeto, salaactual)
    
    return vidaresultado, resultado, objetobueno



def resultadoLucha(personaje, resultado, vidaresultado, monstruoactual, objetoUsado, cualidadObjeto, puntosObjeto, nombreObjeto, salaactual):
    #recalculamos la vida del pj dependiendo del resultado y del objeto
    ########################################################################################## SI GANAMOS
    objetobueno = False
    if cualidadObjeto == monstruoactual[3]: #comparamos sus cualidades, si es la misma
        objetobueno = True
    if resultado == "ganar":
        vidaresultado = vidaresultado + int(monstruoactual[2])
        print("Has derrotado al " + monstruoactual[1] + ", tu vida se ha incrementado a "+ str(vidaresultado))
        if objetoUsado != None: #si hemos usado objeto
            if objetobueno == True:
                print("Has usado un "+nombreObjeto+". Ha sido efectivo, ganas "+puntosObjeto+" puntos de vida.")
                vidaresultado = vidaresultado + int(puntosObjeto)
                if personaje[2] == monstruoactual[3]: #si nuestra cualidad también coincide, sumamos 20%
                    bonus = 0.2*(int(puntosObjeto)+int(monstruoactual[2]))
                    print("Tu cualidad de "+personaje[2]+" ha sido efectiva, recibes un bonus de "+str(bonus)+" de vida.")
                    vidaresultado = vidaresultado + int(bonus)
            else:# si no es la misma
                print("Has usado un "+nombreObjeto+". Ha sido contraproducente, pierdes "+puntosObjeto+" puntos de vida.")
                vidaresultado = vidaresultado - int(puntosObjeto)
        return vidaresultado, objetobueno
    ################################################################################### SI PERDEMOS
    elif resultado == "perder":
        vidaresultado = vidaresultado - int(monstruoactual[2])
        print("Has perdido contra el " + monstruoactual[1] + ", tu vida se ha reducido a "+ str(vidaresultado))
        # de momento voy a restar el objeto, sea de la cualidad que sea.
        if objetoUsado != None: #si hemos usado objeto, considero que no ha sido beneficioso en ningún caso.
            print("Has usado un "+nombreObjeto+". No ha tenido efecto.")
            #vidaresultado = vidaresultado - int(puntosObjeto)
        
        #si estamos en la sala final, supongo que debemos luchar hasta matar al mostruo final, por lo que perder debe
        #iterar el bucle también
        if salaactual == "FIN":
            resultado = "empate"
            if vidaresultado > 0: #mientras tengamos vida, seguimos luchando.
                input("Aún te quedan fuerzas para luchar. Pulsa intro para intentarlo de nuevo.")
                return vidaresultado, objetobueno
            else:
                return vidaresultado, objetobueno#si nos quedamos sin vida, salimos de la función.
        else:
            return vidaresultado, objetobueno
    return vidaresultado, objetobueno



def animacionLucha(window, canvas, resultadolucha, fotopj, fotomonstruo, textosala, monstruoactual, objetobueno, indiceinventario):
    nombremonstruo = monstruoactual[1]
    cualidadmonstruo = monstruoactual[3]
    objetousado = False
    if indiceinventario != "":
        objetousado = True
        
    def moverfoto(foto,mov):
        canvas.move(foto, mov, 0)
        window.update()

        
    def animacionperder():#mueve el mostruo a la izq y a la derecha.
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotomonstruo,-10)
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotomonstruo,10)
            
    def animacionganar():#mueve el personaje a la der e izq
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotopj,10)
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotopj,-10)
            
    def animacionempate():
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotopj,5)
            moverfoto(fotomonstruo,-5)
        for i in range(1, 35):
            canvas.after(10, None)
            moverfoto(fotopj,-5)
            moverfoto(fotomonstruo,5)
    
    if resultadolucha == "perder":
        print(resultadolucha)
        animacionperder()
        
        textosala.configure(text="Has perdido contra el "+nombremonstruo+". Tu vida se ha reducido a "+str(gpj.personaje[1])
                            +".")
    elif resultadolucha == "ganar":
        animacionganar()
        textofinal = "Has vencido al "+nombremonstruo+". Tu vida se ha incrementado a "+str(gpj.personaje[1])
        if objetousado == True:#si hemos usado objeto
            if objetobueno == True:#si el objeto ha sido eficaz
                textofinal = textofinal +". El objeto usado ha sido eficaz."
                if gpj.personaje[2] ==  cualidadmonstruo:
                    textofinal = textofinal + "Tu cualidad "+gpj.personaje[2]+" también ha sido efectiva."
            else:#si no lo ha sido
                textofinal = textofinal +".El objeto usado ha sido contraproducente."

        textosala.configure(text=textofinal)
    else:
        animacionempate()
        textosala.configure(text="Has empatado con el "+nombremonstruo+". Pulsa el botón para intentarlo de nuevo.")
    
    
    
    
    