LEVELS = (
    "недостаточный",
    "удовлетворительный",
    "хороший",
    "отличный",
)


def describe_work_type(work_type: str) -> str:
    """Возвращает текстовое пояснение для типа работы."""
    match work_type:
        case "exam":
            return "экзаменационная работа"
        case "project":
            return "проектная работа"
        case "practice":
            return "практическая работа"
        case _:
            return "неизвестный тип работы"


def classify_student(
    score: int, work_type: str, absences: int
) -> tuple[str | None, str]:
    """Проверяет диапазоны, определяет уровень результата и формирует строку вывода."""
    if score < 0 or score > 100:  # noqa: PLR2004
        return None, f"Ошибка: результат {score} вне допустимого диапазона 0..100."
    elif absences < 0 or absences > 5:
        return (
            None,
            f"Ошибка: количество пропусков {absences} вне допустимого диапазона 0..5.",
        )
    else:
        if score >= 90:
            level_index = 3
        elif score >= 75:
            level_index = 2
        elif score >= 60:
            level_index = 1
        else:
            level_index = 0

        if absences > 3 and level_index > 0:
            level_index -= 1

        level = LEVELS[level_index]
        work_description = describe_work_type(work_type)
        message = (
            f"Результат: {score}, тип: {work_description}, "
            f"пропусков: {absences} -> уровень: {level}"
        )
        return level, message


def run_test_scenarios() -> None:
    """Проверяет классификацию на граничных и особых наборах данных."""
    print("=== Тестовые сценарии (Части 1–4) ===")
    scenarios = [
        (0, "exam", 0, "недостаточный", "экзаменационная работа"),
        (59, "practice", 2, "недостаточный", "практическая работа"),
        (60, "project", 1, "удовлетворительный", "проектная работа"),
        (74, "exam", 3, "удовлетворительный", "экзаменационная работа"),
        (75, "practice", 0, "хороший", "практическая работа"),
        (89, "project", 2, "хороший", "проектная работа"),
        (90, "exam", 1, "отличный", "экзаменационная работа"),
        (100, "project", 3, "отличный", "проектная работа"),
        (95, "exam", 4, "хороший", "экзаменационная работа"),
        (50, "practice", 5, "недостаточный", "практическая работа"),
        (80, "lab", 1, "хороший", "неизвестный тип работы"),
        (105, "exam", 0, None, "Ошибка"),
        (80, "exam", 6, None, "Ошибка"),
    ]

    for index, (
        score,
        work_type,
        absences,
        expected_level,
        expected_fragment,
    ) in enumerate(scenarios, start=1):
        actual_level, message = classify_student(score, work_type, absences)
        assert actual_level == expected_level, (
            f"Сценарий {index}: ожидался уровень {expected_level}, получен {actual_level}"
        )
        assert expected_fragment in message, (
            f"Сценарий {index}: в сообщении '{message}' нет '{expected_fragment}'"
        )
        print(f"{index:2d}. ({score}, {work_type!r}, {absences}) -> {message}")


def run_practical_extension() -> None:
    """Обрабатывает список из 10 записей и выводит сводку по уровням."""
    print("\n=== Практическое расширение (обработка списка записей) ===")
    records = [
        (96, "exam", 1),
        (91, "project", 4),
        (84, "practice", 2),
        (75, "exam", 5),
        (72, "project", 0),
        (60, "practice", 4),
        (58, "exam", 1),
        (100, "practice", 0),
        (88, "seminar", 2),
        (45, "project", 5),
    ]
    original_snapshot = list(records)

    level_counts = {level: 0 for level in LEVELS}
    formatted_results: list[str] = []

    for index, (score, work_type, absences) in enumerate(records, start=1):
        level, message = classify_student(score, work_type, absences)
        formatted_results.append(f"Студент {index:2d}: {message}")
        if level is not None:
            level_counts[level] += 1

    assert records == original_snapshot, "Исходный список записей не должен изменяться"
    assert level_counts == {
        "недостаточный": 3,
        "удовлетворительный": 2,
        "хороший": 3,
        "отличный": 2,
    }

    for line in formatted_results:
        print(line)

    print("\nИтоговая сводка по уровням:")
    for level in LEVELS:
        print(f"    {level}: {level_counts[level]}")


if __name__ == "__main__":
    run_test_scenarios()
    run_practical_extension()
