# Importaciones
import sys

# Tipos de tokens
from enum import Enum, auto


# Definición de tipos de tokens
class TokenType(Enum):
    # Tokens de control
    ENDFILE = auto()
    ERROR = auto()

    # Palabras reservadas
    IF = auto()
    ELSE = auto()
    DO = auto()
    WHILE = auto()
    SWITCH = auto()
    CASE = auto()
    END = auto()
    REPEAT = auto()
    UNTIL = auto()
    READ = auto()
    WRITE = auto()
    INTEGER = auto()
    DOUBLE = auto()
    MAIN = auto()
    AND = auto()
    OR = auto()
    RETURN = auto()

    # Tokens de múltiples caracteres
    ID = auto()
    NUM_INT = auto()
    NUM_REAL = auto()
    
    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    # Operadores relacionales
    EQ = auto()   # igualdad
    NEQ = auto()  # diferente
    LT = auto()   # menor que
    LTE = auto()  # menor o igual que
    GT = auto()   # mayor que
    GTE = auto()  # mayor o igual que

    # Símbolos especiales
    LPAREN = auto()  # paréntesis izquierdo
    RPAREN = auto()  # paréntesis derecho
    LBRACE = auto()  # llave izquierda
    RBRACE = auto()  # llave derecha
    COMMA = auto()   # coma
    SEMICOLON = auto()  # punto y coma
    ASSIGN = auto()  # asignación
    
    #simbolo de comentario múltiple no cerrado
    INMULTIPLECOMMENT = auto()
    
# Tabla de búsqueda de palabras reservadas
reservedWords = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "do": TokenType.DO,
    "while": TokenType.WHILE,
    "switch": TokenType.SWITCH,
    "case": TokenType.CASE,
    "end": TokenType.END,
    "repeat": TokenType.REPEAT,
    "until": TokenType.UNTIL,
    "read": TokenType.READ,
    "write": TokenType.WRITE,
    "int": TokenType.INTEGER,
    "double": TokenType.DOUBLE,
    "main": TokenType.MAIN,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "return": TokenType.RETURN,
    "/*": TokenType.INMULTIPLECOMMENT
}

# Tamaño máximo de un token
MAXTOKENLEN = 256

# Estados en el DFA del escáner
class StateType(Enum):
    START = auto()
    INASSIGN = auto()
    INCOMMENT = auto()
    INNUM = auto()
    INREAL = auto()
    INID = auto()
    DONE = auto()
    INMULTICOMMENT = auto()

# Buffer de longitud BUFLEN para líneas de código fuente
BUFLEN = 256

# Variables globales
source = None  # Variable para almacenar el archivo fuente
lineBuf = ""    # Almacena la línea actual
linepos = 0    # Posición actual en lineBuf
bufsize = 0     # Tamaño actual de la cadena de búfer
EOF_flag = False    # Corrige el comportamiento de ungetNextChar en EOF
lineno = 0       # numero de linea

def getNextChar():
    """
    Obtiene el siguiente carácter no en blanco de lineBuf.
    Actualiza las variables de posición de línea y buffer.
    """
    global linepos, bufsize, EOF_flag, lineBuf, lineno, source
    if not (linepos < bufsize):
        lineBuf = source.readline()
        if lineBuf:
            lineno += 1
            bufsize = len(lineBuf)
            linepos = 0
            return lineBuf[linepos - 1] if bufsize > 0 else ""
        else:
            EOF_flag = True
            return ""
    else:
        linepos += 1
        return lineBuf[linepos - 1] if bufsize > 0 else ""



def ungetNextChar():
    """
    Retrocede un carácter en lineBuf.
    """
    global linepos
    if not EOF_flag:
        linepos -= 1

def reservedLookup(s):
    """
    Busca un identificador y devuelve su tipo de token si es una palabra reservada.
    """
    return reservedWords.get(s, TokenType.ID)

