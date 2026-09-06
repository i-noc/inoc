import sys
import os

# Adiciona o diretório 'src' ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.interpreter import Interpreter

def test(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    for stmt in ast.statements:
        interpreter.execute(stmt)
    return interpreter

print("Verificando aliases...")

# 1. Keywords
interp = test("a = verdadeiro e não falso")
assert interp.globals['a'] == True

# 2. Elementos e Propriedades
interp = test('|#entrada "X"| # color = "red", size = 20, id = campo')
el = interp._find_element_by_id(interp.ui_registry.values(), "campo")
assert el['type'] == 'input'
assert el['props']['cor'] == 'red'
assert el['props']['tamanho'] == 20

# 3. Built-ins
interp = test("s = size([1,2])")
assert interp.globals['s'] == 2

# Verificando se o nome 'define' existe no dicionário de builtins
interp_obj = Interpreter()
assert "define" in interp_obj.builtins
assert "set" in interp_obj.builtins

print("Verificação concluída com sucesso!")
