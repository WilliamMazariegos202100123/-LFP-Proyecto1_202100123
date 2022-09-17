import pathlib
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkPDFViewer import tkPDFViewer as pdf 
contenidoruta=""
archivoextension=""
def backpdf():
    win_manualtecnico.destroy()
    window_main.deiconify()
def backpdf2():
    win_manualusuario.destroy()
    window_main.deiconify()
def backayuda():
    ayuda_win.destroy()
    window_main.deiconify()
def back3():
    print("contenidoruta:",contenidoruta)
    print("archivoextension: ",archivoextension)
    abrir_win.destroy()
    window_main.deiconify()
def back4():
    analizar_win.destroy()
    window_main.deiconify()
def back5():
    error_win.destroy()
    window_main.deiconify()
def manualtecnico():
    window_main.withdraw()  
    global win_manualtecnico
    win_manualtecnico=Toplevel(window_main) 
    win_manualtecnico.iconbitmap("icono.ico") 
    win_manualtecnico.resizable(width=False, height=False)
    win_manualtecnico.title("Manual Tecnico")
    ancho=700
    alto=700
    sw=win_manualtecnico.winfo_screenwidth()
    sh=win_manualtecnico.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    win_manualtecnico.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    img_back= PhotoImage(file="backpdf.png")
    bt_regresar=Button(win_manualtecnico,command=backpdf) #Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=0)
    v1 = pdf.ShowPdf() 
    v1.img_object_li.clear()
    v2 = v1.pdf_view(win_manualtecnico,pdf_location = "proyecto.pdf",width = 80, height = 45)             
    v2.place(x=40,y=0) 
    win_manualtecnico.mainloop()

def abrirarchivo():
    window_main.withdraw() 
    global abrir_win
    abrir_win=Toplevel(window_main) 
    abrir_win.iconbitmap("icono.ico") 
    abrir_win.resizable(width=False, height=False)
    abrir_win.title("Archivo de Texto")
    ancho=1000
    alto=700
    sw=abrir_win.winfo_screenwidth()
    sh=abrir_win.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    abrir_win.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    def explorador():
        global archivo,contenidoruta,archivoextension
        archivo=filedialog.askopenfilename(initialdir="C:/",filetypes=(("Archivos de Texto", "*.txt"),("Todos los ficheros","*.*")), title = "Seleccionar archivo")
        extension=pathlib.Path(archivo)
        archivoextension=extension.name
        if str(extension.suffix)==".txt":
            text_area.delete("0.0",END)
            labelruta.config(text=archivo)
            f = open (archivo,'r')
            contenido = f.read()
            f.close()
            text_area.insert(END,contenido)
            contenidoruta=labelruta.cget("text")
            lbarchivocargado.config(background="white",text=str(extension.name),font=("Arial Black",12))


        elif str(extension.suffix)!=".txt" and len(archivo)!=0:
            messagebox.showerror("",str(extension.name)+" no es archivo valido")
    
    def save():
        global contenidoruta
        contenidoruta=labelruta.cget("text")
        contenidocaja=text_area.get("1.0",'end-1c')
        if len(contenidoruta)==0:
            messagebox.showerror("","No hay archivo para guardar.")
        else:
            modificado=open(contenidoruta,'w')
            modificado.write(str(contenidocaja))
            modificado.close()
            messagebox.showinfo("","Cambios realizados")

    def saveas():
        global contenidoruta,archivoextension
        nuevoarchivo=filedialog.asksaveasfilename(title="Guardar como",initialdir="C:/",filetypes=(("Archivos de Texto", "*.txt"),("Todos los ficheros","*.*")),defaultextension=".txt")
        extension=pathlib.Path(nuevoarchivo)
        archivoextension=extension.name
        if len(nuevoarchivo)!=0:
            labelruta.config(text=nuevoarchivo)
            contenidocaja=text_area.get("1.0",'end-1c')
            nuevo=open(nuevoarchivo,'w')
            nuevo.write(str(contenidocaja))
            nuevo.close()
            contenidoruta=labelruta.cget("text")
            lbarchivocargado.config(text=str(extension.name))
            lbarchivocargado.place(x=840,y=300,width=150,height=30)
            lbarchivocargado2.place(x=840,y=330,width=150,height=30)
            messagebox.showinfo("","Archivo Guardado")
        else:
            messagebox.showerror("","No selecciono ninguna ruta de almecenamiento")


    fondo=PhotoImage(file="fondoabrir.png")
    lbfondo=Label(abrir_win,image=fondo).place(x=-2,y=0)  #Fondo
    img_back= PhotoImage(file="regresar.png")
    bt_regresar=Button(abrir_win,command=back3) #Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=0)
    text_area = scrolledtext.ScrolledText(abrir_win,insertbackground="red", wrap=WORD, font=("Consolas", 13),bg="black") #caja de texto
    text_area.config(foreground="sky blue")   
    text_area.focus()
    text_area.place(x=30,y=100,width=800,height=550)
    img_exp= PhotoImage(file="explorar.png")
    bt_explorar=Button(abrir_win,command=explorador) #EXPLORAR
    bt_explorar.config(image=img_exp)
    bt_explorar.place(x=850,y=20)
    lbarchivocargado=Label(abrir_win,background="white",font=("Arial Black",11),text=str(archivoextension)) #Etiqueta que muestra el archivo cargado
    lbarchivocargado2=Label(abrir_win,background="white",text="Cargado al Sistema")
    lbarchivocargado.place(x=840,y=300,width=150,height=30)
    lbarchivocargado2.place(x=840,y=330,width=150,height=30)
    labelruta=Label(abrir_win,font=("Consolas",12))
    labelruta.place(x=120,y=20,width=650,height=40)
    img_save= PhotoImage(file="save.png")
    bt_save=Button(abrir_win,command=save) # GUARDAR
    bt_save.config(image=img_save)
    bt_save.place(x=850,y=100)
    img_saveas= PhotoImage(file="saveas.png")
    bt_saveas=Button(abrir_win,command=saveas) # GUARDAR COMO
    bt_saveas.config(image=img_saveas)
    bt_saveas.place(x=850,y=160)
    
    abrir_win.mainloop()

