from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class InocNode: pass

@dataclass
class Expression(InocNode): pass

@dataclass
class ObjectLiteralExpr(Expression): pass

@dataclass
class ListLiteralExpr(Expression):
    elements: List[Expression]

@dataclass
class LiteralExpr(Expression):
    value: Any

@dataclass
class IdentifierExpr(Expression):
    name: str

@dataclass
class UnaryExpr(Expression):
    operator: str
    right: Expression

@dataclass
class BinaryExpr(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class LogicalExpr(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class GetExpr(Expression):
    obj: Expression
    name: str

@dataclass
class IndexExpr(Expression):
    target: Expression
    index: Expression

@dataclass
class GroupingExpr(Expression):
    expression: Expression

@dataclass
class CallExpr(Expression):
    callee: Expression
    arguments: List[Expression]

@dataclass
class Statement(InocNode): pass

@dataclass
class Program(InocNode):
    statements: List[Statement]

@dataclass
class AppStmt(Statement):
    name: str
    configs: List['ConfigStmt']

@dataclass
class ScreenStmt(Statement):
    name: str

@dataclass
class ObjectDefStmt(Statement):
    name: str

@dataclass
class ModuleStmt(Statement):
    name: str

@dataclass
class FunctionStmt(Statement):
    name: str
    params: List[str]
    body: List[Statement]

@dataclass
class ReturnStmt(Statement):
    value: Optional[Expression]

@dataclass
class AssignmentStmt(Statement):
    name: str
    value: Expression

@dataclass
class SetStmt(Statement):
    obj: Expression
    name: str
    value: Expression

@dataclass
class SetIndexStmt(Statement):
    target: Expression
    index: Expression
    value: Expression

@dataclass
class PrintStmt(Statement):
    value: Expression

@dataclass
class ConfigStmt(Statement):
    element_label: Expression
    property: str
    value: Expression

@dataclass
class ElementStmt(Statement):
    element_type: str
    content: Expression
    configs: List[ConfigStmt]
    line: int = 0

@dataclass
class ContainerStmt(Statement):
    name: str
    configs: List[ConfigStmt]
    children: List[Statement]
    line: int = 0

@dataclass
class InputStmt(Statement):
    target: Expression

@dataclass
class InputExpr(Expression):
    id_label: Expression

@dataclass
class UIRefExpr(Expression):
    name: str

@dataclass
class EventStmt(Statement):
    target: Expression

@dataclass
class NavigationStmt(Statement):
    label: Expression
    target: str

@dataclass
class ElseIfBranch:
    condition: Expression
    body: List[Statement]

@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: List[Statement]
    elif_branches: List[ElseIfBranch]
    else_branch: List[Statement]

@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class ForEachStmt(Statement):
    item_name: str
    collection: Expression
    body: List[Statement]
