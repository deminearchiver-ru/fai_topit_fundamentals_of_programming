from typing import Callable, Sequence


course = "Основы программирования"


def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка."""
    if not values:
        return 0.0

    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к нужному регистру."""
    parts = name.split()
    if not parts:
        return ""
    return " ".join(part.capitalize() for part in parts)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет о результатах студента."""
    normalized = normalize_name(student)
    if not normalized:
        return f"{prefix}: имя студента не указано"
    if not results:
        return f"{prefix} ({normalized}): нет результатов"

    mean_value = arithmetic_mean([float(x) for x in results])
    return f"{prefix} ({normalized}): средний балл = {mean_value:.{precision}f}"


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    if not tags:
        return ()

    seen: set[str] = set()
    cleaned: list[str] = []

    for raw_tag in tags:
        tag = raw_tag.strip()
        if not tag:
            continue
        if lowercase:
            tag = tag.lower()
        if tag not in seen:
            seen.add(tag)
            cleaned.append(tag)

    return tuple(cleaned)


def demonstrate_legb() -> tuple[str, int, str]:
    """Демонстрирует правило LEGB и использование nonlocal без изменения глобального имени."""
    attempts = 0
    topic = "Функции и области видимости"

    def inner_step(label: str) -> str:
        nonlocal attempts
        attempts += 1
        # Чтение: label (Local), attempts/topic (Enclosing), course (Global), len (Built-in)
        return (
            f"Шаг {attempts} ({label}): курс='{course}' "
            f"(длина={len(course)}), тема='{topic}'"
        )

    first_message = inner_step("проверка")
    second_message = inner_step("повтор")
    return first_message, attempts, second_message


def add_result_buggy(value: int, results: list[int] = []) -> list[int]:
    """Ошибочная реализация с изменяемым значением по умолчанию."""
    results.append(value)
    return results


def add_result_fixed(value: int, results: list[int] | None = None) -> list[int]:
    """Исправленная реализация: новый список создается при каждом вызове без аргумента."""
    if results is None:
        results = []
    results.append(value)
    return results


def apply_to_results(
    operation: Callable[[int], int | float],
    values: Sequence[int],
) -> list[int | float]:
    """Применяет функцию operation к каждому элементу последовательности и возвращает новый список."""
    return [operation(value) for value in values]


def make_threshold_checker(threshold: float) -> Callable[[float], bool]:
    """Создает функцию-замыкание для проверки достижения порога threshold."""

    def check(score: float) -> bool:
        return score >= threshold

    return check


def add_bonus(score: int) -> int:
    """Добавляет 5 бонусных баллов, но не выше 100."""
    return 100 if score + 5 > 100 else score + 5


def run_demo() -> None:
    print("=== Проверки основных функций (assert) ===")

    # 1. arithmetic_mean
    sample_values = [10.0, 20.0, 30.0]
    assert arithmetic_mean(sample_values) == 20.0
    assert arithmetic_mean([5.0]) == 5.0
    assert arithmetic_mean([]) == 0.0
    assert sample_values == [10.0, 20.0, 30.0]

    # 2. normalize_name
    assert normalize_name("  анна   иванова  ") == "Анна Иванова"
    assert normalize_name("БОРИС петров") == "Борис Петров"
    assert normalize_name("   ") == ""

    # 3. build_report (позиционные и именованные аргументы)
    scores = [80, 90, 85]
    report_default = build_report("  анна  иванова ", scores)
    report_custom = build_report("борис", [70, 75], precision=1, prefix="Итог")
    report_empty = build_report("дарья", [], prefix="Сводка")
    assert report_default == "Результат (Анна Иванова): средний балл = 85.00"
    assert report_custom == "Итог (Борис): средний балл = 72.5"
    assert report_empty == "Сводка (Дарья): нет результатов"
    assert scores == [80, 90, 85]

    # 4. collect_tags
    assert collect_tags(" Python ", "python", "", "  ", "Algorithms") == (
        "python",
        "algorithms",
    )
    assert collect_tags("Python", "python", lowercase=False) == ("Python", "python")
    assert collect_tags() == ()

    print("1.", report_default)
    print("2.", report_custom)
    print("3.", report_empty)
    print("4. Теги:", collect_tags(" Python ", "python", "", "Algorithms"))

    print("\n=== Демонстрация распаковки * и ** ===")
    raw_tags = ["  Lab_03 ", "python", "PYTHON", ""]
    unpacked_tags = collect_tags(*raw_tags)
    report_args = ["илья смирнов", [91, 95, 89]]
    report_kwargs = {"precision": 1, "prefix": "Отчет"}
    unpacked_report = build_report(*report_args, **report_kwargs)

    assert unpacked_tags == ("lab_03", "python")
    assert unpacked_report == "Отчет (Илья Смирнов): средний балл = 91.7"
    print("Распаковка списка (*raw_tags):", unpacked_tags)
    print("Распаковка (*report_args, **report_kwargs):", unpacked_report)

    print("\n=== Исследование LEGB ===")
    msg1, total_attempts, msg2 = demonstrate_legb()
    assert total_attempts == 2
    assert course == "Основы программирования"
    print(msg1)
    print(msg2)
    print("Глобальное имя course не изменено:", course)

    print("\n=== Ошибка изменяемого значения по умолчанию ===")
    buggy_first = add_result_buggy(5)
    buggy_second = add_result_buggy(4)
    assert buggy_first is buggy_second
    assert buggy_second == [5, 4]
    print("Ошибочная функция (общий список):", buggy_first, buggy_second)

    fixed_first = add_result_fixed(5)
    fixed_second = add_result_fixed(4)
    assert fixed_first is not fixed_second
    assert fixed_first == [5] and fixed_second == [4]
    print("Исправленная функция (независимые списки):", fixed_first, fixed_second)

    print("\n=== Практическое расширение: функции высшего порядка и замыкания ===")
    base_results = [65, 80, 97]
    with_bonus = apply_to_results(add_bonus, base_results)
    doubled = apply_to_results(lambda x: x * 2, base_results)

    assert with_bonus == [70, 85, 100]
    assert doubled == [130, 160, 194]
    assert base_results == [65, 80, 97]
    print("С именованной функцией add_bonus:", with_bonus)
    print("С lambda (умножение на 2):", doubled)

    is_pass = make_threshold_checker(60)
    is_excellent = make_threshold_checker(90)
    assert is_pass(60) is True and is_pass(59) is False
    assert is_excellent(89) is False and is_excellent(90) is True
    print("Порог 60 -> 59:", is_pass(59), "| 60:", is_pass(60))
    print("Порог 90 -> 89:", is_excellent(89), "| 90:", is_excellent(90))


if __name__ == "__main__":
    run_demo()
