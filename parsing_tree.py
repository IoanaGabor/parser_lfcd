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
        self.indexInTreeSequence = 1

    def build(self, ws):
        print(ws)
        print(len(ws))
        self.ws = ws
        nonterminal, rhs = self.grammar.getProductionForIndex(int(self.ws[0]))
        self.root = Node(nonterminal, None, None)
        self.root.child = self.build_recursive(self.grammar.splitRhs(rhs))
        return self.root

    def build_recursive(self, currentTransition):
        if self.indexInTreeSequence == len(self.ws) and currentTransition == ['E']:
           pass
        elif currentTransition == [] or self.indexInTreeSequence >= len(self.ws):
            return None
        currentSymbol = currentTransition[0]
        if currentSymbol in self.grammar.E:
            node = Node(currentSymbol, None, None)
            print("current value: " + node.value)
            print("finished terminal branch")
            node.right_sibling = self.build_recursive(currentTransition[1:])
            return node
        elif currentSymbol in self.grammar.N:
            transitionNumber = self.ws[self.indexInTreeSequence]
            _, production = self.grammar.getProductionForIndex(int(transitionNumber))
            node = Node(currentSymbol, None, None)
            print("current value: " + node.value)
            print("finished nonterminal branch")
            self.indexInTreeSequence += 1
            node.child = self.build_recursive(self.grammar.splitRhs(production))
            node.right_sibling = self.build_recursive(currentTransition[1:])
            return node
        else:
            print('E branch')
            return Node("E", None, None)

    def print_table(self):
        self.bfs(self.root)

    def bfs(self, node, father_crt=None, left_sibling_crt=None):
        if node is None:
            return []
        print("{} | {} | {} | {}".format(self.crt, node.value, father_crt, left_sibling_crt))

        crt = self.crt
        self.crt += 1

        if left_sibling_crt is not None:
            return [[node.child, crt, None]] + self.bfs(node.right_sibling, father_crt, crt)
        else:
            children = [[node.child, crt, None]] + self.bfs(node.right_sibling, father_crt, crt)
            for child in children:
                self.bfs(*child)

    def __str__(self):
        string = ""
        node = self.root
        while node is not None:
            string += str(node)
            node = node.right_sibling
        return string