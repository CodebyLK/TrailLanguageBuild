from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def current_type(self):
        # Correctly extracts just the type string
        return self.current_token()[0]

    def consume(self, expected_type):
        if self.current_type() == expected_type:
            self.pos += 1
        else:
            raise RuntimeError(f"Expected {expected_type}, got {self.current_token()}")

    def parse_program(self):
        statements = []
        while self.current_type() != 'EOF':
            statements.append(self.parse_statement())
        self.consume('EOF')
        return Program(statements)

    def parse_statement(self):
        # Assignments in Trail start with 'var'
        if self.current_type() == 'VAR':
            return self.parse_assignment()
        elif self.current_type() == 'PRINT':
            return self.parse_print_stmt()
        else:
            raise RuntimeError(f"Unexpected token: {self.current_token()}")

    def parse_assignment(self):
        # Consume the 'var' keyword first
        self.consume('VAR')
        
        name = self.current_token()[1]  # Get the actual variable name
        self.consume('IDENTIFIER')
        self.consume('EQUAL')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return AssignmentStatement(Identifier(name), expr)

    def parse_print_stmt(self):
        self.consume('PRINT')
        # Trail uses function-style print(expr)
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return PrintStatement(expr)

    def parse_expression(self):
        node = self.parse_term()
        while self.current_type() in ('PLUS', 'MINUS'):
            op_type, op_value = self.current_token()
            self.consume(op_type)
            right = self.parse_term()
            node = BinaryExpression(node, op_value, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_type() in ('STAR', 'SLASH'):
            op_type, op_value = self.current_token()
            self.consume(op_type)
            right = self.parse_factor()
            node = BinaryExpression(node, op_value, right)
        return node

    def parse_factor(self):
        token_type, value = self.current_token()
        if token_type == 'INTEGER':
            self.consume('INTEGER')
            return IntegerLiteral(int(value))
        elif token_type == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            return Identifier(value)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        else:
            raise RuntimeError(f"Invalid factor: {token_type}")
        

# Test for parser
if __name__ == '__main__':
    from lexer import tokenize

    # A valid test program using Trail syntax
    sample_code = "var x = 3 + 4 * 5; print(x);"

    # 1. Lex the code into tokens
    tokens = tokenize(sample_code)

    # 2. Parse the tokens into an AST
    parser = Parser(tokens)
    ast_root = parser.parse_program()

    print(f"Successfully parsed {len(ast_root.statements)} statements!")
    for stmt in ast_root.statements:
        print(f"Found: {type(stmt).__name__}")