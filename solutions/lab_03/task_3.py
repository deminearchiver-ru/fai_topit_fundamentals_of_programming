Submission = tuple[str, str, int]


def add_submission(
    record: Submission,
    students: set[str],
    laboratories: set[str],
    attempts_by_student: dict[str, list[tuple[str, int]]],
    best_results: dict[tuple[str, str], int],
    attempts_count: dict[tuple[str, str], int],
    students_by_lab: dict[str, set[str]],
) -> None:
    """Добавляет одну запись о сдаче и обновляет все структуры без полного перестроения."""
    student, lab, score = record
    key = (student, lab)

    students.add(student)
    laboratories.add(lab)

    attempts_by_student.setdefault(student, []).append((lab, score))

    if key not in best_results or score > best_results[key]:
        best_results[key] = score

    attempts_count[key] = attempts_count.get(key, 0) + 1
    students_by_lab.setdefault(lab, set()).add(student)


def build_structures(
    submissions: list[Submission],
) -> tuple[
    set[str],
    set[str],
    dict[str, list[tuple[str, int]]],
    dict[tuple[str, str], int],
    dict[tuple[str, str], int],
    dict[str, set[str]],
]:
    """Строит все требуемые коллекции из исходного списка записей."""
    students: set[str] = set()
    laboratories: set[str] = set()
    attempts_by_student: dict[str, list[tuple[str, int]]] = {}
    best_results: dict[tuple[str, str], int] = {}
    attempts_count: dict[tuple[str, str], int] = {}
    students_by_lab: dict[str, set[str]] = {}

    for record in submissions:
        add_submission(
            record,
            students,
            laboratories,
            attempts_by_student,
            best_results,
            attempts_count,
            students_by_lab,
        )

    return (
        students,
        laboratories,
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    )


def handle_query(
    query: str,
    attempts_by_student: dict[str, list[tuple[str, int]]],
    best_results: dict[tuple[str, str], int],
    attempts_count: dict[tuple[str, str], int],
    students_by_lab: dict[str, set[str]],
) -> str:
    """Обрабатывает текстовый запрос к построенным структурам без аварийного завершения."""
    parts = query.strip().split()
    if not parts:
        return "Ошибка: пустой запрос."

    match parts:
        case ["student", student]:
            attempts = attempts_by_student.get(student)
            if attempts is None:
                return f"Студент '{student}' не найден."
            return f"Попытки студента {student}: {attempts}"
        case ["best", student, lab]:
            best = best_results.get((student, lab))
            if best is None:
                return f"Нет данных о лучшем результате для ({student}, {lab})."
            return f"Лучший результат для ({student}, {lab}): {best}"
        case ["attempts", student, lab]:
            count = attempts_count.get((student, lab))
            if count is None:
                return f"Нет попыток для ({student}, {lab})."
            return f"Количество попыток для ({student}, {lab}): {count}"
        case ["completed", lab]:
            completed_students = students_by_lab.get(lab)
            if completed_students is None:
                return f"Лабораторная работа '{lab}' не найдена."
            return f"Сдали {lab}: {sorted(completed_students)}"
        case _:
            return f"Неизвестная команда или неверное число аргументов: '{query}'"


def run_demo() -> None:
    submissions: list[Submission] = [
        ("anna", "lab_01", 5),
        ("boris", "lab_01", 4),
        ("anna", "lab_02", 5),
        ("daria", "lab_01", 3),
        ("boris", "lab_02", 5),
        ("anna", "lab_01", 4),
    ]

    (
        students,
        laboratories,
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    ) = build_structures(submissions)

    print("=== Исходные коллекции ===")
    print("1. Все студенты:", sorted(students))
    print("2. Все лабораторные работы:", sorted(laboratories))
    print("3. Попытки по студентам:", attempts_by_student)
    print("4. Лучшие результаты:", best_results)
    print("5. Количество попыток:", attempts_count)

    both_labs = students_by_lab["lab_01"] & students_by_lab["lab_02"]
    print("Студенты, сдавшие обе работы (пересечение множеств):", sorted(both_labs))

    assert students == {"anna", "boris", "daria"}
    assert laboratories == {"lab_01", "lab_02"}
    assert best_results[("anna", "lab_01")] == 5
    assert attempts_count[("anna", "lab_01")] == 2
    assert both_labs == {"anna", "boris"}

    print("\n=== Инкрементальное обновление (добавление новой записи) ===")
    new_record: Submission = ("daria", "lab_02", 4)
    add_submission(
        new_record,
        students,
        laboratories,
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    )
    both_labs_updated = students_by_lab["lab_01"] & students_by_lab["lab_02"]

    assert best_results[("daria", "lab_02")] == 4
    assert attempts_count[("daria", "lab_02")] == 1
    assert both_labs_updated == {"anna", "boris", "daria"}

    print(f"Добавлена запись: {new_record}")
    print("Обновленные попытки daria:", attempts_by_student["daria"])
    print(
        "Обновленный лучший результат (daria, lab_02):",
        best_results[("daria", "lab_02")],
    )
    print("Сдали обе работы после обновления:", sorted(both_labs_updated))

    print("\n=== Практическое расширение: текстовые запросы ===")
    queries = [
        "student anna",
        "best anna lab_01",
        "attempts boris lab_02",
        "completed lab_01",
        "student ivan",
        "best daria lab_03",
        "unknown command",
    ]
    for query in queries:
        response = handle_query(
            query,
            attempts_by_student,
            best_results,
            attempts_count,
            students_by_lab,
        )
        print(f"    > {query}\n      {response}")

    assert "5" in handle_query(
        "best anna lab_01",
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    )
    assert "не найден" in handle_query(
        "student ivan",
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    )
    assert "Неизвестная команда" in handle_query(
        "unknown command",
        attempts_by_student,
        best_results,
        attempts_count,
        students_by_lab,
    )


if __name__ == "__main__":
    run_demo()
