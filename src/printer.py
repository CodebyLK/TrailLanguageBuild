from ast_nodes import *

def print_tree(node, indent=0):
    spacing = "  " * indent
    name = type(node).__name__
    
    if isinstance(node, Program):
        print(f"{spacing}{name}")
        for stmt in node.statements:
            print_tree(stmt, indent + 1)
            
    elif isinstance(node, AssignmentStatement):
        print(f"{spacing}{name}")
        print_tree(node.identifier, indent + 1)
        print_tree(node.expression, indent + 1)
        
    elif isinstance(node, PrintStatement):
        print(f"{spacing}{name}")
        print_tree(node.expression, indent + 1)
        
    elif isinstance(node, BinaryExpression):
        print(f"{spacing}{name}({node.operator})")
        print_tree(node.left, indent + 1)
        print_tree(node.right, indent + 1)
        
    elif isinstance(node, Identifier):
        print(f"{spacing}{name}({node.name})")
        
    elif isinstance(node, IntegerLiteral):
        print(f"{spacing}{name}({node.value})")


# Test for printer

if __name__ == '__main__':
    from lexer import tokenize
    from parser import Parser

    # Test code from your specification
    sample_code = "x = 1; y = x + 2; print y;"
    
    tokens = tokenize(sample_code)
    parser = Parser(tokens)
    ast_root = parser.parse_program()
    
    print_tree(ast_root)

    