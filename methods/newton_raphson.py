"""
methods/newton_raphson.py
Newton-Raphson root-finding method with symbolic derivative validation.
"""

from __future__ import annotations

import math
import sympy as sp


def newton_raphson(expr_str: str, x0: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Find a root using Newton-Raphson: x_{n+1} = x_n - f(x_n) / f'(x_n).
    """
    x = sp.Symbol("x")
    try:
        expr = sp.sympify(expr_str, locals={"x": x})
        derivative = sp.diff(expr, x)
    except Exception as exc:
        raise ValueError(f"Could not parse function or derivative: {exc}")

    if derivative == 0:
        raise ValueError("Newton-Raphson Method requires a non-zero derivative.")

    f = sp.lambdify(x, expr, modules=["math"])
    df = sp.lambdify(x, derivative, modules=["math"])

    iterations = []
    current = x0
    previous_error = None

    for i in range(1, max_iter + 1):
        fx = f(current)
        dfx = df(current)

        if not (math.isfinite(fx) and math.isfinite(dfx)):
            raise ValueError("Newton-Raphson produced a non-finite value. Try another initial guess.")
        if abs(dfx) < 1e-14:
            raise ValueError("Derivative is zero or too close to zero at the current estimate.")

        next_x = current - fx / dfx
        error = abs(next_x - current)

        if not math.isfinite(next_x):
            raise ValueError("Newton-Raphson diverged. Try another initial guess.")
        if previous_error is not None and i > 3 and error > previous_error * 50:
            raise ValueError("Newton-Raphson appears to diverge. Try a closer initial guess.")

        iterations.append(
            {
                "Iteration": i,
                "x_n": round(current, 8),
                "f(x_n)": round(fx, 8),
                "f'(x_n)": round(dfx, 8),
                "x_{n+1}": round(next_x, 8),
                "Error": round(error, 8),
            }
        )

        if error < tol or abs(f(next_x)) < tol:
            return next_x, iterations, f

        previous_error = error
        current = next_x

    return current, iterations, f
