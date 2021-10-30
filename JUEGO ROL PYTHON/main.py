import random
import gestionFicheros as gf #alias para llamar a las funciones de cada modulo
import gestionMonstruos as gm

arraysalas = []
arrayambientes = []
arrayobjetos = []
arraymonstruos = []

def randomizarAmbiente(arrayambientes): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice][1]

    

def avanzarMapa(salaactual, arraysalas, arrayambientes, arraymonstruos, monstruopasado):
    resultadosala = [] #devolveré este array de resultados para saber la siguiente sala, si hubo o no hubo monstruo, etc.
    # dado que hay ciertos problemas a la hora de devolverlos por separado.
    
    try:
        salaactual = int(salaactual)
    except ValueError:
        Print("Este mensaje de error no debería aparecer, pero si aparece, significa que la sala actual toma un valor que no es int.")
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
    #digamos que guardaremos la letra de la salida si en su posición no hay un cero.
    for puerta in range( len(arraysalas[salaactual]) -1 ):
        if arraysalas[salaactual][puerta] != "0" and arraysalas[salaactual][puerta] != arraysalas[salaactual][0]:
            salidas.append(arraysalas[0][puerta])
    
    #mostrar mensaje de ambiente
    ambiente = randomizarAmbiente(arrayambientes)
    print(ambiente)
    input("Pulsa intro para dar un paso adelante.")
    print ("")
    
    # aqui calculamos si hay o no un monstruo
    monstruopasado= gm.invocarMonstruo(monstruopasado)
    resultadosala.append(monstruopasado)
   
    
    # una vez que hayamos hecho lo que sea en la sala, vamos a salir.
    print("Tus salidas son "+" ".join(salidas))
    opcion = input("Elige por donde quieres salir ").upper()
    while opcion not in salidas:
        opcion = input("Te chocas con una pared. Elige otra ruta. ").upper()
        
    print("Has abandonado la sala "+arraysalas[salaactual][0]+" por la puerta "+opcion+"...")
    print("")
    #esta función debería devolver cual es la siguiente sala, la cual está almacenada en la posicion de 1 al 4
    #dependiendo de la opcion que escogemos, del subarray que estamos tratando (el de salaactual)
    if opcion == "N":
        resultadosala.append(arraysalas[salaactual][1])
    elif opcion == "S":
        resultadosala.append(arraysalas[salaactual][2])
    elif opcion == "O":
        resultadosala.append(arraysalas[salaactual][3])
    elif opcion == "E":
        resultadosala.append(arraysalas[salaactual][4])
    else:
        print("Este mensaje no debe aparecer nunca.")

    return resultadosala
    #en resultadosala tenemos: [monstruopasado, salaactual]
 
#cargamos en memoria los elementos del juego. Los comentados se cargan desde su propio modulo.
arraysalas = gf.generarMapa()
arrayambientes = gf.generarAmbientes()
arrayobjetos = gf.generarObjetos()
#arraymonstruos = gf.generarMonstruos()

#inicializamos variables que controlarán el estado actual del juego
salaactual = "1"
resultadosala = []
monstruopasado = False #guardamos si hubo un monstruo en la sala anterior
print("Da comienzo la aventura, te encuentras en la sala "+arraysalas[1][0]+".")

while salaactual != "FIN":
    resultadosala = avanzarMapa(salaactual, arraysalas, arrayambientes, arraymonstruos, monstruopasado)
    salaactual = resultadosala[1]
    monstruopasado = resultadosala[0]
    print("Te encuentras en la sala "+salaactual)
print("Has llegado a la sala final")