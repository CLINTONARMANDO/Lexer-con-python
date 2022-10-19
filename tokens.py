from enum import Enum

class TipoToken(Enum):
    KEYWORD = 0,
    ID = 1,
    IPAREN = 2,
    DPAREN = 3,
    ILLAVE = 4,
    DLLAVE = 5,
    ICORCH = 6,
    DCORCH = 7,
    FIN_SEN = 8,
    DELIM = 9,
    OPERADOR = 10,
    ENTERO = 11,
    DECIMAL = 12,
    MACRO = 13,
    COMA = 14
    LIT_STRING = 15
    LIT_CHAR = 16

    # Mostrar el tipo de token como string
    def __str__(self) -> str:
        return self.name

class Token:
    def __init__(self, tipo: TipoToken, lexema: str) -> None:
        self.tipo = tipo
        self.lexema = lexema

    # Mostrar el token como string
    def __repr__(self) -> str:
        return f'{self.tipo}({self.lexema})'
