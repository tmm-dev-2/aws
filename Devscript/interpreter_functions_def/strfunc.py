def _handle_str_operation(self, operation_name, args):
    if operation_name == 'strContainsFunc':
        return args[1] in args[0]
    
    elif operation_name == 'strEndsWithFunc':
        return args[0].endswith(args[1])
    
    elif operation_name == 'strFormatFunc':
        return args[0].format(*args[1:])
    
    elif operation_name == 'strFormatTimeFunc':
        return time.strftime(args[1], time.localtime(args[0]))
    
    elif operation_name == 'strLengthFunc':
        return len(args[0])
    
    elif operation_name == 'strLowerFunc':
        return args[0].lower()
    
    elif operation_name == 'strMatchFunc':
        import re
        return bool(re.match(args[1], args[0]))
    
    elif operation_name == 'strPosFunc':
        return args[0].find(args[1])
    
    elif operation_name == 'strRepeatFunc':
        return args[0] * args[1]
    
    elif operation_name == 'strReplaceFunc':
        return args[0].replace(args[1], args[2], 1)
    
    elif operation_name == 'strReplaceAllFunc':
        return args[0].replace(args[1], args[2])
    
    elif operation_name == 'strSplitFunc':
        return args[0].split(args[1])
    
    elif operation_name == 'strStartsWithFunc':
        return args[0].startswith(args[1])
    
    elif operation_name == 'strSubstringFunc':
        return args[0][args[1]:args[2] if len(args) > 2 else None]
    
    elif operation_name == 'strToNumberFunc':
        return float(args[0])
    
    elif operation_name == 'strToStringFunc':
        return str(args[0])
    
    elif operation_name == 'strTrimFunc':
        return args[0].strip()
    
    elif operation_name == 'strUpperFunc':
        return args[0].upper()
    
    elif operation_name == 'strIndexOfFunc':
        return args[0].find(args[1], args[2] if len(args) > 2 else 0)
        
    elif operation_name == 'strLastIndexOfFunc':
        return args[0].rfind(args[1])
        
    elif operation_name == 'strCompareFunc':
        return (args[0] > args[1]) - (args[0] < args[1])
        
    elif operation_name == 'strCountFunc':
        return args[0].count(args[1])
        
    elif operation_name == 'strReverseFunc':
        return args[0][::-1]
        
    elif operation_name == 'strPadLeftFunc':
        return args[0].rjust(args[1], args[2] if len(args) > 2 else ' ')
        
    elif operation_name == 'strPadRightFunc':
        return args[0].ljust(args[1], args[2] if len(args) > 2 else ' ')