def analizar():
    window_main.withdraw() 
    global analizar_win
    analizar_win=Toplevel(window_main)  
    analizar_win.iconbitmap("icono.ico")
    analizar_win.resizable(width=False, height=False)
    analizar_win.title("Analizar")
    ancho=1000
    alto=700
    sw=analizar_win.winfo_screenwidth()
    sh=analizar_win.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    analizar_win.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    fondo=PhotoImage(file="fondoanalizar.png")
    lbfondo=Label(analizar_win,image=fondo).place(x=-2,y=0)  #Fondo
    img_back= PhotoImage(file="regresar.png")
    bt_regresar=Button(analizar_win,command=back4) #Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=0)
    text_area = scrolledtext.ScrolledText(analizar_win,insertbackground="red", wrap=WORD, font=("Consolas", 13),bg="black") #caja de texto
    text_area.config(foreground="sky blue",state="disabled")   
    text_area.place(x=30,y=100,width=600,height=550)
    img_generar= PhotoImage(file="generar.png")
    bt_generar=Button(analizar_win) # Boton generar archivo html
    bt_generar.config(image=img_generar)
    bt_generar.place(x=740,y=400)
    
    analizar_win.mainloop()

def errores():
    window_main.withdraw() 
    global error_win
    error_win=Toplevel(window_main)  
    error_win.iconbitmap("icono.ico")
    error_win.resizable(width=False, height=False)
    error_win.title("Errores")
    ancho=1000
    alto=700
    sw=error_win.winfo_screenwidth()
    sh=error_win.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    error_win.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    fondo=PhotoImage(file="fondoerror.png")
    lbfondo=Label(error_win,image=fondo).place(x=-2,y=0)  #Fondo
    img_back= PhotoImage(file="regresar.png")
    bt_regresar=Button(error_win,command=back5) #Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=0)
    img_generar= PhotoImage(file="generar.png")
    bt_generar=Button(error_win) # Boton generar archivo html
    bt_generar.config(image=img_generar)
    bt_generar.place(x=400,y=600)
    #Tabla de errores
    tabla=Treeview(error_win,columns=("c1","c2","c3","c4"))
    tabla.column("#0",width=60, anchor=CENTER)
    tabla.column("c1",width=100, anchor=CENTER)
    tabla.column("c2",width=100, anchor=CENTER)
    tabla.column("c3",width=100, anchor=CENTER)
    tabla.column("c4",width=100, anchor=CENTER)
    tabla.heading("#0",text="No.")
    tabla.heading("c1",text="Lexema")
    tabla.heading("c2",text="Tipo")
    tabla.heading("c3",text="Columna")
    tabla.heading("c4",text="Fila")
    tabla.place(x=20,y=60,height=500,width=700)
    error_win.mainloop()

