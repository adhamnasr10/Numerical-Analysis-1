"""
utils/validators.py
Input validation helpers for all numerical methods.
"""


def validate_float(value: str, name: str) -> float:
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        raise ValueError(f"'{name}' must be a valid number. Got: '{value}'")


def validate_int(value: str, name: str, min_val: int = 1) -> int:
    try:
        v = int(value.strip())
        if v < min_val:
            raise ValueError(f"'{name}' must be >= {min_val}.")
        return v
    except (ValueError, AttributeError):
        raise ValueError(f"'{name}' must be a valid integer. Got: '{value}'")


def validate_points(x_str: str, y_str: str):
    try:
        xs = [float(v.strip()) for v in x_str.split(",") if v.strip()]
        ys = [float(v.strip()) for v in y_str.split(",") if v.strip()]
    except ValueError:
        raise ValueError("Data points must be comma-separated numbers.")
    if len(xs) != len(ys):
        raise ValueError(f"Number of x values ({len(xs)}) must equal number of y values ({len(ys)}).")
    if len(xs) < 2:
        raise ValueError("At least 2 data points are required.")
    if len(set(xs)) != len(xs):
        raise ValueError("x values must be unique.")
    return xs, ys


def validate_bisection_interval(a: float, b: float, f):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError(f"f(a) and f(b) must have opposite signs for Bisection.\nf({a}) = {fa:.4f}, f({b}) = {fb:.4f}")


def validate_equal_spacing(xs: list[float], tol: float = 1e-9):
    if len(xs) < 2:
        raise ValueError("At least 2 data points are required.")
    spacings = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    first = spacings[0]
    if abs(first) < tol:
        raise ValueError("x values must be distinct.")
    if any(abs(step - first) > tol * max(1.0, abs(first)) for step in spacings[1:]):
        raise ValueError("Newton Forward/Backward Interpolation requires equally spaced data points.")
