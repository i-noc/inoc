from lexer import TokenType, Token
from ast_nodes import *
from typing import List, Optional, Union

# Mapeamento de normalização multilíngue (Interno sempre prefere o termo original do código)
NORMALIZATION = {
    # Elementos de UI
    "text": "texto",
    "button": "botao",
    "entrada": "input",
    "window": "janela",

    # Propriedades
    "color": "cor",
    "text_color": "cor_texto",
    "size": "tamanho",
    "font": "fonte",
    "width": "largura",
    "height": "altura",
    "border": "borda",
    "margin": "margem",
    "alignment": "alinhamento"
}

def normalize(name: str) -> str:
    return NORMALIZATION.get(name.lower(), name)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def parse(self) -> Program:
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                if isinstance(stmt, list): statements.extend(stmt)
                else: statements.append(stmt)
        return Program(statements)

    def _error(self, token: Token, message: str):
        err = {"line": token.line, "column": token.column, "message": message}
        self.errors.append(err)
        print(message + f" na linha {token.line}")

    def declaration(self) -> Optional[Union[Statement, List[Statement]]]:
        try:
            if self.match(TokenType.SLASH_COLON): return self.app_declaration()
            if self.match(TokenType.SLASH_PLUS): return self.screen_declaration()
            if self.match(TokenType.DOUBLE_SLASH): return self.object_declaration()
            if self.match(TokenType.QUESTION): return self.if_statement()
            if self.match(TokenType.AMPERSAND_COLON): return self.foreach_statement()
            if self.match(TokenType.AMPERSAND): return self.while_statement()
            if self.match(TokenType.BANG): return self.print_statement()
            if self.match(TokenType.PIPE): return self.element_statement()
            if self.match(TokenType.AT_COLON): return self.event_statement()
            if self.match(TokenType.AT): return self.input_statement()
            if self.match(TokenType.DOLLAR_COLON): return self.return_statement()
            if self.match(TokenType.DOLLAR): return self.function_declaration()
            if self.match(TokenType.SECTION): return self.module_declaration()
            if self.match(TokenType.CENT): return self.container_declaration()

            if self.check(TokenType.IDENTIFIER) or self.check(TokenType.LPAREN) or self.check(TokenType.NOT):
                return self.statement_expression_or_assignment()
            if self.match(TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT): return None
            token = self.peek()
            if token.type != TokenType.EOF:
                self._error(token, f"Erro Sintático: Símbolo inesperado '{token.lexeme}'")
                self.synchronize()
            return None
        except Exception as e:
            self._error(self.peek(), f"Erro ao processar: {e}")
            self.synchronize()
            return None

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE: return
            self.advance()

    def module_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Esperado nome do módulo após '§'.")
        return ModuleStmt(name.lexeme)

    def container_declaration(self) -> Statement:
        line_num = self.previous().line
        name = self.consume(TokenType.IDENTIFIER, "Nome do container esperado.").lexeme
        configs = []

        # Bloco opcional de propriedades # cor = "..."
        if self.match(TokenType.HASH):
            while True:
                prop = normalize(self.consume(TokenType.IDENTIFIER, "Propriedade esperada.").lexeme)
                self.consume(TokenType.EQUAL, "Esperado '='.")
                configs.append(ConfigStmt(element_label=LiteralExpr(name), property=prop, value=self.expression()))
                if not self.match(TokenType.COMMA): break

        # Bloco de filhos indentado
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Bloco indentado esperado após a declaração do container.")
        children = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                if isinstance(stmt, list): children.extend(stmt)
                else: children.append(stmt)
        self.consume(TokenType.DEDENT, "Fim do bloco do container.")

        return ContainerStmt(name=name, configs=configs, children=children, line=line_num)

    def element_statement(self) -> Union[Statement, List[Statement]]:
        line_num = self.previous().line
        el_type = "texto"
        content = LiteralExpr("")
        if self.match(TokenType.HASH):
            el_type = normalize(self.consume(TokenType.IDENTIFIER, "Tipo esperado.").lexeme)
            if not self.check(TokenType.PIPE):
                content = self.expression()
        else: content = self.expression()
        self.consume(TokenType.PIPE, "Esperado '|'.")
        if self.match(TokenType.ARROW):
            return NavigationStmt(label=content, target=self.consume(TokenType.IDENTIFIER, "Destino esperado.").lexeme)
        configs = []
        if self.match(TokenType.HASH):
            while True:
                prop = normalize(self.consume(TokenType.IDENTIFIER, "Propriedade esperada.").lexeme)
                self.consume(TokenType.EQUAL, "Esperado '='.")
                configs.append(ConfigStmt(element_label=content, property=prop, value=self.expression()))
                if not self.match(TokenType.COMMA): break
            return ElementStmt(element_type=el_type, content=content, configs=configs, line=line_num)
        return ElementStmt(element_type=el_type, content=content, configs=configs, line=line_num)

    def statement_expression_or_assignment(self) -> Statement:
        expr = self.expression()
        if self.match(TokenType.EQUAL):
            value = self.expression()
            if isinstance(expr, IdentifierExpr): return AssignmentStmt(expr.name, value)
            if isinstance(expr, GetExpr): return SetStmt(expr.obj, expr.name, value)
            if isinstance(expr, IndexExpr): return SetIndexStmt(expr.target, expr.index, value)
            raise Exception("Alvo de atribuição inválido.")
        return expr

    def function_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Nome esperado.")
        self.consume(TokenType.LPAREN, "Esperado '('.")
        params = []
        if not self.check(TokenType.RPAREN):
            while True:
                params.append(self.consume(TokenType.IDENTIFIER, "Parâmetro esperado.").lexeme)
                if not self.match(TokenType.COMMA): break
        self.consume(TokenType.RPAREN, "Esperado ')'.")
        self.consume(TokenType.NEWLINE, "Quebra de linha necessária.")
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Bloco indentado esperado.")
        body = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                if isinstance(stmt, list): body.extend(stmt)
                else: body.append(stmt)
        self.consume(TokenType.DEDENT, "Fim do bloco.")
        return FunctionStmt(name.lexeme, params, body)

    def return_statement(self) -> Statement: return ReturnStmt(self.expression())
    def if_statement(self) -> Statement:
        cond = self.expression()
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Bloco esperado.")
        then_b = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            s = self.declaration()
            if s:
                if isinstance(s, list): then_b.extend(s)
                else: then_b.append(s)
        self.consume(TokenType.DEDENT, "Fim bloco.")

        elif_branches = []
        while True:
            # Pula linhas vazias
            while self.check(TokenType.NEWLINE): self.advance()

            # Checa por 'else if'
            if self.check(TokenType.ELSE):
                self.advance() # Consome 'else'
                self.consume(TokenType.IF, "Esperado 'if' após 'else'.")

                elif_cond = self.expression()
                while self.match(TokenType.NEWLINE): pass
                self.consume(TokenType.INDENT, "Bloco else if esperado.")
                elif_body = []
                while not self.check(TokenType.DEDENT) and not self.is_at_end():
                    s = self.declaration()
                    if s:
                        if isinstance(s, list): elif_body.extend(s)
                        else: elif_body.append(s)
                self.consume(TokenType.DEDENT, "Fim bloco else if.")
                elif_branches.append(ElseIfBranch(elif_cond, elif_body))
            else:
                break

        else_b = []
        while self.check(TokenType.NEWLINE): self.advance()

        if self.match(TokenType.POUND):
            while self.match(TokenType.NEWLINE): pass
            self.consume(TokenType.INDENT, "Bloco £ esperado.")
            while not self.check(TokenType.DEDENT) and not self.is_at_end():
                s = self.declaration()
                if s:
                    if isinstance(s, list): else_b.extend(s)
                    else: else_b.append(s)
            self.consume(TokenType.DEDENT, "Fim bloco £.")

        return IfStmt(cond, then_b, elif_branches, else_b)

    def while_statement(self) -> Statement:
        cond = self.expression()
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Bloco esperado.")
        body = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            s = self.declaration()
            if s:
                if isinstance(s, list): body.extend(s)
                else: body.append(s)
        self.consume(TokenType.DEDENT, "Fim bloco.")
        return WhileStmt(cond, body)

    def foreach_statement(self) -> Statement:
        item = self.consume(TokenType.IDENTIFIER, "Nome esperado.").lexeme
        coll = self.expression()
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Bloco esperado.")
        body = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            s = self.declaration()
            if s:
                if isinstance(s, list): body.extend(s)
                else: body.append(s)
        self.consume(TokenType.DEDENT, "Fim bloco.")
        return ForEachStmt(item, coll, body)

    def input_statement(self) -> Statement: return InputStmt(target=self.primary())
    def event_statement(self) -> Statement: return EventStmt(target=self.primary())
    def print_statement(self) -> Statement: return PrintStmt(self.expression())

    def expression(self) -> Expression: return self.logic_or()
    def logic_or(self) -> Expression:
        expr = self.logic_and()
        while self.match(TokenType.OR):
            op = self.previous().lexeme
            expr = LogicalExpr(expr, op, self.logic_and())
        return expr
    def logic_and(self) -> Expression:
        expr = self.comparison()
        while self.match(TokenType.AND):
            op = self.previous().lexeme
            expr = LogicalExpr(expr, op, self.comparison())
        return expr
    def comparison(self) -> Expression:
        expr = self.addition()
        ops = (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL, TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL)
        while self.match(*ops):
            op = self.previous().lexeme
            expr = BinaryExpr(expr, op, self.addition())
        return expr
    def addition(self) -> Expression:
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().lexeme
            expr = BinaryExpr(expr, op, self.multiplication())
        return expr
    def multiplication(self) -> Expression:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous().lexeme
            expr = BinaryExpr(expr, op, self.unary())
        return expr
    def unary(self) -> Expression:
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.previous().lexeme
            return UnaryExpr(op, self.unary())
        if self.match(TokenType.AT):
            # v1.4.1: Suporte a leitura de UI por ID (@ id) consolidado
            return InputExpr(self.primary())
        return self.primary()

    def primary(self) -> Expression:
        if self.match(TokenType.STRING, TokenType.NUMBER): return LiteralExpr(self.previous().literal)
        if self.match(TokenType.TRUE): return LiteralExpr(True)
        if self.match(TokenType.FALSE): return LiteralExpr(False)
        if self.match(TokenType.DOUBLE_SLASH): return ObjectLiteralExpr()
        if self.match(TokenType.PIPE):
            name = self.consume(TokenType.IDENTIFIER, "Identificador esperado dentro de |...|.").lexeme
            self.consume(TokenType.PIPE, "Esperado '|' para fechar a referência de UI.")
            return UIRefExpr(name)
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA): break
            self.consume(TokenType.RBRACKET, "']' esperado.")
            return ListLiteralExpr(elements)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "')' esperado.")
            expr = GroupingExpr(expr)
        elif self.match(TokenType.IDENTIFIER):
            expr = IdentifierExpr(self.previous().lexeme)
        else: raise Exception(f"Expressão esperada: {self.peek().lexeme}")
        while True:
            if self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Nome esperado.").lexeme
                expr = GetExpr(expr, name)
            elif self.match(TokenType.LBRACKET):
                idx = self.expression()
                self.consume(TokenType.RBRACKET, "']' esperado.")
                expr = IndexExpr(expr, idx)
            elif self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA): break
                self.consume(TokenType.RPAREN, "')' esperado.")
                expr = CallExpr(expr, args)
            else: break
        return expr

    def app_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Nome app esperado.").lexeme
        configs = []
        if self.match(TokenType.HASH):
            while True:
                prop = normalize(self.consume(TokenType.IDENTIFIER, "Propriedade esperada.").lexeme)
                # v1.1: Permite '#ui web' ou '#ui = "web"'
                if self.match(TokenType.EQUAL):
                    val = self.expression()
                else:
                    # Se nao tem '=', assume que o proximo identificador e o valor
                    val = LiteralExpr(self.consume(TokenType.IDENTIFIER, "Valor esperado.").lexeme)

                configs.append(ConfigStmt(element_label=LiteralExpr(name), property=prop, value=val))
                if not self.match(TokenType.COMMA): break
        return AppStmt(name, configs)
    def screen_declaration(self) -> Statement: return ScreenStmt(self.consume(TokenType.IDENTIFIER, "Nome tela esperado.").lexeme)
    def object_declaration(self) -> Statement: return ObjectDefStmt(self.consume(TokenType.IDENTIFIER, "Nome objeto esperado.").lexeme)
    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t): self.advance(); return True
        return False
    def consume(self, t: TokenType, m: str) -> Token:
        if self.check(t): return self.advance()
        raise Exception(f"Erro linha {self.peek().line}: {m}")
    def check(self, t: TokenType) -> bool: return False if self.is_at_end() else self.peek().type == t
    def advance(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()
    def is_at_end(self) -> bool: return self.peek().type == TokenType.EOF
    def peek(self) -> Token: return self.tokens[self.current]
    def previous(self) -> Token: return self.tokens[self.current - 1]
