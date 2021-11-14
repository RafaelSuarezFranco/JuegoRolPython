
from tkinter import *


def nuevaVentana2():
    ws1 = Tk()
    ws1.title('PythonGuides')
    ws1.geometry('500x300')
    ws1.config(bg='red')

    #img = PhotoImage(file="./pictures/1.png")
    #label = Label(ws,image=img)
    #label.place(x=0, y=0)

    
    def clicked():
        #ws.destroy()
        nuevaVentana()
        
    btn3 = Button(ws1, text="Click Me 1", command=clicked)
    btn3.grid(column=2, row=1)
    
    ws.mainloop()

def nuevaVentana():
    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('500x300')
    
    img = PhotoImage(file="./pictures/1.png")
    label = Label(ws,image=img)
    label.image = img
    label.place(x=0, y=0)

    
    def clicked():
        #ws.destroy()
        nuevaVentana2()
        
    btn3 = Button(ws, text="Click Me 2", command=clicked)
    btn3.grid(column=2, row=1)
    
    ws.mainloop()
    
nuevaVentana()



"""
from tkinter import *

root = Tk()

display = Label(root,text="Starting")
display.pack()

def _change():

    if button.counter == 0:
        display.config(text="I just changed")
    elif button.counter == 1:
        display.config(text="I changed again")
    else:
        display.config(text="I changed once more")
    if button.counter != 2:
        button.counter += 1
    else:
        button.counter = 0

button = Button(root,text="Press me",command=_change)
button.counter = 0
button.pack()
root.mainloop()
"""




"""
from tkinter import *



root = Tk()
root.title("Game")


frame = Frame(root)
frame.pack()


canvas = Canvas(frame, bg="black", width=700, height=400)
canvas.pack()


background = PhotoImage(file="./pictures/personajes.png")
canvas.create_image(350,200,image=background)

character = PhotoImage(file="./pictures/LUCHA.png")
canvas.create_image(30,30,image=character)

root.mainloop()
"""