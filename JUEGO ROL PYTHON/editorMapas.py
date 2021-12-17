"""
a la hora de crear un mapa nuevo, he preferido asegurarme de que el mapa se va creando correctamente paso a paso, en lugar
de dar carta blanca y al final de todo proceder a validarlo. El proceso por el que pasa el usuario es un poco estricto,
pero nos aseguramos de que nunca meta la pata.
"""
import csv

def inputValido(num):
    try:
        num = int(num)
        return True if num >= 0 else False
    except ValueError:
        return False



def crearNuevoMapa():
    siguiente = input("Introduce 1 para ver las instrucciones para crear un mapa nuevo.\n Pulsa intro para empezar a editar")
    if siguiente == "1":
        instrucciones()
    
    nuevomapa = [['1','0','0','0','0']] # el nuevo mapa empieza con la sala 1, sin salidas asignadas
    salasporcrear = ['1'] #guardamos las salas que quedan por crear
    salascreadas = [] # y las ya creadas para que no se creen otras con el mismo nº
    
    #nota importante: para dejar claro el concepto de que una sala está 'creada', la consideramos creada una vez
    #hemos acabado el proceso de asignarle salidas.
    
    while len(salasporcrear) > 0: #mientras queden salas por crear.
        sala = salasporcrear[0] #cogemos la primera sala de las que quedan por crear
        arraysala = []# su subarray y el indice de dicho array también
        indicesala = 0
        c = 0
        for s in nuevomapa:
            if s[0] == sala:
                arraysala = s
                indicesala = c
            c = c + 1
                
        print('Por favor, asigna las salidas de la sala '+sala)
        
        salasporcrear.remove(sala)#la sala que estamos creando la quitamos de salasporcrear
        salascreadas.append(sala)#y la añadimos a salascreadas
        
        #renovamos el array de la sala introduciendo cada salida
        arraysala, salasporcrear, n = asignarSalidas(arraysala, salasporcrear, salascreadas, "norte", 1)
        arraysala, salasporcrear, s = asignarSalidas(arraysala, salasporcrear, salascreadas, "sur", 2)
        arraysala, salasporcrear, o = asignarSalidas(arraysala, salasporcrear, salascreadas, "oeste", 3)
        arraysala, salasporcrear, e = asignarSalidas(arraysala, salasporcrear, salascreadas, "este", 4)
        #recuperamos 3 datos: arraysala porque vamos añadiendo salidas al subarray de la sala que estamos tratando,
        # salasporcrear, porque añadimos ahí los nuevos números de sala utilizados, y el propio número de sala
        #que se asigna a cada salida.
        
        nuevomapa[indicesala] = arraysala #actualizamos el subarray de la sala
        
        """
        ahora bien, debemos crear los arrays (si es necesario) de las nuevas salas con los nuevos números utilizados.
        en dichos arrays se debe respetar la lógica del array que acabamos de crear, es decir
        si hemos creado una salida al norte por ejemplo, en el array de la sala que está al norte debe tener en el
        lado contrario (sur) la sala anterior.
        
        es un poco confuso pero para ello utilizamos la función crearNuevoSubarray, al que le pasamos cada uno de los
        numeros (n,s,o,e) que hemos metido en la sala actual (siempre que no sea un 0). Lo que hace esta función es
        checkear si ese número tiene un subarray dentro del mapa, si no lo tiene, lo crea (con todas las salidas a 0)
        y nos lo devuelve. también devuelve el índice del array nuevomapa en el que debemos meter cada sala.
        
        #una vez creado, insertamos ese nuevo array en el array nuevomapa, y asignamos el valor de la sala en la posición
        #correspondiente. Un ejemplo práctico: queremos crear el siguiente mapa (las líneas son salidas):
        2 - 3
        |   |
        1 - 4
        empezamos por el 1, le ponemos al norte 2 y al este 4, se crean los subarray de la sala 2 y 4, a continuación
        la sala 2, el sur automáticamente es la sala 1, y al este le ponemos la 3 (se crea subarray del 3). Sala 4, al
        oeste tiene la 1, le ponemos el 3 al norte. Finalmente en la sala 3 ya tiene la 2 al oeste y la 4 al sur,
        simplemente nos pedirá si queremos poner algo al norte y este. Si ponemos 0 y 0, ahí se acaba el mapa.
        """
        
        def actualizarNuevoMapa(salida, indice):
            if salida != '0':
                nuevoarray, i = crearNuevoSubarray(nuevomapa, salida)
                if nuevoarray != None:
                    nuevomapa.append(nuevoarray)
                nuevomapa[i][indice] = sala
        
        actualizarNuevoMapa(n, 2) #el indice que le pasamos es la posición del subarray que debemos cambiar,
        actualizarNuevoMapa(s, 1)#1 = norte, 2 = sur, 3 = oeste, 4 = este, es decir, si ponemos una salida al norte(n)
        actualizarNuevoMapa(o, 4)#en la siguiente sala le ponemos esa salida al sur (indice 2)
        actualizarNuevoMapa(e, 3)
        
        print("Este es tu mapa de momento: "+str(nuevomapa))
    #una vez hemos terminado el proceso y no quedan salas por crear.
    
    print("Estas son tus salas creadas:")
    print(salascreadas)
    
    salafin = "-1"
    while salafin not in salascreadas:
        salafin = input("Introduce el número de sala que será la sala final.")
    #recorremos el array y donde ponga el número que hemos elegido, ponemos FIN
    for i in range(len(nuevomapa)):
        for j in range(len(nuevomapa[i])):
            if nuevomapa[i][j] == salafin:
                nuevomapa[i][j] = "FIN"
                
    print("Este es tu mapa final: ")
    print(nuevomapa)

    confirmacion = ""
    while confirmacion != "si" and confirmacion != "no":
        confirmacion = input("¿Quieres guardar el mapa en tus archivos personalizados? (si/no)").lower()
    if confirmacion == "si":
        nuevomapa.insert(0, ['SALA', 'N', 'S', 'O', 'E'])#para respetar la estructura, le ponemos esto como 1º línea.
        guardarMapaPersonalizado(nuevomapa)
    else:
        print("Se ha descartado el mapa.")
    print("")
    
    
