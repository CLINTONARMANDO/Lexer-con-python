from lexer import Lexer

def main():
    with open('prueba.cpp', 'r') as archivo:
        codigo = archivo.read()
        lexer = Lexer(codigo)
        tokens = lexer.escanearTodos()
        print(tokens)

if __name__ == '__main__':
    main()
