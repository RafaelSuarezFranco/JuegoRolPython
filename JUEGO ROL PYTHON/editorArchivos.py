import csv
#salvo el mapa, los archivos en la carpeta custom se pueden editar aquí

def inputValido(num):
    try:
        num = int(num)
        return True if num >= 0 else False
    except ValueError:
        return False



def editarAmbientes():
    input("""Para crear ambientes personalizados, escribe una cadena de texto que describa cada ambiente y pulsa intro
para guardar cada uno de ellos. Cuando no quieras añadir más, simplemente pulsa intro.""")
    
    nuevosambientes = [] 
    ambiente = "."
    
    while ambiente != "":
        ambiente = input("Introduce un nuevo ambiente (pulsa intro sin escribir para terminar)")
        if ambiente != "":
            nuevosambientes.append(ambiente)
    
    if len(nuevosambientes) > 0: #solo guardaremos si hay al menos un ambiente    
        confirmacion = ""
        while confirmacion != "si" and confirmacion != "no":
            confirmacion = input("¿Quieres guardar los nuevos ambientes en tus archivos personalizados? (si/no)").lower()
        if confirmacion == "si":
            #si vamos a guardarlos, transformamos el array en otro que tenga índices.
            arrayambientes = []
            contador = 1
            for i in range(len(nuevosambientes)):
                arrayambientes.append([contador, nuevosambientes[i]])
                contador = contador + 1
                
            guardarFicheroPersonalizado(arrayambientes, "ambientes")
        else:
            print("Ambientes nuevos descartados.")
    else:
        print("Has salido sin crear ningún ambiente.")


def editarMonstruoObjeto(monstruoObjeto):
    #misma función para crear monstruos u objetos, ya que son parecidos.
    input("Para crear "+monstruoObjeto+"s personalizados, se te pedirá que indiques las características del "
          +monstruoObjeto+" una por una.")
    
    nombres = []#características de cada monstruo/objeto
    vidas = []
    habilidades = []
    descripciones = []
    siguiente = ""
    
    while siguiente != "no":
        siguiente = input("¿Quieres crear un nuevo "+monstruoObjeto+"? (si/no)").lower()
        if siguiente == "si":
            
            nombre = ""
            while nombre == "":
                nombre = input("Nombre del "+monstruoObjeto+": ")
            
            vida = ""
            while inputValido(vida) == False:
                vida = input("Vida/puntos del "+monstruoObjeto+": ")
                
            habilidad = ""
            while habilidad != "1" and habilidad != "2" and habilidad != "3":
                habilidad = input("Habilidad del "+monstruoObjeto+" (1 - Lucha, 2 - Magia, 3 - Astucia): ")
                
            if habilidad == "1":
                habilidad = "LUCHA"
            elif habilidad == "2":
                habilidad = "MAGIA"
            else:
                habilidad = "ASTUCIA"
            
            
            descripcion = ""
            if monstruoObjeto == "monstruo":#descripción solo la pedimos para monstruos
                while descripcion == "":
                    descripcion = input("Descripción del monstruo: ")
            
            nombres.append(nombre)
            vidas.append(vida)
            habilidades.append(habilidad)
            descripciones.append(descripcion)
            
    if len(nombres) > 0: #solo guardaremos si hay al menos un monstruo/objeto
        
        confirmacion = ""
        while confirmacion != "si" and confirmacion != "no":
            confirmacion = input("¿Quieres guardar los nuevos "+monstruoObjeto+"s en tus archivos personalizados? (si/no)").lower()
        if confirmacion == "si":
            arrayMonstruoObjeto = []
            contador = 1
            for i in range(len(nombres)):
                if monstruoObjeto == "monstruo":#si estamos guardando monstruos
                    arrayMonstruoObjeto.append([contador, nombres[i], vidas[i], habilidades[i], descripciones[i]])
                else:#si estamos guardando objetos
                    arrayMonstruoObjeto.append([contador, nombres[i], habilidades[i],  vidas[i]])
                contador = contador + 1
                
            guardarFicheroPersonalizado(arrayMonstruoObjeto, monstruoObjeto+"s")
        else:
            print(monstruoObjeto+"s nuevos descartados.")
    else:
        print("Has salido sin crear ningún "+monstruoObjeto+".")

    
def guardarFicheroPersonalizado(array, fichero):
    archivo = open('./custom/'+fichero+'.txt','w', newline='', encoding='utf-8')
    with archivo:
        csvescrito = csv.writer(archivo,delimiter = ';')
        csvescrito.writerows(array)
    archivo.close()
    print("Se han guardado los cambios en /custom/"+fichero+".txt")

