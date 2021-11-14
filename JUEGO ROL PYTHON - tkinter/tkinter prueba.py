from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")
window.geometry('350x200')
lbl = Label(window, text="Hello")
lbl.grid(column=0, row=0)

btn2 = Button(window, text="Click Me", bg="orange", fg="red")
btn2.grid(column=1, row=1)

def clicked():
    lbl.configure(text="Button was clicked !!")#cambia el texto del label.
btn3 = Button(window, text="Click Me", command=clicked)
btn3.grid(column=2, row=1)

txt = Entry(window,width=10)
#txt = Entry(window,width=10, state='disabled')
txt.grid(column=5, row=0)

def clicked2():
    res = "Welcome to " + txt.get()
    lbl.configure(text= res)
    
btn1 = Button(window, text="Click Me", command=clicked2)
btn1.grid(column=1, row=0)


window.mainloop()