
def dibujarSala(salidas, nuevosObjetos, monstruopasado, salaactual):
    puertaN, puertaS = "=","="
    puertaO, puertaE = "||","||"
    for salida in salidas:
        if salida == "N":
            puertaN = "N"
        if salida == "E":
            puertaE = " E"
        if salida == "S":
            puertaS = "S"
        if salida == "O":
            puertaO = "O "
            
    objeto1 = " "
    objeto2 = " "
    if nuevosObjetos != None:
        if len(nuevosObjetos) == 1:
            objeto1 = "X"
        if len(nuevosObjetos) == 2:
            objeto1 = "X"
            objeto2 = "Y"
            
    print("         SALA "+str(salaactual))
    print("==========="+puertaN+"==========")
    dibujarPared(3)
    print("||    {}     {}       ||".format(objeto1,objeto2))
    dibujarPared(2)
    print(puertaO+"                  "+puertaE)
    dibujarMonstruo() if monstruopasado else dibujarPJ()
    print("==========="+puertaS+"==========")

def dibujarPared(filas):
    for i in (1,filas):
        print("||                  ||")
        
def dibujarMonstruo():
    print("||           /¯¯\_  ||")
    print("||         __\Ö / ) ||")
    print("||   O    (__    /  ||")
    print("||  /|\     /    \  ||")
    print("||  / \    /______\ ||")
    
    
def dibujarPJ():
    print("||                  ||")
    print("||                  ||")
    print("||   O              ||")
    print("||  /|\             ||")
    print("||  / \             ||")


    
  
    