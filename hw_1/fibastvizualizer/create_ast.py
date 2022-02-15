import ast
import networkx as nx

from fibastvizualizer import fib
from .fib_ast_visitor import DefAstVisitor


def generate_png(path: str):
    with open(fib.__file__, 'r') as file:
        data = file.read()
    module = ast.parse(data)
    tree = nx.DiGraph()
    visitor = DefAstVisitor(tree)
    visitor.visit(module)
    pydot_tree = nx.drawing.nx_pydot.to_pydot(tree)
    pydot_tree.write_png(path)


if __name__ == "__main__":
    generate_png('../artifacts/ast.png')
