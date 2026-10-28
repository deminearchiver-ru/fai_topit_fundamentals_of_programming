import copy

def print_structures_state(
    stage_title: str,
    original: list,
    alias: list,
    shallow: list,
    deep: list,
) -> None:
    print(f"=== {stage_title} ===")
    structures = {
        "original": original,
        "alias": alias,
        "shallow": shallow,
        "deep": deep,
    }

    print("Содержимое структур:")
    for name, struct in structures.items():
        print(f"    {name.ljust(8)} = {struct}")

    print("\nИдентификаторы (id):")
    for name, struct in structures.items():
        outer_id = id(struct)
        first_inner_id = id(struct[0])
        first_grade_id = id(struct[0][1])
        print(
            f"    {name.ljust(8)} -> внешний список: {outer_id}, "
            f"первый вложенный список: {first_inner_id}, "
            f"первая оценка ({struct[0][1]}): {first_grade_id}"
        )
    print()

def experiment_copying() -> None:
    original = [
        ["Python", 5],
        ["Algorithms", 4],
    ]

    alias = original
    shallow = original.copy()
    deep = copy.deepcopy(original)

    print_structures_state(
        "Исходное состояние (до изменений)",
        original,
        alias,
        shallow,
        deep,
    )

    # Изменение 1: добавление элемента во внешний список
    original.append(["Databases", 5])
    print_structures_state(
        "После original.append(['Databases', 5])",
        original,
        alias,
        shallow,
        deep,
    )

    # Изменение 2: модификация элемента внутри первого вложенного списка
    original[0][1] = 3
    print_structures_state(
        "После original[0][1] = 3",
        original,
        alias,
        shallow,
        deep,
    )

def experiment_matrices() -> None:
    print("=== Исследование создания матрицы ===")

    # Ошибочное создание матрицы
    wrong_matrix = [[0] * 3] * 3
    wrong_matrix[0][0] = 1

    print("Ошибочная матрица (wrong_matrix = [[0] * 3] * 3 после wrong_matrix[0][0] = 1):")
    print("    Значение:", wrong_matrix)
    print(
        "    id строк:",
        id(wrong_matrix[0]),
        id(wrong_matrix[1]),
        id(wrong_matrix[2]),
    )
    print(
        "    Все строки — один и тот же объект?",
        wrong_matrix[0] is wrong_matrix[1] is wrong_matrix[2],
    )

    # Корректное создание матрицы без deepcopy()
    correct_matrix = [[0] * 3 for _ in range(3)]
    correct_matrix[0][0] = 1

    print("\nКорректная матрица (correct_matrix = [[0] * 3 for _ in range(3)] после correct_matrix[0][0] = 1):")
    print("    Значение:", correct_matrix)
    print(
        "    id строк:",
        id(correct_matrix[0]),
        id(correct_matrix[1]),
        id(correct_matrix[2]),
    )
    print(
        "    Строки независимы?",
        (correct_matrix[0] is not correct_matrix[1])
        and (correct_matrix[1] is not correct_matrix[2])
        and (correct_matrix[0] is not correct_matrix[2]),
    )

if __name__ == "__main__":
    experiment_copying()
    experiment_matrices()
