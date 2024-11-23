class Grammar:
    def __init__(self, N, E, P, S):
        self.N = N
        self.E = E
        self.P = P
        self.S = S

    @staticmethod
    def validate(N, E, P, S):
        if S not in N:
            return False
        for key in P.keys():
            if key not in N:
                return False
            for move in P[key]:
                for char in move:
                    if char not in N and char not in E and char != 'E':
                        return False
        return True

    @staticmethod
    def parseLine(line: str) -> list[str]:
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].strip().split(',')]

    @staticmethod
    def fromFile(fileName):

        with open(fileName, 'r') as file:
            N = Grammar.parseLine(file.readline())
            E = Grammar.parseLine(file.readline())
            S = file.readline().split('=')[1].strip()
            P = Grammar.parseRules(Grammar.parseLine(''.join([line for line in file])))

            return Grammar(N, E, P, S)

    @staticmethod
    def parseRules(rules):
        result = {}
        index = 1

        for rule in rules:
            print(rule)
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]

            for value in rhs:
                if lhs in result.keys():
                    result[lhs].append((value,index))
                else:
                    result[lhs] = [(value,index)]
                index+=1

        return result

    def splitRhs(self, prod):
        return prod.split(' ')

    def isNonTerminal(self, value):
        return value in self.N

    def isTerminal(self, value):
        return value in self.E

    def getProductionsFor(self, nonTerminal):
        if not self.isNonTerminal(nonTerminal):
            raise Exception('Can only show productions for non-terminals')
        for key in self.P.keys():
            if key == nonTerminal:
                return self.P[key]

    def getProductionForIndex(self, index):
        for key, value in self.P.items():
            for v in value:
                if v[1] == index:
                    return key, v[0]
    def __str__(self):
        return 'N = { ' + ', '.join(self.N) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'P = { ' + ', '.join([' -> '.join(prod) for prod in self.P]) + ' }\n' \
               + 'S = ' + str(self.S) + '\n'