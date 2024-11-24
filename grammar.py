class Grammar:
    def __init__(self, N, E, P, S):
        self.N = N
        self.E = E
        self.P = P
        self.S = S
        self.FIRST = self.compute_first()
        self.FOLLOW = self.compute_follow(self.FIRST)
        self.parseTable = self.construct_parse_table(self.FIRST, self.FOLLOW)

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
    def parse_line(line: str) -> list[str]:
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].strip().split(',')]

    @staticmethod
    def from_file(fileName):

        with open(fileName, 'r') as file:
            N = Grammar.parse_line(file.readline())
            E = Grammar.parse_line(file.readline())
            S = file.readline().split('=')[1].strip()
            P = Grammar.parse_rules(Grammar.parse_line(''.join([line for line in file])))
            return Grammar(N, E, P, S)

    @staticmethod
    def parse_rules(rules):
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

    def split_rhs(self, prod):
        return prod.split(' ')

    def is_non_terminal(self, value):
        return value in self.N

    def is_terminal(self, value):
        return value in self.E

    def get_productions_for(self, nonTerminal):
        if not self.is_non_terminal(nonTerminal):
            raise Exception('Can only show productions for non-terminals')
        for key in self.P.keys():
            if key == nonTerminal:
                return self.P[key]

    def get_production_for_index(self, index):
        for key, value in self.P.items():
            for v in value:
                if v[1] == index:
                    return key, v[0]
    def __str__(self):
        return 'N = { ' + ', '.join(self.N) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'P = { ' + ', '.join([' -> '.join(prod) for prod in self.P]) + ' }\n' \
               + 'S = ' + str(self.S) + '\n'
    
    def compute_first(self):
        FIRST = {nt: set() for nt in self.N}
        changed = True

        while changed:
            changed = False
            for nt in self.N:
                for prod, _ in self.P[nt]:
                    for symbol in self.split_rhs(prod):
                        if self.is_terminal(symbol):
                            if symbol not in FIRST[nt]:
                                FIRST[nt].add(symbol)
                                changed = True
                            break
                        elif self.is_non_terminal(symbol):
                            new_first = FIRST[symbol] - {'E'}
                            if not new_first.issubset(FIRST[nt]):
                                FIRST[nt].update(new_first)
                                changed = True
                            if 'E' not in FIRST[symbol]:
                                break
                        else:  # Epsilon
                            if 'E' not in FIRST[nt]:
                                FIRST[nt].add('E')
                                changed = True
        return FIRST

    def compute_follow(self, FIRST):
        FOLLOW = {nt: set() for nt in self.N}
        FOLLOW[self.S].add('$')
        changed = True

        while changed:
            changed = False
            for nt in self.N:
                for prod, _ in self.P[nt]:
                    trailer = FOLLOW[nt].copy()
                    for symbol in reversed(self.split_rhs(prod)):
                        if self.is_non_terminal(symbol):
                            if not trailer.issubset(FOLLOW[symbol]):
                                FOLLOW[symbol].update(trailer)
                                changed = True
                            if 'E' in FIRST[symbol]:
                                trailer.update(FIRST[symbol] - {'E'})
                            else:
                                trailer = FIRST[symbol]
                        elif self.is_terminal(symbol):
                            trailer = {symbol}
                        else:  # Epsilon
                            trailer = {'E'}
        return FOLLOW

    def construct_parse_table(self, FIRST, FOLLOW):
        parse_table = {nt: {t: "error" for t in self.E + ['$']} for nt in self.N}
        parse_table.update({t: {t: "pop" for t in self.E + ['$']} for t in self.E})
        parse_table['$'] = {t: "error" for t in self.E}
        parse_table['$']['$'] = "acc"

        for nt in self.N:
            for prod, index in self.P[nt]:
                rhs_symbols = self.split_rhs(prod)
                if len(rhs_symbols) == 1 and rhs_symbols[0] in self.N:
                    for symbol in FIRST[rhs_symbols[0]]:
                        if symbol != 'E':
                            parse_table[nt][symbol] = (prod, index)
                        if 'E' in FIRST[rhs_symbols[0]]:
                            for follow_symbol in FOLLOW[nt]:
                                parse_table[nt][follow_symbol] = ('E', None)
        return parse_table

    def analyzeSequence(self, sequence):
        w = self.split_rhs(sequence)
        stack = [self.S, '$']
        output = ""

        while stack[0] != '$' and w:
            print(w, stack)
            if w[0] == stack[0]:
                w = w[1:]
                stack.pop(0)
            else:
                x = w[0]
                a = stack[0]
                if a not in self.parseTable or x not in self.parseTable[a]:
                    return None
                action = self.parseTable[a][x]
                if isinstance(action, tuple):
                    rhs, index = action
                    rhs = self.split_rhs(rhs)
                    for i in range(len(rhs) - 1, -1, -1):
                        if rhs[i] != 'E':
                            stack.insert(0, rhs[i])
                    output += str(index) + " "
                elif action == "error":
                    return None
                elif action == "pop":
                    stack.pop(0)
        if stack[0] == '$' and w:
            return None

        while stack[0] != '$':
            a = stack[0]
            if a in self.parseTable and '$' in self.parseTable[a]:
                action = self.parseTable[a]['$']
                if isinstance(action, tuple):
                    rhs, index = action
                    output += str(index) + " "
            stack.pop(0)

        return output

