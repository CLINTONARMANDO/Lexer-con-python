from tokens import *
from util import *

class Lexer():
    def __init__(self, texto: str) -> None:
        self.texto = iter(texto)
        self.actual = ''
        self.linea = 1
        self.avanzar()

    def raiseEx(self, msg):
        if self.actual == None:
            self.linea -= 1
        raise Exception(f'{msg} en la linea {self.linea}')

    def avanzar(self):
        try:
            self.actual = next(self.texto)
            if self.actual == '\n':
                self.linea += 1
        except StopIteration:
            self.actual = None

    def escanear(self):
        id_buf = []
        num_buf = []
        op_buf = []

        def vaciar_id():
            if not id_buf:
                return
            s = ''.join(id_buf)
            tipo = 'Keyword' if s in KEYWORDS else 'Id'
            print(f'{tipo}({s})')
            id_buf.clear()

        def vaciar_num():
            if not num_buf:
                return
            s = ''.join(num_buf)
            print(f'Num({s})')
            num_buf.clear()

        def vaciar_op():
            if not op_buf:
                return
            s = ''.join(op_buf)
            if s == '//':
                while self.actual not in ('\n', None):
                    self.avanzar()
                op_buf.clear()
                return
            elif s == '/*':
                anterior = self.actual
                while self.actual != None and f'{anterior}{self.actual}' != '*/':
                    anterior = self.actual
                    self.avanzar()
                if self.actual == None:
                    self.raiseEx("Comentario no terminado")
                op_buf.clear()
                return

            op_buf.clear()
            if s not in OPERADORES:
                self.raiseEx(f'{s} no es un operador valido')
            print(f'Op({s})')

        def vaciar_bufs():
            vaciar_id()
            vaciar_num()
            vaciar_op()

        while self.actual != None:
            if self.actual in ESPACIOS:
                vaciar_bufs()
            elif self.actual in OP_CHARS:
                print(self.actual)
                vaciar_id()
                vaciar_num()
                op_buf.append(self.actual)
            elif self.actual in ID_INICIO:
                vaciar_op()
                id_buf.append(self.actual)
            elif self.actual in ID_TODOS:
                if id_buf:
                    id_buf.append(self.actual)
                elif self.actual in FLOAT_CHARS:
                    num_buf.append(self.actual)
            elif self.actual in FLOAT_CHARS:
                num_buf.append(self.actual)
            elif self.actual in PUNTUACION:
                vaciar_bufs()
                print(f'Pun({self.actual})')
            elif self.actual == "'":
                vaciar_bufs()
                self.avanzar()
                if self.actual == None:
                    self.raiseEx("Se esperaba un literal caracter")
                print(f'LitChar({self.actual})')
                self.avanzar()
                if self.actual == None or self.actual != "'":
                    self.raiseEx("Se esperaba un literal caracter")
            elif self.actual == '"':
                vaciar_bufs()
                s = []
                self.avanzar()
                while True:
                    if self.actual == None:
                        self.raiseEx("Se esperaba un literal string")
                    if self.actual == '"':
                        break
                    s += self.actual
                    self.avanzar()
                s = ''.join(s)
                print(f'LitStr({s})')
            else:
                vaciar_bufs()
            self.avanzar()
