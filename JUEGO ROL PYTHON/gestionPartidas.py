import gestionFicheros as gf
import gestionMonstruos as gm
import gestionObjetos as go
import gestionSalas as gs
import gestionPersonaje as gpj

def nuevaPartida(partida): #le pasamos la partida cargada (si es nueva partida, le pasamos None)
    
    #vaciamos el inventario, si jugamos varias partidas en al misma sesión, es necesario.
    gpj.inventario = []
            
    if partida == None:###################################################### SI LA PARTIDA ES COMPLETAMENTE NUEVA
        gf.opcion = gf.elegirArchivos() #controla si usamos archivos default o custom
        
        #inicializamos variables que controlarán el estado actual del juego
        gpj.personaje = gpj.crearPersonaje()
        dificultad = elegirDificultad()
        salaactual = "1"
        resultadosala = []
        monstruopasado = False #guardamos si hubo un monstruo en la sala anterior
        gs.arraysalas = gf.generarArray("mapa")
        print("Da comienzo la aventura, te encuentras en la sala 1.")
        print("La mazmorra en la que te encuentras es inestable y colapsa a medida que la recorres.")
        print("Cada sala por la que pases se derrumbará y no podrás volver sobre tus pasos. Elige bien a dónde vas.")
        input("Pulsa intro para empezar...")
        
    else: ################# SI LA PARTIDA ES CARGADA, INICILIZAMOS LAS VARIABLES CON LA PARTIDA QUE HEMOS PASADO
        gf.opcion = partida[3] # default o custom guardado en partida[3]
        gpj.personaje = [partida[0], int(partida[1]), partida[2]]
        
        dificultad = 0
        if partida[4] == "facil":
            dificultad = -1
        elif partida[4] == "dificil":
            dificultad = 1
            
        gpj.inventario = eval(partida[7])#casteamos el inventario guardado a array
        
        salaactual = partida[5]
        resultadosala = []
        monstruopasado = True
        if partida[6] == "False":#el monstruo pasado está guardado como string.
            monstruopasado = False
        input("Partida cargada con éxito. Pulsa intro para continuar...")
    ######################################################################### UNA VEZ SE HA CREADO O CARGADO PARTIDA
        
    #cargamos en memoria los elementos del juego. cada array se guarda en una variable global del modulo correspondiente.
    #gs.arraysalas = gf.generarMapa()
    gs.arrayambientes = gf.generarArray("ambientes")
    go.arrayobjetos = gf.generarArray("objetos")
    gm.arraymonstruos = gf.generarArray("monstruos")

    """
    Acerca del array de salas: como el tema sobre no volver a una sala anterior queda un poco a criterio del diseñador, lo
    que he dedidido es que cada sala por la que pasemos se vaya borrando de dicho array, como si el mapa se fuera destruyendo
    a medida que avanzamos. Esto implica que si nos encontramos en un callejón sin salida, el juego se da por perdido.
    """
    
    
    #avanzamos por las salas mientras que no llegemos a la sala FIN o la sala actual valga -1, que significa que estamos
    #en un callejón sin salida.
    while salaactual != "FIN" and salaactual != "-1" and salaactual !="guardar y salir" and gpj.personaje[1] > 0:
        resultadosala = gs.avanzarMapa(salaactual, monstruopasado, dificultad)
        salaactual = resultadosala[1]
        monstruopasado = resultadosala[0]
        if salaactual != "-1" and salaactual != "guardar y salir":
            print("Te encuentras en la sala "+salaactual)
        #si hemos seleccionado guardar partida y salir, salaactual recoge el valor 'guardar y salir'
        #nos indica que debemos salir del juego (romper este bucle)
           
    if salaactual == "FIN":
        print("Has llegado a la sala final")
        resultadosala = gs.avanzarMapa(salaactual, monstruopasado, dificultad)

        

#dificultad afecta a la probabilidad de encontrar objetos, de generar un monstruo, a los dados del monstruo y a la
#penalización por huir de un monstruo.
def elegirDificultad():
    dificultad = ""
    while dificultad != "1" and dificultad != "2" and dificultad != "3":
        print("Elige la dificultad:")
        print("1 - Fácil")
        print("2 - Normal")
        print("3 - Difícil")
        dificultad = input("")
    if dificultad == "1":
        dificultad = -1
    elif dificultad == "2":
        dificultad = 0
    else:
        dificultad = 1
    #aunque pedimos del 1 al 3, me interesa guardar un entero que sea -1, 0, o 1, ya la dificultad será un multiplicador
    #de ciertos parámetros del juego. El 0 será normal, es decir, no influirá, es la dificultad base del juego, mientras
    # que el -1 y el 1 sumarán o restarán a ciertos parámetros para hacer más fácil o difícil el juego.
    return dificultad
            
        