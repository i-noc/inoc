import sys
import os
import queue

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
            # Simula o que o renderer faz: atualiza o ui_registry
            interpreter._builtin_definir([tid, tval])

    if event:
        interpreter.event_queue.put(event)

    try:
        interpreter.interpret(ast)
        return interpreter
    except InocRuntimeError as e:
        print(f"ERRO: {e.message}")
        return None

print("--- TESTE v1.3: Leitura @ id (Sem Aspas) ---")
source1 = """
/: App #ui tk
/+ Principal

|#input "valor_inicial"| # id = email

& true
    @: e
    ? e == "Entrar"
        ! @ email
"""
# Simula usuário digitando 'teste@teste.com'
interp1 = run_test(source1, {"email": "teste@teste.com"}, "Entrar")

print("\n--- TESTE v1.3: ID Inexistente ---")
source2 = """
! @ nao_existe
"""
interp2 = run_test(source2) # Deve gerar erro

print("\n--- TESTE v1.3: Multiplos Inputs Identificadores ---")
source3 = """
|#input ""| # id = u
|#input ""| # id = p

& true
    @: e
    ? e == "login"
        res = @ u + " | " + @ p
        ! res
"""
interp3 = run_test(source3, {"u": "admin", "p": "secret"}, "login")

print("\n--- TESTE v1.3: Compatibilidade Strings ---")
source4 = """
|#input ""| # id = "email_str"
! @ "email_str"
"""
interp4 = run_test(source4, {"email_str": "string_works"})
