import re
from tokens import Token,Error
row=0
col=0
tokens_lista=[]
errores=[]
letras=re.compile(r'[a-z]')
numeros=re.compile(r'[0-9]')
a,b='áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans=str.maketrans(a,b)
def lecturadearchivo():
    global letras,numeros,row,col
    estado=0
    estadoanterior=0
    f = open ('miniprueba.txt','r')
    mensaje = f.read()
    f.close()
    print("")
    auxtoken=""
    auxtokenum=""
    for char in mensaje:
        if char=='\n':
            row+=1
            col=0
            continue
        elif char=='\t':
            col+=1
            continue
        elif char==' ':
            col+=1
            continue
        if estado==0:
            if char=='<':
                guardar_token(row,col,char)
                estado=1
                estadoanterior=0
                col+=1
                continue
            else:
                col+=1
                estado=1
                guardarerror(row,col,char)
                continue
        elif estado==1:
            c=char.translate(trans)
            if bool(letras.search(c.lower()))==True:
                auxtoken+=char
                estado=1
                estadoanterior=1
                col+=1
                continue
            elif char=='>' and estadoanterior!=8:
                guardar_token(row,col,auxtoken)
                auxtoken=""
                col+=1
                guardar_token(row,col,char)
                estado=2
                estadoanterior=1
                continue
            elif char=='>' and estadoanterior==8:
                guardar_token(row,col,char)
                estado=2
                estadoanterior=1
                col+=1
                continue
            elif char=='=':
                guardar_token(row,col,auxtoken)
                auxtoken=""
                col+=1
                guardar_token(row,col,char)
                estado=3
                estadoanterior=1
                continue
            elif char=='/':
                col+=1
                auxtoken=""
                guardar_token(row,col,char)
                estado=5
                estadoanterior=1
                continue
            elif char==' ':
                col+=1
                estado=1
                estadoanterior=1
                continue
            else:
                col+=1
                guardarerror(row,col,char)
                continue
                
        elif estado==2:
            c=char.translate(trans)
            if char=='<':
                guardar_token(row,col,char)
                estado=1
                estadoanterior=2
                col+=1
                continue
            elif bool(numeros.search(char))==True:
                auxtoken+=char
                estado=4
                estadoanterior=2     
                col+=1  
                continue
            elif bool(letras.search(c.lower()))==True or char=='[' or char==']':
                auxtoken+=char
                col+=1
                estado=7
                estadoanterior=2
                continue 
            else:
                col+=1
                guardarerror(row,col,char)
                continue
        elif estado==3:
            c=char.translate(trans)
            if bool(letras.search(c.lower()))==True:
                auxtoken+=char
                estado=1
                estadoanterior=3
                col+=1
                continue
            elif bool(numeros.search(char))==True:
                col+=1
                estado=8
                estadoanterior=3
                auxtokenum+=char
                print("auxtoken ",auxtoken)
            else:
                col+=1
                guardarerror(row,col,char)
                continue
        elif estado==4:
            if bool(numeros.search(char))==True:
                auxtoken+=char
                estado=4
                estadoanterior=4
                col+=1
                continue
            elif char==".":
                auxtoken+=char
                estado=6
                estadoanterior=4
                col+=1
                continue
            elif char=='<':
                guardar_token(row,col,auxtoken)
                auxtoken=""
                col+=1
                guardar_token(row,col,char)
                estado=1
                estadoanterior=4
                
                continue
            else:
                col+=1
                guardarerror(row,col,char)
                continue
        elif estado==5:
            c=char.translate(trans)
            if bool(letras.search(c.lower()))==True:
                auxtoken+=char
                estado=1
                estadoanterior=5
                col+=1
                continue
            else:
                col+=1
                guardarerror(row,col,char)
                continue
        elif estado==6:
            if bool(numeros.search(char))==True:
                auxtoken+=char
                estado=4
                estadoanterior=6
                col+=1
                continue
            else:
                col+=1
                guardarerror(row,col,char)
                continue
                
        elif estado==7:
            if estadoanterior==2:
                auxfila=row
            c=char.translate(trans)
            if bool(letras.search(c.lower()))==True:
                col+=1
                estado=7
                estadoanterior=7
                auxtoken+=char
                aux=col
            elif char==' ' or char=='.' or char==',' or char==']':
                col+=1
                estado=7
                estadoanterior=7
                auxtoken+=char
                aux=col
            elif char=='<':
                guardar_token(auxfila,aux,auxtoken)
                guardar_token(row,col,char)
                auxtoken=""
                estado=1
                estadoanterior=7
                col=0
            else:
                col+=1
                guardarerror(row,col,char)
                continue
        elif estado==8:
            if bool(numeros.search(char))==True:
                auxtokenum+=char
                estado=8
                estadoanterior=8
                col+=1
            elif char=='/':
                print(auxtokenum)
                guardar_token(row,col,auxtokenum)
                col+=1
                print(char)
                guardar_token(row,col,char)
                auxtokenum=""
                estado=1
                estadoanterior=8
                col+=1
            else:
                col+=1
                guardarerror(row,col,char)
                continue


def guardar_token(fila,columna,lexema):
    nuevotoken=Token(fila,columna,lexema)
    tokens_lista.append(nuevotoken)

def guardarerror(fila,columna,lexema):
    nuevotoken=Error(fila,columna,lexema)
    errores.append(nuevotoken)

def imprimir():
    print("|{:<10}|{:<10}|{:<50}|".format('Fila','Columna','Lexema'))
    print('-'*33)
    for i in tokens_lista:
        print("|{:<10}|{:<10}|{:<50}|".format(i.fila,i.columna,i.lexema))
    print('-'*33)
    print("\n ERRORES")
    if len(errores)==0:
        print("No hay errores")
    else:
        for i in errores:
            print(i.fila,i.columna,'\"',i.lexema,'\"')
lecturadearchivo()
imprimir()