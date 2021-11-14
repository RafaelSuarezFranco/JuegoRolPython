from tkinter import *

def centrarPantalla(window_height, window_width, window):
    """ gets the coordinates of the center of the screen """
    global screen_height, screen_width, x_cordinate, y_cordinate

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

#para evitar que se pueda salir de una pantalla pulsando x
def deshabilitarX(window):
    def disable_event():
        pass
    window.protocol("WM_DELETE_WINDOW", disable_event)


    