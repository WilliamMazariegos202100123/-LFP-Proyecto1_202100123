import pathlib
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkPDFViewer import tkPDFViewer as pdf
from tokens import Token, Error
import re
import webbrowser
import numpy
import math
row = 0
col = 0
a, b = 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU'
trans = str.maketrans(a, b)
tokens_lista = []
errores = []
letras = re.compile(r'[a-z]')
numeros = re.compile(r'[0-9]')
contenidoruta = ""
archivoextension = ""
pressanalizar = False
conterrores = 0


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
    win_manualtecnico = Toplevel(window_main)
    win_manualtecnico.iconbitmap("icono.ico")
    win_manualtecnico.resizable(width=False, height=False)
    win_manualtecnico.title("Manual Tecnico")
    ancho = 700
    alto = 700
    sw = win_manualtecnico.winfo_screenwidth()
    sh = win_manualtecnico.winfo_screenheight()
    x = sw/2-ancho/2
    y = sh/2-alto/2-20
    win_manualtecnico.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
    img_back = PhotoImage(file="backpdf.png")
    bt_regresar = Button(win_manualtecnico, command=backpdf)  # Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0, y=0)
    v1 = pdf.ShowPdf()
    v1.img_object_li.clear()
    v2 = v1.pdf_view(win_manualtecnico,
                     pdf_location="proyecto.pdf", width=80, height=45)
    v2.place(x=40, y=0)
    win_manualtecnico.mainloop()


def abrirarchivo():
    window_main.withdraw()
    global abrir_win, tokens_lista, errores
    tokens_lista.clear()
    errores.clear()
    abrir_win = Toplevel(window_main)
    abrir_win.iconbitmap("icono.ico")
    abrir_win.resizable(width=False, height=False)
    abrir_win.title("Archivo de Texto")
    ancho = 1000
    alto = 700
    sw = abrir_win.winfo_screenwidth()
    sh = abrir_win.winfo_screenheight()
    x = sw/2-ancho/2
    y = sh/2-alto/2-20
    abrir_win.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))

    def explorador():
        global archivo, contenidoruta, archivoextension
        archivo = filedialog.askopenfilename(filetypes=(
            ("Archivos de Texto", "*.txt"), ("Todos los ficheros", "*.*")), title="Seleccionar archivo")
        # initialdir="C:/", propieadad para inicar en una carpeta especifica
        extension = pathlib.Path(archivo)
        archivoextension = extension.name
        if str(extension.suffix) == ".txt":
            tokens_lista.clear()
            errores.clear()
            text_area.delete("0.0", END)
            labelruta.config(text=archivo)
            f = open(archivo, 'r')
            contenido = f.read()
            f.close()
            text_area.insert(END, contenido)
            contenidoruta = labelruta.cget("text")
            lbarchivocargado.config(background="white", text=str(
                extension.name), font=("Arial Black", 12))

        elif str(extension.suffix) != ".txt" and len(archivo) != 0:
            messagebox.showerror("", str(extension.name) +
                                 " no es archivo valido")

    def save():
        global contenidoruta
        contenidoruta = labelruta.cget("text")
        contenidocaja = text_area.get("1.0", 'end-1c')
        if len(contenidoruta) == 0:
            messagebox.showerror("", "No hay archivo para guardar.")
        else:
            modificado = open(contenidoruta, 'w')
            modificado.write(str(contenidocaja))
            modificado.close()
            messagebox.showinfo("", "Cambios realizados")

    def saveas():
        global contenidoruta, archivoextension
        nuevoarchivo = filedialog.asksaveasfilename(title="Guardar como", initialdir="C:/", filetypes=(
            ("Archivos de Texto", "*.txt"), ("Todos los ficheros", "*.*")), defaultextension=".txt")
        extension = pathlib.Path(nuevoarchivo)
        archivoextension = extension.name
        if len(nuevoarchivo) != 0:
            labelruta.config(text=nuevoarchivo)
            contenidocaja = text_area.get("1.0", 'end-1c')
            nuevo = open(nuevoarchivo, 'w')
            nuevo.write(str(contenidocaja))
            nuevo.close()
            contenidoruta = labelruta.cget("text")
            lbarchivocargado.config(text=str(extension.name))
            lbarchivocargado.place(x=840, y=300, width=150, height=30)
            lbarchivocargado2.place(x=840, y=330, width=150, height=30)
            messagebox.showinfo("", "Archivo Guardado")
            tokens_lista.clear()
            errores.clear()
        else:
            messagebox.showerror(
                "", "No selecciono ninguna ruta de almecenamiento")

    fondo = PhotoImage(file="fondoabrir.png")
    lbfondo = Label(abrir_win, image=fondo).place(x=-2, y=0)  # Fondo
    img_back = PhotoImage(file="regresar.png")
    bt_regresar = Button(abrir_win, command=back3)  # Boton regresar
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0, y=0)
    text_area = scrolledtext.ScrolledText(abrir_win, insertbackground="red", wrap=WORD, font=(
        "Consolas", 13), bg="black")  # caja de texto
    text_area.config(foreground="sky blue")
    text_area.focus()
    text_area.place(x=30, y=100, width=800, height=550)
    img_exp = PhotoImage(file="explorar.png")
    bt_explorar = Button(abrir_win, command=explorador)  # EXPLORAR
    bt_explorar.config(image=img_exp)
    bt_explorar.place(x=850, y=20)
    lbarchivocargado = Label(abrir_win, background="white", font=("Arial Black", 11), text=str(
        archivoextension))  # Etiqueta que muestra el archivo cargado
    lbarchivocargado2 = Label(
        abrir_win, background="white", text="Cargado al Sistema")
    lbarchivocargado.place(x=840, y=300, width=150, height=30)
    lbarchivocargado2.place(x=840, y=330, width=150, height=30)
    labelruta = Label(abrir_win, font=("Consolas", 12))
    labelruta.place(x=120, y=20, width=650, height=40)
    img_save = PhotoImage(file="save.png")
    bt_save = Button(abrir_win, command=save)  # GUARDAR
    bt_save.config(image=img_save)
    bt_save.place(x=850, y=100)
    img_saveas = PhotoImage(file="saveas.png")
    bt_saveas = Button(abrir_win, command=saveas)  # GUARDAR COMO
    bt_saveas.config(image=img_saveas)
    bt_saveas.place(x=850, y=160)

    abrir_win.mainloop()


