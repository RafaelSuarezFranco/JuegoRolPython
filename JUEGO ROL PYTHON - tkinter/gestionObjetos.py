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
    
    hayObjeto = gm.probalilidad(75 - (dificultad * 10))#generamos 1er objeto
    if hayObjeto == True:
        objeto1 = int(randomizarObjeto())-1
        objetosNuevos.append(objeto1)
        
        hayOtroObjeto = gm.probalilidad(30 - (dificultad * 10))#generamos 2do objeto
        if hayOtroObjeto == True:
            objeto2 = objeto1
            while objeto2 == objeto1: #no permitimos que un segundo objeto sea igual al primero
                objeto2 = int(randomizarObjeto())-1
            objetosNuevos.append(objeto2)
    
    if len(objetosNuevos) > 0:
        return objetosNuevos
    else:
        return None
    

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
    
    if len(nuevosObjetos) > 1:#borramos los botones para que no se puedan coger más.
        btnobjeto2.place_forget() 
    btnobjeto1.place_forget()
    
    nombres = ['Ninguno']
    for obj in gpj.inventario:
        nombres.append(arrayobjetos[int(obj)-1][1])
    comboobjeto['values'] = nombres
    comboobjeto.update()