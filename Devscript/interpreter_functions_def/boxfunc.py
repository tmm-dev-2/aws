#box
def _handle_box_operation(self, operation_name, args):
    if operation_name == 'boxFunc':
        return {
            'left': args[0],
            'top': args[1],
            'right': args[2],
            'bottom': args[3],
            'border_color': args[4] if len(args) > 4 else None,
            'bg_color': args[5] if len(args) > 5 else None
        }
    
    elif operation_name == 'boxCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'boxDeleteFunc':
        return None
    
    elif operation_name == 'boxGetBottomFunc':
        return args[0]['bottom']
    
    elif operation_name == 'boxGetLeftFunc':
        return args[0]['left']
    
    elif operation_name == 'boxGetRightFunc':
        return args[0]['right']
    
    elif operation_name == 'boxGetTopFunc':
        return args[0]['top']
    
    elif operation_name == 'boxNewFunc':
        return {
            'left': 0,
            'top': 0,
            'right': 0,
            'bottom': 0,
            'border_color': None,
            'bg_color': None,
            'text': '',
            'text_color': None,
            'border_width': 1,
            'border_style': 'solid',
            'text_halign': 'center',
            'text_valign': 'middle',
            'text_font_family': 'Arial',
            'text_size': 12,
            'extend': False
        }
    
    elif operation_name == 'boxSetBgColFunc':
        args[0]['bg_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderColFunc':
        args[0]['border_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderStyleFunc':
        args[0]['border_style'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderWidthFunc':
        args[0]['border_width'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBottomFunc':
        args[0]['bottom'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBottomRightPointFunc':
        args[0]['bottom'] = args[1]
        args[0]['right'] = args[2]
        return args[0]
    
    elif operation_name == 'boxSetExtendFunc':
        args[0]['extend'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetLeftFunc':
        args[0]['left'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetLeftTopFunc':
        args[0]['left'] = args[1]
        args[0]['top'] = args[2]
        return args[0]
    
    elif operation_name == 'boxSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextColFunc':
        args[0]['text_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextFontFamilyFunc':
        args[0]['text_font_family'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextHAlignFunc':
        args[0]['text_halign'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextSizeFunc':
        args[0]['text_size'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextVAlignFunc':
        args[0]['text_valign'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextWrapFunc':
        args[0]['text_wrap'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTopFunc':
        args[0]['top'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTopLeftPointFunc':
        args[0]['top'] = args[1]
        args[0]['left'] = args[2]
        return args[0]

    elif operation_name == 'boxSetRightFunc':
        args[0]['right'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetRightBottomFunc':
        args[0]['right'] = args[1]
        args[0]['bottom'] = args[2]
        return args[0]

    elif operation_name == 'boxSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextColFunc':
        args[0]['text_color'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextFontFamilyFunc':
        args[0]['text_font_family'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextHAlignFunc':
        args[0]['text_halign'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextSizeFunc':
        args[0]['text_size'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextVAlignFunc':
        args[0]['text_valign'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextWrapFunc':
        args[0]['text_wrap'] = args[1]
        return args[0]


    return None

