import sys
from lexer import tokenize
from parser import Parser
from printer import print_tree

def main():
    # Ensure the user provided enough arguments
    if len(sys.argv) < 3:
        print("Usage: python main.py <command> <filename>")
        print("Commands: lex, parse")
        return

    command = sys.argv[1]
    filename = sys.argv[2]

    # Read the source code from the provided file
    with open(filename, 'r') as file:
        source_code = file.read()

    # Execute the requested command
    if command == 'lex':
        tokens = tokenize(source_code)
        for token_type, value in tokens:
            if token_type == 'EOF':
                print("EOF")
            else:
                print(f"{token_type}({value})")

    elif command == 'parse':
        tokens = tokenize(source_code)
        parser = Parser(tokens)
        try:
            ast_root = parser.parse_program()
            print_tree(ast_root)
        except RuntimeError as e:
            print(f"Trail Syntax Error: {e}")            
                        
    else:
        print(f"Unknown command: {command}. Use 'lex' or 'parse'.")

if __name__ == '__main__':
    main()


