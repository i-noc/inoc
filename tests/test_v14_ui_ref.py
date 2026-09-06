import sys
import os

# Adiciona o diretório 'src' ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter, InocRuntimeError
from inoc.ast_nodes import WhileStmt, ForEachStmt, EventStmt

def run_test(source, inputs_map=None, event=None):
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()

    # 1. Executa declaracoes iniciais (UI e variaveis)
    for stmt in ast.statements:
        if not isinstance(stmt, (WhileStmt, ForEachStmt, EventStmt)):
             interpreter.execute(stmt)

    # 2. Simula usuario digitando
    if inputs_map:
        for tid, tval in inputs_map.items():
            interpreter._builtin_definir([tid, tval])

    if event:
        interpreter.event_queue.put(event)

    # Executa o resto
    for stmt in ast.statements:
        if isinstance(stmt, (WhileStmt, ForEachStmt, EventStmt)):
             interpreter.execute(stmt)

    return interpreter

print("--- TESTE v1.4: Referencia Simples |id| ---")
source1 = """
|#texto ""| # id = feedback
x = |feedback|
! x
"""
interp1 = run_test(source1)
# Deve imprimir 'feedback'

print("\n--- TESTE v1.4: Uso em definir(|id|) ---")
source2 = """
|#texto "v1"| # id = info
definir(|info|, "v2")
! @ info
"""
interp2 = run_test(source2)
# Deve imprimir 'v2'

print("\n--- TESTE v1.4: Coexistencia id, @id, |id| ---")
source3 = """
|#input "valor_ui"| # id = campo
campo = "valor_logica"
! campo
! @ campo
! |campo|
"""
interp3 = run_test(source3)
# Esperado:
# > valor_logica
# > valor_ui
# > campo

print("\n--- TESTE v1.4: Rejeicao de expressoes complexas ---")
def test_syntax_error(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    parser.parse()
    if len(parser.errors) > 0:
        print(f"Sucesso: Erro capturado: {parser.errors[0]['message']}")
    else:
        print("ERRO: Deveria ter falhado!")

test_syntax_error("x = |a + b|")
test_syntax_error("x = |123|")

print("\n--- TESTE v1.4: ID Inexistente em definir ---")
source4 = """
definir(|inexistente|, "msg")
"""
try:
    run_test(source4)
except Exception as e:
    print(f"Sucesso: Erro capturado: {e}")

print("\n--- TESTE v1.4: Compatibilidade definir('id') ---")
source5 = """
|#texto "v1"| # id = info
definir("info", "v3")
! @ info
"""
interp5 = run_test(source5)
# Deve imprimir 'v3'

print("\nTESTES v1.4 CONCLUIDOS!")
