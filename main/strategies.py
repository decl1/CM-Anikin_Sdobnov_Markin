# strategies library
import numpy as np


def output_example(input_example):
    return "example: " + input_example

#Реализованы жадный, бережливый, бережливо/жадный и жадно/бережливый алгоритмы
#Все алгоритмы на вход получают полную матрицу состояний, которая за пределами алгоритмов приводится к нужному виду
#Матрица расстояний рассматривается по столбцам. Таким образом имитируется нечеткая задача.
#Функции возвращают число - максимальную сумму перестановки партий по этапам, полученную с помощью
# соответствующего алгоритма, то есть S(b)
#
#
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
        min_elem = min(column)
        result += min_elem
        used_batches.append(column.index(min_elem))
    return result

def thrifty_greedy_strategy(num_batches, num_stages, s_matrix, swap_stage):
    result = 0
    used_batches = []
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = float("inf")
        min_elem = min(column)
        result += min_elem
        used_batches.append(column.index(min_elem))
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
        min_elem = min(column)
        result += min_elem
        used_batches.append(column.index(min_elem))
    return result

#k < num_batches - swap_stage + 1
def tkg_strategy(num_batches, num_stages, s_matrix, swap_stage, k):
    result = 0
    used_batches = []
    for j in range(swap_stage):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = float("inf")
        for _ in range(k):
            column[column.index(min(column))] = float("inf")
        min_elem = min(column)
        result += min_elem
        used_batches.append(column.index(min_elem))

    for j in range(swap_stage, num_stages):
        column = [s_matrix[i][j] for i in range(num_batches)]
        for batch in used_batches:
            column[batch] = -1
        max_elem = max(column)
        result += max_elem
        used_batches.append(column.index(max_elem))

    return result

if __name__ == "__main__":
    s_matrix = [[10, 5, 2],
                [7, 3, 1],
                [3, 2, 1]]
    print(greedy_strategy(num_batches=3, num_stages=3, s_matrix=s_matrix))
    print(thrifty_strategy(num_batches=3, num_stages=3, s_matrix=s_matrix))
    print(thrifty_greedy_strategy(num_batches=3, num_stages=3, s_matrix=s_matrix, swap_stage=1))
    print(greedy_thrifty_strategy(num_batches=3, num_stages=3, s_matrix=s_matrix, swap_stage=1))
    print(tkg_strategy(num_batches=3, num_stages=3, s_matrix=s_matrix, swap_stage=1, k=1))