def crearNuevoSubarray(nuevomapa, salida):
    creararray = True
    indice = 0
    nuevoarray = None
    #print(nuevomapa)#descomenta el print para ver como se crean los arrays de las nuevas salas.
    for s in range(len(nuevomapa)):
        if nuevomapa[s][0] == salida:
            #si ya existe un subarray con el nº nuevo
            creararray = False
            indice = s
    if creararray == True:
        nuevoarray = [salida, '0', '0', '0', '0']
        indice = len(nuevomapa)
    return nuevoarray, indice

def asignarSalidas(arraysala, salasporcrear, salascreadas, cadinalidad, indice):
    #print(arraysala)#descomenta el print para ver como se va modificando el array de la sala
    salida = "-1"
    if arraysala[indice] == "0":
        
        salidaexistente = True
        #queremos saber si el numero que se mete es de una sala ya creada, en tal caso, no se puede.
        
        while inputValido(salida) == False or salidaexistente == True: #solo admitimos nº de 0 en adelante.
            salida = input("Salida por el "+cadinalidad+": ")
            if salida not in salascreadas:
                salidaexistente = False
            else:
                print("No puedes volver a utilizar ese nº de sala. Escoge otro.")

        arraysala[indice] = salida
        
        salanueva = False
        if salida not in salasporcrear:
            salanueva = True
            
        if salanueva == True and salida != "0":
            salasporcrear.append(salida)
    if salida == "-1":#como hemos inicializado la salida con un -1, si no la hemos asignado, queremos que sea 0.
        salida = "0"
    return arraysala, salasporcrear, salida
            


    
def guardarMapaPersonalizado(nuevomapa):
    mapas = open('./custom/mapa.txt','w', newline='', encoding='utf-8')
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ';')
        csvescrito.writerows(nuevomapa)
    mapas.close()
    print("Se ha guardado el mapa en /custom/mapa.txt")
    


def instrucciones():
    print("""
-Para crear un mapa, debes crear sala por sala, asignándole a cada sala entre 1 y 4 salidas (N S O E).
Empezarás por la sala 1, se te pedirá que asignes las salidas, siempre en el orden que hemos señalado. Para
asignar o crear una salida, escribe un número entero positivo, si no quieres crear una salida, introduce un 0.

-El número que introduzcas en cada salida será la sala con la que se conecta dicha salida. Por ejemplo, si
a la sala 1 le asignas 2, 3, 0, y 5, quiere decir que por el norte se sale a la sala 2, por el sur a la 3 y
por el este a la 5 (no hay salida al oeste).

-Los números que identifican a cada sala se dejan a tu elección, pero ten encuenta que tendrás que crear tantas salas
como números distintos introduzcas en las salidas. En nuestro ejemplo, deberías crear como mínimo las salas 2, 3 y 5.
Además, se te pedirá en el orden en el que vas usando esos números.

-El editor te seguirá pidiendo que crees cada sala hasta que no introduzcas ningún número nuevo.
La lógica del mapa queda a tu elección, podrías una sala con dos salidas que den a la misma sala,
La única regla es que todas queden conectadas al final.

-Cuando termines, se te pedirá que conviertas una de las salas en sala final. Puedes escoger cualquiera de las
que has creado, incluso la sala 1.

-Como último detalle, no se te pedirá que crees las salidas que vienen de otras salas que ya hay previamente.
Es decir, si la sala 1 tiene la sala 2 al norte, automáticamente se asume que la sala 2 tiene a la sala 1 al sur.
""")
    input("Pulsa intro para empezar.")

