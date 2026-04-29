from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self): return self.tokens[self.pos]
    def current_type(self): return self.current_token()[0]
    
    def consume(self, expected_type):
        if self.current_type() == expected_type:
            token = self.current_token()
            self.pos += 1
            # Optional semicolons for flexibility
            if self.current_type() == 'SEMICOLON': 
                self.pos += 1
            return token
        else:
            token_val = self.current_token()[1]
            line = self.current_token()[2]
            raise RuntimeError(f"Syntax Error on line {line}: Expected {expected_type}, got '{token_val}'")

    def parse_program(self):
        statements = []
        while self.current_type() != 'EOF':
            if self.current_type() == 'SEMICOLON':
                self.pos += 1
                continue
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token_type = self.current_type()
        if token_type == 'VAR': return self.parse_var_declaration()
        elif token_type == 'PRINT': return self.parse_print()
        elif token_type == 'IF': return self.parse_if()
        elif token_type == 'WHILE': return self.parse_while()
        elif token_type == 'FUNCTION': return self.parse_function()
        elif token_type == 'RETURN': return self.parse_return()
        elif token_type == 'BREAK':
            self.consume('BREAK')
            return BreakStatement()
        elif token_type == 'IDENTIFIER':
            # Could be assignment or function call statement
            return self.parse_identifier_statement()
        else:
            raise RuntimeError(f"Syntax Error on line {self.current_token()[2]}: Unexpected statement start '{self.current_token()[1]}'")

    def parse_block(self, end_tokens):
        statements = []
        while self.current_type() not in end_tokens and self.current_type() != 'EOF':
            if self.current_type() == 'SEMICOLON':
                self.pos += 1
                continue
            statements.append(self.parse_statement())
        return statements

    def parse_var_declaration(self):
        self.consume('VAR')
        name = self.consume('IDENTIFIER')[1]
        self.consume('EQUAL')
        expr = self.parse_expression()
        return VarDeclaration(Identifier(name), expr)

    def parse_identifier_statement(self):
        name = self.consume('IDENTIFIER')[1]
        if self.current_type() == 'EQUAL':
            self.consume('EQUAL')
            return Assignment(Identifier(name), None, self.parse_expression())
        elif self.current_type() == 'LBRACKET':
            self.consume('LBRACKET')
            index_expr = self.parse_expression()
            self.consume('RBRACKET')
            self.consume('EQUAL')
            return Assignment(Identifier(name), index_expr, self.parse_expression())
        elif self.current_type() == 'LPAREN':
            self.consume('LPAREN')
            args = self.parse_arguments()
            self.consume('RPAREN')
            return FunctionCall(name, args)
        else:
            line = self.current_token()[2]
            raise RuntimeError(f"Syntax Error on line {line}: Expected assignment or function call after '{name}'")

    def parse_print(self):
        self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        return PrintStatement(expr)

    def parse_if(self):
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('THEN')
        then_block = self.parse_block(['ELSE', 'END'])
        else_block = []
        if self.current_type() == 'ELSE':
            self.consume('ELSE')
            else_block = self.parse_block(['END'])
        self.consume('END')
        return IfStatement(condition, then_block, else_block)

    def parse_while(self):
        self.consume('WHILE')
        condition = self.parse_expression()
        self.consume('DO')
        body = self.parse_block(['END'])
        self.consume('END')
        return WhileStatement(condition, body)

    def parse_function(self):
        self.consume('FUNCTION')
        name = self.consume('IDENTIFIER')[1]
        self.consume('LPAREN')
        params = []
        if self.current_type() != 'RPAREN':
            params.append(self.consume('IDENTIFIER')[1])
            while self.current_type() == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('IDENTIFIER')[1])
        self.consume('RPAREN')
        body = self.parse_block(['END'])
        self.consume('END')
        return FunctionDef(name, params, body)

    def parse_return(self):
        self.consume('RETURN')
        expr = self.parse_expression() if self.current_type() not in ('SEMICOLON', 'END') else None
        return ReturnStatement(expr)

    # Expression parsing with precedence
    def parse_expression(self): return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.current_type() == 'OR':
            op = self.consume('OR')[1]
            node = BinaryExpression(node, op, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_equality()
        while self.current_type() == 'AND':
            op = self.consume('AND')[1]
            node = BinaryExpression(node, op, self.parse_equality())
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while self.current_type() in ('EQ', 'NEQ'):
            op = self.consume(self.current_type())[1]
            node = BinaryExpression(node, op, self.parse_relational())
        return node

    def parse_relational(self):
        node = self.parse_additive()
        while self.current_type() in ('LT', 'GT', 'LEQ', 'GEQ'):
            op = self.consume(self.current_type())[1]
            node = BinaryExpression(node, op, self.parse_additive())
        return node

    def parse_additive(self):
        node = self.parse_term()
        while self.current_type() in ('PLUS', 'MINUS'):
            op = self.consume(self.current_type())[1]
            node = BinaryExpression(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_unary()
        while self.current_type() in ('STAR', 'SLASH', 'MOD'):
            op = self.consume(self.current_type())[1]
            node = BinaryExpression(node, op, self.parse_unary())
        return node

    def parse_unary(self):
        if self.current_type() in ('MINUS', 'NOT'):
            op = self.consume(self.current_type())[1]
            return UnaryExpression(op, self.parse_unary())
        return self.parse_factor()

    def parse_factor(self):
        token_type, value, line = self.current_token()
        
        if token_type == 'FLOAT':
            self.consume('FLOAT')
            return Literal(float(value))
        elif token_type == 'INTEGER':
            self.consume('INTEGER')
            return Literal(int(value))
        elif token_type == 'STRING':
            self.consume('STRING')
            return Literal(value[1:-1])  # Strip quotes
        elif token_type in ('TRUE', 'FALSE'):
            self.consume(token_type)
            return Literal(value.lower() == 'true')
        elif token_type == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            if self.current_type() == 'LPAREN':
                self.consume('LPAREN')
                args = self.parse_arguments()
                self.consume('RPAREN')
                return FunctionCall(value, args)
            elif self.current_type() == 'LBRACKET':
                self.consume('LBRACKET')
                index = self.parse_expression()
                self.consume('RBRACKET')
                return ListAccess(Identifier(value), index)
            return Identifier(value)
        elif token_type == 'LBRACKET':
            self.consume('LBRACKET')
            elements = self.parse_arguments()
            self.consume('RBRACKET')
            return ListLiteral(elements)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        elif token_type == 'INPUT':
            self.consume('INPUT')
            self.consume('LPAREN')
            prompt = self.parse_expression()
            self.consume('RPAREN')
            return InputExpression(prompt)
        else:
            raise RuntimeError(f"Syntax Error on line {line}: Unexpected token '{value}' in expression.")

    def parse_arguments(self):
        args = []
        if self.current_type() not in ('RPAREN', 'RBRACKET'):
            args.append(self.parse_expression())
            while self.current_type() == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expression())
        return args