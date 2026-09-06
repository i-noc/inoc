import sys
import os

# Adiciona o diretório 'src' ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter, InocRuntimeError
from inoc.ast_nodes import WhileStmt, ForEachStmt, EventStmt

def setup_app():
    with open('examples/cadastro_produtos.inoc', 'r', encoding='utf-8') as f:
        source = f.read()
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()

    # Executa declaracoes iniciais
    for stmt in ast.statements:
        if not isinstance(stmt, (WhileStmt, ForEachStmt, EventStmt)):
             interpreter.execute(stmt)

    loop = next(s for s in ast.statements if isinstance(s, WhileStmt))
    return interpreter, loop

def trigger_event(interp, loop, event_name, inputs=None):
    if inputs:
        for tid, tval in inputs.items():
            interp._builtin_definir([tid, tval])
    interp.event_queue.put(event_name)
    for stmt in loop.body:
        interp.execute(stmt)

print("--- TESTE APP PRODUTOS: Cadastro Valido ---")
interp, loop = setup_app()
trigger_event(interp, loop, "Adicionar", {"nome_in": "Cafe", "preco_in": "15.50", "qtd_in": "10"})
feedback = interp._find_element_by_id(interp.ui_registry.values(), "feedback")["value"]
lista = interp._find_element_by_id(interp.ui_registry.values(), "lista_area")["value"]
print(f"Feedback: {feedback}")
print(f"Lista: {lista}")
assert "Cafe" in lista
assert feedback == "Produto adicionado!"

print("\n--- TESTE APP PRODUTOS: Validacao Nome ---")
trigger_event(interp, loop, "Adicionar", {"nome_in": "", "preco_in": "10", "qtd_in": "5"})
feedback = interp._find_element_by_id(interp.ui_registry.values(), "feedback")["value"]
print(f"Feedback: {feedback}")
assert "Nome obrigatorio" in feedback

print("\n--- TESTE APP PRODUTOS: Remover Ultimo ---")
trigger_event(interp, loop, "Remover Ultimo")
feedback = interp._find_element_by_id(interp.ui_registry.values(), "feedback")["value"]
lista = interp._find_element_by_id(interp.ui_registry.values(), "lista_area")["value"]
print(f"Feedback: {feedback}")
assert "Cafe" not in lista
assert "Total: 0" in interp._find_element_by_id(interp.ui_registry.values(), "total_label")["value"]

print("\n--- TESTE APP PRODUTOS: Multiplos Produtos ---")
trigger_event(interp, loop, "Adicionar", {"nome_in": "Pao", "preco_in": "2.00", "qtd_in": "50"})
trigger_event(interp, loop, "Adicionar", {"nome_in": "Leite", "preco_in": "5.50", "qtd_in": "20"})
lista = interp._find_element_by_id(interp.ui_registry.values(), "lista_area")["value"]
total = interp._find_element_by_id(interp.ui_registry.values(), "total_label")["value"]
print(f"Total: {total}")
assert "Pao" in lista
assert "Leite" in lista
assert "Total: 2" in total

print("\n--- TESTE APP PRODUTOS: Preco Invalido ---")
trigger_event(interp, loop, "Adicionar", {"nome_in": "Erro", "preco_in": "-5", "qtd_in": "1"})
feedback = interp._find_element_by_id(interp.ui_registry.values(), "feedback")["value"]
print(f"Feedback: {feedback}")
assert "Preco invalido" in feedback

print("\nAPLICACAO DE PRODUTOS v1.3.0 VALIDADA!")
