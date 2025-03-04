import unittest
from tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_trading_syntax(self):
        code = "rsi(close, 14) > sma(close, 200) and macd(close, 12, 26, 9)"
        tokens = self.tokenizer.tokenize(code)
        self.assertIn(('SYNTAX', 'rsi'), tokens)
        self.assertIn(('SYNTAX', 'sma'), tokens)
        self.assertIn(('SYNTAX', 'macd'), tokens)

    def test_python_control_flow(self):
        code = "if close > sma(close, 20): return True"
        tokens = self.tokenizer.tokenize(code, language='python')
        self.assertIn(('CONTROL', 'if'), tokens)
        self.assertIn(('CONTROL', 'return'), tokens)
        self.assertIn(('BOOLEAN', 'True'), tokens)

    def test_rust_specific(self):
        code = "fn calculate_ma(price: f64) -> f64 { let mut sum = 0.0; }"
        tokens = self.tokenizer.tokenize(code, language='rust')
        self.assertIn(('CONTROL', 'fn'), tokens)
        self.assertIn(('OPERATOR', '->'), tokens)
        self.assertIn(('IDENTIFIER', 'f64'), tokens)

    def test_r_specific(self):
        code = "ma <- mean(close) if(!is.na(close))"
        tokens = self.tokenizer.tokenize(code, language='r')
        self.assertIn(('OPERATOR', '<-'), tokens)
        self.assertIn(('SPECIAL', 'NA'), tokens)

    def test_operators(self):
        code = "a += b * c && d || !e"
        tokens = self.tokenizer.tokenize(code)
        self.assertIn(('OPERATOR', '+='), tokens)
        self.assertIn(('OPERATOR', '*'), tokens)
        self.assertIn(('OPERATOR', '&&'), tokens)
        self.assertIn(('OPERATOR', '||'), tokens)
        self.assertIn(('OPERATOR', '!'), tokens)

    def test_scientific_notation(self):
        code = "1e-10 2.5e+3 -3.14e2"
        tokens = self.tokenizer.tokenize(code)
        self.assertEqual(tokens[0], ('NUMBER', 1e-10))
        self.assertEqual(tokens[1], ('NUMBER', 2.5e+3))
        self.assertEqual(tokens[2], ('NUMBER', -3.14e2))

    def test_string_with_escapes(self):
        code = '"Hello\\nWorld" "Quotes \\"inside\\""'
        tokens = self.tokenizer.tokenize(code)
        self.assertEqual(tokens[0], ('STRING', 'Hello\\nWorld'))
        self.assertEqual(tokens[1], ('STRING', 'Quotes \\"inside\\"'))

    def test_special_symbols(self):
        code = "@decorator #comment $variable"
        tokens = self.tokenizer.tokenize(code)
        self.assertIn(('SPECIAL', '@'), tokens)
        self.assertIn(('SPECIAL', '#'), tokens)
        self.assertIn(('SPECIAL', '$'), tokens)

    def test_mixed_language_trading(self):
        code = """
        if crossover(sma(close, 20), sma(close, 50)):
            strategy.entry("Long", strategy.long)
        """
        tokens = self.tokenizer.tokenize(code)
        self.assertIn(('CONTROL', 'if'), tokens)
        self.assertIn(('SYNTAX', 'crossover'), tokens)
        self.assertIn(('SYNTAX', 'strategy.entry'), tokens)

if __name__ == '__main__':
    unittest.main()
