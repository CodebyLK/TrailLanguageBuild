

# 🛤️ Trail Language & Studio IDE

Trail is a high-level, interpreted programming language designed as a pedagogical bridge between human logic and machine execution. Accompanied by **Trail Studio**, a custom-built, hardware-accelerated IDE, this project demonstrates a complete, from-scratch pipeline: from raw character tokenization to Abstract Syntax Tree (AST) evaluation and visual execution.

## 📐 Architecture Overview

The Trail engine is built natively in Python and operates without third-party parsing libraries. It follows a strict, three-phase compilation pipeline:

1. **Lexer (`lexer.py`):** Consumes raw source code strings and generates a stream of categorized, structural `Tokens`.
2. **Parser (`parser.py`):** Processes tokens using recursive descent to enforce Trail's grammar rules, outputting a formalized Abstract Syntax Tree (AST).
3. **Interpreter (`interpreter.py`):** Traverses the AST, managing variable state, evaluating mathematical/logical expressions, and executing programmatic side effects (like `print`).

## 🖥️ Trail Studio (The IDE)

Trail includes a dedicated, frameless desktop environment built with `PyQt6`. Designed to mimic professional development environments, it provides a distraction-free workspace for writing and testing Trail code.

**Key IDE Features:**
* **Custom Frameless UI:** Overrides the native OS window manager for a seamless, edge-to-edge "Deep Blue" workspace.
* **Hardware-Accelerated Rendering:** Utilizes Qt's rendering engine for subpixel font smoothing and sharp UI geometry.
* **Live File Explorer:** Integrates directly with the local file system to manage `.ml` project files.
* **Dynamic Syntax Highlighting:** Real-time regex-based token coloring for Trail keywords, strings, and numeric literals.
* **Pedagogical Cookbook:** Built-in code templates (Hello World, Loops, Conditionals) allow users to instantly load and study syntax examples.
* **Human-Readable Traces:** Execution errors are caught and printed in high-contrast red in the integrated console to facilitate learning and debugging.

## ⚙️ Installation & Setup

To run Trail Studio locally, you need Python installed along with the PyQt6 framework for the UI.

```bash
# 1. Create a virtual environment (Recommended)
python -m venv env

# 2. Activate the environment
# Windows:
env\Scripts\activate
# Mac/Linux:
source env/bin/activate

# 3. Install the UI Engine
pip install PyQt6

# 4. Launch Trail Studio
python src/trail_gui.py

```

## 📖 Trail Syntax Examples

Trail is designed to be highly readable, favoring explicit block closures (`end`) over curly braces to help beginners visualize scope.

### Variable Assignment & Output

```lua
var status = "Trail Engine Online";
var version = 2.0;

print(status);

```

### Conditionals

```lua
var code = 200;

if code == 200 then
    print("Execution Successful");
else
    print("Execution Failed");
end

```

### Iteration (While Loops)

```lua
var count = 1;

while count < 5 do
    print(count);
    var count = count + 1;
end

```

## 🛡️ Error Handling

A core requirement of Trail's design is comprehensive error handling. The language engine is built to catch logical impossibilities (like adding numbers to strings) and syntactical mistakes, reporting them gracefully to the IDE terminal rather than crashing the host Python process.

