from ast_nodes import *

class TrailTutorError(Exception):
    """Custom error to act as the pedagogical tutor"""
    pass

class BreakException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise TrailTutorError(f"Variable '{name}' accessed before assignment. Did you mean to initialize it with 'var {name} = ...'?")

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise TrailTutorError(f"Variable '{name}' accessed before assignment. Did you mean to initialize it?")

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, node):
        try:
            return self.visit(node, self.env)
        except TrailTutorError as e:
            print(f"\n[Trail Tutor] {e}")
        except RecursionError:
            print("\n[Trail Tutor] Error: Infinite recursion detected. Make sure your function has a base case to stop calling itself.")

    def visit(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Program(self, node, env):
        for stmt in node.statements:
            self.visit(stmt, env)

    def visit_VarDeclaration(self, node, env):
        value = self.visit(node.expression, env)
        env.define(node.identifier.name, value)

    def visit_Assignment(self, node, env):
        value = self.visit(node.expression, env)
        if node.index_expr:
            target_list = env.get(node.identifier.name)
            index = self.visit(node.index_expr, env)
            if not isinstance(target_list, list):
                raise TrailTutorError(f"Cannot use index on '{node.identifier.name}' because it is a {type(target_list).__name__}, not a list.")
            if not isinstance(index, int):
                raise TrailTutorError(f"List index must be an integer, got {type(index).__name__}.")
            if index < 0 or index >= len(target_list):
                raise TrailTutorError(f"List index {index} out of bounds for list of size {len(target_list)}. Remember, lists are zero-indexed!")
            target_list[index] = value
        else:
            env.assign(node.identifier.name, value)

    def visit_PrintStatement(self, node, env):
        value = self.visit(node.expression, env)
        # Handle python booleans translating to Trail booleans
        if isinstance(value, bool): value = "True" if value else "False"
        print(value)

    def visit_IfStatement(self, node, env):
        condition = self.visit(node.condition, env)
        if condition:
            for stmt in node.then_block: self.visit(stmt, env)
        else:
            for stmt in node.else_block: self.visit(stmt, env)

    def visit_WhileStatement(self, node, env):
        while self.visit(node.condition, env):
            try:
                for stmt in node.body: self.visit(stmt, env)
            except BreakException:
                break

    def visit_BreakStatement(self, node, env):
        raise BreakException()

    def visit_FunctionDef(self, node, env):
        env.define(node.name, node)

    def visit_FunctionCall(self, node, env):
        func = env.get(node.name)
        if not isinstance(func, FunctionDef):
            raise TrailTutorError(f"'{node.name}' is not a function.")
        if len(node.args) != len(func.params):
            raise TrailTutorError(f"Function '{node.name}' expects {len(func.params)} arguments, but got {len(node.args)}.")
        
        call_env = Environment(env)
        for param, arg_expr in zip(func.params, node.args):
            call_env.define(param, self.visit(arg_expr, env))
            
        try:
            for stmt in func.body:
                self.visit(stmt, call_env)
        except ReturnException as r:
            return r.value
        return None

    def visit_ReturnStatement(self, node, env):
        value = self.visit(node.value, env) if node.value else None
        raise ReturnException(value)

    def visit_BinaryExpression(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.operator

        # Dynamic type safety enforcement
        if op in ('+', '-', '*', '/', '%', '<', '>', '<=', '>='):
            if type(left) != type(right) and not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                 if op == '+':
                     raise TrailTutorError(f"Cannot add {type(left).__name__} and {type(right).__name__}. Implicit type conversion is forbidden.")
                 raise TrailTutorError(f"Cannot perform math operation '{op}' on {type(left).__name__} and {type(right).__name__}.")

        try:
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/':
                if right == 0: raise TrailTutorError("Division by zero encountered. Did you check if your denominator is zero?")
                return left / right
            elif op == '%': return left % right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '<=': return left <= right
            elif op == '>': return left > right
            elif op == '>=': return left >= right
            elif op == 'and': return left and right
            elif op == 'or': return left or right
        except TypeError:
             raise TrailTutorError(f"Invalid operation '{op}' for types {type(left).__name__} and {type(right).__name__}.")

    def visit_UnaryExpression(self, node, env):
        right = self.visit(node.right, env)
        if node.operator == '-':
            return -right
        elif node.operator == 'not':
            return not right

    def visit_ListAccess(self, node, env):
        target_list = env.get(node.identifier.name)
        index = self.visit(node.index_expr, env)
        if not isinstance(target_list, list):
            raise TrailTutorError(f"Cannot use index on '{node.identifier.name}' because it is a {type(target_list).__name__}, not a list.")
        if index < 0 or index >= len(target_list):
            raise TrailTutorError(f"List index {index} out of bounds. The list only has {len(target_list)} items.")
        return target_list[index]

    def visit_InputExpression(self, node, env):
        prompt = self.visit(node.prompt_expr, env)
        return input(str(prompt))

    def visit_Literal(self, node, env):
        return node.value

    def visit_ListLiteral(self, node, env):
        return [self.visit(el, env) for el in node.elements]

    def visit_Identifier(self, node, env):
        return env.get(node.name)