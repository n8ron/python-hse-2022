import ast

import networkx as nx
from fib_ast_visitor import DefAstVisitor

if __name__ == "__main__":
    with open('fib.py', 'r') as file:
        data = file.read()
    module = ast.parse(data)
    tree = nx.DiGraph()
    visitor = DefAstVisitor(tree)
    visitor.visit(module)
    pydot_tree = nx.drawing.nx_pydot.to_pydot(tree)
    pydot_tree.write_png('../artifacts/ast.png')
