class Program:
    def __init__(self, statements):
        self.statements = statements

class VarDeclaration:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Assignment:
    def __init__(self, identifier, index_expr, expression):
        self.identifier = identifier
        self.index_expr = index_expr  # Used if assigning to a list index
        self.expression = expression

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression

class IfStatement:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStatement:
    def __init__(self, value):
        self.value = value

class BreakStatement:
    pass

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class ListAccess:
    def __init__(self, identifier, index_expr):
        self.identifier = identifier
        self.index_expr = index_expr

class InputExpression:
    def __init__(self, prompt_expr):
        self.prompt_expr = prompt_expr

class Literal:
    def __init__(self, value):
        self.value = value  # Handles int, float, string, and boolean

class ListLiteral:
    def __init__(self, elements):
        self.elements = elements

class Identifier:
    def __init__(self, name):
        self.name = name