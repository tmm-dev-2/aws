def _handle_chart_operation(self, operation_name, args):
    if operation_name == 'chartPointCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'chartPointFromIndexFunc':
        return {
            'index': args[0],
            'price': args[1],
            'time': None,
            'bar_index': args[0],
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointFromTimeFunc':
        return {
            'time': args[0],
            'price': args[1],
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointNewFunc':
        return {
            'time': None,
            'price': None,
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointNowFunc':
        import time
        return {
            'time': time.time(),
            'price': args[0],
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointSetOffsetFunc':
        args[0]['offset'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetPlotCharFunc':
        args[0]['plotchar'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetColorFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetWidthFunc':
        args[0]['width'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointGetIndexFunc':
        return args[0]['index']
    
    elif operation_name == 'chartPointGetPriceFunc':
        return args[0]['price']
    
    elif operation_name == 'chartPointGetTimeFunc':
        return args[0]['time']
    
    elif operation_name == 'chartPointGetBarIndexFunc':
        return args[0]['bar_index']
    
    elif operation_name == 'chartPointGetOffsetFunc':
        return args[0]['offset']
    
    elif operation_name == 'chartPointGetStyleFunc':
        return args[0]['style']
    
    elif operation_name == 'chartPointGetColorFunc':
        return args[0]['color']
    
    elif operation_name == 'chartPointGetWidthFunc':
        return args[0]['width']

    return None
