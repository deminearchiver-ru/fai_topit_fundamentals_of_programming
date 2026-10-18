researcher_name = input("Имя исследователя:\n> ")
experiment_name = input("Название эксперимента:\n> ")
total_run_count = int(
    input("Количество выполненных запусков (целое число):\n> ")
)
single_run_duration = float(
    input("Длительность одного запуска в секундах (вещественное число):\n> ")
)
complex_coefficient = complex(
    float(
        input("Действительная часть комплексного коэффициента (вещественное число):\n> ")
    ),
    float(
        input("Мнимая часть комплексного коэффициента (вещественное число):\n> ")
    ),
)

has_runs = total_run_count > 0
total_run_duration = total_run_count * single_run_duration
total_run_duration_minutes = total_run_duration / 60
modulus_square = complex_coefficient.real ** 2 + complex_coefficient.imag ** 2

print(
    f"""
========================================
ЭКСПЕРИМЕНТ: {experiment_name}
Исследователь: {researcher_name}
Запуски: {total_run_count}
Общее время: {total_run_duration:.2f} с ({total_run_duration_minutes:.2f} мин)
Коэффициент: {complex_coefficient}
Квадрат модуля: {modulus_square:.2f}
Есть выполненные запуски: {has_runs}
========================================"""
)

print(
    f"""
Диагностическая информация:
- researcher_name -> {type(researcher_name).__name__}: {researcher_name}
- experiment_name -> {type(experiment_name).__name__}: {experiment_name}
- total_run_count -> {type(total_run_count).__name__}: {total_run_count}
- single_run_duration -> {type(single_run_duration).__name__}: {single_run_duration}
- complex_coefficient -> {type(complex_coefficient).__name__}: {complex_coefficient}
- has_runs -> {type(has_runs).__name__}: {has_runs}
- total_run_duration -> {type(total_run_duration).__name__}: {total_run_duration}
- total_run_duration_minutes -> {type(total_run_duration_minutes).__name__}: {total_run_duration_minutes}
- modulus_square -> {type(modulus_square).__name__}: {modulus_square}"""
)
