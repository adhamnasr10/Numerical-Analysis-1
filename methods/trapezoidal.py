"""
methods/trapezoidal.py
Numerical integration using the Trapezoidal Rule.
"""

from __future__ import annotations
import numpy as np


def trapezoidal(f, a: float, b: float, n: int):
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(xi) for xi in xs])
    result = h * (ys[0] / 2 + np.sum(ys[1:-1]) + ys[-1] / 2)
    table_data = []
    for i in range(n):
        xi, xi1 = xs[i], xs[i + 1]
        strip = h * (f(xi) + f(xi1)) / 2
        table_data.append({"Strip": i + 1, "x_i": round(xi, 6), "x_{i+1}": round(xi1, 6), "f(x_i)": round(f(xi), 6), "f(x_{i+1})": round(f(xi1), 6), "Strip Area": round(strip, 8)})
    return result, xs, ys, table_data
