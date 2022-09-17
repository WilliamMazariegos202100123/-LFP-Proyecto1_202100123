from tkinter import *
from tkinter import Button
from tkinter import scrolledtext
from tkinter import filedialog
import pathlib
from tkinter import messagebox
from tkinter.ttk import Label
'''def obtener():
    a=text_area.get("1.0",'end-1c')
    print(len(a))
    print(type(a))
    print(a)
'''
root = Tk()
root.geometry("600x600")
root.title("ScrolledText Widget Example")
text_area = scrolledtext.ScrolledText(root, wrap=WORD,width=40, height=5, font=("Consolas", 15),bg="black")
text_area.config(foreground="white")                                 
#text_area.config(state="disabled")
text_area.pack()
def abrir():
    f = open ('conteo.txt','r')
    mensaje = f.read()
    print(mensaje)
    f.close()
    text_area.insert(END,"hola")
    archivo=filedialog.askopenfilename(initialdir="C:/",filetypes=(("Todos los ficheros","*.*"),("Archivos de Texto", "*.txt") ), title = "Seleccionar archivo")
    print(archivo)
    extension=pathlib.Path(archivo)
    if str(extension.suffix)==".txt":
        messagebox.showinfo("","Archivo aceptado")
        mi_Label.config(text=archivo)
        print("esto tiene el label: ",mi_Label.cget("text"))
    elif str(extension.suffix)!=".txt" and len(archivo)!=0:
        messagebox.showerror("",str(extension.name)+" no es archivo valido")
def borrar():
    text_area.delete("0.0",END)
def guardararchivo():
    carp=filedialog.asksaveasfilename(title="Guardar como",filetypes=(("Archivos de Texto", "*.txt"),("Todos los ficheros","*.*")),defaultextension=".txt")
    print(carp)
boton=Button(root,text="abrir archivo",command=abrir)
boton.pack()
mi_Label = Label(root) #Creación del Label
mi_Label.pack()
mi_Label.config(background="red")
boton2=Button(root,text="abrir carpeta",command=guardararchivo)
boton2.pack()    
root.mainloop()