class Node:
    def __init__(self, value, child, rs):
        self.value = value
        self.child = child
        self.right_sibling = rs

    def __str__(self):
        return "({}, {}, {})".format(self.value, self.child, self.right_sibling)


class Tree:
    def __init__(self, grammar):
        self.root = None
        self.grammar = grammar
        self.crt = 1
        self.ws = ""
        self.index_in_tree_sequence = 1

    def build(self, ws):
        print(ws)
        print(len(ws))
        self.ws = ws
        non_terminal, rhs = self.grammar.get_production_for_index(int(self.ws[0]))
        self.root = Node(non_terminal, None, None)
        self.root.child = self._build_recursive(self.grammar.split_rhs(rhs))
        return self.root

    def _build_recursive(self, current_transition):
        if (self.index_in_tree_sequence == len(self.ws) and current_transition == ['E']):
           pass
        elif current_transition == [] or self.index_in_tree_sequence >= len(self.ws):
            return None
        current_symbol = current_transition[0]
        if current_symbol in self.grammar.E:
            node = Node(current_symbol, None, None)
            print("current value: " + node.value)
            print("finished terminal branch")
            node.right_sibling = self._build_recursive(current_transition[1:])
            return node
        elif current_symbol in self.grammar.N:
            transition_number = self.ws[self.index_in_tree_sequence]
            _, production = self.grammar.get_production_for_index(int(transition_number))
            node = Node(current_symbol, None, None)
            print("current value: " + node.value)
            print("finished nonterminal branch")
            self.index_in_tree_sequence += 1
            node.child = self._build_recursive(self.grammar.split_rhs(production))
            node.right_sibling = self._build_recursive(current_transition[1:])
            return node
        else:
            print('E branch')
            return Node("E", None, None)

    def print_table(self):
        self._bfs(self.root)

    def _bfs(self, node, father_crt=None, left_sibling_crt=None):
        if node is None:
            return []
        output = "{} | {} | {} | {}".format(self.crt, node.value, father_crt, left_sibling_crt)
        print(output)
        with open("output.txt", "a") as file:
                file.write(output + "\n")

        crt = self.crt
        self.crt += 1

        if left_sibling_crt is not None:
            return [[node.child, crt, None]] + self._bfs(node.right_sibling, father_crt, crt)
        else:
            children = [[node.child, crt, None]] + self._bfs(node.right_sibling, father_crt, crt)
            for child in children:
                self._bfs(*child)

    def __str__(self):
        string = ""
        node = self.root
        while node is not None:
            string += str(node)
            node = node.right_sibling
        return string