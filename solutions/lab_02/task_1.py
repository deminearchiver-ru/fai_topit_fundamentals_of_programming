import copy


def experiment_a() -> None:
    print("=== Эксперимент A. Неизменяемый объект ===")
    a = 10
    b = a

    # Ожидание: 10 10, одинаковые id(a) и id(b)
    print("До a += 1:")
    print("Значения:", a, b)
    print("id(a), id(b):", id(a), id(b))
    print("a is b:", a is b)

    a += 1

    # Ожидание: 11 10, id(a) изменился (новый объект int 11), id(b) прежний (объект int 10)
    print("\nПосле a += 1:")
    print("Значения:", a, b)
    print("id(a), id(b):", id(a), id(b))
    print("a is b:", a is b)


def experiment_b() -> None:
    print("\n=== Эксперимент B. Изменяемый объект ===")
    first = [10, 20]
    second = first

    # Ожидание: [10, 20] [10, 20], одинаковые id(first) и id(second)
    print("До second.append(30):")
    print("Значения:", first, second)
    print("id(first), id(second):", id(first), id(second))

    second.append(30)

    # Ожидание: [10, 20, 30] [10, 20, 30], id(first) и id(second) остались прежними и равными
    print("\nПосле second.append(30):")
    print("Значения:", first, second)
    print("id(first), id(second):", id(first), id(second))

    # 1. Переназначение second на новый список с теми же элементами
    second = [10, 20, 30]

    # 2. Сравнение списков с помощью == и is
    # Ожидание: first == second -> True (значения равны), first is second -> False (разные объекты в памяти)
    print("\nПосле переназначения second = [10, 20, 30]:")
    print("Значения:", first, second)
    print("id(first), id(second):", id(first), id(second))
    print("first == second:", first == second)
    print("first is second:", first is second)

    # 3. Изменение нового списка и проверка влияния на first
    second.append(40)
    # Ожидание: first остался [10, 20, 30], second стал [10, 20, 30, 40]
    print("\nПосле second.append(40):")
    print("first:", first)
    print("second:", second)


def practical_task() -> None:
    print("\n=== Практическая задача. Конфигурации учебного проекта ===")

    # 1. Получение второй конфигурации простым присваиванием
    config_base = {
        "title": "Анализатор логов",
        "members": ["Анна", "Борис"],
        "launch_params": ["--verbose", ["--threads", 4]],
    }
    config_assigned = config_base

    print("1. Простое присваивание (до изменений):")
    print("config_base:    ", config_base)
    print("config_assigned:", config_assigned)

    config_assigned["title"] = "Анализатор логов (тест)"
    config_assigned["members"].append("Виктор")
    config_assigned["launch_params"][1][1] = 8

    print("\nПосле модификации через config_assigned:")
    print("config_base:    ", config_base)
    print("config_assigned:", config_assigned)
    print(
        "Итог (простое присваивание): "
        f"config_base is config_assigned -> {config_base is config_assigned} "
        "(обе переменные ссылаются на один и тот же словарь и разделяют все вложенные списки)."
    )

    # 2. Создание действительно независимой конфигурации с помощью глубокого копирования
    config_prod = {
        "title": "Анализатор логов",
        "members": ["Анна", "Борис"],
        "launch_params": ["--verbose", ["--threads", 4]],
    }
    config_independent = copy.deepcopy(config_prod)

    print("\n2. Глубокое копирование (до изменений):")
    print("config_prod:       ", config_prod)
    print("config_independent:", config_independent)

    config_independent["title"] = "Анализатор логов (dev)"
    config_independent["members"].append("Дарья")
    config_independent["launch_params"][0] = "--quiet"
    config_independent["launch_params"][1][1] = 16

    print("\nПосле модификации config_independent:")
    print("config_prod:       ", config_prod)
    print("config_independent:", config_independent)

    # Подтверждение независимости с помощью assert
    assert config_prod is not config_independent
    assert config_prod["members"] is not config_independent["members"]
    assert config_prod["launch_params"] is not config_independent["launch_params"]
    assert config_prod["launch_params"][1] is not config_independent["launch_params"][1]
    assert config_prod["title"] == "Анализатор логов"
    assert config_prod["members"] == ["Анна", "Борис"]
    assert config_prod["launch_params"] == ["--verbose", ["--threads", 4]]

    print("\nИтог проверки независимости (assert пройдены успешно):")
    print(f"- Внешний словарь общий?              {config_prod is config_independent}")
    print(f"- Список участников общий?            {config_prod['members'] is config_independent['members']}")
    print(f"- Список параметров запуска общий?    {config_prod['launch_params'] is config_independent['launch_params']}")
    print(f"- Вложенный список параметров общий?  {config_prod['launch_params'][1] is config_independent['launch_params'][1]}")


if __name__ == "__main__":
    experiment_a()
    experiment_b()
    practical_task()
