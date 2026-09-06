import sys
import os

# Adiciona o diretório 'src' ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter
from inoc.ast_nodes import WhileStmt, ForEachStmt, EventStmt

def run_login_cycle(email_input, senha_input):
    with open('examples/login_v13.inoc', 'r', encoding='utf-8') as f:
        source = f.read()

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
    interpreter._builtin_definir(["email", email_input])
    interpreter._builtin_definir(["senha", senha_input])

    # 3. Simula clique no botao (Evento)
    interpreter.event_queue.put("Entrar")

    # 4. Executa a logica reativa (um ciclo do loop & true)
    # Busca o WhileStmt no AST
    loop = next(s for s in ast.statements if isinstance(s, WhileStmt))
    # Executa o corpo do loop uma vez
    for stmt in loop.body:
        interpreter.execute(stmt)

    # 5. Verifica o resultado no elemento 'feedback'
    feedback_el = interpreter._find_element_by_id(interpreter.ui_registry.values(), "feedback")
    return feedback_el["value"]

print("--- TESTE CICLO v1.3: Login Vazio ---")
res1 = run_login_cycle("", "")
print(f"Resultado: '{res1}'")
assert res1 == "O e-mail e obrigatorio"

print("\n--- TESTE CICLO v1.3: Senha Vazia ---")
res2 = run_login_cycle("admin", "")
print(f"Resultado: '{res2}'")
assert res2 == "A senha e obrigatoria"

print("\n--- TESTE CICLO v1.3: Sucesso ---")
res3 = run_login_cycle("admin", "123")
print(f"Resultado: '{res3}'")
assert res3 == "Login realizado!"

print("\n--- TESTE CICLO v1.3: Invalido ---")
res4 = run_login_cycle("usuario", "errado")
print(f"Resultado: '{res4}'")
assert res4 == "Dados invalidos"

print("\nCICLO FUNDAMENTAL V1.3.0 VALIDADO COM SUCESSO!")
