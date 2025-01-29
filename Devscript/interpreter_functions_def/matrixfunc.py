def _handle_matrix_operation(self, operation_name, args):
    import numpy as np

    if operation_name == 'matrixAddColFunc':
        matrix = np.array(args[0])
        col = np.array(args[1])
        return np.column_stack((matrix, col)).tolist()
    
    elif operation_name == 'matrixAddRowFunc':
        matrix = np.array(args[0])
        row = np.array(args[1])
        return np.vstack((matrix, row)).tolist()
    
    elif operation_name == 'matrixAvgFunc':
        return np.mean(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixColFunc':
        return np.array(args[0])[:, args[1]].tolist()
    
    elif operation_name == 'matrixColumnsFunc':
        return len(np.array(args[0])[0])
    
    elif operation_name == 'matrixConcatFunc':
        return np.concatenate((np.array(args[0]), np.array(args[1]))).tolist()
    
    elif operation_name == 'matrixCopyFunc':
        return np.array(args[0]).copy().tolist()
    
    elif operation_name == 'matrixDetFunc':
        return np.linalg.det(np.array(args[0]))
    
    elif operation_name == 'matrixDiffFunc':
        return np.diff(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixEigenValuesFunc':
        return np.linalg.eigvals(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixEigenVectorsFunc':
        return np.linalg.eig(np.array(args[0]))[1].tolist()
    
    elif operation_name == 'matrixElementsCountFunc':
        return np.array(args[0]).size
    
    elif operation_name == 'matrixFillFunc':
        shape = tuple(args[0])
        value = args[1]
        return np.full(shape, value).tolist()
    
    elif operation_name == 'matrixGetFunc':
        matrix = np.array(args[0])
        row = args[1]
        col = args[2]
        return matrix[row, col]
    
    elif operation_name == 'matrixInvFunc':
        return np.linalg.inv(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixIsAntiDiagonalFunc':
        matrix = np.array(args[0])
        n = len(matrix)
        return all(matrix[i][n-1-i] != 0 for i in range(n)) and \
               all(matrix[i][j] == 0 for i in range(n) for j in range(n) if j != n-1-i)
    
    elif operation_name == 'matrixIsAntiSymmetricFunc':
        matrix = np.array(args[0])
        return np.array_equal(matrix, -matrix.T)
    
    elif operation_name == 'matrixIsBinaryFunc':
        return np.all(np.logical_or(np.array(args[0]) == 0, np.array(args[0]) == 1))
    
    elif operation_name == 'matrixIsDiagonalFunc':
        matrix = np.array(args[0])
        return np.all(matrix == np.diag(np.diag(matrix)))
    
    elif operation_name == 'matrixIsIdentityFunc':
        return np.array_equal(np.array(args[0]), np.eye(len(args[0])))
    
    elif operation_name == 'matrixIsSquareFunc':
        matrix = np.array(args[0])
        return matrix.shape[0] == matrix.shape[1]
    
    elif operation_name == 'matrixIsSymmetricFunc':
        matrix = np.array(args[0])
        return np.array_equal(matrix, matrix.T)
    
    elif operation_name == 'matrixIsTriangularFunc':
        matrix = np.array(args[0])
        return np.allclose(np.tril(matrix), matrix) or np.allclose(np.triu(matrix), matrix)
    
    elif operation_name == 'matrixIsZeroFunc':
        return np.all(np.array(args[0]) == 0)
    
    elif operation_name == 'matrixKronFunc':
        return np.kron(np.array(args[0]), np.array(args[1])).tolist()
    
    elif operation_name == 'matrixMaxFunc':
        return np.max(np.array(args[0]))
    
    elif operation_name == 'matrixMinFunc':
        return np.min(np.array(args[0]))
    
    elif operation_name == 'matrixMultFunc':
        return np.matmul(np.array(args[0]), np.array(args[1])).tolist()
    
    elif operation_name == 'matrixNewTypeFunc':
        rows = args[0]
        cols = args[1]
        return np.zeros((rows, cols)).tolist()
    
    elif operation_name == 'matrixRankFunc':
        return np.linalg.matrix_rank(np.array(args[0]))
    
    elif operation_name == 'matrixReshapeFunc':
        matrix = np.array(args[0])
        new_shape = tuple(args[1])
        return matrix.reshape(new_shape).tolist()
    
    elif operation_name == 'matrixReverseFunc':
        return np.flip(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixRowFunc':
        return np.array(args[0])[args[1]].tolist()
    
    elif operation_name == 'matrixRowsFunc':
        return len(np.array(args[0]))
    
    elif operation_name == 'matrixSetFunc':
        matrix = np.array(args[0])
        row = args[1]
        col = args[2]
        value = args[3]
        matrix[row, col] = value
        return matrix.tolist()
    
    elif operation_name == 'matrixSortFunc':
        return np.sort(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixTraceFunc':
        return np.trace(np.array(args[0]))
    
    elif operation_name == 'matrixTransposeFunc':
        return np.transpose(np.array(args[0])).tolist()
