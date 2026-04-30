import customtkinter as ctk
import sys
import io
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

ctk.set_appearance_mode("dark")

class TrailIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        bg_color = "#1B2845"
        editor_bg = "#274060"
        btn_bg = "#4C86C0"
        btn_hover = "#65AFFF"
        text_color = "#FFFFFF"
        console_bg = "#0B111D" 
        console_fg = "#5899E2"

        self.title("Trail Language Editor")
        self.geometry("900x700")
        
        self.configure(fg_color=bg_color)

        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(4, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.editor_label = ctk.CTkLabel(
            self, text="Trail Source Code", font=ctk.CTkFont(size=16, weight="bold"), text_color=text_color
        )
        self.editor_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.editor = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=15), corner_radius=10, 
            fg_color=editor_bg, text_color=text_color
        )
        self.editor.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.editor.insert("0.0", 'var grade = 85;\n\nif grade >= 60 then\n    print("You passed!");\nelse\n    print("Try again!");\nend\n')

        self.run_btn = ctk.CTkButton(
            self, text="▶ Run Trail Code", font=ctk.CTkFont(size=15, weight="bold"), 
            height=40, corner_radius=8, command=self.run_code,
            fg_color=btn_bg, hover_color=btn_hover, text_color=text_color
        )
        self.run_btn.grid(row=2, column=0, padx=20, pady=10)

        self.console_label = ctk.CTkLabel(
            self, text="Tutor Console Output", font=ctk.CTkFont(size=16, weight="bold"), text_color=text_color
        )
        self.console_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")

        self.console = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=15), 
            fg_color=console_bg, text_color=console_fg, corner_radius=10
        )
        self.console.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def run_code(self):
        self.console.delete("0.0", "end")
        
        source_code = self.editor.get("0.0", "end").strip()
        if not source_code:
            return

        def gui_input(prompt_text):
            dialog = ctk.CTkInputDialog(text=prompt_text, title="Trail Input Request")
            return dialog.get_input()

        old_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            tokens = tokenize(source_code)
            parser = Parser(tokens)
            ast_root = parser.parse_program()
            
            interpreter = Interpreter(input_hook=gui_input)
            interpreter.interpret(ast_root)
            
        except Exception as e:
            print(f"\n[Trail Compiler Error] {e}")
            
        finally:
            sys.stdout = old_stdout
            self.console.insert("0.0", captured_output.getvalue())

if __name__ == "__main__":
    app = TrailIDE()
    app.mainloop()