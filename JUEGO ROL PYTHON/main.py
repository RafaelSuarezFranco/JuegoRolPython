import random
import gestionFicheros as gf #alias para llamar a las funciones de ficheros.

arraysalas = []
arrayambientes = []
arrayobjetos = []

def randomizarAmbiente(arrayambientes): #Devuelve una cadena de ambiente aleatoria.
    numAleatorio = random.randint(1, len(arrayambientes))
    for indice in range( len(arrayambientes) ):
        if arrayambientes[indice][0] == str(numAleatorio):
            return arrayambientes[indice][1]



def avanzarMapa(salaactual, arraysalas, arrayambientes):
    try:
        salaactual = int(salaactual)
    except ValueError:
        Print("Este mensaje de error no debería aparecer, pero si aparece, significa que la sala actual toma un valor que no es int.")
    salidas = []#estas serán las salidas posibles, puede contener N S O E
    
    #digamos que guardaremos la letra de la salida si en su posición no hay un cero.
    for puerta in range( len(arraysalas[salaactual]) -1 ):
        if arraysalas[salaactual][puerta] != "0" and arraysalas[salaactual][puerta] != arraysalas[salaactual][0]:
            salidas.append(arraysalas[0][puerta])
    
    ambiente = randomizarAmbiente(arrayambientes)
    print(ambiente)
    input("Pulsa intro para dar un paso adelante.")
    
    print("Tus salidas son "+" ".join(salidas))
    opcion = input("Elige por donde quieres salir ").upper()
    while opcion not in salidas:
        opcion = input("Te chocas con una pared. Elige otra ruta. ").upper()
        
    print("Has abandonado la sala "+arraysalas[salaactual][0]+" por la puerta "+opcion+"...")
    #esta función debería devolver cual es la siguiente sala, la cual está almacenada en la posicion de N del subarray 1
    if opcion == "N":
        return arraysalas[salaactual][1]
    elif opcion == "S":
        return arraysalas[salaactual][2]
    elif opcion == "O":
        return arraysalas[salaactual][3]
    elif opcion == "E":
        return arraysalas[salaactual][4]
    else:
        print("Este mensaje no debe aparecer nunca.")

    
arraysalas = gf.generarMapa()
arrayambientes = gf.generarAmbientes()
arrayobjetos = gf.generarObjetos()
#queremos ver qué sala hay al norte de la sala 1? podemos usar lo siguente:
#print("La sala al norte de la sala 1 es la sala "+arraysalas[1][1])
salaactual = "1"
print("Da comienzo la aventura, te encuentras en la sala "+arraysalas[1][0]+".")
#print("No pienses que el camino que te espera será tan pacífico como esta sala.")

while salaactual != "FIN":
    salaactual = avanzarMapa(salaactual, arraysalas, arrayambientes)
    print("Te encuentras en la sala "+salaactual)
print("Has llegado a la sala final")