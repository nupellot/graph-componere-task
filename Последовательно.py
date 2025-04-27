# По имеющейся матрице смежности распределить вершины графа на подгруппы
# заданного размера таким образом, чтобы минимизировать суммарный вес внешних связей (связей между группами)

import bisect
import copy

# Функция для печати матрицы смежности
def print_adjacency_matrix(matrix):
    for row in matrix:
        for value in row:
            print(f"{value:3}", end="")
        print()
    print()

# Изначальные размеры групп, которые нужно сформировать
target_group_sizes = [4, 5, 5, 6]

# Список для хранения финальных групп
final_groups = []

# Матрица смежности: вершины графа и веса связей между ними
adjacency_matrix = [
    [0,   0,   4,   0,   0,   4,   0,   0,   0,   8,   0,   0,   0,   8,   0,   0,   0,   0,   2,   0],
    [0,   0,   0,   9,   8,   0,   5,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [4,   0,   0,   0,   0,   5,   0,   0,   0,   3,   0,   1,   0,  12,   0,   0,   0,   0,   0,   0],
    [0,   9,   0,   0,   6,   1,  10,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   8,   0,   6,   0,   0,   4,   5,   0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [4,   0,   5,   1,   0,   0,   0,   0,   0,   4,   0,   0,   0,   4,   0,   0,   0,   0,   0,   0],
    [0,   5,   0,  10,   4,   0,   0,   2,   0,   0,   0,   0,   0,   0,   0,   1,   2,   0,   0,   0],
    [0,   0,   0,   3,   5,   0,   2,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   8],
    [8,   0,   3,   0,   2,   4,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  19,   0,   2,   0,   9,   0,   5,   0],
    [0,   0,   1,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   2,   0,   3],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  19,   0,   0,   0,   0,   9,   3,   0,   2,   0],
    [8,   0,  12,   0,   0,   4,   0,   0,   0,   1,   0,   0,   0,   0,   2,   1,   0,   2,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   2,   0,   0,   2,   0,   5,   2,   0,   5,   0],
    [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   9,   1,   5,   0,   3,   0,  11,   0],
    [0,   0,   0,   0,   0,   0,   2,   0,   0,   0,   9,   0,   3,   0,   2,   3,   0,   0,  14,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   2,   0,   2,   0,   0,   0,   0,   0,   1],
    [2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   5,   0,   2,   0,   5,  11,  14,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   8,   0,   0,   3,   0,   0,   0,   0,   0,   1,   0,   0]
]

# Добавляем номера строк и столбцов для удобства
adjacency_matrix.insert(0, [i for i in range(1, len(adjacency_matrix) + 1)])
for i in range(len(adjacency_matrix)):
    adjacency_matrix[i].insert(0, i)

print("Начальная матрица смежности:")
print_adjacency_matrix(adjacency_matrix)





# Главный цикл: пока не останется только одна группа
iteration = 1
while len(target_group_sizes) > 1:
    print(f"=== Итерация {iteration} ===")

    # Вычисляем сумму весов рёбер для каждой вершины
    vertex_weights = [sum(row[1:]) for row in adjacency_matrix[1:]]
    print("Сумма весов рёбер для каждой вершины:", vertex_weights)

    # Выбираем вершину с минимальной суммой весов рёбер
    min_weight = min(vertex_weights)
    candidate_idx = vertex_weights.index(min_weight) + 1
    candidate_vertex = adjacency_matrix[candidate_idx][0]
    print(f"Выбрана вершина {candidate_vertex} с минимальной суммой весов рёбер {min_weight}")

    # Если таких несколько, выбираем ту, у которой меньше нулевых связей
    # Вроде бы для того, чтобы потом легче было находить соседей..
    if vertex_weights.count(min_weight) > 1:
        for i in range(1, len(vertex_weights)):
            if vertex_weights[i] == min_weight:
                if adjacency_matrix[i + 1].count(0) < adjacency_matrix[candidate_idx].count(0):
                    candidate_idx = i + 1
                    candidate_vertex = adjacency_matrix[candidate_idx][0]
    print(f"Итоговый кандидат для начала группы: {candidate_vertex}")


    # Находим смежные вершины
    neighbors = []
    column_index = adjacency_matrix[0].index(candidate_vertex)
    for i in range(1, len(adjacency_matrix)):
        if adjacency_matrix[i][column_index] != 0:
            neighbors.append(adjacency_matrix[i][0])
    # neighbors.append(candidate_vertex)
    bisect.insort(neighbors, candidate_vertex)  # Шоб красиво было!!

    print("Начальная группа (Канидат + его соседи)):", neighbors)

    # Расширяем группу до нужного размера
    while len(neighbors) < target_group_sizes[0]:
        expanded = copy.deepcopy(neighbors)
        for v in expanded:  # Для каждого соседа
            for i in range(1, len(adjacency_matrix)):  # смотрим на все остальные вершины
                # и если с ней есть связь и она ещё не в списке, то добавляем.
                if adjacency_matrix[v][i] != 0 and i not in neighbors:
                    # neighbors.append(adjacency_matrix[0][i])  
                    bisect.insort(neighbors, adjacency_matrix[0][i])
    print(f"Группа после расширения до {target_group_sizes[0]}+: {neighbors}")
    # Тут мы достаточно расширились во все стороны и можно обрезать лишнее

    # Оценка и удаление вершин с максимальной "внешней нагрузкой"
    while len(neighbors) > target_group_sizes[0]:
        max_external_weight = -1
        vertex_to_remove = None

        # Для каждой вершины считаем "внешнюю нагрузку" S[v]
        for vertex in neighbors:
            v_idx = adjacency_matrix[0].index(vertex)
            internal_weight = sum(adjacency_matrix[v_idx][adjacency_matrix[0].index(neighbor)] for neighbor in neighbors)
            external_weight = vertex_weights[v_idx - 1] - internal_weight  # S[v] = вес вершины - вес внутренних связей
                                            # сдвиг, потому что vertex_weights считался по-другому
            if external_weight > max_external_weight:
                max_external_weight = external_weight
                vertex_to_remove = vertex

        # Удаляем вершину с максимальной "внешней нагрузкой"
        neighbors.remove(vertex_to_remove)
        print(f"Удалена вершина {vertex_to_remove} с внешней нагрузкой {max_external_weight}")

    # Сохраняем группу и удаляем её из матрицы
    print(f"Финальная группа {neighbors}")
    final_groups.append(copy.deepcopy(neighbors))
    target_group_sizes.remove(len(neighbors))

    # Удаляем вершины, которые были добавлены в группу
    for v in neighbors:
        idx = adjacency_matrix[0].index(v)  # ищем индекс, на котором в урезанной матрице находится вершина
        adjacency_matrix.pop(idx)  # горизонтально удаляем
        for row in adjacency_matrix:  
            row.pop(idx)  # вертикально удаляем

    print("Матрица после удаления группы:")
    print_adjacency_matrix(adjacency_matrix)
    iteration += 1

# Добавляем оставшиеся вершины в последнюю группу
final_groups.append(adjacency_matrix[0][1:])

# Вывод результата
print("\n=== Финальное разбиение на группы ===")
for i, group in enumerate(final_groups):
    print(f"Группа {i+1} ({len(group)} эл.): {group}")
