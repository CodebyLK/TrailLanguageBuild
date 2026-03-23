***

# Trail Language - Phase 1: Lexer and Parser

**Trail** is a high-level, interpreted language designed as a pedagogical bridge between human logic and machine execution. It is built with a focus on readability, helpful diagnostics, and simplicity to optimize the learning experience for computer science students.

This repository contains Phase 1 of the Trail implementation, which includes a working lexical analyzer (lexer), a recursive descent parser, and an Abstract Syntax Tree (AST) generator.

## 📁 Repository Structure

Based on the project requirements, the repository is organized as follows:

* **`src/`**: Contains the core language implementation.
  * **`trail.py`**: The main command-line interface (CLI) entry point.
  * **`lexer.py`**: Contains the `tokenize` function using Python's regular expressions.
  * **`parser.py`**: The handwritten recursive descent parser that builds the AST.
  * **`ast_nodes.py`**: Defines the object structures for the AST nodes.
  * **`printer.py`**: Contains the utility to print the AST in an indented tree format.
* **`tests/`**: A directory containing 10 valid `.ml` test programs and 5 invalid test programs.
* **`README.md`**: Project documentation and execution instructions.

## 🚀 How to Run

The tool is exposed through a simple command-line interface. You can run it using Python 3 from the root directory of the project.

### 1. Lexical Analysis (Tokenization)
To read a source file and produce a stream of tokens, use the `lex` command:
```bash
python src/trail.py lex tests/test1_valid.ml
```

### 2. Parsing (AST Generation)
To read a source file, tokenize it, parse it according to the grammar rules, and output the indented Abstract Syntax Tree, use the `parse` command:
```bash
python src/trail.py parse tests/test1_valid.ml
```

*Note: If the parser encounters a syntax error, it implements a "fail-fast" immediate abort and prints a simple error message.*

## 📜 Language Grammar (EBNF)

The parser implements strict precedence and associativity (left-associative with standard mathematical precedence). The Phase 1 subset of the Trail grammar is defined as follows:

```ebnf
program       → statement* EOF
statement     → assignment | print_stmt
assignment    → 'var' IDENTIFIER '=' expression ';'
print_stmt    → 'print' '(' expression ')' ';'
expression    → term (('+' | '-') term)*
term          → factor (('*' | '/') factor)*
factor        → INTEGER | IDENTIFIER | '(' expression ')'
```
*Note: Whitespace is ignored during lexical analysis. Identifiers must start with an alphabetic character followed by alphanumeric characters.*

## 🏗️ Architecture Overview

The Phase 1 pipeline follows a classic compiler frontend model: `Source Code → Lexer → Tokens → Parser → AST → Printed Representation`.

1.  **Lexer (Scanner):** Implemented using Python's `re` (RegEx) module. It scans the raw source code string and converts it into a sequence of meaningful tokens (e.g., `VAR`, `IDENTIFIER`, `INTEGER`, `PLUS`).
2.  **Parser:** A handwritten Recursive Descent (Top-Down) parser. It maps each grammar rule directly to a Python function (e.g., `parse_expression`, `parse_term`). This avoids external dependencies and allows for highly customized error handling.
3.  **Abstract Syntax Tree (AST):** The parser outputs a structured object model representing the logical execution flow of the code. Instead of strings, the tree consists of strongly-typed nodes like `BinaryExpression` and `AssignmentStatement`. 

***
