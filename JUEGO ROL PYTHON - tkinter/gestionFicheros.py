import csv
import gestionPersonaje as gpj
import gestionSalas as gs
from tkinter import *
import gestionPantalla as cp
import menuPrincipal as mp
import gestionPartidas as gp
import os
import shutil

opcion = "default" #variable global para saber si la partida que vamos a jugar usa archivos default o custom
# esta variable se rescribe cada vez que iniciamos partida o cargamos partida,
#a su vez, deben rescribirse todos los arrays (en nueva partida)

def elegirArchivos():
    #sirve para elegir la opción a través de una pantalla
    ventana = Tk()
    ventana.title('Elegir mapa')
    cp.centrarPantalla(200, 400, ventana)
    cp.deshabilitarX(ventana)
    ventana.resizable(False, False)
    imagenfondo = PhotoImage(file="./pictures/mapaselect.png")    
    frame = Frame(ventana)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(300,180,image=imagenfondo)
    canvas.pack()
    canvas.create_text(200,30,text='Elige un mapa para la nueva partida', fill='white', font=('freemono', 15, 'bold'))
    
    def seleccionar(op):
        global opcion
        opcion = op
        ventana.destroy()

    Button(ventana, text="Mapa por defecto", command=lambda: seleccionar("default")).place(x=70, y=100)
    Button(ventana, text="Mapa personalizado", command=lambda: seleccionar("custom")).place(x=230, y=100)
    
    ventana.mainloop()



#FUNCIONES DE CARGAR DATOS, PARA NUEVA PARTIDA.
def generarMapa():
    archivoSalas = open('./'+opcion+'/mapa.txt', "r",encoding="utf-8")
    salas = csv.reader(archivoSalas, delimiter = ';')
    arraysalas = list(salas)
    return arraysalas

def generarAmbientes():
    archivoAmbiente = open('./'+opcion+'/ambientes.txt', "r",encoding="utf-8")
    ambientes = csv.reader(archivoAmbiente, delimiter = ';')
    arrayambientes = list(ambientes)
    return arrayambientes

def generarObjetos():
    archivoObjeto = open('./'+opcion+'/objetos.txt', "r",encoding="utf-8")
    objetos = csv.reader(archivoObjeto, delimiter = ';')
    arrayobjetos = list(objetos)
    return arrayobjetos

def generarMonstruos():
    archivoMonstruo = open('./'+opcion+'/monstruos.txt', "r",encoding="utf-8")
    monstruos = csv.reader(archivoMonstruo, delimiter = ';')
    arraymonstruos = list(monstruos)
    return arraymonstruos

#FUNCIONES DE GUARDAR
def guardarPartida(salaactual, monstruopasado, dificultad):
    partidas = open("partidasGuardadas.txt",'a', newline='', encoding='utf-8')
    if dificultad == 0:
        dificultad = "normal"
    elif dificultad == 1:
        dificultad = "dificil"
    elif dificultad == -1:
        dificultad = "facil"  
    #en la partida guardaré la cantidad de objetos también, para saber cuántos hay.
    datosGuardados = [gpj.personaje[0], str(gpj.personaje[1]), gpj.personaje[2], opcion, str(dificultad), str(salaactual),
                      str(monstruopasado), str(len(gpj.inventario))]
    for objeto in gpj.inventario:
        datosGuardados.append(str(objeto))
    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerow(datosGuardados)
    partidas.close()
    
def guardarMapa():
    mapas = open("mapasGuardados.txt",'a', newline='', encoding='utf-8')
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ',')
        csvescrito.writerow(gs.arraysalas)
    mapas.close()
        

