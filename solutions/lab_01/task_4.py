student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

print(f"1.1. Первый символ имени:    {student[0]}")
print(f"1.2. Последний символ имени: {student[-1]}")
print(f"2.1. Имя:     {student[0:4]}")
print(f"2.2. Фамилия: {student[5:]}")
print(f"3.1. Строка в верхнем регистре: {student.upper()}")
print(f"3.2. Строка в нижнем регистре:  {student.lower()}")
print(f"4. Инициалы: {student[0] + "." + student[5] + "."}")
print(f"5. Название курса в обратном порядке: {course[::-1]}")

percentage = (completed / total) * 100

# Старомодное форматирование оператором %, существовавшее до f-строк.
result_old = "%s — %s: %d/%d (%.1f%%)" % (
    student,
    course,
    completed,
    total,
    percentage,
)
print(f"6.1. Оператор %:     {result_old}")

# Форматирование функцией format().
result_format = "{} — {}: {}/{} ({:.1f}%)".format(student, course, completed, total, percentage)
print(f"6.2. Метод format(): {result_format}")

# Форматирование при помощи f-строки.
result_fstring = f"{student} — {course}: {completed}/{total} ({percentage:.1f}%)"
print(f"6.3. f-строка:       {result_fstring}")

symbol = "Я"
code_point = ord(symbol)
restored = chr(code_point)
encoded = symbol.encode("utf-8")

print(f"7.1. Символ:          {symbol}")
print(f"7.2. Кодпоинт:        {code_point}")
print(f"7.3. Восстановленный: {restored}")
print(f"7.4. UTF-8:           {encoded}")
print(f"7.5. UTF-8 длина:     {len(encoded)}")

# 8. Попытка изменить первый символ строки присваиванием по индексу.
#
# Pylint:
# E1137:unsupported-assignment-operation: 'student' does not support item assignment
#
# CPython:
# TypeError: 'str' object does not support item assignment
#
# student[0] = "О"
