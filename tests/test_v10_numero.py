import sys
import os

# Adiciona a pasta src ao path para permitir imports do pacote inoc
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
    # 1. Casos de Sucesso
    run_test("Inteiro", "! numero(\"42\")")
    run_test("Decimal", "! numero(\"3.1415\")")
    run_test("Negativo", "! numero(\"-50\")")
    run_test("Com espaços", "! numero(\"  100  \")")
    run_test("Já é número", "! numero(10.5)")

    # 2. Casos de Erro (InocRuntimeError esperado)
    print("--- TESTES DE ERRO ESPERADOS ---")
    run_test("Texto inválido", "! numero(\"abc\")")
    run_test("Texto parcialmente numérico", "! numero(\"12abc\")")
    run_test("Vazio", "! numero(\"\")")
    run_test("Múltiplos pontos", "! numero(\"3.1.4\")")
    run_test("Argumentos extras", "! numero(\"10\", \"20\")")
