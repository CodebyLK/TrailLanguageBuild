import re

TOKEN_SPECIFICATION = [
    ('COMMENT',         r'#.*'),                   
    ('FLOAT',           r'\d+\.\d+'),              
    ('INTEGER',         r'\d+'),                   
    ('STRING',          r'"[^"]*"'),               # Perfect, closed string
    ('UNCLOSED_STRING', r'"[^"\n]*'),              # Missing closing quote
    ('IF',              r'\bif\b'),                
    ('THEN',            r'\bthen\b'),
    ('ELSE',            r'\belse\b'),
    ('END',             r'\bend\b'),
    ('WHILE',           r'\bwhile\b'),
    ('DO',              r'\bdo\b'),
    ('BREAK',           r'\bbreak\b'),
    ('FUNCTION',        r'\bfunction\b'),
    ('RETURN',          r'\breturn\b'),
    ('VAR',             r'\bvar\b'),
    ('PRINT',           r'\bprint\b'),
    ('INPUT',           r'\binput\b'),
    ('AND',             r'\band\b'),
    ('OR',              r'\bor\b'),
    ('NOT',             r'\bnot\b'),
    ('TRUE',            r'\bTrue\b|\btrue\b'),
    ('FALSE',           r'\bFalse\b|\bfalse\b'),
    ('IDENTIFIER',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('EQ',              r'=='),                    
    ('NEQ',             r'!='),
    ('LEQ',             r'<='),
    ('GEQ',             r'>='),
    ('LT',              r'<'),
    ('GT',              r'>'),
    ('PLUS',            r'\+'),                    
    ('MINUS',           r'-'),
    ('STAR',            r'\*'),
    ('SLASH',           r'/'),
    ('MOD',             r'%'),
    ('EQUAL',           r'='),                     
    ('LPAREN',          r'\('),
    ('RPAREN',          r'\)'),
    ('LBRACKET',        r'\['),
    ('RBRACKET',        r'\]'),
    ('COMMA',           r','),
    ('SEMICOLON',       r';'),                     
    ('SKIP',            r'[ \t\n\r]+'),            
    ('MISMATCH',        r'.'),                     
]

def tokenize(code):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    tokens = []
    line_num = 1
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if '\n' in value:
            line_num += value.count('\n')
            
        if kind in ('SKIP', 'COMMENT'):
            continue
        elif kind == 'UNCLOSED_STRING':
            # --- TUTOR: UNCLOSED STRING ---
            raise RuntimeError(f"Lexical Error on line {line_num}: You started a string with a quote (\"), but forgot to close it! Make sure to put a quote at the end of your text.")
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Lexical Error on line {line_num}: The language doesn't recognize the character '{value}'. Check for typos!")
        else:
            tokens.append((kind, value, line_num))
            
    tokens.append(('EOF', 'EOF', line_num))
    return tokens