#FUNCIONES DE CARGAR PARTIDA GUARDADA
def pantallaCargarPartida():
    ficheropartidas = open("partidasGuardadas.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    
    ventana = Tk()
    ventana.title('Cargar Partida')
    cp.centrarPantalla(350, 550, ventana)
    cp.deshabilitarX(ventana)
    ventana.resizable(False, False)
    imagenfondo = PhotoImage(file="./pictures/cargapartida.png")    
    frame = Frame(ventana)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=700, height=400)
    canvas.create_image(300,180,image=imagenfondo)
    canvas.pack()
    canvas.create_text(268,18,text='Cargar Partida', fill='black', font=('freemono', 20, 'bold'))
    canvas.create_text(270,20,text='Cargar Partida', fill='white', font=('freemono', 20, 'bold'))
    # listbox de partidas guardadas. muestra 15 a la vez, es scrollable.

    partidas = Listbox ( ventana, width=85, height=15)
    refrescarLista(partidas, arraypartidas)

    partidas.place(x=20, y=60)
    
    def cargarseleccion():
        try:
            indicepartida =  int(partidas.curselection()[0]) + 1
            #guardamos el indice de partida para saber que línea de los archivos coger.
            messagebox.showinfo(message="Partida cargada con éxito.", title="Atención")
            ventana.destroy()
        
            gs.arraysalas = cargarMapa(indicepartida)
            gp.nuevaPartida(arraypartidas[indicepartida])
            #a la funcion nuevaPartida le pasamos la partida correspondiente guardada en ese array
        except Exception:
            messagebox.showerror(message="Escoge una partida para cargarla.", title="Error")
        
    btncargar = Button(ventana, text="Cargar", command=cargarseleccion).place(x=60, y=320)
    
    def atras():
        ventana.destroy()
        mp.menuPrincipal()
    btnatras = Button(ventana, text="Atrás", command=atras).place(x=460, y=320)
    
    def borrar():
        try:
            indicepartida =  int(partidas.curselection()[0]) + 1
            #guardamos el indice de partida para saber que línea de los archivos borrar
            borrarPartida(indicepartida)
            arraypartidas.pop(indicepartida)
            messagebox.showinfo(message="Partida borrada con éxito.", title="Atención")
            #borramos la partida seleccionada y actualizamos la lista
            refrescarLista(partidas, arraypartidas)
        except Exception:
            messagebox.showerror(message="Escoge una partida para borrarla.", title="Error")
        
        
    btnborrar = Button(ventana, text="Borrar", command=borrar).place(x=260, y=320)
    
    ventana.mainloop()


def refrescarLista(listbox, arraypartidas):
    listbox.delete(0, END)
    for i in range(1, len(arraypartidas)):
        p = arraypartidas[i] #guardamos cada partida para mostrar algo de info de cada una de ellas en la lista.
        textopartida = "Partida: {} | Nombre: {} - Vida: {} - Habilidad: {} - Dificultad: {} - Sala actual: {} ".format(
            i, p[0],p[1],p[2],p[4],p[5])#formateamos un poco para que quede bien.
        listbox.insert(i, textopartida)


    
def cargarMapa(indice):#carga el mapa guardado en la misma posicion de la partida.
    ficheromapas = open("mapasGuardados.txt",'r', encoding='utf-8')   
    mapasguardados = csv.reader(ficheromapas, delimiter = ',')
    arraymapas = list(mapasguardados)
    arrayfinal = []
    #tal como guardo los mapas (el mapa entero en una linea) cada subarray se guarda como cadena, por lo tanto
    #al recuperarlo aqui, tengo que hacerle un eval a cada string para convertirlo en array.
    for i in range(0, len(arraymapas[indice])):
        array = eval(arraymapas[indice][i])
        arrayfinal.append(array)
    
    return arrayfinal


#FUNCIÓN DE BORRAR PARTIDA
def borrarPartida(indicepartida):
    #igual que la de la versión texto, pero se le pasa el índice desde fuera, elegido en la lista.
    ficheropartidas = open("partidasGuardadas.txt",'r', encoding='utf-8')   
    partidasguardadas = csv.reader(ficheropartidas, delimiter = ';')
    arraypartidas = list(partidasguardadas)
    
    ficheromapas = open("mapasGuardados.txt",'r', encoding='utf-8')   
    mapasguardados = csv.reader(ficheromapas, delimiter = ',')
    arraymapas = list(mapasguardados)

    arraypartidas.pop(indicepartida) #borramos la línea en partidas y mapas guardados.
    arraymapas.pop(indicepartida)
        
    partidas = open("partidasGuardadas.txt",'w', newline='', encoding='utf-8')#rescribir partidas
    with partidas:
        csvescrito = csv.writer(partidas,delimiter = ';')
        csvescrito.writerows(arraypartidas)
    partidas.close()
    
    mapas = open("mapasGuardados.txt",'w', newline='', encoding='utf-8')#reescribir mapas.
    with mapas:
        csvescrito = csv.writer(mapas,delimiter = ',')
        csvescrito.writerows(arraymapas)
    mapas.close()



def importarCustom():
    #permite importar el mapa custom de la versión de texto.
    
    respuesta=messagebox.askyesno('Importar mapa',"""¿Quieres importar el mapa personalizado de la versión
de texto? Hacer esto sobrescribirá el mapa personalizado actual.""")
    if respuesta == True:

        directorioactual = os.getcwd()  
        directoriopadre = os.path.abspath(os.path.join(directorioactual, os.pardir))

        fromDirectory = directoriopadre+"/JUEGO ROL PYTHON/custom/mapa.txt"
        toDirectory = directoriopadre+"/JUEGO ROL PYTHON - tkinter/custom/mapa.txt"
        try:
            shutil.copyfile(fromDirectory, toDirectory)
            messagebox.showinfo(message="Mapa importado con éxito.", title="Atención")
        except Exception:
            messagebox.showinfo(message="Error al importar mapa.", title="Atención")
        

