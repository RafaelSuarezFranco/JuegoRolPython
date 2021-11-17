from tkinter import *

def centrarPantalla(window_height, window_width, window):
    #gets the coordinates of the center of the screen
    global screen_height, screen_width, x_cordinate, y_cordinate

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

#al pulsar las X para salir, cierra todo el programa. Si no uso esto, al cerrar una pantalla se pasa a la siguiente,
#ignorando todo el proceso que se debía hacer en esa pantalla, por lo tanto y con toda probabilidad, saltarían errores.
def deshabilitarX(window):
    def evento_salir():
        respuesta=messagebox.askyesno('Salir del juego','¿Seguro que quieres salir?')
        if respuesta == True:
            exit()
            
    window.protocol("WM_DELETE_WINDOW", evento_salir)
    


    