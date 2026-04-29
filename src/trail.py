import sys
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 3:
        print("Usage: python trail.py <command> <filename>")
        print("Commands:")
        print("  lex   - Tokenizes the file and prints tokens")
        print("  parse - Parses the file and runs syntax check")
        print("  run   - Interprets and executes the Trail program")
        return

    command = sys.argv[1]
    filename = sys.argv[2]

    try:
        with open(filename, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        return

    try:
        tokens = tokenize(source_code)
        
        if command == 'lex':
            for token in tokens:
                print(token)
                
        elif command == 'parse':
            parser = Parser(tokens)
            ast_root = parser.parse_program()
            print("Syntax OK. AST built successfully.")
            
        elif command == 'run':
            parser = Parser(tokens)
            ast_root = parser.parse_program()
            interpreter = Interpreter()
            interpreter.interpret(ast_root)
            
        else:
            print(f"Unknown command: {command}. Use 'lex', 'parse', or 'run'.")
            
    except RuntimeError as e:
        # Catch standard lexer/parser errors
        print(f"\n[Trail Compiler Error] {e}")

if __name__ == '__main__':
    main()