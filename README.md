# Trail Language - Final Implementation

**Trail** is a high-level, interpreted programming language designed as a pedagogical bridge between human logic and machine execution. Built specifically to lower the cognitive barrier for computer science students, Trail focuses on readability, strict logical enforcement, and a highly informative diagnostic system.

This repository contains the Final Phase implementation of Trail, progressing from the Phase 1 Lexer/Parser into a fully Turing-complete language with a custom tree-walking evaluator, interactive desktop IDE, and the "Tutor" error-handling system.

## 📁 Repository Structure

* **`src/`**: Contains the core language implementation.
  * **`trail.py`**: The main command-line interface (CLI) entry point.
  * **`lexer.py`**: Contains the scanner, tokenizing code via regular expressions with protections for unclosed strings.
  * **`parser.py`**: A handwritten recursive descent parser that translates tokens into the AST.
  * **`ast_nodes.py`**: Defines the strongly-typed object structures for the AST nodes.
  * **`interpreter.py`**: The tree-walking evaluator that executes the AST and houses the pedagogical "Tutor" safety nets.
  * **`trail_gui.py`**: The modern desktop IDE built using `customtkinter`.
* **`tests/`**: A directory containing valid `.ml` test programs (to demonstrate logic, loops, and functions) and invalid test programs (to demonstrate the Tutor's error interventions).
* **`README.md`**: Project documentation and execution instructions.

## 🚀 How to Run

Trail can be executed either through its dedicated graphical IDE or via the traditional command-line interface. 

### 1. The Trail IDE (Recommended)
The project includes a modern, dark-mode desktop editor. Ensure you are working within a virtual environment, install the UI dependency, and launch the editor:
```bash
pip install customtkinter
python src/trail_gui.py
```

### 2. Command-Line Execution
To run Trail scripts directly from the terminal, use the `run` command:
```bash
python src/trail.py run tests/test14_whileloop_valid.ml
```

*You can also still access Phase 1 pipeline tools:*
* `python src/trail.py lex <file>` : Outputs the raw token stream.
* `python src/trail.py parse <file>` : Outputs the indented Abstract Syntax Tree.

## 🌟 Core Language Features

* **The Tutor Interpreter:** Instead of failing with obscure Python stack traces, Trail intercepts common beginner mistakes (scope confusion, type mismatches, out-of-bounds array access, misplaced flow control) and provides plain-text, contextual explanations to teach the student how to fix their code.
* **Dynamic but Strong Typing:** Variables can hold any data type and be reassigned dynamically. However, implicit type coercion is strictly forbidden. Adding a String to an Integer will trigger a Tutor error, forcing the student to understand distinct data structures.
* **First-Class Functions:** Supports user-defined functions with localized scope, parameter passing, and return values.
* **Dynamic Data Structures:** Natively supports heterogeneous arrays/lists with index-based access and modification.

## 📜 Language Grammar (EBNF)

The parser implements strict precedence and associativity. The finalized Trail grammar is defined as follows:

```ebnf
program       → statement* EOF
statement     → var_decl | assignment | print_stmt | if_stmt | while_stmt | func_decl | return_stmt | break_stmt | expr_stmt
var_decl      → 'var' IDENTIFIER '=' expression ';'
assignment    → IDENTIFIER ('[' expression ']')? '=' expression ';'
print_stmt    → 'print' '(' expression ')' ';'
if_stmt       → 'if' expression 'then' statement* ('else' statement*)? 'end'
while_stmt    → 'while' expression 'do' statement* 'end'
func_decl     → 'function' IDENTIFIER '(' parameters? ')' statement* 'end'
parameters    → IDENTIFIER (',' IDENTIFIER)*
return_stmt   → 'return' expression? ';'
break_stmt    → 'break' ';'
expr_stmt     → expression ';'

expression    → logical_or
logical_or    → logical_and ('or' logical_and)*
logical_and   → equality ('and' equality)*
equality      → relational (('==' | '!=') relational)*
relational    → additive (('<' | '>' | '<=' | '>=') additive)*
additive      → term (('+' | '-') term)*
term          → factor (('*' | '/' | '%') factor)*
unary         → ('-' | 'not') unary | factor
factor        → INTEGER | FLOAT | STRING | 'true' | 'false' | IDENTIFIER 
              | list_literal | list_access | function_call | input_call | '(' expression ')'

list_literal  → '[' arguments? ']'
list_access   → IDENTIFIER '[' expression ']'
function_call → IDENTIFIER '(' arguments? ')'
input_call    → 'input' '(' expression ')'
arguments     → expression (',' expression)*
```

## 🏗️ Architecture Overview

The final pipeline expands on the Phase 1 compiler frontend by attaching a semantic execution backend: `Source Code → Lexer → Parser → AST → Interpreter → Standard Output`.

1. **Lexer (Scanner):** Converts raw strings into meaningful tokens, catching lexical typos (like unclosed quotes).
2. **Parser (Recursive Descent):** Maps grammar rules directly to Python functions. It enforces strict structural rules (e.g., matching parentheses and block closures).
3. **Abstract Syntax Tree (AST):** A strongly-typed object model representing the logical flow.
4. **Interpreter (Tree-Walker):** Traverses the AST to execute the program. It manages the `Environment` (memory and variable scoping) and evaluates expressions. It is wrapped in the `TrailTutorError` architecture to safely intercept and explain illegal operations at runtime.
5. **GUI Wrapper:** Routes standard output (`sys.stdout`) from the Python console into a modernized `customtkinter` text widget to provide a seamless user experience.
