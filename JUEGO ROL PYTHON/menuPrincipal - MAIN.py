import gestionPartidas as gp
import gestionFicheros as gf
import editorMapas as em

def menuPrincipal():
    menuopcion = ""
    print("BIENVENIDO AL JUEGO ROL EN PYTHON, por Rafael Suárez Franco.")
    while menuopcion != "6":
        print("MENÚ PRINCIPAL")
        print("1 - Nueva Partida")
        print("2 - Cargar Partida")
        print("3 - Editor de mapas")
        print("6 - Salir del juego")
        menuopcion = input("Introduce una opción")
        if menuopcion == "1":
            gp.nuevaPartida( None )
        elif menuopcion == "2":
            gp.nuevaPartida( gf.elegirPartidaGuardada() )
        elif menuopcion == "3":
            em.crearNuevoMapa()
menuPrincipal()
