from grammar import Grammar
from parser import Parser
from parsing_tree import Tree


class UI:

    def __init__(self):
        self.grammar = None
        self.parser = None

    def run(self):
        while True:
            print(">>")
            cmd = input()
            if cmd == "g1":
                self.evaluateG1()
            elif cmd == "g2":
                self.evaluateG2()
            elif cmd == "g2pif":
                self.evaluateG2WithPif()
            elif cmd == "g3":
                self.evaluateG3()

    def readG1(self):
        self.g1 = Grammar.from_file('g1.txt')
        print('Read g1')

    def readG2(self):
        self.g2 = Grammar.from_file('g2.txt')
        print('Read g2')

    def readG3(self):
        self.g3 = Grammar.from_file('g3.txt')
        print('Read g3')

    def readSequence(self, fname):
        sequence = ""
        with open(fname, 'r') as fin:
            for line in fin.readlines():
                sequence += line.strip() + " "
        return sequence.strip()

    def readPif(self, fname):
        pif = ""
        with open(fname, 'r') as fin:
            for line in fin.readlines():
                pif += line.strip().split(' ')[0].lower() + " "
        return pif.strip()

    def evaluateG1(self):
        self.readG1()
        self.p1 = Parser(self.g1)
        print(self.p1.first_set)
        print(self.p1.follow_set)
        for k in self.p1.table.keys():
            print(k, '->', self.p1.table[k])
        result = self.p1.evaluate_sequence(self.readSequence('sequence.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g1)
            t.build(result.strip().split(' '))
            t.print_table()


    def evaluateG2(self):
        self.readG2()
        self.p2 = Parser(self.g2)
        print(self.p2.first_set)
        print(self.p2.follow_set)
        for k in self.p2.table.keys():
            print(k, '->', self.p2.table[k])
        result = self.p2.evaluate_sequence(self.readSequence('seq2.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g2)
            t.build(result.strip().split(' '))
            t.print_table()

    def evaluateG2WithPif(self):
        self.readG2()
        self.p2 = Parser(self.g2)
        print(self.p2.first_set)
        print(self.p2.follow_set)
        for k in self.p2.table.keys():
            print(k, '->', self.p2.table[k])
        result = self.p2.evaluate_sequence(self.readPif('pif2.out'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g2)
            t.build(result.strip().split(' '))
            t.print_table()



    def evaluateG3(self):
        self.readG3()
        self.p3 = Parser(self.g3)
        print(self.p3.first_set)
        print(self.p3.follow_set)
        for k in self.p3.table.keys():
            print(k, '->', self.p3.table[k])
        result = self.p3.evaluate_sequence(self.readSequence('seq3.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g3)
            t.build(result.strip().split(' '))
            t.print_table()
