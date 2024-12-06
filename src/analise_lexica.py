import ply.lex as lex #type: ignore

from .tokens import operators, reserved_words, special_symbols #type: ignore

class AnaliseLexica:
      
    tokens = (
    *operators,
    *reserved_words,
    *special_symbols,
    'INT_CONSTANT',
    'STRING_CONSTANT',
    'FLOAT_CONSTANT',
    'IDENT'
    )  

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_ASSIGN = r'='
    t_EQ = r'=='
    t_NEQ = r'!='
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_RPARENT = r'\)'
    t_LPARENT = r'\('
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'}'
    t_RBRACE = r'{'

    t_ignore = ' \t'
    t_ignore_comments = r'\#.*'

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        
        
    def run(self, data):
        self.input = data
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)


    # TODO - Checar que o jeito que é feito a análise (com o sinal de negativo)
    # Faz com que subtrações não sejam parseadas corretamente
    def t_INT_CONSTANT(self, t: lex.LexToken):
        r'[-]?\d+'
        t.value = int(t.value)
        return t


    def t_FLOAT_CONSTANT(self, t: lex.LexToken):
        r'[-]?\d+\.\d*'
        t.value = float(t.value)
        return t


    def t_STRING_CONSTANT(self, t: lex.LexToken):
        r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\""
        t.value = str(t.value)
        return t


    def t_IDENT(self, t: lex.LexToken):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved_words.get(t.value, 'IDENT')
        return t


    def t_newline(self, t: lex.LexToken):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos


    def t_error(self, t: lex.LexToken):
        print("------------------------------------------------")
        print(f"ERRO LÉXICO: Caractere: {t.value[0]} Linha: {t.lexer.lineno} Coluna: {self.find_column(self.input, t)}")
        print("------------------------------------------------")
        quit()


    def find_column(self, input: str, token: lex.LexToken):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
    