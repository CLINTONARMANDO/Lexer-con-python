from string import digits, ascii_letters
from tokens import TipoToken

DIGITOS = digits
LETRAS = ascii_letters
FLOAT_CHARS = DIGITOS + '.'
ID_INICIO = LETRAS + '_'
ID_TODOS = ID_INICIO + DIGITOS
ESPACIOS = ' \t\n'
OP_CHARS = '+-/*%=!><&|^~?:.'
# PUNTUACION = '{}[]()#;,'
COMILLA_DOBLE = '"'
COMILLA_SIMPLE = "'"

PUNTUACION = {
        '#' : TipoToken.MACRO,
        '{' : TipoToken.ILLAVE,
        '}' : TipoToken.DLLAVE,
        '[' : TipoToken.ICORCH,
        ']' : TipoToken.DCORCH,
        '(' : TipoToken.IPAREN,
        ')' : TipoToken.DPAREN,
        ';' : TipoToken.FIN_SEN,
        ',' : TipoToken.COMA,
}

KEYWORDS = [
'asm',	'double',	'new',	'switch',
'auto',	'else',	'operator',	'template',
'break',	'enum',	'private',	'this',
'case',	'extern',	'protected',	'throw',
'catch',	'float',	'public',	'try',
'char',	'for',	'register',	'typedef',
'class',	'friend',	'return',	'union',
'const',	'goto',	'short',	'unsigned',
'continue',	'if',	'signed',	'virtual',
'default',	'inline',	'sizeof',	'void',
'delete',	'int',	'static',	'volatile', 
'do',	'long',	'struct',	'while', 
]

OPERADORES = [
    # Aritmeticos
    '+', '-', '*', '/', '%',
    # Incremento y decremento
    '++', '--',
    # Asignacion
    '=', '+=', '-=', '*=', '/=', '%=',
    # Relacionales
    '==', '!=', '>', '<', '>=', '<=',
    # Logicos
    '&&', '||', '!',
    # En bits
    '&', '|', '^', '~', '<<', '>>',
    # Otros
    '?', ':', '.', '->', '::'
]