def analizar():
    global tokens_lista, errores, pressanalizar
    pressanalizar = True
    if len(contenidoruta) == 0:
        messagebox.showerror("", "No hay archivo cargado en el sistema")
    else:
        window_main.withdraw()
        global analizar_win
        analizar_win = Toplevel(window_main)
        analizar_win.iconbitmap("icono.ico")
        analizar_win.resizable(width=False, height=False)
        analizar_win.title("Analizar")
        ancho = 1000
        alto = 700
        sw = analizar_win.winfo_screenwidth()
        sh = analizar_win.winfo_screenheight()
        x = sw/2-ancho/2
        y = sh/2-alto/2-20
        analizar_win.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
        fondo = PhotoImage(file="fondoanalizar.png")
        lbfondo = Label(analizar_win, image=fondo).place(x=-2, y=0)  # Fondo
        img_back = PhotoImage(file="regresar.png")
        bt_regresar = Button(analizar_win, command=back4)  # Boton regresar
        bt_regresar.config(image=img_back)
        bt_regresar.place(x=0, y=0)
        # Tabla de errores
        tabla = Treeview(analizar_win, columns=("c1", "c2"))
        tabla.column("#0", width=60, anchor=CENTER)
        tabla.column("c1", width=100, anchor=CENTER)
        tabla.column("c2", width=100, anchor=CENTER)
        tabla.heading("#0", text="Fila")
        tabla.heading("c1", text="Columna")
        tabla.heading("c2", text="Lexemna")

        global letras, numeros, row, col
        row = 0
        col = 0
        estado = 0
        estadoanterior = 0
        f = open(contenidoruta, 'r')
        mensaje = f.read()
        f.close()
        auxtoken = ""
        auxtokenum = ""
        for char in mensaje:
            if char == '\n':
                row += 1
                col = 0
                continue
            elif char == '\t':
                col += 1
                continue
            elif char == ' ':
                col += 1
                continue
            if estado == 0:
                if char == '<':
                    guardar_token(row, col, char)
                    estado = 1
                    estadoanterior = 0
                    col += 1
                    continue
                else:
                    col += 1
                    estado = 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 1:
                c = char.translate(trans)
                if bool(letras.search(c.lower())) == True:
                    auxtoken += char
                    estado = 1
                    estadoanterior = 1
                    col += 1
                    continue
                elif char == '>' and estadoanterior != 8:
                    guardar_token(row, col, auxtoken)
                    auxtoken = ""
                    col += 1
                    guardar_token(row, col, char)
                    estado = 2
                    estadoanterior = 1
                    continue
                elif char == '>' and estadoanterior == 8:
                    guardar_token(row, col, char)
                    estado = 2
                    estadoanterior = 1
                    col += 1
                    continue
                elif char == '=':
                    guardar_token(row, col, auxtoken)
                    auxtoken = ""
                    col += 1
                    guardar_token(row, col, char)
                    estado = 3
                    estadoanterior = 1
                    continue
                elif char == '/':
                    col += 1
                    auxtoken = ""
                    guardar_token(row, col, char)
                    estado = 5
                    estadoanterior = 1
                    continue
                elif char == ' ':
                    col += 1
                    estado = 1
                    estadoanterior = 1
                    continue
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue

            elif estado == 2:
                c = char.translate(trans)
                if char == '<':
                    guardar_token(row, col, char)
                    estado = 1
                    estadoanterior = 2
                    col += 1
                    continue
                elif bool(numeros.search(char)) == True:
                    auxtoken += char
                    estado = 4
                    estadoanterior = 2
                    col += 1
                    continue
                elif bool(letras.search(c.lower())) == True or char == '[' or char == ']':
                    auxtoken += char
                    col += 1
                    estado = 7
                    estadoanterior = 2
                    continue
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 3:
                c = char.translate(trans)
                if bool(letras.search(c.lower())) == True:
                    auxtoken += char
                    estado = 1
                    estadoanterior = 3
                    col += 1
                    continue
                elif bool(numeros.search(char)) == True:
                    col += 1
                    estado = 8
                    estadoanterior = 3
                    auxtokenum += char
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 4:
                if bool(numeros.search(char)) == True:
                    auxtoken += char
                    estado = 4
                    estadoanterior = 4
                    col += 1
                    continue
                elif char == ".":
                    auxtoken += char
                    estado = 6
                    estadoanterior = 4
                    col += 1
                    continue
                elif char == '<':
                    guardar_token(row, col, auxtoken)
                    auxtoken = ""
                    col += 1
                    guardar_token(row, col, char)
                    estado = 1
                    estadoanterior = 4

                    continue
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 5:
                c = char.translate(trans)
                if bool(letras.search(c.lower())) == True:
                    auxtoken += char
                    estado = 1
                    estadoanterior = 5
                    col += 1
                    continue
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 6:
                if bool(numeros.search(char)) == True:
                    auxtoken += char
                    estado = 4
                    estadoanterior = 6
                    col += 1
                    continue
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue

            elif estado == 7:
                if estadoanterior == 2:
                    auxfila = row
                c = char.translate(trans)
                if bool(letras.search(c.lower())) == True:
                    col += 1
                    estado = 7
                    estadoanterior = 7
                    auxtoken += char
                    aux = col
                elif char == ' ' or char == '.' or char == ',' or char == ']':
                    col += 1
                    estado = 7
                    estadoanterior = 7
                    auxtoken += char
                    aux = col
                elif char == '<':
                    guardar_token(auxfila, aux, auxtoken)
                    guardar_token(row, col, char)
                    auxtoken = ""
                    estado = 1
                    estadoanterior = 7
                    col = 0
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue
            elif estado == 8:
                if bool(numeros.search(char)) == True:
                    auxtokenum += char
                    estado = 8
                    estadoanterior = 8
                    col += 1
                elif char == '/':
                    guardar_token(row, col, auxtokenum)
                    col += 1
                    guardar_token(row, col, char)
                    auxtokenum = ""
                    estado = 1
                    estadoanterior = 8
                    col += 1
                else:
                    col += 1
                    guardarerror(row, col, char)
                    continue

        conttokens = 0
        for i in tokens_lista:
            tabla.insert("", END, text=i.fila, values=(i.columna, i.lexema))
            conttokens += 1
        tabla.place(x=20, y=60, height=500, width=700)

        
        img_generar = PhotoImage(file="generar.png")
        bt_generar = Button(analizar_win,command=operaciones)  # Boton generar archivo html
        bt_generar.config(image=img_generar)
        bt_generar.place(x=740, y=400)

        analizar_win.mainloop()


