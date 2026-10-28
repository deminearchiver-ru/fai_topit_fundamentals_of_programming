import sys
import weakref

class Record:
    def __init__(self, name: str = "unnamed") -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Record(name={self.name!r})"

def experiment_refcount() -> None:
    print("=== Часть 1. Изменение счетчика ссылок (sys.getrefcount) ===")
    data = [1, 2, 3]
    # Ожидание: 2 (1 ссылка от имени data + 1 временная ссылка аргумента sys.getrefcount)
    print("После создания:", sys.getrefcount(data))

    alias = data
    # Ожидание: 3 (data, alias + временная ссылка)
    print("После создания alias:", sys.getrefcount(data))

    container = [data]
    # Ожидание: 4 (data, alias, элемент внутри container + временная ссылка)
    print("После помещения в контейнер:", sys.getrefcount(data))

    del alias
    # Ожидание: 3 (data, элемент внутри container + временная ссылка)
    print("После del alias:", sys.getrefcount(data))

    container.clear()
    # Ожидание: 2 (data + временная ссылка)
    print("После очистки контейнера:", sys.getrefcount(data))

def experiment_weakref() -> None:
    print("\n=== Часть 2. Эксперимент со слабой ссылкой (weakref.ref) ===")
    record = Record("single")
    weak_record = weakref.ref(record)

    # Ожидание: объект Record(name='single'), так как сильная ссылка record существует
    print("До del record:", weak_record())
    del record
    # Ожидание: None, так как единственная сильная ссылка удалена и объект уничтожен
    print("После del record:", weak_record())

def practical_task_weak_registry() -> None:
    print("\n=== Практическая задача. Реестр объектов на основе WeakValueDictionary ===")
    registry: weakref.WeakValueDictionary[str, Record] = weakref.WeakValueDictionary()

    # Сохраняем сильные ссылки на первые два объекта, а для третьего — временную ссылку
    rec_1 = Record("alpha")
    rec_2 = Record("beta")
    temp_rec_3 = Record("gamma")

    registry["first"] = rec_1
    registry["second"] = rec_2
    registry["third"] = temp_rec_3

    print("1. До удаления сильных ссылок (все 3 объекта в реестре):")
    print("    Записи в реестре:", dict(registry))

    # Удаляем временную сильную ссылку на третий объект
    del temp_rec_3
    print("\n2. После удаления временной сильной ссылки (del temp_rec_3):")
    print("    Записи в реестре:", dict(registry))
    print("    Существующие ключи:", list(registry.keys()))

    # Удаляем еще одну сильную ссылку (на второй объект)
    del rec_2
    print("\n3. После удаления второй сильной ссылки (del rec_2):")
    print("    Записи в реестре:", dict(registry))
    print("    Существующие ключи:", list(registry.keys()))

    assert list(registry.keys()) == ["first"]
    assert registry["first"] is rec_1
    print("\nИтог: WeakValueDictionary автоматически удаляет записи, когда на объекты не остается сильных ссылок.")

if __name__ == "__main__":
    experiment_refcount()
    experiment_weakref()
    practical_task_weak_registry()
