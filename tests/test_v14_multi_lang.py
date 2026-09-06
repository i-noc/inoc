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

print("--- TESTE v1.4: Equivalencia de Keywords ---")
source_en = "x = true and not false"
source_pt = "x = verdadeiro e não falso"

interp_en = run_test(source_en)
interp_pt = run_test(source_pt)

print(f"EN: {interp_en.globals['x']}")
print(f"PT: {interp_pt.globals['x']}")
assert interp_en.globals['x'] == interp_pt.globals['x']

print("\n--- TESTE v1.4: Equivalencia de Elementos e Propriedades ---")
source_ui_en = """
|#input "Initial"| # id = user, color = "blue"
"""
source_ui_pt = """
|#entrada "Initial"| # id = usuario, cor = "blue"
"""

interp_ui_en = run_test(source_ui_en)
interp_ui_pt = run_test(source_ui_pt)

el_en = interp_ui_en._find_element_by_id(interp_ui_en.ui_registry.values(), "user")
el_pt = interp_ui_pt._find_element_by_id(interp_ui_pt.ui_registry.values(), "usuario")

print(f"EN Type: {el_en['type']}, EN Color: {el_en['props']['cor']}")
print(f"PT Type: {el_pt['type']}, PT Color: {el_pt['props']['cor']}")
# Note: internally it always normalizes to the original code terms
assert el_en['type'] == 'input'
assert el_pt['type'] == 'input'
assert el_en['props']['cor'] == 'blue'
assert el_pt['props']['cor'] == 'blue'

print("\n--- TESTE v1.4: Equivalencia de Built-ins ---")
source_fn_en = "s = size([1,2,3])"
source_fn_pt = "s = tamanho([1,2,3])"

interp_fn_en = run_test(source_fn_en)
interp_fn_pt = run_test(source_fn_pt)

print(f"EN size: {interp_fn_en.globals['s']}")
print(f"PT size: {interp_fn_pt.globals['s']}")
assert interp_fn_en.globals['s'] == interp_fn_pt.globals['s']

print("\nTESTES MULTILINGUE CONCLUIDOS!")
