from tkinter import *
from tkinter import Button
from tkinter import scrolledtext
import re

root = Tk()
root.geometry("600x600")
root.title("ScrolledText Widget Example")
text_area = scrolledtext.ScrolledText(root, wrap=WORD,width=40, height=5, font=("Consolas", 15),bg="black")
text_area.config(foreground="white")                                 
#text_area.config(state="disabled")
text_area.pack()
cadena='Realizar las operaciones básicas de suma, resta, multiplicación y división, así como operaciones complejas. '
a,b='áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans=str.maketrans(a,b)
print(cadena,len(cadena))
c=cadena.translate(trans)
print(c,len(c))




boton3=Button(root,text="analizar")
boton3.pack()   
root.mainloop()