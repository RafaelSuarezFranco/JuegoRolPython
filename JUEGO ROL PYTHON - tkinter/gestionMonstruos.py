import random
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
    
    bonusastucia = 12 if gpj.personaje[2] == "ASTUCIA" else 0 #bonus de la habilidad de astucia
        #si el pj tiene la habilidad de ASTUCIA, reduce la probabilidad de encontrar monstruo
    
    if monstruopasado == False: #si no hubo monstruo en la sala anterior
        hayMonstruo = probalilidad(75 + (dificultad * 5) - bonusastucia )
    else: # la dificultad hace un 5% más o menos probable que hayan monstruos.
        hayMonstruo = probalilidad(66 + (dificultad * 5) - bonusastucia )
    
    if salaactual == "FIN": #si es la sala final, debe haber monstruo
        hayMonstruo = True
    
    monstruoactual = ""
    if hayMonstruo == True:
        monstruopasado = True
        monstruoactual = randomizarMonstruo() #en monstruo actual se almacena una línea del fichero de monstruos
    else:
        monstruopasado = False
    return monstruopasado, monstruoactual


def lucha(elementosVentana, monstruoactual, indiceinventario, salaactual, dificultad):
    
    objetoUsado = None #controla si se usa o no se usa objeto. en este caso el indice de objeto viene dado de fuera.
    objetoLucha = ["", "", ""] #guarda el objeto que se usa para luchar.
    if indiceinventario != "":
        index = int(indiceinventario)-1 # estos unos son para reajustar el índice y objeto escogido, dado que en el combobox se usa fórmula distinta
        objetoUsado = gpj.inventario[index]-1
        objetoLucha = [go.arrayobjetos[objetoUsado][1], go.arrayobjetos[objetoUsado][2], go.arrayobjetos[objetoUsado][3]]
        #contiene nombre, cualidad y puntos del objeto.
        gpj.inventario.pop(index)
    
    #tendremos una variable para saber la vida que le queda al pj despues del encuentro.
    vidaresultado = gpj.personaje[1]
    resultadolucha = "empate"
    objetobueno = False
    
    while resultadolucha == "empate" or (resultadolucha != "ganar" and salaactual == "FIN" and vidaresultado > 0):
        # repetimos hasta que una de las partes gane
        # si es sala final, repetimos hasta que ganemos o muramos.
        
        bonuslucha = 3 if gpj.personaje[2] == "LUCHA" else 0 #bonus de la habilidad de lucha
        #si el pj tiene la habilidad de LUCHA, aumenta el máximo de sus dados
        bonusobjetolucha= 4 if objetoLucha[1] == "LUCHA" else 0 
        #si usamos un objeto de LUCHA, aumenta el mínimo de nuestros dados
        
        #hacemos 3 tiradas y las guardamos ordenadas
        r1 = []
        for i in range(0, 3):
            r1.append(random.randint(1 + bonusobjetolucha, 20 + bonuslucha))
        r1 = sorted(r1, key=int, reverse=True)
        
        dadoenemigolucha = 1 if monstruoactual[3] == "LUCHA" else 0 #si el monstruo es de LUCHA, tiene un dado más
        
        r2 = [] #dos tiradas para el enemigo (3 si es de lucha), las guardamos ordenadas.
        for i in range(0, 2 + dadoenemigolucha):    
            r2.append(random.randint(1, 25 + (dificultad * 5)))
            #la dificultad aumenta o disminuye las probabilidades de ganar del monstruo.   
        r2 = sorted(r2, key=int, reverse=True)
        
    
        #posibles resultados:
        #si ambos nº del pj pasan los del enemigo, ganamos, si uno lo sobrepasa y el otro es igual, ganamos
        #si uno lo sobrepasa y el otro queda por debajo, empate. si ambos nº son iguales a los del enemigo, empate
        #si uno de los nº esta por debajo y el otro también o empata, perdemos
    
        if (r1[0] == r2[0] and r1[1] == r2[1]) or (r1[0] > r2[0] and r1[1] < r2[1]) or (r1[0] < r2[0] and r1[1] > r2[1]):
            resultadolucha = "empate"
            
            if objetoLucha[1] == "ASTUCIA":#si usamos un objeto de ASTUCIA, convierte el empate en victoria.
                resultadolucha = "ganar"
            
        elif (r1[0] > r2[0] and r1[1] > r2[1]) or (r1[0] > r2[0] and r1[1] == r2[1]) or (r1[0] == r2[0] and r1[1] > r2[1]):
            resultadolucha = "ganar"
            
        else:
            resultadolucha = "perder"
        vidaresultado, objetobueno = resultadoDeLuchar(resultadolucha, vidaresultado, monstruoactual,
                                                       objetoUsado, objetoLucha, salaactual)
        animacionLucha(elementosVentana, vidaresultado, resultadolucha, monstruoactual, objetobueno, indiceinventario)
    
    gpj.personaje[1] = vidaresultado



