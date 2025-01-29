def _handle_label_operation(self, operation_name, args):
    if operation_name == 'labelFunc':
        return {
            'text': args[0],
            'x': args[1],
            'y': args[2],
            'color': args[3] if len(args) > 3 else None,
            'style': args[4] if len(args) > 4 else 'label_style_none',
            'textcolor': args[5] if len(args) > 5 else None,
            'size': args[6] if len(args) > 6 else 'size_auto',
            'textalign': args[7] if len(args) > 7 else 'align_center'
        }
    
    elif operation_name == 'labelCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'labelDeleteFunc':
        return None
    
    elif operation_name == 'labelGetTextFunc':
        return args[0]['text']
    
    elif operation_name == 'labelGetXFunc':
        return args[0]['x']
    
    elif operation_name == 'labelGetYFunc':
        return args[0]['y']
    
    elif operation_name == 'labelNewFunc':
        return {
            'text': '',
            'x': 0,
            'y': 0,
            'color': None,
            'style': 'label_style_none',
            'textcolor': None,
            'size': 'size_auto',
            'textalign': 'align_center',
            'tooltip': '',
            'xloc': 'xloc_bar',
            'yloc': 'yloc_price'
        }
    
    elif operation_name == 'labelSetColFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetPointFunc':
        args[0]['x'] = args[1]['x']
        args[0]['y'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'labelSetSizeFunc':
        args[0]['size'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextFontFamilyFunc':
        args[0]['font_family'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextAlignFunc':
        args[0]['textalign'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextColFunc':
        args[0]['textcolor'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetToolTipFunc':
        args[0]['tooltip'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXFunc':
        args[0]['x'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXLocFunc':
        args[0]['xloc'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXYFunc':
        args[0]['x'] = args[1]
        args[0]['y'] = args[2]
        return args[0]
    
    elif operation_name == 'labelSetYFunc':
        args[0]['y'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetYLocFunc':
        args[0]['yloc'] = args[1]
        return args[0]
