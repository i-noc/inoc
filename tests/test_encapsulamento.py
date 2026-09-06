import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter

def run_test():
    # Nota: os modulos precisam estar onde o script e executado ou tratar caminho
    code = """
/: TesteEncapsulamento

$ local()
  $: "Local"

! "Chamada local: " + local()
"""
    print("=== TESTE DE ENCAPSULAMENTO v0.5 ===\n")
    lexer = Lexer(code)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    run_test()
