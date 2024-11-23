from grammar import Grammar

file_name = 'g1.txt'
grammar = Grammar.fromFile(file_name)

print(grammar)

print(Grammar.validate(grammar.N, grammar.E, grammar.P, grammar.S))

productions_S = grammar.getProductionsFor('S')
print("Productions for S:", productions_S)

production_index = grammar.getProductionForIndex(2)
print("Production at pos 2:", production_index)

symbol = 'A'
print(f"{symbol} is Non-Terminal:", grammar.isNonTerminal(symbol))
print(f"{symbol} is Terminal:", grammar.isTerminal(symbol))