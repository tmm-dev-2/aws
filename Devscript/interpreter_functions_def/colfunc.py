def _handle_color_operation(self, operation_name, args):
    if operation_name == 'colFunc':
        return {'r': args[0], 'g': args[1], 'b': args[2], 't': args[3] if len(args) > 3 else 0}
    
    elif operation_name == 'colBFunc':
        return args[0]['b']
    
    elif operation_name == 'colFromGradientFunc':
        start_color = args[0]
        end_color = args[1]
        step = args[2]
        return {
            'r': start_color['r'] + (end_color['r'] - start_color['r']) * step,
            'g': start_color['g'] + (end_color['g'] - start_color['g']) * step,
            'b': start_color['b'] + (end_color['b'] - start_color['b']) * step,
            't': start_color['t'] + (end_color['t'] - start_color['t']) * step
        }
    
    elif operation_name == 'colGFunc':
        return args[0]['g']
    
    elif operation_name == 'colNewFunc':
        return {'r': 0, 'g': 0, 'b': 0, 't': 0}
    
    elif operation_name == 'colRFunc':
        return args[0]['r']
    
    elif operation_name == 'colRgbFunc':
        return {'r': args[0], 'g': args[1], 'b': args[2], 't': args[3] if len(args) > 3 else 0}
    
    elif operation_name == 'colTFunc':
        return args[0]['t']
