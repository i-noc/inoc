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

    # Executa a declaração da UI primeiro para preencher o registry
    for stmt in ast.statements:
        if not isinstance(stmt, (WhileStmt, ForEachStmt, EventStmt)):
             interpreter.execute(stmt)

    # Simula a chegada de dados da UI
    if inputs_map:
        for tid, tval in inputs_map.items():
            interpreter._builtin_definir([tid, tval])

    if event:
        interpreter.event_queue.put(event)

    try:
        interpreter.interpret(ast)
        return interpreter
    except InocRuntimeError as e:
        print(f"ERRO: {e.message}")
        return None

print("--- TESTE DISTINCAO: UI ID vs Variavel ---")
source = """
|#input "valor_ui"| # id = campo
campo = "valor_logica"
! @ campo
! campo
"""
interp = run_test(source, {"campo": "valor_ui_modificado"})
# Esperado:
# > valor_ui_modificado
# > valor_logica

print("\n--- TESTE DISTINCAO: Mesmos Nomes ---")
source2 = """
|#input "valor_inicial"| # id = email
email = @ email
! "Variavel email: " + email
! "UI email: " + @ email
"""
interp2 = run_test(source2, {"email": "novo@email.com"})
# Esperado:
# > Variavel email: novo@email.com
# > UI email: novo@email.com

print("\n--- TESTE PROTECAO: Acesso ID sem @ ---")
source3 = """
|#input ""| # id = meu_id
! meu_id
"""
interp3 = run_test(source3) # Deve dar erro de variavel nao definida
