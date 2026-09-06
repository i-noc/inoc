import sys
import os
import json

# Adiciona a pasta src ao path para permitir imports do pacote inoc
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from inoc.lexer import Lexer
from inoc.parser import Parser
from inoc.ast_nodes import AppStmt, ScreenStmt
from inoc.interpreter import Interpreter
from inoc.runtime import UIRuntime

def find_file(filename):
    # 1. Tenta o caminho direto
    if os.path.exists(filename):
        return filename

    # 2. Tenta dentro de examples/
    path_examples = os.path.join("examples", filename)
    if os.path.exists(path_examples):
        return path_examples

    # 3. Tenta dentro de examples/internal/
    path_internal = os.path.join("examples", "internal", filename)
    if os.path.exists(path_internal):
        return path_internal

    return None

def check_file(filepath):
    target = find_file(filepath)
    if not target:
        print(json.dumps([{"line": 1, "column": 1, "message": f"Arquivo não encontrado: {filepath}"}]))
        return

    try:
        with open(target, 'r', encoding='utf-8') as f:
            code = f.read()

        lexer = Lexer(code)
        tokens = lexer.scan_tokens()
        parser = Parser(tokens)
        parser.parse()

        all_errors = lexer.errors + parser.errors
        print(json.dumps(all_errors))
    except Exception as e:
        print(json.dumps([{"line": 1, "column": 1, "message": f"Erro interno: {str(e)}"}]))

def run_file(filepath):
    target = find_file(filepath)

    if not target:
        print(f"Erro: Arquivo '{filepath}' nao encontrado na raiz ou em /examples.")
        return

    if not target.endswith(".inoc"):
        print(f"Erro: O arquivo '{target}' deve ter a extensao .inoc")
        return

    try:
        with open(target, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    print(f"--- EXECUTANDO: {target} ---")

    try:
        lexer = Lexer(code)
        tokens = lexer.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()

        if lexer.errors or parser.errors:
            print(f"Abortado devido a {len(lexer.errors) + len(parser.errors)} erro(s) de sintaxe.")
            return

        if not ast or not ast.statements:
            print("Aviso: O programa parece estar vazio ou contem erros de sintaxe.")
            return

        interpreter = Interpreter()
        runtime = UIRuntime(interpreter, ast)
        runtime.run()

    except Exception as e:
        print(f"\n[ERRO DE EXECUCAO]: {e}")

    print("--------------------------\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.inoc> [--check]")
    else:
        if "--check" in sys.argv:
            filepath = sys.argv[1] if sys.argv[1] != "--check" else sys.argv[2]
            check_file(filepath)
        else:
            run_file(sys.argv[1])
