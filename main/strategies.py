# strategies library
import numpy as np

def output_example(input_example):
    return "example: " + input_example

#Реализованы жадный, бережливый, бережливо/жадный и жадно/бережливый алгоритмы
#Все алгоритмы на вход получают полную матрицу состояний, которая за пределами алгоритмов приводится к нужному виду
#Матрица расстояний рассматривается по столбцам. Таким образом имитируется нечеткая задача.
#Функции возвращают число - максимальную сумму перестановки партий по этапам, полученную с помощью
# соответствующего алгоритма, то есть S(b)

def greedy_strategy(num_batches, num_stages, s_matrix):
    result = 0
    used_batches = []
    for j in range(num_stages):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    return result

def thrifty_strategy(num_batches, num_stages, s_matrix):
    result = 0
    used_batches = []
    for j in range(num_stages):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = float("inf")
        max_elem = min(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    return result

def thrifty_greedy_strategy(num_batches, num_stages, s_matrix, swap_stage):
    result = 0
    used_batches = []
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = float("inf")
        max_elem = min(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    for j in range(swap_stage, num_stages):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    return result

def greedy_thrifty_strategy(num_batches, num_stages, s_matrix, swap_stage):
    result = 0
    used_batches = []
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    for j in range(swap_stage, num_stages):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = float("inf")
        max_elem = min(column)
        result += max_elem
        used_batches.append(column.index(max_elem))
    return result
