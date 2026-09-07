from lexer import Lexer, TokenType
from parser import Parser, normalize
from ast_nodes import *

class InocAnalyzer:
    def __init__(self):
        self.symbols = []
        self.builtins = [
            "tamanho", "texto", "inserir", "remover", "tipo", "subtexto",
            "procurar", "chaves", "arredondar", "absoluto", "definir", "numero",
            "size", "text", "insert", "remove", "type", "substring",
            "search", "find", "keys", "round", "absolute", "abs", "define", "set", "number"
        ]
        self.ui_properties = [
            "cor", "cor_texto", "tamanho", "fonte", "largura", "altura",
            "borda", "margem", "alinhamento", "id",
            "color", "text_color", "size", "font", "width", "height",
            "border", "margin", "alignment"
        ]
        self.ui_elements = ["texto", "botao", "input", "janela", "text", "button", "entrada", "window"]

    def analyze(self, source: str):
        import io
        from contextlib import redirect_stdout

        # Captura saídas de erro do lexer e parser para não corromper o JSON-RPC (stdout)
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                lexer = Lexer(source)
                tokens = lexer.scan_tokens()
                parser = Parser(tokens)
                ast = parser.parse()
                self.symbols = self._extract_symbols(ast)
                return {"ast": ast, "tokens": tokens, "errors": lexer.errors + parser.errors}
            except Exception:
                # Fallback: tenta retornar tokens se o parser falhar
                try:
                    lexer = Lexer(source)
                    tokens = lexer.scan_tokens()
                    return {"ast": None, "tokens": tokens, "errors": lexer.errors}
                except:
                    return {"ast": None, "tokens": [], "errors": []}

    def _extract_symbols(self, node):
        symbols = []
        if isinstance(node, Program):
            for stmt in node.statements:
                symbols.extend(self._extract_symbols(stmt))
        elif isinstance(node, AssignmentStmt):
            symbols.append({"name": node.name, "kind": "variable"})
        elif isinstance(node, FunctionStmt):
            symbols.append({"name": node.name, "kind": "function", "params": node.params})
            for stmt in node.body:
                symbols.extend(self._extract_symbols(stmt))
        elif isinstance(node, ContainerStmt):
            symbols.append({"name": node.name, "kind": "container"})
            for child in node.children:
                symbols.extend(self._extract_symbols(child))
        elif isinstance(node, ElementStmt):
             # Procura por ID nas configurações do elemento
             for config in node.configs:
                 if config.property == "id" and isinstance(config.value, LiteralExpr):
                     symbols.append({"name": str(config.value.value), "kind": "ui_element"})
        elif isinstance(node, IfStmt):
            for stmt in node.then_branch: symbols.extend(self._extract_symbols(stmt))
            for branch in node.elif_branches:
                for stmt in branch.body: symbols.extend(self._extract_symbols(stmt))
            for stmt in node.else_branch: symbols.extend(self._extract_symbols(stmt))
        elif isinstance(node, WhileStmt) or isinstance(node, ForEachStmt):
            for stmt in node.body: symbols.extend(self._extract_symbols(stmt))

        return symbols

    def get_completions(self, source: str, line: int, column: int):
        analysis = self.analyze(source)
        tokens = analysis.get("tokens", [])

        # Encontra o token na posição do cursor ou o imediatamente anterior
        last_token = None
        for t in tokens:
            if t.line < line or (t.line == line and t.column <= column):
                last_token = t
            else:
                break

        completions = []

        # Lógica de contexto
        context = "global"
        if last_token:
            if last_token.type == TokenType.HASH:
                context = "property"
            elif last_token.type == TokenType.PIPE and last_token.lexeme == "|#":
                context = "element_type"
            elif last_token.type == TokenType.AT:
                context = "ui_reference"

        if context == "property":
            for p in self.ui_properties:
                completions.append({"label": p, "kind": "property", "detail": "Propriedade de UI"})

        elif context == "element_type":
            for e in self.ui_elements:
                completions.append({"label": e, "kind": "type", "detail": "Elemento de UI"})

        elif context == "ui_reference":
            # Sugere apenas IDs de elementos de UI encontrados na AST
            for s in self.symbols:
                if s["kind"] == "ui_element":
                    completions.append({"label": s["name"], "kind": "ui_element", "detail": "ID de elemento UI"})

        else:
            # Sugere Builtins
            for b in self.builtins:
                completions.append({"label": b, "kind": "function", "detail": "Função nativa I-NOC"})

            # Sugere Símbolos extraídos da AST
            seen = set()
            for s in self.symbols:
                if s["name"] not in seen:
                    completions.append({"label": s["name"], "kind": s["kind"], "detail": f"Definido no código ({s['kind']})"})
                    seen.add(s["name"])

            # Sugere Palavras-chave
            keywords = ["se", "senão", "verdadeiro", "falso", "e", "ou", "não", "if", "else", "true", "false", "and", "or", "not"]
            for k in keywords:
                completions.append({"label": k, "kind": "keyword"})

        return completions
