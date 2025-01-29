def _handle_array_operation(self, operation_name, args):
    if operation_name == 'arrAbs':
        return [abs(x) for x in args[0]]
    
    elif operation_name == 'arrAvg':
        return sum(args[0]) / len(args[0]) if args[0] else 0
    
    elif operation_name == 'arrBinarySearch':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                return mid
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    elif operation_name == 'arrBinarySearchLeftmost':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                result = mid
                right = mid - 1
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    elif operation_name == 'arrBinarySearchRightmost':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                result = mid
                left = mid + 1
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    elif operation_name == 'arrClear':
        args[0].clear()
        return args[0]
    
    elif operation_name == 'arrConcat':
        return args[0] + args[1]
    
    elif operation_name == 'arrCopy':
        return args[0].copy()
    
    elif operation_name == 'arrCovariance':
        if len(args[0]) != len(args[1]) or len(args[0]) == 0:
            return 0
        mean_x = sum(args[0]) / len(args[0])
        mean_y = sum(args[1]) / len(args[1])
        return sum((x - mean_x) * (y - mean_y) for x, y in zip(args[0], args[1])) / len(args[0])
    
    elif operation_name == 'arrEvery':
        return all(args[0])
    
    elif operation_name == 'arrFill':
        return [args[1]] * args[0]
    
    elif operation_name == 'arrFirst':
        return args[0][0] if args[0] else None
    
    elif operation_name == 'arrFrom':
        return list(args[0])
    
    elif operation_name == 'arrGet':
        return args[0][args[1]] if 0 <= args[1] < len(args[0]) else None
    
    elif operation_name == 'arrIncludes':
        return args[1] in args[0]
    
    elif operation_name == 'arrIndexOf':
        try:
            return args[0].index(args[1])
        except ValueError:
            return -1
    
    elif operation_name == 'arrInsert':
        args[0].insert(args[1], args[2])
        return args[0]
    
    elif operation_name == 'arrJoin':
        return args[1].join(map(str, args[0]))
    
    elif operation_name == 'arrLast':
        return args[0][-1] if args[0] else None
    
    elif operation_name == 'arrLastIndexOf':
        return len(args[0]) - 1 - args[0][::-1].index(args[1]) if args[1] in args[0] else -1
    
    elif operation_name == 'arrMax':
        return max(args[0]) if args[0] else None
    
    elif operation_name == 'arrMedian':
        sorted_arr = sorted(args[0])
        n = len(sorted_arr)
        if n % 2 == 0:
            return (sorted_arr[n//2 - 1] + sorted_arr[n//2]) / 2
        return sorted_arr[n//2]
    
    elif operation_name == 'arrMin':
        return min(args[0]) if args[0] else None
    
    elif operation_name == 'arrMode':
        from collections import Counter
        return Counter(args[0]).most_common(1)[0][0] if args[0] else None

    elif operation_name == 'arrPercentileLinearInterpolation':
        sorted_arr = sorted(args[0])
        p = args[1]
        n = len(sorted_arr)
        r = p * (n - 1) / 100
        i = int(r)
        f = r - i
        return sorted_arr[i] + f * (sorted_arr[i + 1] - sorted_arr[i]) if i + 1 < n else sorted_arr[i]

    elif operation_name == 'arrPercentileNearestRank':
        sorted_arr = sorted(args[0])
        p = args[1]
        n = len(sorted_arr)
        r = int(round(p * (n - 1) / 100))
        return sorted_arr[r]

    elif operation_name == 'arrPercentRank':
        value = args[1]
        arr = sorted(args[0])
        return sum(1 for x in arr if x < value) * 100 / len(arr)

    elif operation_name == 'arrPop':
        return args[0].pop() if args[0] else None

    elif operation_name == 'arrPush':
        args[0].append(args[1])
        return len(args[0])

    elif operation_name == 'arrRange':
        return list(range(args[0], args[1], args[2] if len(args) > 2 else 1))

    elif operation_name == 'arrRemove':
        del args[0][args[1]]
        return args[0]

    elif operation_name == 'arrReverse':
        return args[0][::-1]

    elif operation_name == 'arrSet':
        args[0][args[1]] = args[2]
        return args[0]

    elif operation_name == 'arrShift':
        return args[0].pop(0) if args[0] else None

    elif operation_name == 'arrSize':
        return len(args[0])

    elif operation_name == 'arrSlice':
        start = args[1]
        end = args[2] if len(args) > 2 else None
        return args[0][start:end]

    elif operation_name == 'arrSome':
        return any(args[0])

    elif operation_name == 'arrSort':
        return sorted(args[0], reverse=args[1] if len(args) > 1 else False)

    elif operation_name == 'arrSortIndices':
        return sorted(range(len(args[0])), key=lambda k: args[0][k], reverse=args[1] if len(args) > 1 else False)

    elif operation_name == 'arrStandardize':
        mean = sum(args[0]) / len(args[0])
        std = (sum((x - mean) ** 2 for x in args[0]) / len(args[0])) ** 0.5
        return [(x - mean) / std for x in args[0]] if std != 0 else [0] * len(args[0])

    elif operation_name == 'arrStdev':
        mean = sum(args[0]) / len(args[0])
        return (sum((x - mean) ** 2 for x in args[0]) / len(args[0])) ** 0.5

    elif operation_name == 'arrSum':
        return sum(args[0])

    elif operation_name == 'arrUnshift':
        args[0].insert(0, args[1])
        return len(args[0])

    elif operation_name == 'arrVariance':
        mean = sum(args[0]) / len(args[0])
        return sum((x - mean) ** 2 for x in args[0]) / len(args[0])

    elif operation_name.startswith('arrNew'):
        size = args[0]
        initial_value = args[1] if len(args) > 1 else None
        
        if operation_name == 'arrNewBool':
            return [bool(initial_value)] * size if initial_value is not None else [False] * size
        elif operation_name == 'arrNewFloat':
            return [float(initial_value)] * size if initial_value is not None else [0.0] * size
        elif operation_name == 'arrNewInt':
            return [int(initial_value)] * size if initial_value is not None else [0] * size
        elif operation_name == 'arrNewString':
            return [str(initial_value)] * size if initial_value is not None else [''] * size
        elif operation_name in ['arrNewBox', 'arrayNewCol', 'arrayNewLabel', 'arrayNewLine', 'arrayNewTable']:
            return [None] * size
        elif operation_name == 'arrNewType':
            return [{}] * size

    return None
