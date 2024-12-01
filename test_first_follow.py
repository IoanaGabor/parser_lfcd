import unittest
from parser import Parser


class Grammar:
    def __init__(self, N, E, S, P):
        self.N = N
        self.E = E
        self.S = S
        self.P = P

    def isNonTerminal(self, symbol):
        return symbol in self.N

    def splitRhs(self, rhs):
        return rhs.split()


class TestFirstFollow(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(
            N={"program", "statement", "statement_list", "compound_statement", "expression",
               "term", "factor", "iostmt", "simple_type", "array_declaration",
               "declaration_stmt", "assignment_statement", "if_statement",
               "while_statement", "return_statement", "for_statement", "for_header",
               "condition", "relation"},
            E={"begin", "(", ")", "{", "}", ";", "+", "-", "*", "/", "%", "<", "<=", ">",
               ">=", "and", "or", "read", "show", "if", "elif", "else", "while", "becomes",
               "eq", "diff", "int", "float", "string", "stop"},
            S="program",
            P={
                "program": [("begin compound_statement stop", 0)],
                "statement": [("declaration_stmt", 1), ("assignment_statement", 2),
                              ("if_statement", 3), ("while_statement", 4),
                              ("return_statement", 5), ("for_statement", 6), ("iostmt", 7)],
                "statement_list": [("statement", 8), ("statement ; statement_list", 9)],
                "compound_statement": [("{ statement_list }", 10)],
                "expression": [("expression + term", 11), ("expression - term", 12),
                               ("term", 13)],
                "term": [("term * factor", 14), ("term / factor", 15),
                         ("term % factor", 16), ("factor", 17)],
                "factor": [("( expression )", 18), ("IDENTIFIER", 19), ("CONST", 20)],
                "iostmt": [("read ( IDENTIFIER )", 21), ("show ( IDENTIFIER )", 22),
                           ("show ( CONST )", 23)],
                "simple_type": [("int", 24), ("string", 25), ("float", 26)],
                "array_declaration": [("array simple_type IDENTIFIER [ ]", 27)],
                "declaration_stmt": [("simple_type IDENTIFIER", 28),
                                     ("array_declaration", 29)],
                "assignment_statement": [("IDENTIFIER becomes expression", 30)],
                "if_statement": [("if ( condition ) compound_statement", 31),
                                 ("if ( condition ) compound_statement else compound_statement", 32)],
                "while_statement": [("while ( condition ) compound_statement", 33)],
                "return_statement": [("return expression", 34)],
                "for_statement": [("for for_header compound_statement", 35)],
                "for_header": [("( int assignment_statement ; condition ; assignment_statement )", 36)],
                "condition": [("expression relation expression", 37)],
                "relation": [("<", 38), ("<=", 39), ("eq", 40), ("diff", 41), (">=", 42), (">", 43)],
            }
        )
        self.parser = Parser(self.grammar)

    def test_first_set(self):
        # Convert sets to sorted lists for comparison
        expected_first = {
            "program": {"begin"},
            "statement": {"int", "string", "float", "IDENTIFIER", "if", "while", "return", "for", "read", "show"},
            "expression": {"(", "IDENTIFIER", "CONST"},
            "term": {"(", "IDENTIFIER", "CONST"},
            "factor": {"(", "IDENTIFIER", "CONST"},
            "relation": {"<", "<=", "eq", "diff", ">=", ">"},
        }
        for non_terminal, expected in expected_first.items():
            with self.subTest(non_terminal=non_terminal):
                self.assertEqual(set(self.parser.firstSet[non_terminal]), expected)

    def test_follow_set(self):
        # Convert sets to sorted lists for comparison
        expected_follow = {
            "program": {"$"},
            "statement": {";", "}"},
            "expression": {")", ";", "+", "-", "<", "<=", ">", ">=", "eq", "diff"},
            "term": {"+", "-", ")", ";", "<", "<=", ">", ">=", "eq", "diff"},
            "factor": {"*", "/", "%", "+", "-", ")", ";", "<", "<=", ">", ">=", "eq", "diff"},
        }
        for non_terminal, expected in expected_follow.items():
            with self.subTest(non_terminal=non_terminal):
                self.assertEqual(set(self.parser.followSet[non_terminal]), expected)


if __name__ == "__main__":
    unittest.main()
