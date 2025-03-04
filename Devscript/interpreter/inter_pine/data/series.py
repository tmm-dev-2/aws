
import numpy as np
import pandas as pd
from typing import List, Dict, Union, Optional, Callable, Any
from dataclasses import dataclass

class ArrayEngine:
    def __init__(self):
        self.arrays = {}

    def create_float_array(self, size: int) -> np.ndarray:
        return np.zeros(size, dtype=np.float64)

    def create_int_array(self, size: int) -> np.ndarray:
        return np.zeros(size, dtype=np.int64)
        
    def create_bool_array(self, size: int) -> np.ndarray:
        return np.zeros(size, dtype=bool)

    def create_string_array(self, size: int) -> np.ndarray:
        return np.array([''] * size, dtype=str)

    def create_color_array(self, size: int) -> np.ndarray:
        return np.array(['#000000'] * size, dtype=str)

    def create_line_array(self, size: int) -> List:
        return [None] * size

    def create_label_array(self, size: int) -> List:
        return [None] * size

    def create_box_array(self, size: int) -> List:
        return [None] * size

    def push(self, arr: np.ndarray, value: Any) -> np.ndarray:
        return np.append(arr, value)

    def pop(self, arr: np.ndarray) -> tuple:
        return arr[:-1], arr[-1]

    def insert(self, arr: np.ndarray, index: int, value: Any) -> np.ndarray:
        return np.insert(arr, index, value)

    def remove(self, arr: np.ndarray, index: int) -> np.ndarray:
        return np.delete(arr, index)

    def shift(self, arr: np.ndarray) -> tuple:
        return arr[1:], arr[0]

    def unshift(self, arr: np.ndarray, value: Any) -> np.ndarray:
        return np.insert(arr, 0, value)

    def slice(self, arr: np.ndarray, start: int, end: int) -> np.ndarray:
        return arr[start:end]

    def splice(self, arr: np.ndarray, start: int, count: int) -> tuple:
        return np.delete(arr, slice(start, start + count)), arr[start:start + count]

    def join(self, arr: np.ndarray, separator: str) -> str:
        return separator.join(map(str, arr))

    def reverse(self, arr: np.ndarray) -> np.ndarray:
        return np.flip(arr)

    def calculate_sum(self, arr: np.ndarray) -> float:
        return np.sum(arr)

    def calculate_average(self, arr: np.ndarray) -> float:
        return np.mean(arr)

    def calculate_median(self, arr: np.ndarray) -> float:
        return np.median(arr)

    def calculate_mode(self, arr: np.ndarray) -> Any:
        return pd.Series(arr).mode()[0]

    def calculate_standard_deviation(self, arr: np.ndarray) -> float:
        return np.std(arr)

    def calculate_variance(self, arr: np.ndarray) -> float:
        return np.var(arr)

    def calculate_covariance(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        return np.cov(arr1, arr2)[0,1]

    def find_minimum(self, arr: np.ndarray) -> Any:
        return np.min(arr)

    def find_maximum(self, arr: np.ndarray) -> Any:
        return np.max(arr)

    def sort_array(self, arr: np.ndarray) -> np.ndarray:
        return np.sort(arr)

    def find_index(self, arr: np.ndarray, value: Any) -> int:
        indices = np.where(arr == value)[0]
        return indices[0] if len(indices) > 0 else -1

    def find_last_index(self, arr: np.ndarray, value: Any) -> int:
        indices = np.where(arr == value)[0]
        return indices[-1] if len(indices) > 0 else -1

    def includes_value(self, arr: np.ndarray, value: Any) -> bool:
        return value in arr

    def find_element(self, arr: np.ndarray, predicate: Callable) -> Any:
        mask = np.vectorize(predicate)(arr)
        indices = np.where(mask)[0]
        return arr[indices[0]] if len(indices) > 0 else None

    def find_element_index(self, arr: np.ndarray, predicate: Callable) -> int:
        mask = np.vectorize(predicate)(arr)
        indices = np.where(mask)[0]
        return indices[0] if len(indices) > 0 else -1

    def test_every_element(self, arr: np.ndarray, predicate: Callable) -> bool:
        return np.all(np.vectorize(predicate)(arr))

    def test_some_elements(self, arr: np.ndarray, predicate: Callable) -> bool:
        return np.any(np.vectorize(predicate)(arr))

    def filter_array(self, arr: np.ndarray, predicate: Callable) -> np.ndarray:
        mask = np.vectorize(predicate)(arr)
        return arr[mask]

    def map_array(self, arr: np.ndarray, mapper: Callable) -> np.ndarray:
        return np.vectorize(mapper)(arr)

class MatrixEngine:
    def create_matrix(self, rows: int, cols: int) -> np.ndarray:
        return np.zeros((rows, cols))

    def create_from_arrays(self, arrays: List[np.ndarray]) -> np.ndarray:
        return np.array(arrays)

    def create_identity_matrix(self, size: int) -> np.ndarray:
        return np.eye(size)

    def create_zero_matrix(self, rows: int, cols: int) -> np.ndarray:
        return np.zeros((rows, cols))

    def create_ones_matrix(self, rows: int, cols: int) -> np.ndarray:
        return np.ones((rows, cols))

    def create_random_matrix(self, rows: int, cols: int) -> np.ndarray:
        return np.random.rand(rows, cols)

    def add_matrices(self, m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
        return np.add(m1, m2)

    def subtract_matrices(self, m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
        return np.subtract(m1, m2)

    def multiply_matrices(self, m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
        return np.matmul(m1, m2)

    def divide_matrices(self, m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
        return np.divide(m1, m2)

    def transpose_matrix(self, m: np.ndarray) -> np.ndarray:
        return np.transpose(m)

    def inverse_matrix(self, m: np.ndarray) -> np.ndarray:
        return np.linalg.inv(m)

    def calculate_determinant(self, m: np.ndarray) -> float:
        return np.linalg.det(m)

    def calculate_eigenvalues(self, m: np.ndarray) -> np.ndarray:
        return np.linalg.eigvals(m)

    def set_value(self, m: np.ndarray, row: int, col: int, value: float) -> None:
        m[row, col] = value

    def get_value(self, m: np.ndarray, row: int, col: int) -> float:
        return m[row, col]

    def get_row(self, m: np.ndarray, row: int) -> np.ndarray:
        return m[row, :]

    def get_column(self, m: np.ndarray, col: int) -> np.ndarray:
        return m[:, col]

    def get_submatrix(self, m: np.ndarray, row_start: int, row_end: int, col_start: int, col_end: int) -> np.ndarray:
        return m[row_start:row_end, col_start:col_end]

    def reshape_matrix(self, m: np.ndarray, new_rows: int, new_cols: int) -> np.ndarray:
        return np.reshape(m, (new_rows, new_cols))

    def concatenate_matrices(self, m1: np.ndarray, m2: np.ndarray, axis: int) -> np.ndarray:
        return np.concatenate((m1, m2), axis=axis)

    def decompose_matrix(self, m: np.ndarray, method: str) -> tuple:
        if method == 'lu':
            return np.linalg.lu(m)
        elif method == 'svd':
            return np.linalg.svd(m)
        elif method == 'qr':
            return np.linalg.qr(m)
        raise ValueError(f"Unknown decomposition method: {method}")

class MathEngine:
    def absolute_value(self, x: float) -> float:
        return abs(x)

    def power(self, x: float, y: float) -> float:
        return np.power(x, y)

    def square_root(self, x: float) -> float:
        return np.sqrt(x)

    def cube_root(self, x: float) -> float:
        return np.cbrt(x)

    def exponential(self, x: float) -> float:
        return np.exp(x)

    def natural_log(self, x: float) -> float:
        return np.log(x)

    def log_base_10(self, x: float) -> float:
        return np.log10(x)

    def floor_value(self, x: float) -> float:
        return np.floor(x)

    def ceiling_value(self, x: float) -> float:
        return np.ceil(x)

    def round_value(self, x: float, decimals: int) -> float:
        return np.round(x, decimals)

    def sign_value(self, x: float) -> int:
        return np.sign(x)

    def maximum(self, x: float, y: float) -> float:
        return max(x, y)

    def minimum(self, x: float, y: float) -> float:
        return min(x, y)

    def average(self, arr: np.ndarray) -> float:
        return np.mean(arr)

    def sum_values(self, arr: np.ndarray) -> float:
        return np.sum(arr)

    def product_values(self, arr: np.ndarray) -> float:
        return np.prod(arr)

    def sine(self, x: float) -> float:
        return np.sin(x)

    def cosine(self, x: float) -> float:
        return np.cos(x)

    def tangent(self, x: float) -> float:
        return np.tan(x)

    def arc_sine(self, x: float) -> float:
        return np.arcsin(x)

    def arc_cosine(self, x: float) -> float:
        return np.arccos(x)

    def arc_tangent(self, x: float) -> float:
        return np.arctan(x)

    def arc_tangent2(self, y: float, x: float) -> float:
        return np.arctan2(y, x)

    def hyperbolic_sine(self, x: float) -> float:
        return np.sinh(x)

    def hyperbolic_cosine(self, x: float) -> float:
        return np.cosh(x)

    def hyperbolic_tangent(self, x: float) -> float:
        return np.tanh(x)

    def radians_to_degrees(self, x: float) -> float:
        return np.degrees(x)

    def degrees_to_radians(self, x: float) -> float:
        return np.radians(x)

    def calculate_correlation(self, x: np.ndarray, y: np.ndarray) -> float:
        return np.corrcoef(x, y)[0,1]

    def calculate_covariance(self, x: np.ndarray, y: np.ndarray) -> float:
        return np.cov(x, y)[0,1]

    def standard_deviation(self, arr: np.ndarray) -> float:
        return np.std(arr)

    def variance(self, arr: np.ndarray) -> float:
        return np.var(arr)

    def skewness(self, arr: np.ndarray) -> float:
        return pd.Series(arr).skew()

    def kurtosis(self, arr: np.ndarray) -> float:
        return pd.Series(arr).kurtosis()

    def percentile(self, arr: np.ndarray, p: float) -> float:
        return np.percentile(arr, p)

    def z_score(self, x: float, mean: float, std: float) -> float:
        return (x - mean) / std

    def normal_cumulative_distribution(self, x: float, mean: float, std: float) -> float:
        return pd.Series(x).apply(lambda x: pd.Series.normal_cdf(x, mean, std))

    def normal_inverse_cumulative_distribution(self, p: float, mean: float, std: float) -> float:
        return pd.Series(p).apply(lambda p: pd.Series.normal_ppf(p, mean, std))

    def present_value(self, fv: float, r: float, n: int) -> float:
        return fv / (1 + r)**n

    def future_value(self, pv: float, r: float, n: int) -> float:
        return pv * (1 + r)**n

    def number_of_periods(self, pv: float, pmt: float, fv: float, r: float) -> float:
        return np.log(fv/pv) / np.log(1 + r)

    def payment(self, pv: float, fv: float, r: float, n: int) -> float:
        return (pv * r * (1 + r)**n) / ((1 + r)**n - 1)

    def internal_rate_of_return(self, cashflows: np.ndarray) -> float:
        return np.irr(cashflows)

    def net_present_value(self, rate: float, cashflows: np.ndarray) -> float:
        return np.npv(rate, cashflows)

    def irregular_internal_rate_of_return(self, cashflows: np.ndarray, dates: np.ndarray) -> float:
        return np.xirr(cashflows, dates)

    def irregular_net_present_value(self, rate: float, cashflows: np.ndarray, dates: np.ndarray) -> float:
        return np.xnpv(rate, cashflows, dates)

    def modified_internal_rate_of_return(self, cashflows: np.ndarray, finance_rate: float, reinvest_rate: float) -> float:
        return np.mirr(cashflows, finance_rate, reinvest_rate)

    def interest_rate(self, nper: int, pmt: float, pv: float, fv: float) -> float:
        return np.rate(nper, pmt, pv, fv)

    def duration(self, cashflows: np.ndarray, yields: np.ndarray) -> float:
        weights = np.arange(1, len(cashflows) + 1)
        return np.sum(weights * cashflows) / np.sum(cashflows)

    def modified_duration(self, duration: float, yield_rate: float) -> float:
        return duration / (1 + yield_rate)

    def convexity(self, cashflows: np.ndarray, yields: np.ndarray) -> float:
        weights = np.arange(1, len(cashflows) + 1)
        return np.sum(weights * (weights + 1) * cashflows) / (np.sum(cashflows) * (1 + yields[0])**2)

class SeriesSyntax:
    def __init__(self):
        self.array_engine = ArrayEngine()
        self.matrix_engine = MatrixEngine()
        self.math_engine = MathEngine()
        
        self.syntax_mappings = {
            'array_new_float': lambda size: self.array_engine.create_float_array(size),
            'array_new_int': lambda size: self.array_engine.create_int_array(size),
            'array_new_bool': lambda size: self.array_engine.create_bool_array(size),
            'array_new_string': lambda size: self.array_engine.create_string_array(size),
            'array_new_color': lambda size: self.array_engine.create_color_array(size),
            'array_new_line': lambda size: self.array_engine.create_line_array(size),
            'array_new_label': lambda size: self.array_engine.create_label_array(size),
            'array_new_box': lambda size: self.array_engine.create_box_array(size),
            'array_push': lambda arr, value: self.array_engine.push(arr, value),
            'array_pop': lambda arr: self.array_engine.pop(arr),
            'array_insert': lambda arr, index, value: self.array_engine.insert(arr, index, value),
            'array_remove': lambda arr, index: self.array_engine.remove(arr, index),
            'array_shift': lambda arr: self.array_engine.shift(arr),
            'array_unshift': lambda arr, value: self.array_engine.unshift(arr, value),
            'array_slice': lambda arr, start, end: self.array_engine.slice(arr, start, end),
            'array_splice': lambda arr, start, count: self.array_engine.splice(arr, start, count),
            'array_join': lambda arr, separator: self.array_engine.join(arr, separator),
            'array_reverse': lambda arr: self.array_engine.reverse(arr),
            'array_sum': lambda arr: self.array_engine.calculate_sum(arr),
            'array_avg': lambda arr: self.array_engine.calculate_average(arr),
            'array_median': lambda arr: self.array_engine.calculate_median(arr),
            'array_mode': lambda arr: self.array_engine.calculate_mode(arr),
            'array_stdev': lambda arr: self.array_engine.calculate_standard_deviation(arr),
            'array_variance': lambda arr: self.array_engine.calculate_variance(arr),
            'array_covariance': lambda arr1, arr2: self.array_engine.calculate_covariance(arr1, arr2),
            'array_min': lambda arr: self.array_engine.find_minimum(arr),
            'array_max': lambda arr: self.array_engine.find_maximum(arr),
            'array_sort': lambda arr: self.array_engine.sort_array(arr),
            'array_indexOf': lambda arr, value: self.array_engine.find_index(arr, value),
            'array_lastIndexOf': lambda arr, value: self.array_engine.find_last_index(arr, value),
            'array_includes': lambda arr, value: self.array_engine.includes_value(arr, value),
            'array_find': lambda arr, predicate: self.array_engine.find_element(arr, predicate),
            'array_findIndex': lambda arr, predicate: self.array_engine.find_element_index(arr, predicate),
            'array_every': lambda arr, predicate: self.array_engine.test_every_element(arr, predicate),
            'array_some': lambda arr, predicate: self.array_engine.test_some_elements(arr, predicate),
            'array_filter': lambda arr, predicate: self.array_engine.filter_array(arr, predicate),
            'array_map': lambda arr, mapper: self.array_engine.map_array(arr, mapper),
            'matrix_new': lambda rows, cols: self.matrix_engine.create_matrix(rows, cols),
            'matrix_new_from_arrays': lambda arrays: self.matrix_engine.create_from_arrays(arrays),
            'matrix_new_identity': lambda size: self.matrix_engine.create_identity_matrix(size),
            'matrix_new_zero': lambda rows, cols: self.matrix_engine.create_zero_matrix(rows, cols),
            'matrix_new_ones': lambda rows, cols: self.matrix_engine.create_ones_matrix(rows, cols),
            'matrix_new_random': lambda rows, cols: self.matrix_engine.create_random_matrix(rows, cols),
            'matrix_add': lambda m1, m2: self.matrix_engine.add_matrices(m1, m2),
            'matrix_subtract': lambda m1, m2: self.matrix_engine.subtract_matrices(m1, m2),
            'matrix_multiply': lambda m1, m2: self.matrix_engine.multiply_matrices(m1, m2),
            'matrix_divide': lambda m1, m2: self.matrix_engine.divide_matrices(m1, m2),
            'matrix_transpose': lambda m: self.matrix_engine.transpose_matrix(m),
            'matrix_inverse': lambda m: self.matrix_engine.inverse_matrix(m),
            'matrix_determinant': lambda m: self.matrix_engine.calculate_determinant(m),
            'matrix_eigenvalues': lambda m: self.matrix_engine.calculate_eigenvalues(m),
            'matrix_set': lambda m, row, col, value: self.matrix_engine.set_value(m, row, col, value),
            'matrix_get': lambda m, row, col: self.matrix_engine.get_value(m, row, col),
            'matrix_row': lambda m, row: self.matrix_engine.get_row(m, row),
            'matrix_col': lambda m, col: self.matrix_engine.get_column(m, col),
            'matrix_submatrix': lambda m, row_start, row_end, col_start, col_end: self.matrix_engine.get_submatrix(m, row_start, row_end, col_start, col_end),
            'matrix_reshape': lambda m, new_rows, new_cols: self.matrix_engine.reshape_matrix(m, new_rows, new_cols),
            'matrix_concat': lambda m1, m2, axis: self.matrix_engine.concatenate_matrices(m1, m2, axis),
            'matrix_decomposition': lambda m, method: self.matrix_engine.decompose_matrix(m, method),
            'abs': lambda x: self.math_engine.absolute_value(x),
            'pow': lambda x, y: self.math_engine.power(x, y),
            'sqrt': lambda x: self.math_engine.square_root(x),
            'cbrt': lambda x: self.math_engine.cube_root(x),
            'exp': lambda x: self.math_engine.exponential(x),
            'log': lambda x: self.math_engine.natural_log(x),
            'log10': lambda x: self.math_engine.log_base_10(x),
            'floor': lambda x: self.math_engine.floor_value(x),
            'ceil': lambda x: self.math_engine.ceiling_value(x),
            'round': lambda x, decimals: self.math_engine.round_value(x, decimals),
            'sign': lambda x: self.math_engine.sign_value(x),
            'max': lambda x, y: self.math_engine.maximum(x, y),
            'min': lambda x, y: self.math_engine.minimum(x, y),
            'avg': lambda arr: self.math_engine.average(arr),
            'sum': lambda arr: self.math_engine.sum_values(arr),
            'product': lambda arr: self.math_engine.product_values(arr),
            'sin': lambda x: self.math_engine.sine(x),
            'cos': lambda x: self.math_engine.cosine(x),
            'tan': lambda x: self.math_engine.tangent(x),
            'asin': lambda x: self.math_engine.arc_sine(x),
            'acos': lambda x: self.math_engine.arc_cosine(x),
            'atan': lambda x: self.math_engine.arc_tangent(x),
            'atan2': lambda y, x: self.math_engine.arc_tangent2(y, x),
            'sinh': lambda x: self.math_engine.hyperbolic_sine(x),
            'cosh': lambda x: self.math_engine.hyperbolic_cosine(x),
            'tanh': lambda x: self.math_engine.hyperbolic_tangent(x),
            'degrees': lambda x: self.math_engine.radians_to_degrees(x),
            'radians': lambda x: self.math_engine.degrees_to_radians(x),
            'correlation': lambda x, y: self.math_engine.calculate_correlation(x, y),
            'covariance': lambda x, y: self.math_engine.calculate_covariance(x, y),
            'standarddev': lambda arr: self.math_engine.standard_deviation(arr),
            'variance': lambda arr: self.math_engine.variance(arr),
            'skew': lambda arr: self.math_engine.skewness(arr),
            'kurtosis': lambda arr: self.math_engine.kurtosis(arr),
            'percentile': lambda arr, p: self.math_engine.percentile(arr, p),
            'zscore': lambda x, mean, std: self.math_engine.z_score(x, mean, std),
            'normal_cdf': lambda x, mean, std: self.math_engine.normal_cumulative_distribution(x, mean, std),
            'normal_inverse': lambda p, mean, std: self.math_engine.normal_inverse_cumulative_distribution(p, mean, std),
            'pv': lambda fv, r, n: self.math_engine.present_value(fv, r, n),
            'fv': lambda pv, r, n: self.math_engine.future_value(pv, r, n),
            'nper': lambda pv, pmt, fv, r: self.math_engine.number_of_periods(pv, pmt, fv, r),
            'pmt': lambda pv, fv, r, n: self.math_engine.payment(pv, fv, r, n),
            'irr': lambda cashflows: self.math_engine.internal_rate_of_return(cashflows),
            'npv': lambda rate, cashflows: self.math_engine.net_present_value(rate, cashflows),
            'xirr': lambda cashflows, dates: self.math_engine.irregular_internal_rate_of_return(cashflows, dates),
            'xnpv': lambda rate, cashflows, dates: self.math_engine.irregular_net_present_value(rate, cashflows, dates),
            'mirr': lambda cashflows, finance_rate, reinvest_rate: self.math_engine.modified_internal_rate_of_return(cashflows, finance_rate, reinvest_rate),
            'rate': lambda nper, pmt, pv, fv: self.math_engine.interest_rate(nper, pmt, pv, fv),
            'duration': lambda cashflows, yields: self.math_engine.duration(cashflows, yields),
            'modified_duration': lambda duration, yield_rate: self.math_engine.modified_duration(duration, yield_rate),
            'convexity': lambda cashflows, yields: self.math_engine.convexity(cashflows, yields)
        }
