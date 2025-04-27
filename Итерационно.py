# Оптимизируем решение задачи по разделению графа на подгруппы итерационным методом
# пробуем менять все вершины графа со всеми таким образом, чтобы уменьшать метрику delta

import copy

# Функция для печати матрицы смежности
# matrix: двумерный список, где matrix[0] и matrix[i][0] — это заголовки
# значения matrix[i][j] — вес ребра между вершинами
# i, j начинаются с 1 для реальных вершин

def print_adjacency_matrix(matrix):
    for row in matrix:
        print("".join(f"{val:3}" for val in row))
    print()

# Исходная матрица смежности DataMass (с заголовками столбцов/строк после вставки)
# каждая ячейка [i][j] — вес ребра между вершинами i и j
DataMass = [
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




# Добавляем заголовки: первая строка и первый столбец
DataMass.insert(0, [i for i in range(1, len(DataMass) + 1)])
for idx, row in enumerate(DataMass):
    row.insert(0, idx)

print("Исходная матрица смежности:")
print_adjacency_matrix(DataMass)

# Начальное решение: группы вершин, полученные эвристикой
groups = [
    [9, 12, 18, 20],
    [2, 4, 5, 7, 8],
    [11, 15, 16, 17, 19],
    [1, 3, 6, 10, 13, 14]
]

# Итеративная оптимизация: ищем обмены пар вершин между группами для увеличения внутренней связности
for i, base_group in enumerate(groups[:-1]):
    print(f"\n--- Оптимизация группы {i} ---")

    while True:
        # Составляем список всех кандидатов для обмена: пары (u из base_group, v из любой группы j>i)
        # Для каждого u и v считаем дельту выгоды delta(u,v)
        deltas = []  # список кортежей (delta, idx_u, idx_v, group_index_v)
        # Пробегаем по всем вершинам u текущей группы
        for idx_u, u in enumerate(base_group):
            # Связь u со всеми вершинами его группы (интернальные связи)
            sum_u_in = sum(DataMass[u][v] for v in base_group)
            # Связь u со всеми вершинами всех остальных групп (экстернальные)
            for j in range(i+1, len(groups)):
                for idx_v_in_j, v in enumerate(groups[j]):
                    sum_u_to_j = sum(DataMass[u][w] for w in groups[j])
                    sum_v_in = sum(DataMass[v][w] for w in groups[j])
                    sum_v_to_i = sum(DataMass[v][w] for w in base_group)
                    # delta = (u->group j - u->base_group) + (v->base_group - v->group j) - 2*weight(u,v)
                    delta = (
                        sum_u_to_j - sum_u_in
                        + sum_v_to_i - sum_v_in
                        - 2 * DataMass[u][v]  # этих связей на самом деле не будет, т.к. вершины переехали
                    )
                    deltas.append((delta, idx_u, idx_v_in_j, j))

        # Находим лучший обмен с максимальной положительной дельтой
        best = max(deltas, key=lambda x: x[0]) if deltas else (None, None, None, None)
        best_delta, best_idx_u, best_idx_v, best_group_j = best

        # Если улучшений нет - выходим
        if best_delta is None or best_delta <= 0:
            print(f"Группа {i}: больше нет положительных обменов (max delta = {best_delta})")
            break

        # Иначе выполняем обмен
        u = base_group[best_idx_u]
        v = groups[best_group_j][best_idx_v]
        print(f"Обмен: вершина {u} (группа {i}) <--> вершина {v} (группа {best_group_j}), delta={best_delta}")
        # Меняем местами
        groups[best_group_j][best_idx_v], base_group[best_idx_u] = u, v

    print(f"Группа {i} после оптимизации: {base_group}")

# Вывод финальных групп
print("\nОптимизированные группы:")
for idx, grp in enumerate(groups):
    print(f" Группа {idx}: {grp}")

# Строим новую упорядоченную матрицу по оптимизированному разбиению
n = len(DataMass)
new_order = [v for grp in groups for v in grp]
# Добавляем заголовок 0 в начало
new_order = [0] + new_order

NewOptMass = [[0] * (n) for _ in range(n)]
# Заполняем заголовки
NewOptMass[0] = new_order
for i in range(n):
    NewOptMass[i][0] = new_order[i]
# Заполняем веса
for i in range(1, n):
    for j in range(1, n):
        orig_u = NewOptMass[i][0]
        orig_v = NewOptMass[0][j]
        NewOptMass[i][j] = DataMass[orig_u][orig_v]

print("\nНовая матрица после оптимизации:")
print_adjacency_matrix(NewOptMass)