def ayuda():
    window_main.withdraw()  
    global ayuda_win
    ayuda_win=Toplevel(window_main)  
    ayuda_win.iconbitmap("icono.ico")
    ayuda_win.resizable(width=False, height=False)
    ayuda_win.title("Datos Programador")
    ancho=600
    alto=500
    sw=ayuda_win.winfo_screenwidth()
    sh=ayuda_win.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    ayuda_win.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    fondo=PhotoImage(file="fondoayuda.png")
    lbfondo=Label(ayuda_win,image=fondo).place(x=-2,y=-2)
    img_back= PhotoImage(file="backpdf.png")
    bt_regresar=Button(ayuda_win,command=backayuda) #Boton cerrar prograama
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=1)
    ayuda_win.mainloop()

def manualusuario():
    window_main.withdraw()  
    global win_manualusuario
    win_manualusuario=Toplevel(window_main)  
    win_manualusuario.resizable(width=False, height=False)
    win_manualusuario.iconbitmap("icono.ico")
    win_manualusuario.title("Manual de Usuario")
    ancho=700
    alto=700
    sw=win_manualusuario.winfo_screenwidth()
    sh=win_manualusuario.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    win_manualusuario.geometry("%dx%d+%d+%d"%(ancho,alto,x,y))
    img_back= PhotoImage(file="backpdf.png")
    bt_regresar=Button(win_manualusuario,command=backpdf2) #Boton cerrar prograama
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0,y=0)
    usuario = pdf.ShowPdf() 
    usuario.img_object_li.clear()
    usuario2 = usuario.pdf_view(win_manualusuario,pdf_location = "TEXTO.pdf",width = 80, height = 45)             
    usuario2.place(x=40,y=0) 
    win_manualusuario.mainloop()

def cerrarprograma():
    window_main.destroy()


def Main():
    global window_main
    window_main=Tk()
    print("archivoextension: ",archivoextension)
    window_main.resizable(width=False, height=False)
    window_main.title("Menu de opciones")
    window_main.iconbitmap("icono.ico")
    ancho=900
    alto=600
    sw=window_main.winfo_screenwidth()
    sh=window_main.winfo_screenheight()
    x=sw/2-ancho/2
    y=sh/2-alto/2-20
    window_main.geometry("%dx%d+%d+%d"%(ancho,alto,x,y)) #Fin de configurar ventana
    fondo=PhotoImage(file="fondomain.png")
    lbfondo=Label(window_main,image=fondo).place(x=-3,y=-3)
    img_salir= PhotoImage(file="salir.png")
    bt_regresar=Button(window_main,command=cerrarprograma) #Boton cerrar prograama
    bt_regresar.config(image=img_salir)
    bt_regresar.place(x=10,y=10)
    img_abrir=PhotoImage(file="abrir.png")
    bt_abrir=Button(window_main,command=abrirarchivo) #Boton abrir archivo
    bt_abrir.config(image=img_abrir)
    bt_abrir.place(x=140,y=250)
    img_analizar=PhotoImage(file="analizar.png")
    bt_analizar=Button(window_main,command=analizar) #Boton analizar archivo
    bt_analizar.config(image=img_analizar)
    bt_analizar.place(x=140,y=310)
    img_errores=PhotoImage(file="errores.png")
    bt_errores=Button(window_main,command=errores) #Boton errores
    bt_errores.config(image=img_errores)
    bt_errores.place(x=140,y=370)
    img_tecnico=PhotoImage(file="tecnico.png")
    bt_tecnico=Button(window_main,command=manualtecnico) #Boton manual tecnico
    bt_tecnico.config(image=img_tecnico)
    bt_tecnico.place(x=560,y=250)
    img_usuario=PhotoImage(file="usuario.png")
    bt_usuario=Button(window_main,command=manualusuario) #Boton manual usuario
    bt_usuario.config(image=img_usuario)
    bt_usuario.place(x=560,y=310)
    img_ayuda=PhotoImage(file="ayuda.png")
    bt_ayuda=Button(window_main,command=ayuda) #Boton ayuda
    bt_ayuda.config(image=img_ayuda)
    bt_ayuda.place(x=560,y=370)
    window_main.mainloop()

Main()