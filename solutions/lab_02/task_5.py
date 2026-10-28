from dataclasses import dataclass
import sys
import tracemalloc

@dataclass
class ObjectSizeRecord:
    label: str
    type_name: str
    length: int | None
    size_bytes: int

@dataclass
class ListGrowthStep:
    length: int
    size_bytes: int

@dataclass
class TracemallocScenarioResult:
    name: str
    elements_count: int
    outer_size_bytes: int
    current_kb: float
    peak_kb: float

@dataclass
class MemoryReportData:
    object_sizes: list[ObjectSizeRecord]
    growth_steps: list[ListGrowthStep]
    scenarios: list[TracemallocScenarioResult]
    peak_ratio: float

def measure_object_sizes() -> list[ObjectSizeRecord]:
    empty_list: list[int] = []
    ten_ints_list = list(range(10))
    ten_ints_tuple = tuple(range(10))
    ten_chars_str = "abcdefghij"
    integer_obj = 42
    none_obj = None

    items = [
        ("Пустой список []", empty_list, len(empty_list)),
        ("Список из 10 целых чисел", ten_ints_list, len(ten_ints_list)),
        ("Кортеж из 10 целых чисел", ten_ints_tuple, len(ten_ints_tuple)),
        ("Строка из 10 символов", ten_chars_str, len(ten_chars_str)),
        ("Целое число (42)", integer_obj, None),
        ("Объект None", none_obj, None),
    ]

    records: list[ObjectSizeRecord] = []
    for label, obj, length in items:
        records.append(
            ObjectSizeRecord(
                label=label,
                type_name=type(obj).__name__,
                length=length,
                size_bytes=sys.getsizeof(obj),
            )
        )
    return records

def measure_list_growth(limit: int = 100) -> list[ListGrowthStep]:
    dynamic_list: list[int] = []
    previous_size = sys.getsizeof(dynamic_list)
    steps = [ListGrowthStep(length=0, size_bytes=previous_size)]

    for item in range(limit):
        dynamic_list.append(item)
        current_size = sys.getsizeof(dynamic_list)
        if current_size != previous_size:
            steps.append(ListGrowthStep(length=len(dynamic_list), size_bytes=current_size))
            previous_size = current_size

    return steps

def measure_list_range_scenario(count: int = 100_000) -> TracemallocScenarioResult:
    tracemalloc.start()
    numbers = list(range(count))
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    outer_size = sys.getsizeof(numbers)
    tracemalloc.stop()

    return TracemallocScenarioResult(
        name=f"list(range({count:_}))",
        elements_count=len(numbers),
        outer_size_bytes=outer_size,
        current_kb=current_bytes / 1024,
        peak_kb=peak_bytes / 1024,
    )

def measure_range_scenario(count: int = 100_000) -> TracemallocScenarioResult:
    tracemalloc.start()
    numbers = range(count)
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    outer_size = sys.getsizeof(numbers)
    tracemalloc.stop()

    return TracemallocScenarioResult(
        name=f"range({count:_})",
        elements_count=len(numbers),
        outer_size_bytes=outer_size,
        current_kb=current_bytes / 1024,
        peak_kb=peak_bytes / 1024,
    )

def collect_all_measurements() -> MemoryReportData:
    object_sizes = measure_object_sizes()
    growth_steps = measure_list_growth(100)
    list_scenario = measure_list_range_scenario(100_000)
    range_scenario = measure_range_scenario(100_000)

    peak_ratio = (
        list_scenario.peak_kb / range_scenario.peak_kb
        if range_scenario.peak_kb > 0
        else float("inf")
    )

    return MemoryReportData(
        object_sizes=object_sizes,
        growth_steps=growth_steps,
        scenarios=[list_scenario, range_scenario],
        peak_ratio=peak_ratio,
    )

def print_memory_report(data: MemoryReportData) -> None:
    print("=== Часть 1. Размер отдельных объектов (sys.getsizeof) ===")
    label_width = max(len(r.label) for r in data.object_sizes)
    type_width = max(len(r.type_name) for r in data.object_sizes)
    for rec in data.object_sizes:
        len_str = f"len={rec.length:<2}" if rec.length is not None else "len=- "
        print(
            f"    {rec.label.ljust(label_width)} | "
            f"тип: {rec.type_name.ljust(type_width)} | "
            f"{len_str} | "
            f"размер: {rec.size_bytes} байт"
        )

    print("\n=== Часть 2. Динамический рост списка при добавлении 100 элементов ===")
    for step in data.growth_steps:
        print(f"    Длина: {step.length:>3} -> Размер списка: {step.size_bytes:>4} байт")

    print("\n=== Часть 3 и Практическая задача. Сравнение сценариев через tracemalloc ===")
    header = (
        f"    {'Сценарий':<22} | {'Элементов':>10} | "
        f"{'Внешний объект (Б)':>18} | {'Текущая память (КБ)':>19} | {'Пиковая память (КБ)':>19}"
    )
    print(header)
    print("    " + "-" * (len(header) - 4))
    for sc in data.scenarios:
        print(
            f"    {sc.name:<22} | {sc.elements_count:>10} | "
            f"{sc.outer_size_bytes:>18} | {sc.current_kb:>19.2f} | {sc.peak_kb:>19.2f}"
        )

    print(
        f"\nОтношение пикового объема памяти ({data.scenarios[0].name} / {data.scenarios[1].name}): "
        f"{data.peak_ratio:.2f}x"
    )

if __name__ == "__main__":
    report_data = collect_all_measurements()
    print_memory_report(report_data)
