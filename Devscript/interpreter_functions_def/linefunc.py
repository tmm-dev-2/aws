def _handle_line_operation(self, operation_name, args):
    if operation_name == 'lineFunc':
        return {
            'x1': args[0],
            'y1': args[1],
            'x2': args[2],
            'y2': args[3],
            'color': args[4] if len(args) > 4 else None,
            'width': args[5] if len(args) > 5 else 1,
            'style': args[6] if len(args) > 6 else 'solid',
            'extend': False
        }
    
    elif operation_name == 'lineCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'lineDeleteFunc':
        return None
    
    elif operation_name == 'lineGetPriceFunc':
        x = args[1]
        line = args[0]
        # Linear interpolation
        if x <= line['x1']:
            return line['y1']
        if x >= line['x2']:
            return line['y2']
        ratio = (x - line['x1']) / (line['x2'] - line['x1'])
        return line['y1'] + ratio * (line['y2'] - line['y1'])
    
    elif operation_name == 'lineGetX1Func':
        return args[0]['x1']
    
    elif operation_name == 'lineGetX2Func':
        return args[0]['x2']
    
    elif operation_name == 'lineGetY1Func':
        return args[0]['y1']
    
    elif operation_name == 'lineGetY2Func':
        return args[0]['y2']
    
    elif operation_name == 'lineNewFunc':
        return {
            'x1': 0,
            'y1': 0,
            'x2': 0,
            'y2': 0,
            'color': None,
            'width': 1,
            'style': 'solid',
            'extend': False
        }
    
    elif operation_name == 'lineSetColFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetExtendFunc':
        args[0]['extend'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetFirstPointFunc':
        args[0]['x1'] = args[1]['x']
        args[0]['y1'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'lineSetSecondPointFunc':
        args[0]['x2'] = args[1]['x']
        args[0]['y2'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'lineSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetWidthFunc':
        args[0]['width'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetX1Func':
        args[0]['x1'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetX2Func':
        args[0]['x2'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetXLocFunc':
        args[0]['xloc'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetXY1Func':
        args[0]['x1'] = args[1]
        args[0]['y1'] = args[2]
        return args[0]
    
    elif operation_name == 'lineSetXY2Func':
        args[0]['x2'] = args[1]
        args[0]['y2'] = args[2]
        return args[0]
    
    elif operation_name == 'lineSetY1Func':
        args[0]['y1'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetY2Func':
        args[0]['y2'] = args[1]
        return args[0]
    
    elif operation_name == 'lineFillFunc':
        return {
            'line1': args[0],
            'line2': args[1],
            'color': args[2] if len(args) > 2 else None
        }
    
    elif operation_name == 'lineFillDeleteFunc':
        return None
    
    elif operation_name == 'lineFillGetLine1Func':
        return args[0]['line1']
    
    elif operation_name == 'lineFillGetLine2Func':
        return args[0]['line2']
    
    elif operation_name == 'lineFillNewFunc':
        return {
            'line1': None,
            'line2': None,
            'color': None
        }
    
    elif operation_name == 'lineFillSetColFunc':
        args[0]['color'] = args[1]
        return args[0]
