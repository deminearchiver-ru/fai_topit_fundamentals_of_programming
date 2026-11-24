CATEGORIES = (
    "отличный",
    "хороший",
    "удовлетворительный",
    "недостаточный",
    "нет данных",
)


def mean(values: list[int]) -> float | None:
    """Возвращает среднее арифметическое списка или None для пустого списка."""
    if not values:
        return None
    total = 0
    for value in values:
        total += value
    return total / len(values)


def minimum(values: list[int]) -> int | None:
    """Возвращает минимальное значение списка без использования min() или None."""
    if not values:
        return None
    min_value = values[0]
    for value in values[1:]:
        min_value = min(min_value, value)
    return min_value


def maximum(values: list[int]) -> int | None:
    """Возвращает максимальное значение списка без использования max() или None."""
    if not values:
        return None
    max_value = values[0]
    for value in values[1:]:
        max_value = max(max_value, value)
    return max_value


def classify(score: float | None) -> str:
    """Возвращает текстовую категорию результата по среднему баллу."""
    if score is None:
        return "нет данных"
    if score >= 90:
        return "отличный"
    if score >= 75:
        return "хороший"
    if score >= 60:
        return "удовлетворительный"
    return "недостаточный"


def student_summary(name: str, results: list[int]) -> dict[str, object]:
    """Формирует словарь со статистикой одного студента."""
    avg_score = mean(results)
    return {
        "name": name,
        "count": len(results),
        "mean": avg_score,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(avg_score),
    }


def find_top_students(students: dict[str, list[int]]) -> list[str]:
    """Возвращает список студентов с наибольшим средним результатом."""
    best_mean: float | None = None
    leaders: list[str] = []

    for name, results in students.items():
        avg_score = mean(results)
        if avg_score is None:
            continue
        if best_mean is None or avg_score > best_mean:
            best_mean = avg_score
            leaders = [name]
        elif avg_score == best_mean:
            leaders.append(name)

    return leaders


def build_ranking(
    student_data: list[dict[str, object]],
) -> list[tuple[str, float | None]]:
    """Формирует рейтинг студентов по убыванию среднего балла без изменения исходных данных."""
    ranking: list[tuple[str, float | None]] = [
        (str(item["name"]), item["mean"])  # type: ignore[arg-type]
        for item in student_data
    ]

    length = len(ranking)
    for i in range(length - 1):
        best_index = i
        for j in range(i + 1, length):
            curr_mean = ranking[j][1]
            best_mean = ranking[best_index][1]
            if best_mean is None and curr_mean is not None:
                best_index = j
            elif (
                curr_mean is not None
                and best_mean is not None
                and curr_mean > best_mean
            ):
                best_index = j
        if best_index != i:
            ranking[i], ranking[best_index] = ranking[best_index], ranking[i]

    return ranking


def group_summary(students: dict[str, list[int]]) -> dict[str, object]:
    """Вычисляет общую статистику группы без изменения исходного словаря."""
    student_data = [
        student_summary(name, results) for name, results in students.items()
    ]
    category_counts = {category: 0 for category in CATEGORIES}

    means_sum = 0.0
    students_with_results = 0

    for item in student_data:
        category = str(item["category"])
        category_counts[category] += 1
        avg_score = item["mean"]
        if isinstance(avg_score, (int, float)):
            means_sum += avg_score
            students_with_results += 1

    group_mean = (
        means_sum / students_with_results if students_with_results > 0 else None
    )

    return {
        "student_count": len(students),
        "students_with_results": students_with_results,
        "group_mean": group_mean,
        "top_students": find_top_students(students),
        "categories": category_counts,
        "ranking": build_ranking(student_data),
    }


