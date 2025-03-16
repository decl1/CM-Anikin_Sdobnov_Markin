# strategies library
import sys

from munkres import Munkres
import numpy as np

import generate_data as g


def output_example(input_example):
    return "example: " + input_example


# Реализованы жадный, бережливый, бережливо/жадный и жадно/бережливый алгоритмы
# Все алгоритмы на вход получают полную матрицу состояний, которая за пределами алгоритмов приводится к нужному виду
# Матрица расстояний рассматривается по столбцам. Таким образом имитируется нечеткая задача.
# Функции возвращают число - максимальную сумму перестановки партий по этапам, полученную с помощью
# соответствующего алгоритма, то есть S(b)

from munkres import Munkres

def greedy_strategy(n, s_matrix):
    result = 0
    used_batches = []
    selected_indices = []
    
    for j in range(n):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        index = column.index(max_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    return result, selected_indices


def thrifty_strategy(n, s_matrix):
    result = 0
    used_batches = []
    selected_indices = []
    
    for j in range(n):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = float("inf")
        min_elem = min(column)
        result += min_elem
        index = column.index(min_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    return result, selected_indices


def thrifty_greedy_strategy(n, s_matrix, swap_stage):
    result = 0
    used_batches = []
    selected_indices = []
    
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = float("inf")
        min_elem = min(column)
        result += min_elem
        index = column.index(min_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    for j in range(swap_stage, n):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        index = column.index(max_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    return result, selected_indices


def greedy_thrifty_strategy(n, s_matrix, swap_stage):
    result = 0
    used_batches = []
    selected_indices = []
    
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        index = column.index(max_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    for j in range(swap_stage, n):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = float("inf")
        min_elem = min(column)
        result += min_elem
        index = column.index(min_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    return result, selected_indices


def tkg_strategy(n, s_matrix, swap_stage, k):
    result = 0
    used_batches = []
    selected_indices = []
    
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = float("inf")
        for _ in range(k):
            column[column.index(min(column))] = float("inf")
        min_elem = min(column)
        result += min_elem
        index = column.index(min_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    for j in range(swap_stage, n):
        column = [s_matrix[i][j] for i in range(n)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        index = column.index(max_elem)
        used_batches.append(index)
        selected_indices.append((index, j))
    
    return result, selected_indices


def hungarian_strategy(s_matrix):
    new_matrix = []
    
    for i in range(len(s_matrix)):  
        row_max = max(s_matrix[i])  
        new_row = [x - row_max for x in s_matrix[i]]  
        new_matrix.append(new_row)  
    
    final_matrix = [[-x for x in row] for row in new_matrix]

    m = Munkres()
    indexes = m.compute(final_matrix)
    
    total = 0
    selected_indices = []
    for row, column in indexes:
        value = s_matrix[row][column]
        total += value
        selected_indices.append((row, column))
    
    return total, selected_indices

def calculate_S1(S2, x, C):
    x = np.array(x)  # Преобразуем x в массив numpy
    C = np.array(C)  # Преобразуем C в матрицу numpy
    
    S1 = S2 + np.sum(x[:, None] * C)  # Вычисляем S1
    return S1

def run_experiment(n, ):
    C = generate(matrix_size, base_min, base_max, hi_min, hi_max)
    results = []
    swap_stage = n / 3
    k = n - swap_stage

    algorithms = [
        ("Greedy", greedy_strategy, (n, C)),
        ("Thrifty", thrifty_strategy, (n, C)),
        ("Thrifty-Greedy", thrifty_greedy_strategy, (n, C, swap_stage)),
        ("Greedy-Thrifty", greedy_thrifty_strategy, (n, C, swap_stage)),
        ("TKG", tkg_strategy, (n, C, swap_stage, k)),
        ("Hungarian", hungarian_strategy, (C,))
    ]
    
    hungarian_value, _ = hungarian_strategy(C)
    min_loss = float("inf")
    best_order = None

    for name, algorithm, args in algorithms:
        value, indices = algorithm(*args)
        S1 = calculate_S1(value, [C[i][j] for i, j in indices], C)
        loss = hungarian_value - S1
        results.append({
            "Algorithm": name,
            "Indices": indices,
            "Sum": value,
            "S1": S1,
            "Loss": loss
        })
        if 0 < loss < min_loss:
            min_loss = loss
            best_order = indices
    
    if best_order:
        D = generate_D(n, best_order)
    else:
        D = None
    

    return results, C, D