def getToken():
    """
    Analiza el archivo fuente y devuelve el siguiente token encontrado.
    """
    global linepos, lineno, source
    tokenString = ""
    tokenStringIndex = 0
    currentToken = None
    state = StateType.START
    save = False
    column_number = 0

    while state != StateType.DONE:
        column_number = linepos + 1
        c = getNextChar()
        save = True
        if state == StateType.START:
            if c.isdigit():
                state = StateType.INNUM
            elif c.isalpha():
                state = StateType.INID
            elif c in [' ', '\t', '\n']:
                save = False
            elif c == '/':
                next_char = getNextChar()
                if next_char == '/':
                    save = False
                    state = StateType.INCOMMENT
                elif next_char == '*':
                    save = False
                    state = StateType.INMULTICOMMENT
                    currentToken = TokenType.INMULTIPLECOMMENT
                else:
                    ungetNextChar()  # Retornamos el caracter leído
                    state = StateType.DONE
                    currentToken = TokenType.DIVIDE
            else:
                state = StateType.DONE
                if c == "":
                    save = False
                    currentToken = TokenType.ENDFILE
                elif c == '=':
                    currentToken = TokenType.EQ
                elif c == '<':
                    currentToken = TokenType.LT
                elif c == '>':
                    currentToken = TokenType.GT
                elif c == '+':
                    currentToken = TokenType.PLUS
                elif c == '-':
                    currentToken = TokenType.MINUS
                elif c == '*':
                    currentToken = TokenType.TIMES
                elif c == '/':
                    currentToken = TokenType.DIVIDE
                elif c == '%':
                    currentToken = TokenType.MODULO
                elif c == '^':
                    currentToken = TokenType.POWER
                elif c == '(':
                    currentToken = TokenType.LPAREN
                elif c == ')':
                    currentToken = TokenType.RPAREN
                elif c == '{':
                    currentToken = TokenType.LBRACE
                elif c == '}':
                    currentToken = TokenType.RBRACE
                elif c == ',':
                    currentToken = TokenType.COMMA
                elif c == ';':
                    currentToken = TokenType.SEMICOLON
                elif c == ':':
                    currentToken = TokenType.ASSIGN
                else:
                    currentToken = TokenType.ERROR
        elif state == StateType.INCOMMENT:
            save = False
            if c == '\n' or c == "":
                state = StateType.START
        elif state == StateType.INMULTICOMMENT:
            save = False
            if c == '*':
                next_char = getNextChar()
                if next_char == '/':
                    state = StateType.START
                else:
                    ungetNextChar()  # Retornamos el caracter leído
            elif c == "":
                print(f"Error: '/*' Multiline comment not closed.\n", file=sys.stderr)
                
                state = StateType.START
            else:
                pass
        elif state == StateType.INNUM:
            if not c.isdigit() and c != '.':
                ungetNextChar()
                save = False
                state = StateType.DONE
                currentToken = TokenType.NUM_INT
            elif c == '.':
                state = StateType.INREAL
        elif state == StateType.INREAL:
            if not c.isdigit():
                ungetNextChar()
                save = False
                state = StateType.DONE
                currentToken = TokenType.NUM_REAL
        elif state == StateType.INID:
            if not c.isalnum() and c != '_':
                ungetNextChar()
                save = False
                state = StateType.DONE
                currentToken = reservedLookup(tokenString)

        if save and c != '\n':
            tokenString += c

        if state == StateType.DONE:
            if currentToken == TokenType.ID:
                currentToken = reservedLookup(tokenString)
            return currentToken, tokenString, lineno, column_number
        
# Prueba del escáner
if __name__ == "__main__":
    # Abre el archivo de código fuente
    source_file = sys.argv[1]
    
    with open(source_file, "r") as source:

        # Llama a la función getToken() hasta que se alcanza el final del archivo
        while True:
            token, tokenString, lineno, column = getToken()
            if token == TokenType.ENDFILE:
                print(f"{token.name}")
                break
            elif token == TokenType.ERROR:
                print(f"Lexical error: {tokenString} is not a valid token in line: {lineno} and column: {column}\n", file=sys.stderr)
            print(f"{token.name} ({tokenString})\n")