import re

TOKEN_SPECIFICATION = [
    ('COMMENT',    r'#.*'),                   # Single-line comments
    ('FLOAT',      r'\d+\.\d+'),              # Floating-point numbers
    ('INTEGER',    r'\d+'),                   # Integers
    ('STRING',     r'"[^"]*"'),               # Strings
    ('IF',         r'\bif\b'),                # Keywords...
    ('THEN',       r'\bthen\b'),
    ('ELSE',       r'\belse\b'),
    ('END',        r'\bend\b'),
    ('WHILE',      r'\bwhile\b'),
    ('DO',         r'\bdo\b'),
    ('BREAK',      r'\bbreak\b'),
    ('FUNCTION',   r'\bfunction\b'),
    ('RETURN',     r'\breturn\b'),
    ('VAR',        r'\bvar\b'),
    ('PRINT',      r'\bprint\b'),
    ('INPUT',      r'\binput\b'),
    ('AND',        r'\band\b'),
    ('OR',         r'\bor\b'),
    ('NOT',        r'\bnot\b'),
    ('TRUE',       r'\bTrue\b|\btrue\b'),
    ('FALSE',      r'\bFalse\b|\bfalse\b'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),# Variable names
    ('EQ',         r'=='),                    # Multi-char operators
    ('NEQ',        r'!='),
    ('LEQ',        r'<='),
    ('GEQ',        r'>='),
    ('LT',         r'<'),
    ('GT',         r'>'),
    ('PLUS',       r'\+'),                    # Single-char operators
    ('MINUS',      r'-'),
    ('STAR',       r'\*'),
    ('SLASH',      r'/'),
    ('MOD',        r'%'),
    ('EQUAL',      r'='),                     # <--- Fixed: r'=' instead of r='='
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LBRACKET',   r'\['),
    ('RBRACKET',   r'\]'),
    ('COMMA',      r','),
    ('SEMICOLON',  r';'),                     # Kept for flexibility
    ('SKIP',       r'[ \t\n\r]+'),            # Whitespace and newlines
    ('MISMATCH',   r'.'),                     # Unknown character
]

def tokenize(code):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    tokens = []
    line_num = 1
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        # Keep track of lines for error reporting
        if '\n' in value:
            line_num += value.count('\n')
            
        if kind in ('SKIP', 'COMMENT'):
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Lexical Error on line {line_num}: Unexpected character '{value}'")
        else:
            tokens.append((kind, value, line_num))
            
    tokens.append(('EOF', 'EOF', line_num))
    return tokens