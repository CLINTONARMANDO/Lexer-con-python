from typing import Generator
from tokens import * 
from util import *

class Lexer:
    def __init__(self, text) -> None:
        self.it = iter(text)
        self.actual = None
        self.linea = 1
        self.avanzar()

    # Avanza al siguiente caracter
    def avanzar(self) -> None:
        try:
            self.actual = next(self.it)
            if self.actual == '\n':
                self.linea += 1
        except StopIteration:
            self.actual = None

    def error(self, msg: str) -> Exception:
        return Exception(f'{msg} (Linea {self.linea})')

    # Escanea el siguiente token
    def escanear(self) -> Generator[Token, None, None]:
        buf = []
        while self.actual:
            if self.actual in ESPACIOS:
                self.avanzar()
            elif self.actual in PUNTUACION:
                token = Token(PUNTUACION[self.actual], self.actual)
                self.avanzar()
                yield token
            elif self.actual in ID_INICIO:
                leido = self.escanearConjunto(buf, ID_TODOS)
                yield self.decidirTexto(leido)
            elif self.actual == '/':
                self.avanzar()
                if self.actual in ('/', '*'):
                    self.consumirComentario(f'/{self.actual}')
                else:
                    buf.append('/')
                    leido = self.escanearConjunto(buf, OP_CHARS)
                    yield self.operadorValido(leido)
            elif self.actual in OP_CHARS:
                yield self.escanearOps()
            elif self.actual in DIGITOS:
                leido = self.escanearConjunto(buf, FLOAT_CHARS)
                yield self.decidirNum(leido)
            elif self.actual == COMILLA_DOBLE:
                yield self.escanearStr(buf)
            elif self.actual == COMILLA_SIMPLE:
                yield self.escanearChar()
            else:
                raise self.error(f'Caracter {self.actual} invalido')

    # Escanea todos los tokens y los retorna como lista
    def escanearTodos(self) -> list[Token]:
        return list(self.escanear())

    # Escanea un texto conformado por caracteres en un conjunto
    def escanearConjunto(self, buf: list[str], conjunto: str) -> str:
        while self.actual and self.actual in conjunto:
            buf.append(self.actual)
            self.avanzar()
        leido = ''.join(buf)
        buf.clear()
        return leido

    # Decide si un texto conformado por caracteres que forman un id
    # conforma una palabra clave o un identificador
    def decidirTexto(self, texto: str) -> Token:
        if texto in KEYWORDS:
            return Token(TipoToken.KEYWORD, texto)
        else:
            return Token(TipoToken.ID, texto)

    # Devuelve el token si es un operador valido, caso contrario
    # arroja una excepcion
    def operadorValido(self, texto: str) -> Token:
        if texto not in OPERADORES:
            raise self.error(f'{texto} no es un operador valido')
        return Token(TipoToken.OPERADOR, texto)

    # Decide el tipo de numero
    def decidirNum(self, texto: str) -> Token:
        puntos = texto.count('.')
        if puntos == 0:
            return Token(TipoToken.ENTERO, texto)
        elif puntos == 1:
            return Token(TipoToken.DECIMAL, texto)
        else:
            raise self.error(f'{texto} no es un numero valido')

    # Escanea el valor de un string
    def escanearStr(self, buf: list[str]) -> Token:
        self.avanzar()
        # Leemos string
        while self.actual != None and self.actual not in ('\n', COMILLA_DOBLE):
            buf.append(self.actual)
            self.avanzar()
        # Errores
        if self.actual != COMILLA_DOBLE:
            raise self.error('No se acabo de cerrar el literal string')
        # Solo puede ser COMILLA_DOBLE
        self.avanzar()
        lexema = ''.join(buf)
        buf.clear()
        return Token(TipoToken.LIT_STRING, lexema)

    # Escanea un literal caracter
    def escanearChar(self) -> Token:
        self.avanzar()
        if self.actual is None:
            raise self.error('No se acabo de cerrar el literal char')
        ch = self.actual
        # Secuencias de escape
        if ch == '\\':
            self.avanzar()
            if self.actual is None:
                raise self.error('No se acabo de cerrar el literal char')
            ch += self.actual
        self.avanzar()
        # Cerrar el string
        if self.actual != COMILLA_SIMPLE:
            raise self.error(f'No se acabo de cerrar el literal char')
        self.avanzar()
        return Token(TipoToken.LIT_CHAR, ch)
    
    def escanearOps(self) -> Token:
        if self.actual is None:
            raise self.error('No hay un operador valido')
        primer = self.actual
        self.avanzar()
        largo = f'{primer}{self.actual}' 
        if largo in OPERADORES:
            self.avanzar()
            return Token(TipoToken.OPERADOR, largo)
        return Token(TipoToken.OPERADOR, primer)

    # Consume el comentario sin generar ningun token
    def consumirComentario(self, inicio: str) -> None:
        if inicio == '//':
            while self.actual and self.actual != '\n':
                self.avanzar()
        elif inicio == '/*':
            anterior = ''
            while self.actual and f'{anterior}{self.actual}' != '*/':
                anterior = self.actual
                self.avanzar()
            if self.actual is None:
                raise self.error('No se acabo de cerrar el comentario multilinea')
            self.avanzar()

