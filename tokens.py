class Token:
    def __init__(self,fila,columna,lexema):
        self.fila=fila
        self.columna=columna
        self.lexema=lexema

class Error:
    def __init__(self,No,lexema,tipo,columna,fila):
        self.fila=fila
        self.columna=columna
        self.lexema=lexema
        self.No=No
        self.tipo=tipo
