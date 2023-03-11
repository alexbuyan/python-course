import ast

from ast_visitor import AstVisitor


def main():
    with open('fib.py', 'r') as f:
        ast_obj = ast.parse(f.read())
        visitor = AstVisitor()
        visitor.visit(ast_obj)
        visitor.draw_graph()


if __name__ == "__main__":
    main()
