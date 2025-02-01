def _handle_map_operation(self, operation_name, args):
    if operation_name == 'mapClearFunc':
        args[0].clear()
        return args[0]
    
    elif operation_name == 'mapContainsFunc':
        return args[1] in args[0]
    
    elif operation_name == 'mapCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'mapGetFunc':
        return args[0].get(args[1])
    
    elif operation_name == 'mapKeysFunc':
        return list(args[0].keys())
    
    elif operation_name == 'mapNewTypeFunc':
        return {}
    
    elif operation_name == 'mapPutFunc':
        args[0][args[1]] = args[2]
        return args[0]
    
    elif operation_name == 'mapPutAllFunc':
        args[0].update(args[1])
        return args[0]
    
    elif operation_name == 'mapRemoveFunc':
        if args[1] in args[0]:
            del args[0][args[1]]
        return args[0]
    
    elif operation_name == 'mapSizeFunc':
        return len(args[0])
    
    elif operation_name == 'mapValuesFunc':
        return list(args[0].values())

    elif operation_name == 'mapNewBoolFunc':
        return {'type': 'bool', 'value': bool(args[0]) if args else False}
        
    elif operation_name == 'mapNewFloatFunc':
        return {'type': 'float', 'value': float(args[0]) if args else 0.0}
        
    elif operation_name == 'mapNewIntFunc':
        return {'type': 'int', 'value': int(args[0]) if args else 0}
        
    elif operation_name == 'mapNewStringFunc':
        return {'type': 'string', 'value': str(args[0]) if args else ''}
