
from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('500x300')
ws.config(bg='yellow')

img = PhotoImage(file="./pictures/1.png")
label = Label(ws,image=img)
label.place(x=0, y=0)

ws.mainloop()


