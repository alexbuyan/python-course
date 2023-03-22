import ast

from astconstructor import AstVisitor

if __name__ == "__main__":
    with open('astconstructor/fib.py', 'r') as f:
        ast_obj = ast.parse(f.read())
        visitor = AstVisitor()
        visitor.visit(ast_obj)
        visitor.draw_graph()