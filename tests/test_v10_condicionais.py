import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter

def run_test(name, code):
    print(f"--- TESTE v1.0: {name} ---")
    try:
        lexer = Lexer(code)
        tokens = lexer.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Erro Inesperado: {e}")
    print("--------------------------\n")

if __name__ == "__main__":
    # 1. ? sem £
    run_test("? sem £", "? true\n  ! \"OK\"")

    # 2. ? + £
    run_test("? + £", "? false\n  ! \"Nao\"\n£\n  ! \"OK (£)\"")

    # 3. ? + else if
    run_test("? + else if", "? false\n  ! \"Um\"\nelse if true\n  ! \"Dois (else if)\"\n£\n  ! \"Tres\"")

    # 4. Vários else if
    code4 = """
cor = "vermelho"
? cor == "azul"
  ! "Azul"
else if cor == "vermelho"
  ! "Vermelho"
else if cor == "amarelo"
  ! "Amarelo"
£
  ! "Desconhecido"
"""
    run_test("Múltiplos else if", code4)

    # 5. £ sem ?
    run_test("£ sem ?", "£\n  ! \"Erro\"")

    # 6. Rejeição ??
    run_test("Rejeição ??", "? true\n  ! \"OK\"\n??\n  ! \"Erro\"")
