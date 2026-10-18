import math

def experiment_a():
    print("Experiment A")
    x = 17
    y = 5
    results = {
        "x": x,
        "y": y,
        "x + y": x + y,
        "x - y": x - y,
        "x * y": x * y,
        "x / y": x / y,
        "x // y": x // y,
        "x % y": x % y,
        "x ** y": x ** y,
    }
    results_display = list(
        zip(
            results.keys(),
            results.values(),
            (str(result) for result in results.values())
        )
    )
    max_expression_width = max(len(expression) for expression, _, _ in results_display)
    max_display_width = max(len(display) for _, _, display in results_display)
    for expression, result, display in results_display:
        print(
            f"{
                expression.ljust(max_expression_width)
            } = {
                display.ljust(max_display_width)
            } ({type(result).__name__})"
        )

def experiment_b():
    print("Experiment B")
    result = 2 ** 1000
    print(f"result = {result} ({type(result).__name__})")

def experiment_c():
    print("Experiment C")
    result = 0.1 + 0.2
    results = {
        "result": result,
        "result == 0.3": result == 0.3,
        "result - 0.3": result - 0.3,
        "math.isclose(result, 0.3)": math.isclose(result, 0.3),
    }
    results_display = list(
        zip(
            results.keys(),
            results.values(),
            (str(result) for result in results.values())
        )
    )
    max_expression_width = max(len(expression) for expression, _, _ in results_display)
    max_display_width = max(len(display) for _, _, display in results_display)
    for expression, result, display in results_display:
        print(
            f"{
                expression.ljust(max_expression_width)
            } = {
                display.ljust(max_display_width)
            } ({type(result).__name__})"
        )

def experiment_d():
    print("Experiment D")
    results = {
        "int(\"42\")": int("42"),
        "float(\"3.14\")": float("3.14"),
        "str(2026)": str(2026),
        "bool(0)": bool(0),
        "bool(-1)": bool(-1),
        "bool("")": bool(""),
        "bool(\"False\")": bool("False"),
        "complex(2, -3)": complex(2, -3),
        "complex(2, -3).real": complex(2, -3).real,
        "complex(2, -3).imag": complex(2, -3).imag,
    }
    results_display = list(
        zip(
            results.keys(),
            results.values(),
            (str(result) for result in results.values())
        )
    )
    max_expression_width = max(len(expression) for expression, _, _ in results_display)
    max_display_width = max(len(display) for _, _, display in results_display)
    for expression, result, display in results_display:
        print(
            f"{
                expression.ljust(max_expression_width)
            } = {
                display.ljust(max_display_width)
            } ({type(result).__name__})"
        )

experiment_a()
print()
experiment_b()
print()
experiment_c()
print()
experiment_d()
