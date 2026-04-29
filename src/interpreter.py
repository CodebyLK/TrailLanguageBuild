from ast_nodes import *

class TrailTutorError(Exception): pass
class BreakException(Exception): pass
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
            raise TrailTutorError(f"Scope Error: You tried to update the variable '{name}', but it hasn't been created yet. Did you mean to initialize it with 'var {name} = ...'?")

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise TrailTutorError(f"Scope Error: You tried to use the variable '{name}', but it hasn't been created yet. Did you misspell it, or did you forget to initialize it first using 'var {name} = ...'?")

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, node):
        try:
            return self.visit(node, self.env)
        except TrailTutorError as e:
            print(f"\n[Trail Tutor] {e}")
        except RecursionError:
            print("\n[Trail Tutor] Logic Error: Infinite recursion detected. Make sure your function has a base case to stop calling itself.")

    def visit(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Program(self, node, env):
        try:
            for stmt in node.statements:
                self.visit(stmt, env)
        except BreakException:
            # --- TUTOR: MISPLACED BREAK ---
            raise TrailTutorError("Flow Error: You used a 'break' statement outside of a loop! 'break' is only used to escape a 'while' loop.")
        except ReturnException:
            # --- TUTOR: MISPLACED RETURN ---
            raise TrailTutorError("Flow Error: You used a 'return' statement outside of a function! 'return' is only meant to send a value back from a function.")

    def visit_VarDeclaration(self, node, env):
        value = self.visit(node.expression, env)
        env.define(node.identifier.name, value)

    def visit_Assignment(self, node, env):
        value = self.visit(node.expression, env)
        if node.index_expr:
            target_list = env.get(node.identifier.name)
            index = self.visit(node.index_expr, env)
            
            if not isinstance(target_list, list):
                raise TrailTutorError(f"Type Error: Cannot use a list index on '{node.identifier.name}' because it is a {type(target_list).__name__}, not a List.")
            if not isinstance(index, int):
                raise TrailTutorError(f"Type Error: A list index must be an integer, but you provided a {type(index).__name__}.")
            
            if index < 0 or index >= len(target_list):
                max_idx = len(target_list) - 1 if len(target_list) > 0 else 0
                raise TrailTutorError(f"List Boundary Error: You tried to modify item {index}, but your list only has {len(target_list)} items. Remember, computer lists start counting at 0! Valid indexes for this list are 0 through {max_idx}.")
            
            target_list[index] = value
        else:
            env.assign(node.identifier.name, value)

    def visit_PrintStatement(self, node, env):
        value = self.visit(node.expression, env)
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
            raise TrailTutorError(f"Type Error: '{node.name}' is not a function.")
        if len(node.args) != len(func.params):
            raise TrailTutorError(f"Argument Error: Function '{node.name}' expects {len(func.params)} arguments, but you gave it {len(node.args)}.")
        
        call_env = Environment(env)
        for param, arg_expr in zip(func.params, node.args):
            call_env.define(param, self.visit(arg_expr, env))
            
        try:
            for stmt in func.body:
                self.visit(stmt, call_env)
        except ReturnException as r:
            return r.value
        except BreakException:
            # Catch a break that escaped a loop inside a function
            raise TrailTutorError("Flow Error: You used a 'break' statement outside of a loop! 'break' is only used to escape a 'while' loop.")
        return None

    def visit_ReturnStatement(self, node, env):
        value = self.visit(node.value, env) if node.value else None
        raise ReturnException(value)

    def visit_BinaryExpression(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.operator

        if op in ('+', '-', '*', '/', '%', '<', '>', '<=', '>='):
            if type(left) != type(right) and not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                 raise TrailTutorError(
                     f"Type Mismatch: You are trying to use '{op}' between a {type(left).__name__} and a {type(right).__name__}. "
                     f"Trail doesn't guess what you mean. If you want to do math, make sure both are numbers. If you want to combine text, make sure both are strings!"
                 )

        try:
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/':
                if right == 0: 
                    raise TrailTutorError("Math Error: You attempted to divide by zero, which is mathematically impossible! Check your logic to ensure your denominator variable isn't accidentally set to 0.")
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
        
        # --- TUTOR: UNARY TYPE SAFETY ---
        if node.operator == '-': 
            if not isinstance(right, (int, float)) or isinstance(right, bool):
                raise TrailTutorError(f"Type Mismatch: You tried to make a {type(right).__name__} negative using '-'. You can only make numbers negative!")
            return -right
        elif node.operator == 'not': 
            if not isinstance(right, bool):
                raise TrailTutorError(f"Type Mismatch: You used 'not' on a {type(right).__name__}. 'not' is a logical operator and only works with True or False.")
            return not right

    def visit_ListAccess(self, node, env):
        target_list = env.get(node.identifier.name)
        index = self.visit(node.index_expr, env)
        
        if not isinstance(target_list, list):
            raise TrailTutorError(f"Type Error: Cannot use a list index on '{node.identifier.name}' because it is a {type(target_list).__name__}, not a List.")
        
        if index < 0 or index >= len(target_list):
            max_idx = len(target_list) - 1 if len(target_list) > 0 else 0
            raise TrailTutorError(f"List Boundary Error: You tried to access item {index}, but your list only has {len(target_list)} items. Remember, computer lists start counting at 0! Valid indexes for this list are 0 through {max_idx}.")
            
        return target_list[index]

    def visit_InputExpression(self, node, env):
        prompt = self.visit(node.prompt_expr, env)
        user_in = input(str(prompt))
        
        # --- TUTOR: SMART CASTING FOR BEGINNERS ---
        try:
            if '.' in user_in: return float(user_in)
            return int(user_in)
        except ValueError:
            if user_in.lower() == 'true': return True
            if user_in.lower() == 'false': return False
            return user_in

    def visit_Literal(self, node, env):
        return node.value

    def visit_ListLiteral(self, node, env):
        return [self.visit(el, env) for el in node.elements]

    def visit_Identifier(self, node, env):
        return env.get(node.name)