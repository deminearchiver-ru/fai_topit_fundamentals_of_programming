import sys


def analyze_measurements(values: list[int]) -> dict[str, int | float]:
    """Вычисляет статистику списка без использования min(), max(), sum() и list.count()."""
    if not values:
        raise ValueError("Список измерений не должен быть пустым.")

    # Этап 1: один проход — сумма, минимум, максимум, количество четных
    total = 0
    min_value = values[0]
    max_value = values[0]
    even_count = 0

    for item in values:
        total += item
        min_value = min(min_value, item)
        max_value = max(max_value, item)
        if item % 2 == 0:
            even_count += 1

    average = total / len(values)

    # Этап 2: второй проход — количество значений больше среднего
    above_average_count = 0
    for item in values:
        if item > average:
            above_average_count += 1

    return {
        "total": total,
        "average": average,
        "min": min_value,
        "max": max_value,
        "even_count": even_count,
        "above_average_count": above_average_count,
    }


def linear_search(values: list[int], target: int) -> tuple[int, int]:
    """Линейный поиск первого вхождения target. Возвращает (индекс или -1, число сравнений)."""
    comparisons = 0
    for index, item in enumerate(values):
        comparisons += 1
        if item == target:
            return index, comparisons
    return -1, comparisons


def is_prime(number: int) -> bool:
    """Проверяет простоту положительного целого числа перебором делителей до sqrt(number)."""
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def selection_sort(values: list[int]) -> list[int]:
    """Сортировка выбором по возрастанию (возвращает новый отсортированный список)."""
    result = list(values)
    length = len(result)

    for i in range(length - 1):
        min_index = i
        for j in range(i + 1, length):
            if result[j] < result[min_index]:
                min_index = j
        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result


def binary_search(sorted_values: list[int], target: int) -> tuple[int, int]:
    """Бинарный поиск в отсортированном списке. Возвращает (индекс или -1, число сравнений)."""
    left = 0
    right = len(sorted_values) - 1
    comparisons = 0

    while left <= right:
        middle = (left + right) // 2
        comparisons += 1
        if sorted_values[middle] == target:
            return middle, comparisons
        comparisons += 1
        if sorted_values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1, comparisons


def run_demo() -> None:
    measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

    print("=== Базовые алгоритмические схемы ===")
    stats = analyze_measurements(measurements)
    assert stats["total"] == 144
    assert stats["average"] == 14.4
    assert stats["min"] == 7
    assert stats["max"] == 21
    assert stats["even_count"] == 4
    assert stats["above_average_count"] == 6

    print(f"Исходные данные: {measurements}")
    print(f"Сумма: {stats['total']}")
    print(f"Среднее арифметическое: {stats['average']:.2f}")
    print(f"Минимум: {stats['min']}")
    print(f"Максимум: {stats['max']}")
    print(f"Четных значений: {stats['even_count']}")
    print(f"Значений больше среднего: {stats['above_average_count']}")

    print("\n=== Линейный поиск ===")
    if sys.stdin.isatty():
        raw_input = input(
            "Введите целое число для поиска в measurements (Enter для 15): "
        ).strip()
        target = int(raw_input) if raw_input else 15
    else:
        target = 15

    found_index, found_comparisons = linear_search(measurements, target)
    print(f"Поиск {target}: индекс = {found_index} (сравнений: {found_comparisons})")

    # Проверки линейного поиска
    assert linear_search(measurements, 15)[0] == 1
    assert linear_search(measurements, 18)[0] == 3
    assert linear_search(measurements, 99)[0] == -1
    print(
        f"Поиск отсутствующего числа 99: индекс = {linear_search(measurements, 99)[0]}"
    )

    print("\n=== Проверка простоты числа ===")
    prime_cases = [
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (25, False),
        (29, True),
        (97, True),
        (100, False),
    ]
    for value, expected in prime_cases:
        actual = is_prime(value)
        assert actual == expected, (
            f"is_prime({value}): ожидалось {expected}, получено {actual}"
        )
        print(f"    {value:3d} -> {'простое' if actual else 'не простое'}")

    print("\n=== Практическое расширение: сортировка выбором и сравнение поисков ===")
    sorted_measurements = selection_sort(measurements)
    assert sorted_measurements == [7, 9, 11, 12, 15, 15, 18, 18, 18, 21]
    assert measurements == [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
    print(f"Отсортированный список measurements: {sorted_measurements}")

    sizes = [10, 100, 1000]
    print(
        f"\n{'Размер':>8} | {'Сценарий':<18} | {'Цель':>6} | "
        f"{'Линейный (сравн.)':>17} | {'Бинарный (сравн.)':>17}"
    )
    print("-" * 78)

    for size in sizes:
        # Исходный список в обратном порядке сортируем сортировкой выбором
        unsorted_data = list(range(size, 0, -1))
        data = selection_sort(unsorted_data)
        assert data[0] == 1 and data[-1] == size

        test_targets = [
            ("начало (1)", 1),
            ("середина", size // 2),
            ("конец", size),
            ("отсутствует", size + 1),
        ]

        for label, search_target in test_targets:
            lin_idx, lin_cmp = linear_search(data, search_target)
            bin_idx, bin_cmp = binary_search(data, search_target)
            assert lin_idx == bin_idx, (
                f"Индексы не совпали для size={size}, target={search_target}"
            )
            print(
                f"{size:8d} | {label:<18} | {search_target:6d} | "
                f"{lin_cmp:17d} | {bin_cmp:17d}"
            )


if __name__ == "__main__":
    run_demo()
