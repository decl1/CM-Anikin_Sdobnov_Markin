# strategies library
from hungarian_algorithm import algorithm


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

def hungarian_strategy(s_matrix):
    matrix = {
        f"#{row_idx}": {str(col_idx): s_matrix[row_idx][col_idx] for col_idx in range(len(s_matrix[row_idx]))}
        for row_idx in range(len(s_matrix))
    }
    return algorithm.find_matching(matrix, matching_type='max', return_type='total')

#Наша эвристическая функция. На каждом этапе выбирает партию наиболее близкую к среднему значению
#
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

if __name__ == "__main__":
    s_matrix = [[10, 5, 2],
                [7, 3, 1],
                [3, 2, 1],
                [1, 1, 1]]
    print(greedy_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix))
    print(thrifty_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix))
    print(thrifty_greedy_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix, swap_stage=1))
    print(greedy_thrifty_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix, swap_stage=1))
    print(tkg_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix, swap_stage=1, k=1))
    print(hungarian_strategy(s_matrix))
    print(average_strategy(num_batches=4, num_stages=3, s_matrix=s_matrix))