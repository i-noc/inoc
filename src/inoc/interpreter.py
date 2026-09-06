from .ast_nodes import *
from .lexer import Lexer, TokenType
from . import parser as parser_inoc
import operator
import os
import queue
from typing import Any, List, Dict, Set

class InocRuntimeError(Exception):
    def __init__(self, message): self.message = message

class ReturnInterrupt(Exception):
    def __init__(self, value): self.value = value

class Interpreter:
    def __init__(self, input_source=None):
        self.globals = {}
        self.functions = {}
        self.loaded_modules: Set[str] = set()
        self.input_source = input_source if input_source else []
        self.input_index = 0
        self.input_queue = None
        self.event_queue = queue.Queue()
        self.app_name = "InocApp"
        self.ui_type = "tk"
        self.initial_screen = None
        self.current_screen = "Principal"
        self.ui_registry = {self.current_screen: []}
        self.ui_version = 0
        self._setup_builtins()
        # Pilha para gerenciar o aninhamento de containers durante a execução
        self._ui_stack = []

    def _setup_builtins(self):
        self.builtins = {
            "tamanho": self._builtin_tamanho,
            "texto": self._builtin_texto,
            "inserir": self._builtin_inserir,
            "remover": self._builtin_remover,
            "tipo": self._builtin_tipo,
            "subtexto": self._builtin_subtexto,
            "procurar": self._builtin_procurar,
            "chaves": self._builtin_chaves,
            "arredondar": self._builtin_arredondar,
            "absoluto": self._builtin_absoluto,
            "definir": self._builtin_definir,
            "numero": self._builtin_numero,

            # Aliases em Inglês
            "size": self._builtin_tamanho,
            "text": self._builtin_texto,
            "insert": self._builtin_inserir,
            "remove": self._builtin_remover,
            "type": self._builtin_tipo,
            "substring": self._builtin_subtexto,
            "search": self._builtin_procurar,
            "find": self._builtin_procurar,
            "keys": self._builtin_chaves,
            "round": self._builtin_arredondar,
            "absolute": self._builtin_absoluto,
            "abs": self._builtin_absoluto,
            "define": self._builtin_definir,
            "set": self._builtin_definir,
            "number": self._builtin_numero
        }

    def _builtin_definir(self, args):
        if len(args) != 2: raise InocRuntimeError("definir() espera 2 argumentos (id, valor).")
        target_id, new_val = str(args[0]), self.stringify(args[1])
        found = self._update_element_recursive(self.ui_registry.values(), target_id, new_val)
        if found:
            self.ui_version += 1
            return new_val
        raise InocRuntimeError(f"Elemento com id '{target_id}' nao encontrado.")

    def _update_element_recursive(self, collections, target_id, new_val):
        el = self._find_element_by_id(collections, target_id)
        if el:
            el["value"] = new_val
            return True
        return False

    def _builtin_numero(self, args):
        if len(args) != 1: raise InocRuntimeError("numero() espera 1 argumento.")
        val = args[0]
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str):
            try:
                clean_val = val.strip()
                if clean_val == "": raise ValueError()
                return float(clean_val)
            except ValueError:
                raise InocRuntimeError(f"Valor '{val}' nao pode ser convertido para numero.")
        raise InocRuntimeError("numero() exige texto ou numero.")

    def _builtin_tamanho(self, args):
        if len(args) != 1: raise InocRuntimeError("tamanho() espera 1 argumento.")
        val = args[0]
        if isinstance(val, (list, str)): return float(len(val))
        raise InocRuntimeError("tamanho() exige lista ou texto.")

    def _builtin_texto(self, args):
        if len(args) != 1: raise InocRuntimeError("texto() espera 1 argumento.")
        return self.stringify(args[0])

    def _builtin_inserir(self, args):
        if len(args) != 2: raise InocRuntimeError("inserir() espera 2 argumentos.")
        lst, item = args[0], args[1]
        if isinstance(lst, list):
            lst.append(item)
            return item
        raise InocRuntimeError("inserir() exige uma lista.")

    def _builtin_remover(self, args):
        if len(args) != 2: raise InocRuntimeError("remover() espera 2 argumentos.")
        lst, idx = args[0], args[1]
        if isinstance(lst, list) and isinstance(idx, (int, float)):
            i = int(idx)
            if 0 <= i < len(lst): return lst.pop(i)
            raise InocRuntimeError("Índice de remoção fora dos limites.")
        raise InocRuntimeError("remover() exige lista e índice numérico.")

    def _builtin_tipo(self, args):
        if len(args) != 1: raise InocRuntimeError("tipo() espera 1 argumento.")
        val = args[0]
        if isinstance(val, bool): return "booleano"
        if isinstance(val, (int, float)): return "numero"
        if isinstance(val, str): return "texto"
        if isinstance(val, list): return "lista"
        if isinstance(val, dict): return "objeto"
        return "nada"

    def _builtin_subtexto(self, args):
        if len(args) != 3: raise InocRuntimeError("subtexto() espera 3 argumentos (texto, inicio, fim).")
        t, i, f = args[0], args[1], args[2]
        if isinstance(t, str) and isinstance(i, (int, float)) and isinstance(f, (int, float)):
            return t[int(i):int(f)]
        raise InocRuntimeError("subtexto() exige (texto, numero, numero).")

    def _builtin_procurar(self, args):
        if len(args) != 2: raise InocRuntimeError("procurar() espera 2 argumentos (texto, termo).")
        t, termo = args[0], args[1]
        if isinstance(t, str) and isinstance(termo, str):
            return float(t.find(termo))
        raise InocRuntimeError("procurar() exige (texto, texto).")

    def _builtin_chaves(self, args):
        if len(args) != 1: raise InocRuntimeError("chaves() espera 1 argumento (objeto).")
        obj = args[0]
        if isinstance(obj, dict):
            return list(obj.keys())
        raise InocRuntimeError("chaves() exige um objeto.")

    def _builtin_arredondar(self, args):
        if len(args) != 1: raise InocRuntimeError("arredondar() espera 1 argumento.")
        n = args[0]
        if isinstance(n, (int, float)): return float(round(n))
        raise InocRuntimeError("arredondar() exige um número.")

    def _builtin_absoluto(self, args):
        if len(args) != 1: raise InocRuntimeError("absoluto() espera 1 argumento.")
        n = args[0]
        if isinstance(n, (int, float)): return float(abs(n))
        raise InocRuntimeError("absoluto() exige um número.")

    def interpret(self, program: Program):
        try:
            for statement in program.statements: self.execute(statement)
            if not self.initial_screen: self.initial_screen = "Principal"
            self.render_ui()
        except InocRuntimeError as e: print(f"Erro de Execução: {e.message}")

    def execute(self, stmt: Statement):
        if isinstance(stmt, AppStmt):
            self.app_name = stmt.name
            for c in stmt.configs:
                if c.property == "ui":
                    val = self.evaluate(c.value)
                    if val in ["tk", "web"]: self.ui_type = val
        elif isinstance(stmt, ScreenStmt):
            self.current_screen = stmt.name
            if not self.initial_screen: self.initial_screen = self.current_screen
            if self.current_screen not in self.ui_registry: self.ui_registry[self.current_screen] = []
        elif isinstance(stmt, ObjectDefStmt): self.globals[stmt.name] = {}
        elif isinstance(stmt, ModuleStmt): self._load_module(stmt.name)
        elif isinstance(stmt, FunctionStmt): self.functions[stmt.name] = stmt
        elif isinstance(stmt, ReturnStmt): raise ReturnInterrupt(self.evaluate(stmt.value) if stmt.value else None)
        elif isinstance(stmt, ElementStmt):
            val = self.evaluate(stmt.content)
            el = self._add_element(val, stmt.element_type, stmt.line)
            for c in stmt.configs:
                if c.property == "id" and isinstance(c.value, IdentifierExpr):
                    el["props"][c.property] = c.value.name
                else:
                    el["props"][c.property] = self.evaluate(c.value)
        elif isinstance(stmt, ContainerStmt):
            container = self._add_element(stmt.name, "container", stmt.line)
            container["children"] = []

            # Aplica configs do container
            for c in stmt.configs:
                if c.property == "id" and isinstance(c.value, IdentifierExpr):
                    container["props"][c.property] = c.value.name
                else:
                    container["props"][c.property] = self.evaluate(c.value)

            # Salva o contexto atual e entra no container
            self._ui_stack.append(container["children"])
            for child in stmt.children: self.execute(child)
            self._ui_stack.pop()

        elif isinstance(stmt, EventStmt):
            event_val = self._get_ui_event()
            target = stmt.target
            if isinstance(target, IdentifierExpr): self.globals[target.name] = event_val
        elif isinstance(stmt, NavigationStmt):
            label = self.evaluate(stmt.label)
            el = self._add_element(label, "texto", 0)
            el["action"] = {"type": "navegacao", "target": stmt.target}
        elif isinstance(stmt, ConfigStmt):
            target_list = self._ui_stack[-1] if self._ui_stack else self.ui_registry[self.current_screen]
            if target_list:
                el = target_list[-1]
                el["props"][stmt.property] = self.evaluate(stmt.value)
        elif isinstance(stmt, PrintStmt): print(f"> {self.stringify(self.evaluate(stmt.value))}")
        elif isinstance(stmt, InputStmt):
            val = self._infer_type(self._get_input())
            target = stmt.target
            if isinstance(target, IdentifierExpr): self.globals[target.name] = val
            elif isinstance(target, GetExpr):
                obj = self.evaluate(target.obj)
                if isinstance(obj, dict): obj[target.name] = val
            elif isinstance(target, IndexExpr):
                lst = self.evaluate(target.target)
                lst[self._evaluate_index(target.index, lst)] = val
        elif isinstance(stmt, AssignmentStmt): self.globals[stmt.name] = self.evaluate(stmt.value)
        elif isinstance(stmt, SetStmt):
            obj = self.evaluate(stmt.obj)
            if isinstance(obj, dict): obj[stmt.name] = self.evaluate(stmt.value)
        elif isinstance(stmt, SetIndexStmt):
            lst = self.evaluate(stmt.target)
            lst[self._evaluate_index(stmt.index, lst)] = self.evaluate(stmt.value)
        elif isinstance(stmt, IfStmt):
            if self.is_truthy(self.evaluate(stmt.condition)):
                for s in stmt.then_branch: self.execute(s)
            else:
                executed = False
                for branch in stmt.elif_branches:
                    if self.is_truthy(self.evaluate(branch.condition)):
                        for s in branch.body: self.execute(s)
                        executed = True
                        break
                if not executed:
                    for s in stmt.else_branch: self.execute(s)
        elif isinstance(stmt, WhileStmt):
            while self.is_truthy(self.evaluate(stmt.condition)):
                for s in stmt.body: self.execute(s)
        elif isinstance(stmt, ForEachStmt):
            coll = self.evaluate(stmt.collection)
            old = self.globals.get(stmt.item_name)
            for item in coll:
                self.globals[stmt.item_name] = item
                for s in stmt.body: self.execute(s)
            if old is not None: self.globals[stmt.item_name] = old
            elif stmt.item_name in self.globals: del self.globals[stmt.item_name]
        elif isinstance(stmt, CallExpr): self.evaluate(stmt)

    def _add_element(self, label: str, el_type: str, line: int) -> Dict:
        # v1.2: Adiciona ao container atual se houver um na pilha
        target_list = self._ui_stack[-1] if self._ui_stack else self.ui_registry[self.current_screen]
        el = {"type": el_type, "value": label, "action": None, "props": {}, "line": line}
        target_list.append(el)
        self.ui_version += 1
        return el

    def _load_module(self, name: str):
        if name in self.loaded_modules: return

        filename = f"{name}.inoc"
        possible_paths = [
            filename,
            os.path.join("examples", "modulos", filename),
            os.path.join("examples", filename)
        ]

        target_path = None
        for p in possible_paths:
            if os.path.exists(p):
                target_path = p
                break

        if not target_path:
            raise InocRuntimeError(f"Modulo '{name}' nao encontrado.")

        with open(target_path, 'r', encoding='utf-8') as f:
            source = f.read()
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        parser = parser_inoc.Parser(tokens)
        module_ast = parser.parse()
        module_interpreter = Interpreter()
        for stmt in module_ast.statements:
            module_interpreter.execute(stmt)
        module_obj = {}
        for k, v in module_interpreter.globals.items(): module_obj[k] = v
        for k, v in module_interpreter.functions.items(): module_obj[k] = v
        self.globals[name] = module_obj
        self.loaded_modules.add(name)

    def _find_element_by_id(self, collections, target_id):
        for collection in collections:
            for el in collection:
                if el["props"].get("id") == target_id: return el
                if "children" in el:
                    found = self._find_element_by_id([el["children"]], target_id)
                    if found: return found
        return None

    def evaluate(self, expr: Expression) -> Any:
        if isinstance(expr, InputExpr):
            if isinstance(expr.id_label, IdentifierExpr):
                target_id = expr.id_label.name
            else:
                target_id = str(self.evaluate(expr.id_label))

            el = self._find_element_by_id(self.ui_registry.values(), target_id)
            if el: return el.get("value", "")
            raise InocRuntimeError(f"Elemento com id '{target_id}' nao encontrado na UI.")

        if isinstance(expr, UIRefExpr):
            return expr.name

        if isinstance(expr, ObjectLiteralExpr): return {}
        if isinstance(expr, ListLiteralExpr): return [self.evaluate(e) for e in expr.elements]
        if isinstance(expr, LiteralExpr): return expr.value
        if isinstance(expr, GroupingExpr): return self.evaluate(expr.expression)
        if isinstance(expr, IdentifierExpr):
            if expr.name in self.globals: return self.globals[expr.name]
            if expr.name in self.functions: return self.functions[expr.name]
            if expr.name in self.builtins: return f"__builtin__:{expr.name}"
            raise InocRuntimeError(f"Variável ou função não definida: '{expr.name}'")
        if isinstance(expr, UnaryExpr):
            right = self.evaluate(expr.right)
            if expr.operator == "not": return not self.is_truthy(right)
            if expr.operator == "-":
                if not isinstance(right, (int, float)):
                    raise InocRuntimeError("Operador '-' unário exige número.")
                return -right
        if isinstance(expr, LogicalExpr):
            left = self.evaluate(expr.left)
            if expr.operator == "or":
                if self.is_truthy(left): return left
            else: # and
                if not self.is_truthy(left): return left
            return self.evaluate(expr.right)
        if isinstance(expr, GetExpr):
            obj = self.evaluate(expr.obj)
            if isinstance(obj, dict) and expr.name in obj: return obj[expr.name]
            raise InocRuntimeError(f"Propriedade '{expr.name}' não encontrada.")
        if isinstance(expr, IndexExpr):
            lst = self.evaluate(expr.target)
            return lst[self._evaluate_index(expr.index, lst)]
        if isinstance(expr, CallExpr): return self._call(expr)
        if isinstance(expr, BinaryExpr):
            l = self.evaluate(expr.left); r = self.evaluate(expr.right); op = expr.operator
            if op == '+':
                if isinstance(l, str) or isinstance(r, str): return self.stringify(l) + self.stringify(r)
                self._check_num(op, l, r); return l + r
            if op == '-': self._check_num(op, l, r); return l - r
            if op == '*': self._check_num(op, l, r); return l * r
            if op == '/':
                self._check_num(op, l, r)
                return l / r if r != 0 else 0
            if op == '>': return l > r
            if op == '>=': return l >= r
            if op == '<': return l < r
            if op == '<=': return l <= r
            if op == '==': return l == r
            if op == '!=': return l != r
        return None

    def _call(self, expr: CallExpr) -> Any:
        callee = self.evaluate(expr.callee)
        if isinstance(callee, str) and callee.startswith("__builtin__:"):
            name = callee.split(":")[1]
            args = [self.evaluate(a) for a in expr.arguments]
            return self.builtins[name](args)
        if isinstance(callee, FunctionStmt):
            func = callee
            name = func.name
        else:
            raise InocRuntimeError(f"Tentativa de chamar algo que não é uma função.")
        if len(expr.arguments) != len(func.params):
            raise InocRuntimeError(f"'{name}' espera {len(func.params)} args.")
        args = [self.evaluate(a) for a in expr.arguments]
        old_globals = self.globals.copy()
        for i, param_name in enumerate(func.params): self.globals[param_name] = args[i]
        res = None
        try:
            for s in func.body: self.execute(s)
        except ReturnInterrupt as ri: res = ri.value
        finally: self.globals = old_globals
        return res

    def _check_num(self, op, l, r):
        if not (isinstance(l, (int, float)) and not isinstance(l, bool) and isinstance(r, (int, float)) and not isinstance(r, bool)):
            raise InocRuntimeError(f"Operador '{op}' exige números.")

    def _evaluate_index(self, index_expr: Expression, target: Any) -> int:
        idx_val = self.evaluate(index_expr)
        if not isinstance(idx_val, (int, float)) or isinstance(idx_val, bool) or not float(idx_val).is_integer():
            raise InocRuntimeError("Índice deve ser inteiro.")
        idx = int(idx_val)
        if idx < 0 or idx >= len(target): raise InocRuntimeError("Índice fora dos limites.")
        return idx

    def _get_input(self) -> str:
        if self.input_queue: return self.input_queue.get()
        if self.input_index < len(self.input_source):
            val = self.input_source[self.input_index]; self.input_index += 1; return val
        return input()

    def _get_ui_event(self) -> str:
        if self.event_queue: return self.event_queue.get()
        return "nada"

    def _infer_type(self, text: str) -> Any:
        if text.lower() == "true": return True
        if text.lower() == "false": return False
        try: return float(text)
        except ValueError: pass
        return text

    def is_truthy(self, val) -> bool: return bool(val) if val is not None else False

    def stringify(self, val) -> str:
        if isinstance(val, list): return "[" + ", ".join(self.stringify(i) for i in val) + "]"
        if isinstance(val, bool): return "true" if val else "false"
        if isinstance(val, float) and str(val).endswith(".0"): return str(val)[:-2]
        return str(val) if val is not None else "nada"

    def render_ui(self):
        print("\n=== ESTADO DA UI ABSTRATA ===")
        for s, elements in self.ui_registry.items():
            print(f"Tela: {s}")
            self._print_ui_recursive(elements, 1)

    def _print_ui_recursive(self, elements, level):
        for data in elements:
            indent = "    " * level
            print(f"{indent}<{data['type']}> value: \"{data['value']}\"")
            if "children" in data:
                self._print_ui_recursive(data["children"], level + 1)