def format_report(
    student_data: list[dict[str, object]],
    group_data: dict[str, object],
) -> str:
    """Формирует итоговый текстовый отчет по студентам и группе."""
    lines: list[str] = ["--- Статистика по студентам ---"]

    if not student_data:
        lines.append("Нет студентов в группе.")
    else:
        for item in student_data:
            if item["mean"] is None:
                lines.append(
                    f"    {item['name']}: нет результатов (категория: {item['category']})"
                )
            else:
                lines.append(
                    f"    {item['name']}: средний = {item['mean']:.2f}, "
                    f"мин = {item['min']}, макс = {item['max']}, "
                    f"категория = {item['category']}"
                )

    lines.append("--- Общая статистика группы ---")
    group_mean = group_data["group_mean"]
    group_mean_text = (
        f"{group_mean:.2f}" if isinstance(group_mean, (int, float)) else "нет данных"
    )
    top_students: list[str] = group_data["top_students"]  # type: ignore[assignment]
    top_text = ", ".join(top_students) if top_students else "нет данных"

    lines.append(f"    Всего студентов: {group_data['student_count']}")
    lines.append(f"    Общий средний результат группы: {group_mean_text}")
    lines.append(f"    Лидер(ы): {top_text}")

    lines.append("    Распределение по категориям:")
    categories: dict[str, int] = group_data["categories"]  # type: ignore[assignment]
    for category in CATEGORIES:
        lines.append(f"        {category}: {categories[category]}")

    lines.append("    Рейтинг:")
    ranking: list[tuple[str, float | None]] = group_data["ranking"]  # type: ignore[assignment]
    if not ranking:
        lines.append("        нет данных")
    else:
        for place, (name, avg_score) in enumerate(ranking, start=1):
            score_text = f"{avg_score:.2f}" if avg_score is not None else "нет данных"
            lines.append(f"        {place}. {name} ({score_text})")

    return "\n".join(lines)


def run_scenarios() -> None:
    students = {
        "Анна": [78, 91, 84, 88],
        "Борис": [60, 72, 68],
        "Дарья": [95, 93, 97, 90],
        "Илья": [55, 61],
    }

    # Сценарий 1: обычный набор данных
    print("=== Сценарий 1. Обычный набор данных ===")
    original_copy = {name: list(scores) for name, scores in students.items()}
    s1_students = [student_summary(name, scores) for name, scores in students.items()]
    s1_group = group_summary(students)
    assert students == original_copy
    assert s1_group["top_students"] == ["Дарья"]
    assert s1_group["categories"] == {
        "отличный": 1,
        "хороший": 1,
        "удовлетворительный": 1,
        "недостаточный": 1,
        "нет данных": 0,
    }
    print(format_report(s1_students, s1_group))

    # Сценарий 2: один студент
    print("\n=== Сценарий 2. Один студент ===")
    one_student = {"Елена": [80, 90]}
    s2_students = [
        student_summary(name, scores) for name, scores in one_student.items()
    ]
    s2_group = group_summary(one_student)
    assert s2_group["top_students"] == ["Елена"]
    assert s2_group["group_mean"] == 85.0
    print(format_report(s2_students, s2_group))

    # Сценарий 3: несколько лидеров
    print("\n=== Сценарий 3. Несколько лидеров ===")
    tied_group = {
        "Анна": [90, 90],
        "Борис": [85, 95],
        "Виктор": [70, 80],
    }
    s3_students = [student_summary(name, scores) for name, scores in tied_group.items()]
    s3_group = group_summary(tied_group)
    assert s3_group["top_students"] == ["Анна", "Борис"]
    print(format_report(s3_students, s3_group))

    # Сценарий 4: пустая группа
    print("\n=== Сценарий 4. Пустая группа ===")
    empty_group: dict[str, list[int]] = {}
    s4_students = [
        student_summary(name, scores) for name, scores in empty_group.items()
    ]
    s4_group = group_summary(empty_group)
    assert s4_group["student_count"] == 0
    assert s4_group["group_mean"] is None
    assert s4_group["top_students"] == []
    print(format_report(s4_students, s4_group))

    # Сценарий 5: студент без результатов
    print("\n=== Сценарий 5. Студент без результатов ===")
    with_empty_student = {
        "Анна": [80, 90],
        "Олег": [],
    }
    s5_students = [
        student_summary(name, scores) for name, scores in with_empty_student.items()
    ]
    s5_group = group_summary(with_empty_student)
    assert s5_group["top_students"] == ["Анна"]
    assert s5_group["categories"]["нет данных"] == 1
    assert s5_group["ranking"] == [("Анна", 85.0), ("Олег", None)]
    print(format_report(s5_students, s5_group))

    # Сценарий 6: граничные значения категорий
    print("\n=== Сценарий 6. Граничные значения категорий ===")
    boundary_group = {
        "Студент_0": [0],
        "Студент_59": [59],
        "Студент_60": [60],
        "Студент_74": [74],
        "Студент_75": [75],
        "Студент_89": [89],
        "Студент_90": [90],
        "Студент_100": [100],
    }
    s6_students = [
        student_summary(name, scores) for name, scores in boundary_group.items()
    ]
    s6_group = group_summary(boundary_group)
    assert s6_group["categories"] == {
        "отличный": 2,
        "хороший": 2,
        "удовлетворительный": 2,
        "недостаточный": 2,
        "нет данных": 0,
    }
    assert s6_group["top_students"] == ["Студент_100"]
    print(format_report(s6_students, s6_group))


if __name__ == "__main__":
    run_scenarios()
