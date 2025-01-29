def _handle_weird_operation(self, operation_name, args):
    if operation_name == 'dayOfMonthFunc':
        return datetime.now().day
    
    elif operation_name == 'dayOfWeekFunc':
        return datetime.now().weekday()
    
    elif operation_name == 'fillFunc':
        return args[0]
    
    elif operation_name == 'fixNanFunc':
        return args[1] if args[0] is None or math.isnan(args[0]) else args[0]
    
    elif operation_name == 'floatFunc':
        return float(args[0])
    
    elif operation_name == 'hLineFunc':
        return {'price': args[0], 'color': args[1] if len(args) > 1 else None}
    
    elif operation_name == 'hourFunc':
        return datetime.now().hour
    
    elif operation_name == 'indicatorFunc':
        return {'name': args[0], 'parameters': args[1:]}
    
    elif operation_name == 'maxBarsBackFunc':
        return args[0]
    
    elif operation_name == 'minuteFunc':
        return datetime.now().minute
    
    elif operation_name == 'monthFunc':
        return datetime.now().month
    
    elif operation_name == 'naFunc':
        return None
    
    elif operation_name == 'nzFunc':
        return args[1] if args[0] is None else args[0]
    
    elif operation_name == 'barColFunc':
        return args[0]
    
    elif operation_name == 'bgColFunc':
        return args[0]
    
    elif operation_name == 'boolFunc':
        return bool(args[0])

    elif operation_name == 'polylineDeleteFunc':
        return None
        
    elif operation_name == 'polylineNewFunc':
        return {'points': [], 'color': args[0] if args else None}
        
    elif operation_name == 'requestCurrencyRateFunc':
        return {'currency': args[0], 'rate': args[1]}
        
    elif operation_name == 'requestDividendsFunc':
        return {'symbol': args[0], 'dividends': args[1]}
        
    elif operation_name == 'requestEarningsFunc':
        return {'symbol': args[0], 'earnings': args[1]}
        
    elif operation_name == 'requestEconomicFunc':
        return {'indicator': args[0], 'value': args[1]}
        
    elif operation_name == 'requestFinancialFunc':
        return {'symbol': args[0], 'data': args[1]}
        
    elif operation_name == 'requestQuandlFunc':
        return {'code': args[0], 'data': args[1]}
        
    elif operation_name == 'requestSecurityFunc':
        return {'symbol': args[0], 'data': args[1]}
        
    elif operation_name == 'requestSecurityLowerTfFunc':
        return {'symbol': args[0], 'timeframe': args[1], 'data': args[2]}
        
    elif operation_name == 'requestSeedFunc':
        return args[0]
        
    elif operation_name == 'requestSplitsFunc':
        return {'symbol': args[0], 'splits': args[1]}
        
    elif operation_name == 'runtimeErrorFunc':
        raise RuntimeError(args[0])
        
    elif operation_name == 'secondFunc':
        return datetime.now().second
