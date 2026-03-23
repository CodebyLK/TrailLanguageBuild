import re

# Define the token types and their regex patterns
TOKEN_SPECIFICATION = [
    ('VAR',        r'var\b'),                 # Trail assignment keyword
    ('PRINT',      r'print\b'),               # Print keyword
    ('INTEGER',    r'\d+'),                   # Integer literals like 5, 42, 1000
    ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9]*'),  # Variables like x or total1
    ('PLUS',       r'\+'),                    # Addition
    ('MINUS',      r'-'),                     # Subtraction
    ('STAR',       r'\*'),                    # Multiplication
    ('SLASH',      r'/'),                     # Division
    ('EQUAL',      r'='),                     # Assignment
    ('SEMICOLON',  r';'),                     # Statement terminator
    ('LPAREN',     r'\('),                    # Left Parenthesis
    ('RPAREN',     r'\)'),                    # Right Parenthesis
    ('SKIP',       r'[ \t\n]+'),              # Whitespace (ignored)
    ('MISMATCH',   r'.'),                     # Unknown character
]

def tokenize(code):
    # Combine all individual regex patterns into one master pattern
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'SKIP':
            continue  # Ignore whitespace
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}') # Terminate on unknown characters
        else:
            tokens.append((kind, value))
            
    # The specification requires an EOF token at the end
    tokens.append(('EOF', 'EOF'))
    
    return tokens

# Test for tokenizer
if __name__ == '__main__':
    sample_code = "var x = 5; print(x);"
    tokens = tokenize(sample_code)
    for token in tokens:
        print(token)