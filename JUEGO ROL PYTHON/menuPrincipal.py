import gestionPartidas as gp
import gestionFicheros as gf
import editorMapas as em
import editorArchivos as ea

def menuPrincipal():
    menuopcion = ""
    print("Bienvenido a la Mazmorra Azarosa, por Rafael Suárez Franco.")
    while menuopcion != "5":
        print("")
        print("MENÚ PRINCIPAL")
        print("1 - Nueva Partida")
        print("2 - Cargar Partida")
        print("3 - Borrar Partida")
        print("4 - Editor de archivos")
        print("5 - Salir del juego")
        menuopcion = input("Introduce una opción")
        if menuopcion == "1":
            gp.nuevaPartida( None )
        elif menuopcion == "2":
            gp.nuevaPartida( gf.elegirPartidaGuardada() )
        elif menuopcion == "3":
            gf.borrarPartida()
        elif menuopcion == "4":
            submenuEditores()

def submenuEditores():
    opcion = ""
    while opcion != "5":
        print("")
        print("EDITOR DE ARCHIVOS")
        print("1 - Editar mapa")
        print("2 - Editar ambientes")
        print("3 - Editar monstruos")
        print("4 - Editar objetos")
        print("5 - Volver al menú principal")
        opcion = input("Introduce una opción")
        
        if opcion == "1":
            em.crearNuevoMapa()
        elif opcion == "2":
            ea.editarAmbientes()
        elif opcion == "3":
            ea.editarMonstruoObjeto("monstruo")
        elif opcion == "4":
            ea.editarMonstruoObjeto("objeto")