def operaciones():
    print("lista errores: ",len(errores))
    if len(errores)>0:
        messagebox.showerror("Html Failed","No se puede generar un html porque el archivo presenta errores, verifique su archivo de entrada.")
    else:
        htmloperacion=""
        cont=0
        titulo=""
        sizetitulo=""
        colortitulo=""
        descripcion=""
        sizedescripcion=""
        colordescripcion=""
        sizecontenido=""
        colorcontenido=""
        for i in tokens_lista:
            a=str(i.lexema).lower()
            if a=='titulo' and len(titulo)==0:
                titulo+=tokens_lista[cont+2].lexema
            elif a=='titulocolor' and len(colortitulo)==0:
                colortitulo+=str(tokens_lista[cont+2].lexema).lower()
                colortitulo=colortitulo.replace('tamanio','')
                sizetitulo+=str(tokens_lista[cont+4].lexema)
            elif a=='texto' and len(descripcion)==0:
                descripcion+=tokens_lista[cont+2].lexema
            elif a=='descripcioncolor' and len(colordescripcion)==0:
                colordescripcion+=str(tokens_lista[cont+2].lexema).lower()
                colordescripcion=colordescripcion.replace('tamanio','')
                sizedescripcion+=str(tokens_lista[cont+4].lexema)
            elif a=='contenidocolor' and len(colorcontenido)==0:
                colorcontenido+=str(tokens_lista[cont+2].lexema).lower()
                colorcontenido=colorcontenido.replace('tamanio','')
                sizecontenido+=str(tokens_lista[cont+4].lexema)
            cont+=1

        if colorcontenido=='azul':
            colorcontenido='blue'
        elif colorcontenido=='rojo':
            colorcontenido='red'
        elif colorcontenido=='verde':
            colorcontenido='green'
        elif colorcontenido=='amarillo':
            colorcontenido='red'
        elif colorcontenido=='gris':
            colorcontenido='gray'
        else: 
            colorcontenido='black'

        if colortitulo=='azul':
            colortitulo='blue'
        elif colortitulo=='rojo':
            colortitulo='red'
        elif colortitulo=='verde':
            colortitulo='green'
        elif colortitulo=='amarillo':
            colortitulo='red'
        elif colortitulo=='gris':
            colortitulo='gray'
        else: 
            colortitulo='black'

        if colordescripcion=='azul':
            colordescripcion='blue'
        elif colordescripcion=='rojo':
            colordescripcion='red'
        elif colordescripcion=='verde':
            colordescripcion='green'
        elif colordescripcion=='amarillo':
            colordescripcion='red'
        elif colordescripcion=='gris':
            colordescripcion='gray'
        else: 
            colordescripcion='black'
        
        htmloperacion+="""
        <html>
            <head>
                <title>Operaciones_202100123</title>
            </head>
            <style>
                .titulo{
                    font-size: """+str(sizetitulo)+";"+"""
                    color: """+str(colortitulo)+"""
                }
                .descripcion{
                    font-size:"""+str(sizedescripcion)+";"+"""
                    color: """+str(colordescripcion)+"""
                }
                .contenido{
                    font-size:"""+str(sizecontenido)+";"+"""
                    color: """+str(colorcontenido)+"""
                }
            </style>
            <body>
                <div class="titulo" >"""
        htmloperacion+="\n\t\t\t\t"+str(titulo)+"""
                </div>
                <div class="descripcion">"""
        htmloperacion+="\n\t\t\t\t"+str(descripcion)+"""
                </div>
                <div class="contenido">
        """
        print("\n\n")
        potencia=[]
        suma=[]
        resta=[]
        multi=[]
        ftrigo=[]
        div=[]
        modulos=[]
        inversos=[]
        pos=[]
        raiz=[]
        cadope=""
        cont=0
        for i in tokens_lista:
            aux=str(i.lexema)
            c = aux.translate(trans)
            if c.lower()=='suma': #1
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            suma.append(a)
                        except:
                            continue
            elif c.lower()=='resta': #2
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            resta.append(a)
                        except:
                            continue
            elif c.lower()=='division': #3
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            div.append(a)
                        except:
                            continue
            elif c.lower()=='potencia': #4
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            potencia.append(a)
                        except:
                            continue

            elif c.lower()=='multiplicacion': #5
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            multi.append(a)
                        except:
                            continue
            elif c.lower()=='raiz': #6
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=int(tokens_lista[j].lexema)
                            raiz.append(a)
                        except:
                            continue

            elif c.lower()=='mod': #7
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=int(tokens_lista[j].lexema)
                            modulos.append(a)
                        except:
                            continue
            elif c.lower()=='inverso': #9
                pos.append(cont)
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=int(tokens_lista[j].lexema)
                            b=1/a
                            d=str(a)+"^-1 ="+str(b)
                            inversos.append(d)
                        except:
                            continue

            elif c.lower()=='coseno' or 'seno' or 'tangente': #10
                pos.append(cont)
                
                for j in range(cont,len(tokens_lista)):
                    if str(tokens_lista[j].lexema).lower()=='operacion':
                        break
                    else:
                        try:
                            a=float(tokens_lista[j].lexema)
                            aux=""
                            if c.lower()=='coseno':
                                b=math.cos(a)
                                aux+="Cos("+str(a)+")="+str(b)
                                ftrigo.append(aux)
                            elif c.lower()=='seno':
                                b=math.sin(a)
                                aux+="Seno("+str(a)+")="+str(b)
                                ftrigo.append(aux)
                            elif c.lower()=='tangente':
                                b=math.tan(a)
                                aux+="Tan("+str(a)+")="+str(b)
                                ftrigo.append(aux)
                        except:
                            continue
            cont+=1
        if len(inversos)>0:
            htmloperacion+="\t\t\tINVERSOS: <br>\n"
            for i in inversos:
                htmloperacion+="\t\t\t\t"+str(i)+" <br>\n"
            htmloperacion+="\t\t\t\t<br>\n"
        if len(ftrigo)>0:
            htmloperacion+="\t\t\t\tOPERACIONES TRIGONOMETRICAS: <br>\n"
            for i in ftrigo:
                htmloperacion+="\t\t\t\t"+str(i)+" <br>\n"
            htmloperacion+="\t\t\t\t<br>\n"
        if len(suma)>0:
            htmloperacion+="\t\t\t\tSUMA: <br>\n"
            for i in range(len(suma)):
                cadope+=str(suma[i])+"+"
            Sum=sum(suma)
            cadope=cadope[:-1]
            cadope+="="+str(Sum)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""

        if len(resta)>0:
            htmloperacion+="\t\t\t\tRESTA: <br>\n"
            aux=resta[0]
            a=0
            cadope+=str(aux)+"-"
            for i in range(len(resta)):
                if i>0:
                    a=aux-resta[i]
                    aux=a
                    cadope+=str(resta[i])+"-"
            cadope=cadope[:-1]
            cadope+="="+str(a)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""
        if len(multi)>0:
            htmloperacion+="\t\t\t\tMULTIPLICACION: <br>\n"
            for i in range(len(multi)):
                cadope+=str(multi[i])+"*"
            Multi=numpy.prod(multi)
            cadope=cadope[:-1]
            cadope+="="+str(Multi)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""
        if len(div)>0:
            htmloperacion+="\t\t\t\tDIVISION: <br>\n"
            Div=div[0]/div[1]
            cadope=str(div[0])+"/"+str(div[1])
            cadope+="="+str(Div)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""

        if len(potencia)>0:
            htmloperacion+="\t\t\t\tPOTENCIA: <br>\n"
            aux=potencia[0]
            a=0
            cadope+=str(aux)+"^"
            for i in range(len(potencia)):
                if i>0:
                    a=aux**potencia[i]
                    aux=a
                    cadope+=str(potencia[i])+"^"
            cadope=cadope[:-1]
            cadope+="="+str(a)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""

        if len(raiz)==2:
            htmloperacion+="\t\t\t\tRAIZ: <br>\n"
            a=pow(raiz[0],1/raiz[1])
            cadope+="("+str(raiz[1])+")"+"√"+str(raiz[0])+"="+str(a)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""
        if len(modulos)>1:
            htmloperacion+="\t\t\t\tMODULO: <br>\n"
            aux=modulos[0]
            a=0
            cadope+=str(aux)+"%"
            for i in range(len(modulos)):
                if i>0:
                    a=aux % modulos[i]
                    aux=a
                    cadope+=str(modulos[i])+"%"
            cadope=cadope[:-1]
            cadope+="="+str(a)
            htmloperacion+="\t\t\t\t"+cadope+" <br><br>\n"
        cadope=""
        htmloperacion+="""\t\t\t</div>
    \t\t</body>
    \t</html>"""
        potencia.clear()
        suma.clear()
        resta.clear()
        multi.clear()
        ftrigo.clear()
        div.clear()
        modulos.clear()
        inversos.clear()
        pos.clear()
        raiz.clear()
        f = open('OPERACIONES_202100123.html','w')
        f.write(htmloperacion)
        f.close()
        messagebox.showinfo("","Tabla de Operaciones generada con exito")
        #time.sleep(2)
        webbrowser.open_new_tab('OPERACIONES_202100123.html')

