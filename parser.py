from copy import deepcopy


class Parser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.first_set = {i: set() for i in self.grammar.N}
        self.follow_set = {i: set() for i in self.grammar.N}
        self.table = {}
        self.generate_first()
        self.generate_follow()
        self.generate_table()

    def inner_loop(self, initial_set, items, additional_set):
        copy_set = initial_set
        for i in range(len(items)):
            print(f"Inner Loop: processing item {items[i]}")
            if self.grammar.is_non_terminal(items[i]):
                copy_set = copy_set.union(entry for entry in self.first_set[items[i]] if entry != 'E')
                print(f"  Added first set of {items[i]}: {self.first_set[items[i]]}")
                if 'E' in self.first_set[items[i]]:
                    if i < len(items) - 1:
                        continue
                    copy_set = copy_set.union(additional_set)
                    print(f"  Added additional set: {additional_set}")
                    break
                else:
                    break
            else:
                copy_set = copy_set.union({items[i]})
                print(f"  Added terminal: {items[i]}")
                break
        print(f"  Updated set: {copy_set}")
        return copy_set

    def generate_first(self):
        is_set_changed = False
        print("Generating First Sets...")
        for key, value in self.grammar.P.items():
            for v in value:
                v = self.grammar.split_rhs(v[0])
                copy_set = self.first_set[key]
                copy_set = copy_set.union(self.inner_loop(copy_set, v, ['E']))
                print(f"First Set for {key}: {self.first_set[key]}")

                if len(self.first_set[key]) != len(copy_set):
                    self.first_set[key] = copy_set
                    is_set_changed = True

        while is_set_changed:
            is_set_changed = False
            for key, value in self.grammar.P.items():
                for v in value:
                    v = self.grammar.split_rhs(v[0])
                    copy_set = self.first_set[key]
                    copy_set = copy_set.union(self.inner_loop(copy_set, v, ['E']))
                    print(f"First Set for {key}: {self.first_set[key]}")

                    if len(self.first_set[key]) != len(copy_set):
                        self.first_set[key] = copy_set
                        is_set_changed = True

    def generate_follow(self):
        self.follow_set[self.grammar.S].add('E')
        is_set_changed = False
        print("Generating Follow Sets...")
        for key, value in self.grammar.P.items():
            for v in value:
                v = self.grammar.split_rhs(v[0])
                for i in range(len(v)):
                    print(f"Processing {v[i]} in follow generation")
                    if not self.grammar.is_non_terminal(v[i]):
                        continue
                    copy_set = self.follow_set[v[i]]
                    if i < len(v) - 1:
                        copy_set = copy_set.union(self.inner_loop(copy_set, v[i + 1:], self.follow_set[key]))
                    else:
                        copy_set = copy_set.union(self.follow_set[key])

                    print(f"Updated Follow Set for {v[i]}: {self.follow_set[v[i]]}")

                    if len(self.follow_set[v[i]]) != len(copy_set):
                        self.follow_set[v[i]] = copy_set
                        is_set_changed = True
        while is_set_changed:
            is_set_changed = False
            for key, value in self.grammar.P.items():
                for v in value:
                    v = self.grammar.split_rhs(v[0])
                    for i in range(len(v)):
                        if not self.grammar.is_non_terminal(v[i]):
                            continue
                        copy_set = self.follow_set[v[i]]
                        if i < len(v) - 1:
                            copy_set = copy_set.union(self.inner_loop(copy_set, v[i + 1:], self.follow_set[key]))
                        else:
                            copy_set = copy_set.union(self.follow_set[key])

                        if len(self.follow_set[v[i]]) != len(copy_set):
                            self.follow_set[v[i]] = copy_set
                            is_set_changed = True

    def generate_table(self):
        non_terminals = self.grammar.N
        terminals = self.grammar.E
        print("Generating Parsing Table...")

        for key, value in self.grammar.P.items():
            row_symbol = key
            for v in value:
                rule = self.grammar.split_rhs(v[0])
                index = v[1]
                print(f"Processing rule: {key} -> {rule}")

                for column_symbol in terminals + ['E']:
                    pair = (row_symbol, column_symbol)
                    print(f"Checking pair: {pair}")
                    if rule[0] == column_symbol and column_symbol != 'E':
                        self.table[pair] = v
                    elif rule[0] in non_terminals and column_symbol in self.first_set[rule[0]]:
                        if pair not in self.table.keys():
                            self.table[pair] = v
                        else:
                            print(pair)
                            print("Grammar is not LL(1).")
                            assert False
                    else:
                        if rule[0] == 'E':
                            for b in self.follow_set[row_symbol]:
                                if b == 'E':
                                    b = '$'
                                self.table[(row_symbol, b)] = v
                        else:
                            firsts = set()
                            for symbol in self.grammar.P[row_symbol]:
                                if symbol in non_terminals:
                                    firsts = firsts.union(self.first_set[symbol])
                            if 'E' in firsts:
                                for b in self.follow_set[row_symbol]:
                                    if b == 'E':
                                        b = '$'
                                    if (row_symbol, b) not in self.table.keys():
                                        self.table[(row_symbol, b)] = v
        print("Parsing Table:")
        for key, value in self.table.items():
            print(f"{key}: {value}")

        for t in terminals:
            self.table[(t, t)] = ('pop', -1)

        self.table[('$', '$')] = ('acc', -1)

    def evaluate_sequence(self, sequence):
        w = self.grammar.split_rhs(sequence)
        stack = [self.grammar.S, '$']
        output = ""
        print(f"Evaluating sequence: {sequence}")
        while stack[0] != '$' and w:
            print(f"Stack: {stack}, Input: {w}")
            if w[0] == stack[0]:
                w = w[1:]
                stack.pop(0)
            else:
                x = w[0]
                a = stack[0]
                if (a, x) not in self.table.keys():
                    print("Error: no entry in parsing table for pair", (a, x))
                    return None
                else:
                    stack.pop(0)
                    rhs, index = self.table[(a, x)]
                    rhs = self.grammar.split_rhs(rhs)
                    for i in range(len(rhs) - 1, -1, -1):
                        if rhs[i] != 'E':
                            stack.insert(0, rhs[i])
                    output += str(index) + " "
            print(f"Output: {output}")
        if stack[0] == '$' and w:
            print("Error: input sequence not fully consumed.")
            return None
        elif not w:
            while stack[0] != '$':
                a = stack[0]
                if (a, '$') in self.table.keys():
                    output += str(self.table[(a, '$')][1]) + " "
                stack.pop(0)
            return output
