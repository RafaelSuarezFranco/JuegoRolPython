import gestionPartidas as gp
import gestionFicheros as gf
from tkinter import *
import gestionPantalla as cp

def menuPrincipal():
    ventana = Tk()
    ventana.title('JUEGO ROL PYTHON - VERSIÓN TKINTER')
    cp.centrarPantalla(350, 500, ventana)
    cp.deshabilitarX(ventana)
    ventana.resizable(False, False)
    imagenfondo = PhotoImage(file="./pictures/menuppal.png")    
    # crear un canvas para poner la foto de fondo y otras fotos encima.
    frame = Frame(ventana)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(200,180,image=imagenfondo)
    canvas.pack()
    canvas.create_text(238,18,text='MENÚ PRINCIPAL', fill='black', font=('freemono', 20, 'bold'))
    canvas.create_text(240,20,text='MENÚ PRINCIPAL', fill='white', font=('freemono', 20, 'bold'))

    def botonnueva():
        ventana.destroy()
        gp.nuevaPartida(None)
    
    def botoncargar():
        ventana.destroy()
        gf.pantallaCargarPartida()
        
    def descripcion():
        ventana.destroy()
        ventanaInfo()

    botonnueva = Button(ventana, text="Nueva Partida", command=botonnueva)
    botonnueva.place(x=10, y=280)

    botoncargar = Button(ventana, text="Cargar Partida", command=botoncargar)
    botoncargar.place(x=105, y=280)
    
    botonimportar = Button(ventana, text="Importar mapa personalizado", command=gf.importarCustom)
    botonimportar.place(x=10, y=315)
    
    botondescripcion = Button(ventana, text="Información extra", command=descripcion)
    botondescripcion.place(x=190, y=315)
    
    botonsalir = Button(ventana, text="Salir", command=exit)
    botonsalir.place(x=450, y=315)

    ventana.mainloop()
    

infoobjeto = """
    Para entender el juego un poco mejor:
    
    Los objetos, monstruos y el personaje tienen una habilidad (entre
    LUCHA, MAGIA y ASTUCIA). Utilizar un objeto contra un monstruo es
    una apuesta, ya que en principio no sabemos qué habilidades poseen.
    
    Si ganamos a un monstruo utilizando un objeto, este nos otorgará
    un bonus de vida si su habilidad coindice con la del monstruo. Si no
    coindice, nos restará ese bonus. Si perdemos, ni suma ni resta. Si
    obtenemos dicho bonus y la habilidad de nuestro personaje coincide
    también, obtenemos un bonus mayor.
    """
infohabilidades = """
    Ahora bien, dichas habilidades aportan ciertas características
    (independientemente de que coincidan o no).
    
    Personaje:
    - LUCHA: aumenta probabilidades de ganar el combate.
    - MAGIA: aumenta la vida inicial.
    - ASTUCIA: reduce probabilidad de encontrar un monstruo.
    Monstruo:
    - LUCHA: aumenta probabilidades del monstruo ganar el combate.
    - MAGIA: monstruo inflige daño adicional si nos derrota.
    - ASTUCIA: el monstruo nos roba un objeto si nos derrota.
    Objeto:
    - LUCHA: aumenta probabilidades de ganar el combate.
    - MAGIA: reduce el daño recibido si perdemos.
    - ASTUCIA: si se produce un empate, ganamos automáticamente.
    """
infocombate = """
    En cuanto a los combates:
    
    El combate está basado en RNG, el cuál está influido por
    las habilidades de las partes implicadas como hemos dicho,
    además de la dificultad.
    
    Si somos derrotados en una sala normal, podemos continuar
    mientras tengamos vida. Si empatamos, se repite la lucha
    hasta que salga un resultado que no sea empate.
    
    Si nos encontramos en la sala final, debemos ganar al monstruo
    final. Si perdemos, se repetirá la lucha hasta que ganemos
    o nos quedemos sin vida.
    """

def ventanaInfo():   
    ventana = Tk()
    ventana.title('Información del juego')
    cp.centrarPantalla(350, 500, ventana)
    cp.deshabilitarX(ventana)
    ventana.resizable(False, False)
    imagenfondo = PhotoImage(file="./pictures/informacion.png")    
    frame = Frame(ventana)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(150,150,image=imagenfondo)
    canvas.pack()
    canvas.create_text(240,20,text='Información de extra del juego', fill='white', font=('freemono', 20, 'bold'))
    info = canvas.create_text(240,180,text=infoobjeto, fill='white', font=('freemono', 10, 'bold'))

    def siguiente():
        if botoninfo.counter == 1:
            canvas.itemconfigure(info, text=infohabilidades)
            botoninfo.counter = 2
        elif botoninfo.counter == 2:
            canvas.itemconfigure(info, text=infocombate)
            botoninfo.counter = 3
        elif botoninfo.counter == 3:
            canvas.itemconfigure(info, text=infoobjeto)
            botoninfo.counter = 1 
    
    botoninfo = Button(ventana, text="Siguiente", command=siguiente)
    botoninfo.counter = 1
    botoninfo.place(x=200, y=315)
    
    def atras():
        ventana.destroy()
        menuPrincipal()
    
    botonatras = Button(ventana, text="Volver al menú", command=atras)
    botonatras.place(x=380, y=315)
    
    ventana.mainloop()
    