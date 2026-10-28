import gc

def experiment_cycle_lists() -> None:
    print("=== Часть 1. Цикл из двух списков и параметры GC ===")
    print("Автоматический сборщик мусора включен (gc.isenabled()):", gc.isenabled())
    print("Пороги поколений (gc.get_threshold()):", gc.get_threshold())
    print("Статистика поколений (gc.get_stats()):")
    for gen_idx, stat in enumerate(gc.get_stats()):
        print(f"    Поколение {gen_idx}: {stat}")

    # Очистим мусор перед чистым экспериментом
    gc.collect()

    first = []
    second = []

    first.append(second)
    second.append(first)

    print("\nПроверка связей:")
    print("first ссылается на second:", first[0] is second)
    print("second ссылается на first:", second[0] is first)

    # 1. Запомните идентификаторы двух списков
    first_id = id(first)
    second_id = id(second)
    print(f"id(first)  = {first_id}")
    print(f"id(second) = {second_id}")

    # 2. Удалите имена first и second
    del first
    del second

    # 3. Запустите gc.collect() и сохраните возвращенное значение
    collected_count = gc.collect()
    print("Количество собранных объектов после del first, second и gc.collect():", collected_count)

def experiment_disabled_gc() -> None:
    print("\n=== Часть 2. Дополнительный эксперимент с временным отключением GC ===")
    gc.collect()
    gc.disable()
    try:
        print("GC включен во время создания циклов?:", gc.isenabled())
        # Создаем 3 циклические пары списков (6 объектов в циклах)
        for _ in range(3):
            a = []
            b = []
            a.append(b)
            b.append(a)
            del a
            del b

        print("Счетчики поколений до ручного gc.collect() (gc.get_count()):", gc.get_count())
        collected_manual = gc.collect()
        print("Собрано объектов при ручном вызове gc.collect():", collected_manual)
    finally:
        gc.enable()
        print("GC восстановлен (gc.isenabled()):", gc.isenabled())

def practical_task_graph() -> None:
    print("\n=== Практическая задача. Модель графа с циклом из трех узлов и независимым узлом ===")
    # Предварительная сборка мусора и замер до создания графа
    baseline_collected = gc.collect()
    print("Собрано объектов до создания графа (базовый замер):", baseline_collected)

    gc.disable()
    try:
        node_a = {"name": "A", "neighbors": []}
        node_b = {"name": "B", "neighbors": []}
        node_c = {"name": "C", "neighbors": []}
        node_d = {"name": "D (independent)", "neighbors": []}

        # Связываем A -> B -> C -> A по циклу
        node_a["neighbors"].append(node_b)
        node_b["neighbors"].append(node_c)
        node_c["neighbors"].append(node_a)

        print("\nСвязи в созданном графе:")
        print(f"    {node_a['name']} -> {[n['name'] for n in node_a['neighbors']]}")
        print(f"    {node_b['name']} -> {[n['name'] for n in node_b['neighbors']]}")
        print(f"    {node_c['name']} -> {[n['name'] for n in node_c['neighbors']]}")
        print(f"    {node_d['name']} -> {[n['name'] for n in node_d['neighbors']]}")

        # Проверка цикличности
        assert node_a["neighbors"][0] is node_b
        assert node_b["neighbors"][0] is node_c
        assert node_c["neighbors"][0] is node_a

        # Удаляем внешние имена циклических узлов
        del node_a
        del node_b
        del node_c

        # Выполняем ручную сборку мусора
        after_graph_collected = gc.collect()
        print("\nСобрано объектов после удаления внешних имен A, B, C и вызова gc.collect():", after_graph_collected)
        print(
            f"Сравнение: до создания графа = {baseline_collected}, "
            f"после удаления циклических узлов = {after_graph_collected} "
            "(3 словаря узлов + 3 списка neighbors = 6 контейнерных объектов)."
        )

        # Проверка доступности независимого узла
        assert node_d is not None and node_d["name"] == "D (independent)"
        print("Независимый узел остается доступен:", node_d)
    finally:
        gc.enable()

if __name__ == "__main__":
    experiment_cycle_lists()
    experiment_disabled_gc()
    practical_task_graph()
