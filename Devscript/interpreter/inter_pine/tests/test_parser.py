import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.parser import Parser, NodeType, Token, TokenType
from core.tokenizer import Tokenizer

class TestParser(unittest.TestCase):
    def parse_code(self, code: str):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_literals(self):
        test_cases = [
            ("42", NodeType.LITERAL),
            ("3.14", NodeType.LITERAL),
            ("'hello'", NodeType.LITERAL),
            ("true", NodeType.LITERAL),
            ("false", NodeType.LITERAL),
        ]
        
        for code, expected_type in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, expected_type)

    def test_binary_operations(self):
        test_cases = [
            ("1 + 2", "+"),
            ("3 - 4", "-"),
            ("5 * 6", "*"),
            ("8 / 2", "/"),
            ("9 > 8", ">"),
            ("7 < 10", "<"),
            ("5 >= 5", ">="),
            ("6 <= 6", "<="),
            ("7 == 7", "=="),
            ("8 != 9", "!="),
        ]
        
        for code, operator in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.BINARY_OP)
            self.assertEqual(ast.children[0].value, operator)

    def test_variable_declarations(self):
        test_cases = [
            "var x = 10;",
            "var myString = 'test';",
            "var isTrue = true;",
            "var price = close;",
            "var ma = sma(close, 14);"
        ]
        
        for code in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.VARIABLE_DECL)

    def test_assignments(self):
        test_cases = [
            "x = 100;",
            "myMA = sma(close, 14);",
            "signal = crossover(fast, slow);",
            "result = (high + low) / 2;"
        ]
        
        for code in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.ASSIGNMENT)

    def test_function_calls(self):
        test_cases = [
            ("plot(close)", 1),
            ("sma(close, 14)", 2),
            ("rsi(close, 14, 'RSI')", 3),
            ("crossover(fast, slow)", 2),
            ("strategy.entry('Long', strategy.long, when = close > open)", 3)
        ]
        
        for code, arg_count in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.FUNCTION_CALL)
            self.assertEqual(len(ast.children[0].children), arg_count)

    def test_control_flow(self):
        test_cases = [
            """
            if (close > open) {
                buy := true;
            } else {
                buy := false;
            }
            """,
            """
            for i = 0 to 10 {
                sum := sum + close[i];
            }
            """,
            """
            while (condition) {
                counter := counter + 1;
            }
            """
        ]
        
        expected_types = [NodeType.IF_STATEMENT, NodeType.FOR_STATEMENT, NodeType.WHILE_STATEMENT]
        
        for code, expected_type in zip(test_cases, expected_types):
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, expected_type)

    def test_complex_expressions(self):
        test_cases = [
            "sma(ema(close, 12), rsi(close, 14));",
            "(high + low + close) / 3;",
            "crossover(sma(close, 10), sma(close, 20));",
            "strategy.position_size > 0 and rsi(close, 14) < 30;"
        ]
        
        for code in test_cases:
            ast = self.parse_code(code)
            self.assertIsNotNone(ast)
            self.assertTrue(len(ast.children) > 0)

    def test_error_handling(self):
        test_cases = [
            "1 +;",
            "if (true) {",
            "func(;",
            "var ;",
            "x = ;"
        ]
        
        for code in test_cases:
            parser = Parser(Tokenizer(code).tokenize())
            ast = parser.parse()
            self.assertTrue(parser.had_error)
            self.assertTrue(len(parser.errors) > 0)

    def test_member_access(self):
        test_cases = [
            "strategy.entry;",
            "series.close;",
            "indicator.sma;",
            "plot.style_line;"
        ]
        
        for code in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.MEMBER_ACCESS)

    def test_array_access(self):
        test_cases = [
            "close[1];",
            "high[i];",
            "sma[length - 1];",
            "values[index + offset];"
        ]
        
        for code in test_cases:
            ast = self.parse_code(code)
            self.assertEqual(ast.children[0].type, NodeType.ARRAY_ACCESS)

if __name__ == '__main__':
    unittest.main()
