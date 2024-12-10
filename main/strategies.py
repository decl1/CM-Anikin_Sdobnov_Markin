# strategies library
import sys

from munkres import Munkres

import generate_data as generator
from hungarian_algorithm import algorithm


def output_example(input_example):
    return "example: " + input_example


# Реализованы жадный, бережливый, бережливо/жадный и жадно/бережливый алгоритмы
# Все алгоритмы на вход получают полную матрицу состояний, которая за пределами алгоритмов приводится к нужному виду
# Матрица расстояний рассматривается по столбцам. Таким образом имитируется нечеткая задача.
# Функции возвращают число - максимальную сумму перестановки партий по этапам, полученную с помощью
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


# k < num_batches - swap_stage + 1
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


def hungarian_strategy(s_matrix):
    # Создаем новую матрицу, в которой будем хранить результат
    new_matrix = []

    # Шаг 1 и 2: Для каждой строки находим максимальный элемент и вычитаем его
    for i in range(len(s_matrix)):  # Проходим по строкам
        row_max = max(s_matrix[i])  # Находим максимальный элемент в строке
        new_row = [x - row_max for x in s_matrix[i]]  # Вычитаем максимальный элемент из всех элементов строки
        new_matrix.append(new_row)  # Добавляем измененную строку в новую матрицу

    # Шаг 3: Умножаем всю новую матрицу на -1
    final_matrix = [[-x for x in row] for row in new_matrix]

    m = Munkres()
    indexes = m.compute(final_matrix)
    total = 0
    for row, column in indexes:
        value = s_matrix[row][column]
        total += value

    return total
#    matrix = {
#        f"#{row_idx}": {str(col_idx): s_matrix[row_idx][col_idx] for col_idx in range(len(s_matrix[row_idx]))}
#        for row_idx in range(len(s_matrix))
#    }
#    print(matrix)
#    return algorithm.find_matching(matrix, matching_type='max', return_type='total')


# Наша эвристическая функция. На каждом этапе выбирает партию наиболее близкую к среднему значению
def average_strategy(num_batches, num_stages, s_matrix):
    result = 0
    used_batches = []
    for j in range(num_stages):
        # Строим текущий столбец
        column = [s_matrix[i][j] for i in range(num_batches)]

        # Исключаем уже использованные партии
        for batch in used_batches:
            column[batch] = -1

        # Вычисляем среднее арифметическое для текущего столбца
        avg = sum(column) / len([x for x in column if x != -1])

        # Находим элемент, ближайший к среднему
        closest_value = min(column, key=lambda x: abs(x - avg) if x != -1 else float('inf'))

        # Добавляем выбранный элемент в результат
        result += closest_value

        # Добавляем индекс выбранной партии в список использованных
        used_batches.append(column.index(closest_value))

    return result


def experiment(m, d, batches, stages, sugarMin, sugarMax, degMin, degMax, concentrate=False, ripening=0, inoInf=False):
    _, _, s_matrix = generator.generate(batches_=batches, stages_=stages, sugarMin_=sugarMin,
                                                   sugarMax_=sugarMax, degMin_=degMin,
                                                   degMax_=degMax, concentrate_=concentrate, ripening_=ripening,
                                                   inoInf_=inoInf)

    swap_stage = stages // 2
    k = stages - swap_stage

    results = {strategy: {'sugar': 0, 'losses': 0} for strategy in
               ["Greedy", "Thrifty", "Thrifty/Greedy", "Greedy/Thrifty", "T(k)G", "Average"]}

    strategies = {
        "Greedy": greedy_strategy,
        "Thrifty": thrifty_strategy,
        "Thrifty/Greedy": lambda b, s, sm: thrifty_greedy_strategy(b, s, sm, swap_stage),
        "Greedy/Thrifty": lambda b, s, sm: greedy_thrifty_strategy(b, s, sm, swap_stage),
        "T(k)G": lambda b, s, sm: tkg_strategy(b, s, sm, swap_stage, k),
        "Average": average_strategy
    }

    max_sugar = m * d * hungarian_strategy(s_matrix)

    for name, strategy in strategies.items():
        strategy_sugar = strategy(batches, stages, s_matrix) * m * d
        strategy_losses = max_sugar - strategy_sugar
        results[name] = {'sugar': strategy_sugar, 'losses': strategy_losses}

    return results

def run_virtual_experiments(num_experiments, m, d, batches, stages, sugarMin, sugarMax, degMin, degMax, concentrate=False, ripening=0, inoInf=False):
    total_results = {strategy: {'sugar': 0, 'losses': 0} for strategy in ["Greedy", "Thrifty", "Thrifty/Greedy", "Greedy/Thrifty", "T(k)G",  "Average"]}

    for _ in range(num_experiments):

        experiment_results = experiment(m, d, batches, stages, sugarMin, sugarMax, degMin, degMax, concentrate, ripening, inoInf)
        for strategy, value in experiment_results.items():
            total_results[strategy]['sugar'] += value['sugar']
            total_results[strategy]['losses'] += value['losses']

    # Усреднение результатов
    for strategy in total_results:
        total_results[strategy]['sugar'] /= num_experiments
        total_results[strategy]['losses'] /= num_experiments

    return total_results


if __name__ == "__main__":
    s_matrix = [[10, 5, 2],
                [7, 3, 1],
                [3, 2, 1],
                [1, 1, 1]]
    print(run_virtual_experiments(30,3000, 7, 20, 15, 0.12, 0.22, 0.85, 1.0))
