from functools import reduce
from astconstructor import AstVisitor, fib
import ast, inspect

def create_tex_file(filename, content):
    begin_tex = '\\documentclass[12pt]{article} \n'
    begin_tex += '\\usepackage[utf8]{inputenc} \n'
    begin_tex += '\\usepackage[english]{babel} \n'
    begin_tex += '\\usepackage{graphicx} \n'
    begin_tex += '\\graphicspath{ {./artifacts/} } \n'
    begin_tex += '\\begin{document} \n'
    end_tex = '\\end{document}'
    with open(f'artifacts/{filename}.tex', 'w') as f:
        f.write(begin_tex)
        f.write(content)
        f.write(end_tex)


def easy(table, create_file=True):
    latex = '\\begin{tabular}'
    latex += '{ '
    n = max(map(len, table))
    latex += '|c' * n
    latex += '| } \n'
    sep = '\\hline \n'
    ampersand = ' & '
    newline = ' \\\\\n'
    latex += sep
    contents = reduce(
        lambda line, other_lines: line + sep + other_lines,
        map(
            lambda current_line: reduce(lambda elem, other_elems: str(elem) + ampersand + str(other_elems),
                                        current_line) + newline,
            table
        )
    )
    latex += contents
    latex += sep
    latex += '\\end{tabular}\n'
    if create_file:
        create_tex_file('easy_task', latex)
    return latex


def medium(table, graphics_path):
    latex = easy(table, create_file=False)
    latex += '\n\n\n'
    latex += '\\includegraphics[scale=0.1]{' + graphics_path + '} \n'
    create_tex_file('medium_task', latex)


def main():
    rows, columns = 3, 5
    table = [[str(i + j) for j in range(columns)] for i in range(rows)]
    table.append([f'column {i}' for i in range(6)])
    print('-- table --')
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j], end=' ')
        print('')
    print('-- table --')
    latex = easy(table)
    print('-- generated latex by easy --')
    print(latex)
    print('-- generated latex by easy --')
    print('-- generating tex for medium task --')
    ast_obj = ast.parse(inspect.getsource(fib))
    visitor = AstVisitor()
    visitor.visit(ast_obj)
    visitor.draw_graph()
    medium(table, 'ast.png')
    print('-- tex generated successfully --')


if __name__ == "__main__":
    main()
