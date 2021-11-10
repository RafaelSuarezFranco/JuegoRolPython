import gestionPartidas as gp
import gestionFicheros as gf

def menuPrincipal():
    menuopcion = ""

    while menuopcion != "6":
        print("MENÚ PRINCIPAL")
        print("1 - Nueva Partida")
        print("2 - Cargar Partida")
        print("6 - Salir del juego")
        menuopcion = input("Introduce una opción")
        if menuopcion == "1":
            gp.nuevaPartida(None)
        elif menuopcion == "2":
            gp.nuevaPartida( gf.elegirPartidaGuardada())
            
menuPrincipal()
