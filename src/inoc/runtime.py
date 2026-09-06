import threading
import queue
from .ast_nodes import AppStmt
from .renderers.tk_renderer import TkRenderer
from .renderers.web_renderer import WebRenderer

class UIRuntime:
    def __init__(self, interpreter, ast):
        self.interpreter = interpreter
        self.ast = ast
        self.app_name = getattr(interpreter, "app_name", "I-NOC")
        self.input_widgets = [] # Usado pelo TkRenderer
        self.input_queue = queue.Queue()
        self.interpreter.input_queue = self.input_queue

        self.color_map = {
            "azul": "blue", "verde": "green", "vermelho": "red",
            "amarelo": "yellow", "preto": "black", "branco": "white",
            "cinza": "gray", "rosa": "pink", "roxo": "purple", "laranja": "orange"
        }
        self.align_map = {
            "centro": "center", "esquerda": "w", "direita": "e",
            "cima": "n", "baixo": "s"
        }

    def run(self):
        # Pré-executa para pegar o app_name e ui_type
        for stmt in self.ast.statements:
            if isinstance(stmt, AppStmt):
                self.interpreter.execute(stmt)
                self.app_name = self.interpreter.app_name
                break

        # Inicia o Interpretador
        threading.Thread(target=self.interpreter.interpret, args=(self.ast,), daemon=True).start()

        ui_type = getattr(self.interpreter, "ui_type", "tk")
        if ui_type == "web":
            renderer = WebRenderer(self)
        else:
            renderer = TkRenderer(self)

        renderer.start()
