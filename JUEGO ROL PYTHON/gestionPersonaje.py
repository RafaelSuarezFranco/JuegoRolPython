import random

personaje = []
#el personaje e inventario se guardarán como una listas globales a las que hay que llamar desde este módulo.
inventario = []

def crearPersonaje():
    personaje = []
    print("Vamos a crear tu personaje")
    nombre = input("Nombre de tu personaje: ")
    while nombre == "":
        nombre = input("¿Crees que te voy a dejar avanzar sin que escribas un nombre?")

    vidarand = random.randint(0, 100)
    vida = 100 + vidarand
    print("Los dioses te han condedido "+str(vida)+" puntos de vida.")

    habilidad = input("Elige tu habilidad: 1 - Lucha. 2 - Magia. 3 - Astucia")
    while habilidad != "1" and habilidad != "2" and habilidad != "3":
        habilidad = input("No es tan difícil. Escribe 1, 2, o 3.")
    if habilidad == "1":
        habilidad = "LUCHA"
    elif habilidad == "2":
        habilidad = "MAGIA"
    else:
        habilidad = "ASTUCIA"
        
    personaje.extend((nombre, vida, habilidad))
    return personaje

def mostrarPersonaje():
    print("Estado actual de tu personaje:")
    print("Nombre: " + personaje[0])
    print("Vida: " + str(personaje[1]))
    print("Habilidad: " + personaje[2])