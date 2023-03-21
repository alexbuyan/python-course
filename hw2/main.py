from functools import reduce

def create_tex_file(filename, content):
    begin_tex = '\\documentclass[12pt]{article} \n'
    begin_tex += '\\usepackage[utf8]{inputenc} \n'
    begin_tex += '\\usepackage[english]{babel} \n'
    # TODO add graphix
    begin_tex += '\\begin{document} \n'
    end_tex = '\\end{document}'
    with open(f'artifacts/{filename}.txt', 'w') as f:
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


def medium():
    pass


def main():
    rows, columns = 3, 5
    table = [[str(i + j) for j in range(columns)] for i in range(rows)]
    table.append([f'column {i}' for i in range(rows + columns)])
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


if __name__ == "__main__":
    main()