def resultadoDeLuchar(resultado, vidaresultado, monstruoactual, objetoUsado, objetoLucha, salaactual):
    nombreObjeto = ""
    cualidadObjeto = ""
    puntosObjeto = ""
    if objetoUsado != None:
        nombreObjeto = objetoLucha[0]
        cualidadObjeto = objetoLucha[1]
        puntosObjeto = objetoLucha[2]
        
    objetobueno = False
    if cualidadObjeto == monstruoactual[3]: #guardamos esta variable para saber si el objeto ha sido efectivo.
        objetobueno = True
        
    #recalculamos la vida del pj dependiendo del resultado y del objeto
    ########################################################################################## SI GANAMOS
    if resultado == "ganar" and objetoUsado == None:#######si hemos ganado sin objeto
        vidaresultado = vidaresultado + int(monstruoactual[2])
        return vidaresultado, objetobueno
    
    elif resultado == "ganar" and objetoUsado != None: #######si hemos ganado con objeto
        vidaresultado = vidaresultado + int(monstruoactual[2])
        if objetobueno == True:#si las cualidades coindicieron
            vidaresultado = vidaresultado + int(puntosObjeto)
            
            if gpj.personaje[2] == monstruoactual[3]: #si nuestra cualidad también coincide, sumamos 20%
                bonus = 0.2*(int(puntosObjeto)+int(monstruoactual[2]))
                vidaresultado = vidaresultado + int(bonus)
                
        else:#si las cualidades no coindicieron
            vidaresultado = vidaresultado - int(puntosObjeto)
        return vidaresultado, objetobueno
    ################################################################################### SI PERDEMOS
    elif resultado == "perder":
        
        bonusenemigomagia = 1.3 if monstruoactual[3] == "MAGIA" else 1
        #si el monstruo es de MAGIA, inglige % adicional
        bonusobjetomagia  = 0.5 if cualidadObjeto == "MAGIA" else 1
        #si usamos un objeto de MAGIA, reduce un 50% el daño si perdemos.
        
        vidaresultado = int(vidaresultado - int(monstruoactual[2]) * bonusenemigomagia * bonusobjetomagia)
        
        if monstruoactual[3] == "ASTUCIA": #si el monstruo es de ASTUCIA, nos roba un objeto.
            if len(gpj.inventario) > 0: #si tenemos alguno, obviamente.
                gpj.inventario.pop(0)
        
        #if objetoUsado != None: #si hemos usado objeto, considero que no ha sido beneficioso en ningún caso.
        #    print("Has usado un "+nombreObjeto+". No ha tenido efecto.")
        return vidaresultado, objetobueno

    else: ##################################################################################SI EMPATAMOS
        return vidaresultado, objetobueno



def animacionLucha(elementosVentana, vidaresultado, resultadolucha, monstruoactual, objetobueno, indiceinventario):
    window, canvas, textosala, fotopj, fotomonstruo = elementosVentana
    
    nombremonstruo = monstruoactual[1]
    cualidadmonstruo = monstruoactual[3]
    objetousado = False
    if indiceinventario != "":
        objetousado = True
        
    def moverfoto(foto,mov):
        canvas.after(10, None)
        canvas.move(foto, mov, 0)
        window.update()
        
    def animacionperder():#mueve el mostruo a la izq y a la derecha.
        for i in range(1, 35):
            moverfoto(fotomonstruo,-10)
        for i in range(1, 35):
            moverfoto(fotomonstruo,10)
            
    def animacionganar():#mueve el personaje a la der e izq
        for i in range(1, 35):
            moverfoto(fotopj,10)
        for i in range(1, 35):
            moverfoto(fotopj,-10)
            
    def animacionempate():
        for i in range(1, 17):
            moverfoto(fotopj,9)
            moverfoto(fotomonstruo,-9)
        for i in range(1, 17):
            moverfoto(fotopj,-9)
            moverfoto(fotomonstruo,9)
    
    if resultadolucha == "perder":
        animacionperder()
        textosala.configure(text="Has perdido contra el "+nombremonstruo+
                            ". Tu vida se ha reducido a "+str(vidaresultado)+".")
        
    elif resultadolucha == "ganar":
        animacionganar()
        
        textofinal = "Has vencido al "+nombremonstruo+"."
        if objetousado == True:#si hemos usado objeto
            if objetobueno == True:#si el objeto ha sido eficaz
                textofinal = textofinal +" El objeto usado ha sido eficaz."
                if gpj.personaje[2] ==  cualidadmonstruo:#si además nuestra habilidad coincide
                    textofinal = textofinal + " Tu cualidad "+gpj.personaje[2]+" también ha sido efectiva."
            else:#si no ha sido bueno
                textofinal = textofinal +" El objeto usado ha sido contraproducente."

        textosala.configure(text=textofinal+" Tu vida se ha incrementado a "+str(vidaresultado)+".")
    else:#si empatamos
        textosala.configure(text="La pelea contra el "+nombremonstruo+" está igualada...")
        animacionempate()
    
