from interpreter.inter_pine.core import Parser
from interpreter.inter_pine.indicators import OrderFlowEngine, AuctionMarketEngine

def test_engines():
    # Initialize engines and parser
    order_flow = OrderFlowEngine()
    auction = AuctionMarketEngine()
    parser = Parser()
    
    # Test data
    test_trades = [
        {'volume': 100, 'side': 'buy', 'price': 100},
        {'volume': 50, 'side': 'sell', 'price': 101}
    ]
    
    # Test parser with some tokens
    test_tokens = [
        {'type': 'IDENTIFIER', 'value': 'volume_delta'},
        {'type': 'LPAREN', 'value': '('},
        {'type': 'NUMBER', 'value': 100},
        {'type': 'RPAREN', 'value': ')'}
    ]
    
    parsed_result = parser.parse(test_tokens)
    print("Parser Result:", parsed_result)
    
    # Test engines
    print("Volume Delta:", order_flow.calculate_volume_delta(test_trades))
    print("Market Profile:", auction.generate_market_profile(test_trades))

if __name__ == "__main__":
    test_engines()
