"""
methods/simpson.py
Numerical integration using Simpson's 1/3 and 3/8 Rules.
"""

from __future__ import annotations
import numpy as np


def simpson_one_third(f, a: float, b: float, n: int):
    """Approximate the integral using Composite Simpson's 1/3 Rule."""
    if n % 2 != 0:
        raise ValueError("Simpson 1/3 Rule requires an even number of intervals.")

    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(xi) for xi in xs])
    result = h / 3 * (ys[0] + 4 * np.sum(ys[1:-1:2]) + 2 * np.sum(ys[2:-2:2]) + ys[-1])

    table_data = []
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            coeff = 1
        elif i % 2 == 1:
            coeff = 4
        else:
            coeff = 2
        table_data.append({"i": i, "x_i": round(xi, 6), "f(x_i)": round(yi, 8), "Coefficient": coeff, "Weighted f": round(coeff * yi, 8)})
    return result, xs, ys, table_data


def simpson_three_eighth(f, a: float, b: float, n: int):
    """Approximate the integral using Composite Simpson's 3/8 Rule."""
    if n % 3 != 0:
        raise ValueError("Simpson 3/8 Rule requires intervals divisible by 3.")

    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(xi) for xi in xs])
    total = ys[0] + ys[-1]
    total += 3 * np.sum([ys[i] for i in range(1, n) if i % 3 != 0])
    total += 2 * np.sum([ys[i] for i in range(3, n, 3)])
    result = 3 * h * total / 8

    table_data = []
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            coeff = 1
        elif i % 3 == 0:
            coeff = 2
        else:
            coeff = 3
        table_data.append({"i": i, "x_i": round(xi, 6), "f(x_i)": round(yi, 8), "Coefficient": coeff, "Weighted f": round(coeff * yi, 8)})
    return result, xs, ys, table_data


def simpsons(f, a: float, b: float, n: int):
    """Backward-compatible alias for Simpson's 1/3 Rule."""
    return simpson_one_third(f, a, b, n)