def guardar_token(fila, columna, lexema):
    nuevotoken = Token(fila, columna, lexema)
    tokens_lista.append(nuevotoken)

def guardarerror(fila, columna, lexema):
    global conterrores
    conterrores += 1
    nuevotoken = Error(conterrores, lexema, "Error", columna, fila)
    errores.append(nuevotoken)


def abrirerrores():
    global errores, tokens_lista, pressanalizar
    if len(contenidoruta) == 0:
        messagebox.showerror(
            "No hay archivo", "No hay archivo de lectura cargado en el sistema.")
        pressanalizar = False
    elif len(errores) == 0 and pressanalizar == False:
        messagebox.showwarning("Ojo!", "Necesita analizar el archivo primero.")
        pressanalizar = False
    elif len(errores) == 0 and pressanalizar == True:
        messagebox.showinfo(
            "No hay errores", "En hora buena, el archivo no contiene errores lexicos")
        pressanalizar = False
    else:
        pressanalizar = False
        window_main.withdraw()
        global error_win
        error_win = Toplevel(window_main)
        error_win.iconbitmap("icono.ico")
        error_win.resizable(width=False, height=False)
        error_win.title("Errores")
        ancho = 1000
        alto = 700
        sw = error_win.winfo_screenwidth()
        sh = error_win.winfo_screenheight()
        x = sw/2-ancho/2
        y = sh/2-alto/2-20
        error_win.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
        fondo = PhotoImage(file="fondoerror.png")
        lbfondo = Label(error_win, image=fondo).place(x=-2, y=0)  # Fondo
        img_back = PhotoImage(file="regresar.png")
        bt_regresar = Button(error_win, command=back5)  # Boton regresar
        bt_regresar.config(image=img_back)
        bt_regresar.place(x=0, y=0)

        def generarhtmlerror():
            htmlerror = ""
            htmlerror+="""<html>
            <head>
                <title>Errores Lexicos</title>
            </head>
            <style>
                body {
                    background-image: linear-gradient(180deg, #5d6366 0, #415460 25%, #1f4459 50%, #003553 75%, #00264d 100%);
                }

                table.greenTable {
                    font-family: "Comic Sans MS", cursive, sans-serif;
                    border: 6px solid #24943A;
                    background-color: #D4EED1;
                    width: 80%;
                    text-align: center;
                }

                table.greenTable td,
                table.greenTable th {
                    border: 1px solid #24943A;
                    padding: 3px 2px;
                }

                table.greenTable tbody td {
                    font-size: 16px;
                    font-weight: bold;
                }

                table.greenTable thead {
                    background: #24943A;
                    background: -moz-linear-gradient(top, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    background: -webkit-linear-gradient(top, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    background: linear-gradient(to bottom, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    border-bottom: 0px solid #444444;
                }

                table.greenTable thead th {
                    font-size: 19px;
                    font-weight: bold;
                    color: #F0F0F0;
                    text-align: center;
                    border-left: 2px solid #24943A;
                }

                table.greenTable thead th:first-child {
                    border-left: none;
                }

                table.greenTable tfoot {
                    font-size: 13px;
                    font-weight: bold;
                    color: #F0F0F0;
                    background: #24943A;
                    background: -moz-linear-gradient(top, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    background: -webkit-linear-gradient(top, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    background: linear-gradient(to bottom, #5baf6b 0%, #3a9e4d 66%, #24943A 100%);
                    border-top: 1px solid #24943A;
                }

                table.greenTable tfoot td {
                    font-size: 13px;
                }

                table.greenTable tfoot .links {
                    text-align: right;
                }

                table.greenTable tfoot .links a {
                    display: inline-block;
                    background: #FFFFFF;
                    color: #24943A;
                    padding: 2px 8px;
                    border-radius: 5px;
                }
            </style>

            <body>
                <font color="white">
                    <center><h1>Tabla de errores</h1></center>
                </font>
                <center>
                <table class="greenTable">
                    <thead>
                        <tr>
                            <th>No.</th>
                            <th>Lexema</th>
                            <th>Tipo</th>
                            <th>Columna</th>
                            <th>Fila</th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                            <td colspan="5">
                                <div class="links"><a href="#">&laquo;</a> <a class="active" href="#">1</a> <a href="#">2</a> <a
                                        href="#">3</a> <a href="#">4</a> <a href="#">&raquo;</a></div>
                            </td>
                        </tr>
                    </tfoot>
                    <tbody>\n"""
            for i in errores:
                htmlerror+="\t<tr>\n"
                htmlerror+="\t\t<td>"+str(i.No)+"</td>\n"
                htmlerror+="\t\t<td>"+str(i.lexema)+"</td>\n"
                htmlerror+="\t\t<td>"+str(i.tipo)+"</td>\n"
                htmlerror+="\t\t<td>"+str(i.columna)+"</td>\n"
                htmlerror+="\t\t<td>"+str(i.fila)+"</td>\n"
                htmlerror+="\t</tr>\n"  
            htmlerror+="""</tbody>
                </table>
                </center>
            </body>
            </html>"""
            f = open('ERRORES_202100123.html','w')
            f.write(htmlerror)
            f.close()
            messagebox.showinfo("","Tabla de Errores generada con exito")
            #time.sleep(2)
            webbrowser.open_new_tab('ERRORES_202100123.html')

        img_generar = PhotoImage(file="generar.png")
        bt_generar = Button(error_win,command=generarhtmlerror)  # Boton generar archivo html
        bt_generar.config(image=img_generar)
        bt_generar.place(x=400, y=600)
        # Tabla de errores
        tabla = Treeview(error_win, columns=("c1", "c2", "c3", "c4"))
        tabla.column("#0", width=60, anchor=CENTER)
        tabla.column("c1", width=100, anchor=CENTER)
        tabla.column("c2", width=100, anchor=CENTER)
        tabla.column("c3", width=100, anchor=CENTER)
        tabla.column("c4", width=100, anchor=CENTER)
        tabla.heading("#0", text="No.")
        tabla.heading("c1", text="Lexema")
        tabla.heading("c2", text="Tipo")
        tabla.heading("c3", text="Columna")
        tabla.heading("c4", text="Fila")

        for i in errores:
            tabla.insert("", END, text=i.No, values=(
                i.lexema, i.tipo, i.columna, i.fila))
        tabla.place(x=20, y=60, height=500, width=700)

        error_win.mainloop()


