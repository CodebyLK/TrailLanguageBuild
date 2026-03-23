class Program:
    def __init__(self, statements):
        self.statements = statements  # A list of statement nodes

class AssignmentStatement:
    def __init__(self, identifier, expression):
        self.identifier = identifier  # An Identifier node
        self.expression = expression  # The expression being assigned

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression  # The expression to print

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left          # Left side of the operation
        self.operator = operator  # The math symbol (+, -, *, /)
        self.right = right        # Right side of the operation

class IntegerLiteral:
    def __init__(self, value):
        self.value = value        # The actual integer number

class Identifier:
    def __init__(self, name):
        self.name = name          # The variable name