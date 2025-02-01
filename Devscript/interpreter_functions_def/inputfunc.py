def _handle_input_operation(self, operation_name, args):
    if operation_name == 'inputFunc':
        return args[0]
    
    elif operation_name == 'inputBoolFunc':
        return bool(args[0])
    
    elif operation_name == 'inputColFunc':
        return args[0]
    
    elif operation_name == 'inputEnumFunc':
        options = args[1]
        default_index = args[2] if len(args) > 2 else 0
        return options[default_index]
    
    elif operation_name == 'inputFloatFunc':
        return float(args[0])
    
    elif operation_name == 'inputIntFunc':
        return int(args[0])
    
    elif operation_name == 'inputPriceFunc':
        return float(args[0])
    
    elif operation_name == 'inputSessionFunc':
        return args[0]
    
    elif operation_name == 'inputSourceFunc':
        return args[0]
    
    elif operation_name == 'inputStringFunc':
        return str(args[0])
    
    elif operation_name == 'inputSymbolFunc':
        return args[0]
    
    elif operation_name == 'inputTextAreaFunc':
        return args[0]
    
    elif operation_name == 'inputTimeFunc':
        return args[0]
    
    elif operation_name == 'inputTimeFrameFunc':
        return args[0]
