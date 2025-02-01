def _handle_math_operation(self, operation_name, args):
    import math

    if operation_name == 'mathAbsFunc':
        return abs(args[0])
    
    elif operation_name == 'mathAcosFunc':
        return math.acos(args[0])
    
    elif operation_name == 'mathAsinFunc':
        return math.asin(args[0])
    
    elif operation_name == 'mathAtanFunc':
        return math.atan(args[0])
    
    elif operation_name == 'mathAvgFunc':
        return sum(args[0]) / len(args[0])
    
    elif operation_name == 'mathCeilFunc':
        return math.ceil(args[0])
    
    elif operation_name == 'mathCosFunc':
        return math.cos(args[0])
    
    elif operation_name == 'mathExpFunc':
        return math.exp(args[0])
    
    elif operation_name == 'mathFloorFunc':
        return math.floor(args[0])
    
    elif operation_name == 'mathLogFunc':
        return math.log(args[0])
    
    elif operation_name == 'mathLog10Func':
        return math.log10(args[0])
    
    elif operation_name == 'mathMaxFunc':
        return max(args[0])
    
    elif operation_name == 'mathMinFunc':
        return min(args[0])
    
    elif operation_name == 'mathPowFunc':
        return math.pow(args[0], args[1])
    
    elif operation_name == 'mathRandomFunc':
        return random.random()
    
    elif operation_name == 'mathRoundFunc':
        return round(args[0])
    
    elif operation_name == 'mathRoundToMinTickFunc':
        return round(args[0] / args[1]) * args[1]
    
    elif operation_name == 'mathSignFunc':
        return (1 if args[0] > 0 else -1) if args[0] != 0 else 0
    
    elif operation_name == 'mathSinFunc':
        return math.sin(args[0])
    
    elif operation_name == 'mathSqrtFunc':
        return math.sqrt(args[0])
    
    elif operation_name == 'mathSumFunc':
        return sum(args[0])
    
    elif operation_name == 'mathTanFunc':
        return math.tan(args[0])
    
    elif operation_name == 'mathToDegreesFunc':
        return math.degrees(args[0])
    
    elif operation_name == 'mathToRadiansFunc':
        return math.radians(args[0])
