from grammar import Grammar
from parsing_tree import Tree
class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = grammar.FIRST
        self.followSet = grammar.FOLLOW
        self.table = grammar.parseTable
    def analyze_sequence(self, sequence):
        return self.grammar.analyzeSequence(sequence)
def read_sequence(fname):
    sequence = ""
    with open(fname, 'r') as fin:
        for line in fin.readlines():
            sequence += line.strip() + " "
    return sequence.strip()

def main():
    file_name = 'g1.txt'
    sequence_file = 'sequence.txt'
    grammar = Grammar.from_file(file_name)

    print(grammar)
    parser = Parser(grammar)

    print("FIRST Set:", parser.firstSet)
    print("FOLLOW Set:", parser.followSet)

    print("Parse Table:")
    for k, v in parser.table.items():
        print(f"{k} -> {v}")

    sequence = read_sequence(sequence_file)
    print(f"Input Sequence: {sequence}")
    result = parser.analyze_sequence(sequence)

    if result is None:
        print("Sequence not accepted.")
    else:
        print("Sequence accepted with result:", result)

        tree = Tree(grammar)
        tree.build(result.strip().split())
        print("Parsing Tree:")
        tree.print_table()

if __name__ == "__main__":
    main()
