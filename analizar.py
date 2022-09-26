import re
from turtle import color
from tokens import Token, Error
import numpy
import math
row = 0
col = 0
tokens_lista = []
errores = []
letras = re.compile(r'[a-z]')
numeros = re.compile(r'[0-9]')
a, b = 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU'
trans = str.maketrans(a, b)
operadores=['suma','resta','multiplicacion','division','potencia','raiz','inverso','seno','coseno','tangente','mod']

def lecturadearchivo():
    global letras, numeros, row, col
    estado = 0
    estadoanterior = 0
    f = open('miniprueba.txt', 'r')
    mensaje = f.read()
    f.close()
    print("")
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


def guardar_token(fila, columna, lexema):
    nuevotoken = Token(fila, columna, lexema)
    tokens_lista.append(nuevotoken)

cont=0
def guardarerror(fila, columna, lexema):
    global cont
    cont+=1
    nuevotoken = Error(cont,lexema,"Error",columna,fila)
    errores.append(nuevotoken)


def imprimir():
    print("|{:<10}|{:<10}|{:<50}|".format('Fila', 'Columna', 'Lexema'))
    print('-'*33)
    for i in tokens_lista:
        print("|{:<10}|{:<10}|{:<50}|".format(i.fila, i.columna, i.lexema))
    print('-'*33)
    print("\n ERRORES")
    if len(errores) == 0:
        print("No hay errores")
    else:
        for i in errores:
            print(i.No,i.tipo,i.fila, i.columna, '\"', i.lexema, '\"')


def operaciones():
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
            <title>Operaciones</title>
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
    print(htmloperacion)
    
lecturadearchivo()
#imprimir()
operaciones()