def ayuda():
    window_main.withdraw()
    global ayuda_win
    ayuda_win = Toplevel(window_main)
    ayuda_win.iconbitmap("icono.ico")
    ayuda_win.resizable(width=False, height=False)
    ayuda_win.title("Datos Programador")
    ancho = 600
    alto = 500
    sw = ayuda_win.winfo_screenwidth()
    sh = ayuda_win.winfo_screenheight()
    x = sw/2-ancho/2
    y = sh/2-alto/2-20
    ayuda_win.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
    fondo = PhotoImage(file="fondoayuda.png")
    lbfondo = Label(ayuda_win, image=fondo).place(x=-2, y=-2)
    img_back = PhotoImage(file="backpdf.png")
    # Boton cerrar prograama
    bt_regresar = Button(ayuda_win, command=backayuda)
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0, y=1)
    ayuda_win.mainloop()


def manualusuario():
    window_main.withdraw()
    global win_manualusuario
    win_manualusuario = Toplevel(window_main)
    win_manualusuario.resizable(width=False, height=False)
    win_manualusuario.iconbitmap("icono.ico")
    win_manualusuario.title("Manual de Usuario")
    ancho = 700
    alto = 700
    sw = win_manualusuario.winfo_screenwidth()
    sh = win_manualusuario.winfo_screenheight()
    x = sw/2-ancho/2
    y = sh/2-alto/2-20
    win_manualusuario.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
    img_back = PhotoImage(file="backpdf.png")
    # Boton cerrar prograama
    bt_regresar = Button(win_manualusuario, command=backpdf2)
    bt_regresar.config(image=img_back)
    bt_regresar.place(x=0, y=0)
    usuario = pdf.ShowPdf()
    usuario.img_object_li.clear()
    usuario2 = usuario.pdf_view(
        win_manualusuario, pdf_location="TEXTO.pdf", width=80, height=45)
    usuario2.place(x=40, y=0)
    win_manualusuario.mainloop()


