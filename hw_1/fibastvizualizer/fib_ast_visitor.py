import ast
from typing import Tuple

import networkx as nx

_COLORS = {
    'Constant': '#FF00FF',
    'Module': '#800080',
    'Name': '#FFFF00',
    'Load': '#808080',
    'Store': '#808080',
    'Tuple': '#FF8000',
    'List': '#FF8000',
    'BinOp': '#00BFFF',
    'Add': '#00BFFF',
    'Sub': '#00BFFF',
    'Call': '#008000',
    'Assign': '#FF0000',
    'For': '#FF8080',
    'Return': '#FF8080',
    'FunctionDef': '#FF8080',
    'Attribute': '#808000',
    'Expr': '#66FF00',
    'arguments': '#BBFF66',
    'arg': '#BBFF66'
}


def get_label_color(node: ast.AST) -> Tuple[str, str]:
    label = node.__class__.__name__
    color = _COLORS.get(label, '#FFFFFF')
    if isinstance(node, ast.Constant):
        label = f"Const = {node.value}"
    elif isinstance(node, ast.Name):
        label = f"Name = {node.id}"
    elif isinstance(node, ast.Attribute):
        label = f"Attr = {node.attr}"
    elif isinstance(node, ast.Sub):
        label = "-"
    elif isinstance(node, ast.Add):
        label = "+"
    elif isinstance(node, ast.FunctionDef):
        label = f"Def {node.name}"
    elif isinstance(node, ast.arg):
        label = f"arg = {node.arg}"
    return label, color


class DefAstVisitor:

    def __init__(self, graph: nx.DiGraph):
        self._graph = graph
        self._n_node = 0

    def visit(self, node: ast.AST) -> int:
        node_idx = self._n_node
        label, color = get_label_color(node)
        self._graph.add_node(node_idx, label=label, color=color, style='filled', shape='rect')
        self._n_node += 1

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        child_idx = self.visit(item)
                        self._graph.add_edge(node_idx, child_idx)
            elif isinstance(value, ast.AST):
                child_idx = self.visit(value)
                self._graph.add_edge(node_idx, child_idx)
        return node_idx
