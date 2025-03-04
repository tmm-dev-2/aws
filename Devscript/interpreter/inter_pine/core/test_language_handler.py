from language_handler import LanguageHandler

def test_multilanguage():
    handler = LanguageHandler()
    
    # Test Python
    python_code = """
    data = [1, 2, 3, 4, 5]
    result = sum(data)/len(data)
    """
    handler.execute(python_code, 'python')
    
    # Test R
    r_code = """
    x <- c(1, 2, 3, 4, 5)
    mean(x)
    """
    r_result = handler.execute(r_code, 'r')
    print(f"R calculation result: {r_result[0]}")
    
    # Share data between languages
    handler.share_data('prices', [10, 20, 30, 40, 50])
    
    # Use shared data in R
    r_shared = """
    prices <- c(prices)
    mean(prices)
    """
    shared_result = handler.execute(r_shared, 'r')
    print(f"Shared data calculation: {shared_result[0]}")

if __name__ == "__main__":
    test_multilanguage()
