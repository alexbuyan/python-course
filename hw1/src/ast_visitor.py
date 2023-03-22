import ast
import networkx as nx


class AstVisitor(ast.NodeVisitor):
    def __init__(self):
        self.__graph = nx.Graph()
        self.__counter = 0
        self.__node_styles = dict()

    def draw_graph(self):
        agraph = nx.drawing.nx_agraph.to_agraph(nx.dfs_tree(self.__graph))
        for node in agraph.nodes():
            node_counter = int(node)
            for k, v in self.__node_styles[node_counter].items():
                node.attr[k] = v
        agraph.layout('dot')
        agraph.draw('artifacts/ast.png', format='png')

    def __get_node_name(self, node):
        return node.__class__.__name__

    def __visit_node(self, node, name, fillcolor='white', shape='circle'):
        self.__counter += 1
        node_counter = self.__counter
        self.__node_styles[node_counter] = {
            'style': 'filled',
            'label': name,
            'fillcolor': fillcolor,
            'shape': shape
        }

        self.__graph.add_node(node_counter)
        neighbours = self.generic_visit(node)

        edges = []
        for neighbor in neighbours:
            edges.append((node_counter, neighbor))
        self.__graph.add_edges_from(edges)

        return node_counter

    def generic_visit(self, node):
        neighbours = []
        for _, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                neighbor = self.visit(value)
                if not isinstance(neighbor, list):
                    neighbours.append(neighbor)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        neighbor = self.visit(item)
                        if not isinstance(neighbor, list):
                            neighbours.append(neighbor)
        return neighbours

    def visit_FunctionDef(self, node):
        return self.__visit_node(node, f'Function "{node.name}"', fillcolor='lightyellow')

    def visit_arguments(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='lightcoral', shape='rectangle')

    def visit_arg(self, node):
        return self.__visit_node(node, f'arg "{node.arg}"', fillcolor='lightcoral', shape='square')

    def visit_Name(self, node):
        return self.__visit_node(node, f'var "{node.id}"', fillcolor='springgreen', shape='diamond')

    def visit_Assign(self, node):
        return self.__visit_node(node, '=', fillcolor='darkorange', shape='square')

    def visit_List(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='palegreen', shape='polygon')

    def visit_Constant(self, node):
        return self.__visit_node(node, f'const {node.value}', fillcolor='gold', shape='cds')

    def visit_Expr(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='pink')

    def visit_Call(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='hotpink')

    def visit_BinOp(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='darkorange', shape='square')

    def visit_Add(self, node):
        return self.__visit_node(node, '+', fillcolor='darkorange', shape='square')

    def visit_Sub(self, node):
        return self.__visit_node(node, '-', fillcolor='darkorange', shape='square')

    def visit_Return(self, node):
        return self.__visit_node(node, self.__get_node_name(node), fillcolor='fuchsia', shape='larrow')

    def visit_For(self, node):
        return self.__visit_node(node, f'{self.__get_node_name(node)} loop', fillcolor='skyblue', shape='ellipse')

    def visit_Attribute(self, node):
        return self.__visit_node(node, f"attr: {node.attr}", fillcolor='violet', shape='rect')

    def visit_Subscript(self, node):
        return self.__visit_node(node, '[ ]', fillcolor='cornflowerblue', shape='square')
