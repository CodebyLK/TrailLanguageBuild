import sys
import os
import io

# ==========================================
# PATHING FIX
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# ==========================================
# TRAIL ENGINE IMPORTS
# ==========================================
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame,
                             QTreeView, QFileDialog, QComboBox)
from PyQt6.QtGui import (QFont, QColor, QSyntaxHighlighter, QTextCharFormat,
                         QMouseEvent, QFileSystemModel)
from PyQt6.QtCore import Qt, QRegularExpression

# ==========================================
# FUNCTIONAL TITLE BAR
# ==========================================
class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(35)
        self.setStyleSheet("background-color: #0D1117; border-bottom: 1px solid #1E293B;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 0, 0)

        self.title = QLabel("Trail Studio - Unsaved")
        self.title.setStyleSheet("color: #8B949E; font-size: 12px; font-family: 'Segoe UI'; font-weight: bold;")
        layout.addWidget(self.title)

        layout.addStretch()

        btn_style = "QPushButton { background-color: transparent; color: #8B949E; border: none; font-size: 14px; } QPushButton:hover { background-color: #1E293B; color: #E2E8F0; }"
        close_style = "QPushButton { background-color: transparent; color: #8B949E; border: none; font-size: 14px; } QPushButton:hover { background-color: #E81123; color: #FFFFFF; }"

        min_btn = QPushButton("─")
        min_btn.setFixedSize(45, 35)
        min_btn.setStyleSheet(btn_style)
        min_btn.clicked.connect(self.parent_window.showMinimized)

        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(45, 35)
        self.max_btn.setStyleSheet(btn_style)
        self.max_btn.clicked.connect(self.toggle_maximize)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(45, 35)
        close_btn.setStyleSheet(close_style)
        close_btn.clicked.connect(self.parent_window.close)

        layout.addWidget(min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(close_btn)

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent_window.showMaximized()
            self.max_btn.setText("❐")

    def set_title(self, filename):
        self.title.setText(f"Trail Studio - {filename}")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.parent_window.isMaximized():
            self.click_pos = event.globalPosition().toPoint() - self.parent_window.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if hasattr(self, 'click_pos') and event.buttons() == Qt.MouseButton.LeftButton and not self.parent_window.isMaximized():
            self.parent_window.move(event.globalPosition().toPoint() - self.click_pos)
            event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
            event.accept()

# ==========================================
# SYNTAX HIGHLIGHTER
# ==========================================
class TrailHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF79C6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [r'\bvar\b', r'\bif\b', r'\bthen\b', r'\belse\b', r'\bend\b',
                    r'\bwhile\b', r'\bdo\b', r'\bfunction\b', r'\breturn\b', r'\bprint\b']
        for word in keywords:
            self.rules.append((QRegularExpression(word), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#50FA7B"))
        self.rules.append((QRegularExpression(r'"[^"\n]*"'), string_format))

        num_format = QTextCharFormat()
        num_format.setForeground(QColor("#FFB86C"))
        self.rules.append((QRegularExpression(r'\b\d+(\.\d+)?\b'), num_format))

    def highlightBlock(self, text: str) -> None:
        for expression, format in self.rules:
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

# ==========================================
# MAIN APPLICATION
# ==========================================
class TrailStudio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint)
        self.resize(1200, 800)
        self.current_file = None

        self.setStyleSheet("""
            QMainWindow { background-color: #0D1117; }
            
            QFrame#Sidebar { background-color: #0F172A; border-right: 1px solid #1E293B; }
            QFrame#Toolbar { background-color: #162032; border-bottom: 1px solid #1E293B; }
            QFrame#StatusBar { background-color: #007ACC; }
            
            QTreeView { 
                background-color: transparent; color: #94A3B8; border: none; font-family: 'Segoe UI'; font-size: 13px;
            }
            QTreeView::item:selected { background-color: #1E293B; color: #E2E8F0; }
            
            QTextEdit#Editor { 
                background-color: #162032; color: #E2E8F0; border: none; font-family: 'Cascadia Code', 'Consolas';
                font-size: 15px; padding: 15px; line-height: 1.5;
            }
            
            QTextEdit#Console { 
                background-color: #0D1117; color: #94A3B8; border-top: 1px solid #1E293B;
                font-family: 'Cascadia Code', 'Consolas'; font-size: 14px; padding: 15px;
            }

            QPushButton.ActionBtn, QComboBox.Dropdown {
                background-color: transparent; color: #94A3B8; border: 1px solid #1E293B;
                border-radius: 4px; font-family: 'Segoe UI'; font-weight: bold; padding: 6px 12px;
            }
            QPushButton.ActionBtn:hover, QComboBox.Dropdown:hover { background-color: #1E293B; color: #E2E8F0; }
            QComboBox.Dropdown QAbstractItemView {
                background-color: #0D1117; color: #E2E8F0; selection-background-color: #1E293B; border: 1px solid #1E293B;
            }
            
            QPushButton#RunBtn {
                background-color: #38BDF8; color: #0D1117; border-radius: 4px;
                font-family: 'Segoe UI'; font-weight: bold; padding: 6px 20px;
            }
            QPushButton#RunBtn:hover { background-color: #7DD3FC; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Title Bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        workspace_layout = QHBoxLayout()
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # 2. Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 15, 10, 10)

        lbl_explorer = QLabel("LIVE EXPLORER")
        lbl_explorer.setStyleSheet("color: #64748B; font-size: 11px; font-weight: bold; font-family: 'Segoe UI'; padding-left: 5px;")
        sidebar_layout.addWidget(lbl_explorer)

        project_root = os.path.dirname(current_dir)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(project_root)

        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(project_root))
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setHeaderHidden(True)
        self.tree.doubleClicked.connect(self.tree_open_file)

        sidebar_layout.addWidget(self.tree)
        workspace_layout.addWidget(sidebar)

        # 3. Editor Column
        editor_column = QWidget()
        editor_layout = QVBoxLayout(editor_column)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        toolbar = QFrame()
        toolbar.setObjectName("Toolbar")
        toolbar.setFixedHeight(45)
        tool_layout = QHBoxLayout(toolbar)
        tool_layout.setContentsMargins(15, 0, 15, 0)

        # --- NEW: THE COOKBOOK DROPDOWN ---
        self.cookbook = QComboBox()
        self.cookbook.setProperty("class", "Dropdown")
        self.cookbook.addItems(["Cookbook Examples...", "1. Hello World", "2. Basic Loop", "3. Conditionals"])
        self.cookbook.currentIndexChanged.connect(self.load_cookbook)
        tool_layout.addWidget(self.cookbook)

        btn_open = QPushButton("Open File")
        btn_open.setProperty("class", "ActionBtn")
        btn_open.clicked.connect(self.open_file)

        btn_save = QPushButton("Save File")
        btn_save.setProperty("class", "ActionBtn")
        btn_save.clicked.connect(self.save_file)

        tool_layout.addWidget(btn_open)
        tool_layout.addWidget(btn_save)
        tool_layout.addStretch()

        self.run_btn = QPushButton("▶ Run Code")
        self.run_btn.setObjectName("RunBtn")
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_code)
        tool_layout.addWidget(self.run_btn)

        editor_layout.addWidget(toolbar)

        self.editor = QTextEdit()
        self.editor.setObjectName("Editor")
        self.editor.setAcceptRichText(False)
        self.highlighter = TrailHighlighter(self.editor.document())
        self.editor.cursorPositionChanged.connect(self.update_status)
        editor_layout.addWidget(self.editor)

        self.console = QTextEdit()
        self.console.setObjectName("Console")
        self.console.setReadOnly(True)
        self.console.setFixedHeight(220)
        editor_layout.addWidget(self.console)

        workspace_layout.addWidget(editor_column)
        main_layout.addLayout(workspace_layout)

        # 4. Status Bar
        status_bar = QFrame()
        status_bar.setObjectName("StatusBar")
        status_bar.setFixedHeight(24)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(15, 0, 15, 0)

        self.status_lbl = QLabel("Ln 1, Col 1")
        self.status_lbl.setStyleSheet("color: #FFFFFF; font-family: 'Segoe UI'; font-size: 11px; font-weight: bold;")
        status_layout.addWidget(self.status_lbl)

        status_layout.addStretch()

        engine_lbl = QLabel("Trail Language Engine | UTF-8")
        engine_lbl.setStyleSheet("color: #FFFFFF; font-family: 'Segoe UI'; font-size: 11px;")
        status_layout.addWidget(engine_lbl)

        main_layout.addWidget(status_bar)

        self.editor.setText('var engine = "Ready";\nprint(engine);')

    # --- FUNCTIONALITY ---

    # Loads pre-written Trail scripts into the editor
    def load_cookbook(self):
        choice = self.cookbook.currentText()
        if choice == "1. Hello World":
            self.editor.setText('var msg = "Hello from Trail!";\nprint(msg);')
        elif choice == "2. Basic Loop":
            self.editor.setText('var count = 1;\nwhile count < 5 do\n    print(count);\n    var count = count + 1;\nend')
        elif choice == "3. Conditionals":
            self.editor.setText('var status = 200;\nif status == 200 then\n    print("Success");\nelse\n    print("Error");\nend')

        # Reset dropdown to default after selection
        self.cookbook.setCurrentIndex(0)
        self.title_bar.set_title("Unsaved Example")

    def update_status(self):
        cursor = self.editor.textCursor()
        ln = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_lbl.setText(f"Ln {ln}, Col {col}")

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", current_dir, "All Files (*);;Trail Files (*.ml)")
        if filename:
            self.load_file_to_editor(filename)

    def tree_open_file(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            self.load_file_to_editor(path)

    def load_file_to_editor(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.editor.setText(f.read())
            self.current_file = filename
            self.title_bar.set_title(os.path.basename(filename))
        except Exception as e:
            # Displays file load errors in red
            self.console.setHtml(f'<span style="color: #FF79C6;">File Error: {e}</span>')

    def save_file(self):
        if not self.current_file:
            self.current_file, _ = QFileDialog.getSaveFileName(self, "Save File", current_dir, "Trail Files (*.ml);;All Files (*)")

        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.title_bar.set_title(os.path.basename(self.current_file))

    def run_code(self):
        self.console.clear()
        code = self.editor.toPlainText().strip()
        if not code: return

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            tokens = tokenize(code)
            ast = Parser(tokens).parse_program()
            Interpreter().interpret(ast)

            # Print successful output normally
            output = new_stdout.getvalue()
            # Replace newlines with HTML breaks to format correctly in rich text
            self.console.setHtml(f'<span style="color: #E2E8F0;">{output.replace(chr(10), "<br>")}</span>')

        except Exception as e:
            # Prints the human-readable errors generated by your backend in Bright Red
            self.console.setHtml(f'<span style="color: #E81123; font-weight: bold;">[Trail Error] {e}</span>')
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrailStudio()
    window.show()
    sys.exit(app.exec())