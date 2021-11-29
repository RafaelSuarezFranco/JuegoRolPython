from tkinter import *

from tkinter.ttk import *

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

combo = Combobox(window)

combo['values']= (1, 2, 3, 4, 5, "Text")

combo.current(0) #set the selected item

combo.grid(column=0, row=0)

lbl = Label(window, text="Hello")

lbl.grid(column=5, row=0)
lbl.configure(text= combo.get())

#radio
selected = IntVar()

rad1 = Radiobutton(window,text='First', value=1, variable=selected)

rad2 = Radiobutton(window,text='Second', value=2, variable=selected)

rad3 = Radiobutton(window,text='Third', value=3, variable=selected)

def clicked():

   print(selected.get())

btn = Button(window, text="Click Me", command=clicked)

rad1.grid(column=0, row=1)

rad2.grid(column=1, row=1)

rad3.grid(column=2, row=1)

btn.grid(column=3, row=1)



window.mainloop()