def cerrarprograma():
    window_main.destroy()


def Main():
    global window_main
    window_main = Tk()
    window_main.resizable(width=False, height=False)
    window_main.title("Menu de opciones")
    window_main.iconbitmap("icono.ico")
    ancho = 900
    alto = 600
    sw = window_main.winfo_screenwidth()
    sh = window_main.winfo_screenheight()
    x = sw/2-ancho/2
    y = sh/2-alto/2-20
    # Fin de configurar ventana
    window_main.geometry("%dx%d+%d+%d" % (ancho, alto, x, y))
    fondo = PhotoImage(file="fondomain.png")
    lbfondo = Label(window_main, image=fondo).place(x=-3, y=-3)
    img_salir = PhotoImage(file="salir.png")
    # Boton cerrar prograama
    bt_regresar = Button(window_main, command=cerrarprograma)
    bt_regresar.config(image=img_salir)
    bt_regresar.place(x=10, y=10)
    img_abrir = PhotoImage(file="abrir.png")
    bt_abrir = Button(window_main, command=abrirarchivo)  # Boton abrir archivo
    bt_abrir.config(image=img_abrir)
    bt_abrir.place(x=140, y=250)
    img_analizar = PhotoImage(file="analizar.png")
    # Boton analizar archivo
    bt_analizar = Button(window_main, command=analizar)
    bt_analizar.config(image=img_analizar)
    bt_analizar.place(x=140, y=310)
    img_errores = PhotoImage(file="errores.png")
    bt_errores = Button(window_main, command=abrirerrores)  # Boton errores
    bt_errores.config(image=img_errores)
    bt_errores.place(x=140, y=370)
    img_tecnico = PhotoImage(file="tecnico.png")
    # Boton manual tecnico
    bt_tecnico = Button(window_main, command=manualtecnico)
    bt_tecnico.config(image=img_tecnico)
    bt_tecnico.place(x=560, y=250)
    img_usuario = PhotoImage(file="usuario.png")
    # Boton manual usuario
    bt_usuario = Button(window_main, command=manualusuario)
    bt_usuario.config(image=img_usuario)
    bt_usuario.place(x=560, y=310)
    img_ayuda = PhotoImage(file="ayuda.png")
    bt_ayuda = Button(window_main, command=ayuda)  # Boton ayuda
    bt_ayuda.config(image=img_ayuda)
    bt_ayuda.place(x=560, y=370)
    window_main.mainloop()

Main()
