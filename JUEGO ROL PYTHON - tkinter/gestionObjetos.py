import random
import gestionMonstruos as gm
from tkinter.ttk import *
from tkinter import *
import gestionPantalla as cp
import gestionPersonaje as gpj

arrayobjetos = []

def esEntero(num):
    try:
        entero = int(num)
        num = entero
        return True
    except ValueError:
        return False
    
def randomizarObjeto(): #Devuelve un objeto (solo su número, si queremos checkear su info, la buscamos en el arrayobjetos)
    numAleatorio = random.randint(1, len(arrayobjetos))
    for indice in range( len(arrayobjetos) ):
        if arrayobjetos[indice][0] == str(numAleatorio):
            return arrayobjetos[indice][0]
            
        
def invocarObjeto(dificultad):# por cada sala, esta función generará 0, 1 o 2 objetos aleatorios.
    #la dificultad hace más o menos probable que hayan objetos. si es fácil, será 85 y 40, si es difícil, será 65 y 20.
    objetosNuevos = []
    hayObjeto = gm.probalilidad(75 - (dificultad * 10))
    if hayObjeto == True:
        objeto1 = int(randomizarObjeto())-1
        objetosNuevos.append(objeto1)
        print("En la sala hay " + arrayobjetos[objeto1][1]+".")
        hayOtroObjeto = gm.probalilidad(30 - (dificultad * 10))
        if hayOtroObjeto == True:
            objeto2 = objeto1
            while objeto2 == objeto1: #no permitimos que un segundo objeto sea igual al primero
                objeto2 = int(randomizarObjeto())-1
            objetosNuevos.append(objeto2)
            print("Además, hay " + arrayobjetos[objeto2][1]+".")
    
    if len(objetosNuevos) > 0:
        return objetosNuevos
    else:
        return None
    
def consultarInventario():
    contador = 0
    if len(gpj.inventario) > 0:
        print("Estos son tus objetos disponibles")
        for objeto in gpj.inventario:
            print(str(contador)+" - "+arrayobjetos[objeto][1])#mostramos un número y el nombre del objeto, el cual consultamos en el array
            contador = contador + 1
    else:
        print("No hay ningún objeto en tu inventario")


"""        
def recogerObjeto(nuevosObjetos):
    recogido = False
    ventanaobjeto = Tk()
    ventanaobjeto.title('Recoger Objeto')
    cp.centrarPantalla(200, 400, ventanaobjeto)
    ventanaobjeto.resizable(False, False)
    
    lbl = Label(ventanaobjeto, text="")
    lbl.place(x=70,y=150)
    
    def recoger1():
        gpj.inventario.append(o1)
        objeto1.place_forget()
        if len(nuevosObjetos) > 1: 
            objeto2.place_forget()
        lbl.configure(text="Has recogido "+arrayobjetos[o1][1])
        recogido = True
        
    o1 = int(nuevosObjetos[0])
    objeto1 = Button(ventanaobjeto, text="Recoger "+arrayobjetos[o1][1], command=recoger1)
    objeto1.place(x=70,y=30)
    
    o2 = ""
    def recoger2():
        gpj.inventario.append(o2)
        objeto1.place_forget()
        objeto2.place_forget()
        lbl.configure(text="Has recogido "+arrayobjetos[o2][1])
        recogido = True
        
    if len(nuevosObjetos) > 1:
        o2 = int(nuevosObjetos[1])
        objeto2 = Button(ventanaobjeto, text="Recoger "+arrayobjetos[o2][1], command=recoger2)
        objeto2.place(x=70,y=60)
        
    
    def salir():
        ventanaobjeto.destroy()
        
    salir = Button(ventanaobjeto, text="Salir", command=salir)
    salir.place(x=70,y=100)
    
    ventanaobjeto.mainloop()   
    return recogido

"""
"""
def usarObjeto(): #en la funcion de lucha, llamamos a esta función para dar la opción de escoger un objeto.
    usarObjeto = ""
    while usarObjeto != "si" and usarObjeto != "no":
        usarObjeto = input("¿Quieres utilizar un objeto? (si/no)").lower()
    if usarObjeto == "si":
        consultarInventario()
        objetoUsado = ""
        while esEntero(objetoUsado) == False or objetoUsado == "":
            objetoUsado = input("Introduce el número a la izquierda del objeto que quieres usar")
            try: # queremos que el usuario meta un número desde 0 hasta el contador máximo de objeto
                # ej: tenemos 4 objetos, el usuario puede elegir del 0 al 3
                objetoUsado = int(objetoUsado)
                if objetoUsado >= 0 and objetoUsado < len(gpj.inventario):
                    return objetoUsado #lo que estamos devolviendo es el INDICE del inventario que tenemos que usar y quitar
                else:
                    objetoUsado = ""
            except ValueError:
                objetoUsado = "" # iterar el bucle
    else:#si elige no usar objeto
        return None
"""
#esta función podría pertenecer a gestionPersonaje, ya que el inventario se almacena allí.
def crearInventario(panelinferior):
    combo = Combobox(panelinferior, state="readonly") # crear combobox no editable, al que se añaden los objetos.
    nombres = ['Ninguno']
    for objeto in gpj.inventario:
        nombres.append(arrayobjetos[int(objeto)-1][1])
    combo['values']= nombres
    combo.current(0)
    return combo

def recogerObjeto(objeto, comboobjeto, nuevosObjetos, btnobjeto1, btnobjeto2):
    #le pasamos el objeto recogido y el combobox para añadirlo
    gpj.inventario.append(objeto+1)
    if len(nuevosObjetos) >1:
        btnobjeto2.place_forget() 
    btnobjeto1.place_forget()
    nombres = ['Ninguno']
    for obj in gpj.inventario:
        nombres.append(arrayobjetos[int(obj)-1][1])
    comboobjeto['values'] = nombres
    comboobjeto.update()