"""
methods/newton_interpolation.py
Newton Forward and Backward Interpolation using finite differences.
"""

from __future__ import annotations
import numpy as np


def _build_difference_table(ys: list[float]) -> np.ndarray:
    n = len(ys)
    table = np.zeros((n, n))
    table[:, 0] = ys
    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = table[i + 1, j - 1] - table[i, j - 1]
    return table


def newton_forward(xs: list, ys: list, x_target: float):
    n = len(xs)
    h = xs[1] - xs[0]
    table = _build_difference_table(ys)
    s = (x_target - xs[0]) / h
    result = table[0, 0]
    s_term = 1.0
    steps = [{"Term": "y0", "Value": round(table[0, 0], 8), "Cumulative": round(result, 8)}]
    fact = 1
    for k in range(1, n):
        s_term *= (s - (k - 1))
        fact *= k
        delta_k = table[0, k]
        contribution = (s_term / fact) * delta_k
        result += contribution
        steps.append({"Term": f"Delta^{k}y0", "Value": round(delta_k, 8), "Coefficient": round(s_term / fact, 8), "Contribution": round(contribution, 8), "Cumulative": round(result, 8)})
    return result, table, steps


def newton_backward(xs: list, ys: list, x_target: float):
    n = len(xs)
    h = xs[1] - xs[0]
    table = _build_difference_table(ys)
    s = (x_target - xs[-1]) / h
    result = table[n - 1, 0]
    s_term = 1.0
    steps = [{"Term": "yn", "Value": round(table[n - 1, 0], 8), "Cumulative": round(result, 8)}]
    fact = 1
    for k in range(1, n):
        s_term *= (s + (k - 1))
        fact *= k
        delta_k = table[n - 1 - k, k]
        contribution = (s_term / fact) * delta_k
        result += contribution
        steps.append({"Term": f"Nabla^{k}yn", "Value": round(delta_k, 8), "Coefficient": round(s_term / fact, 8), "Contribution": round(contribution, 8), "Cumulative": round(result, 8)})
    return result, table, steps


def difference_table_as_dicts(xs: list, ys: list) -> list[dict]:
    n = len(xs)
    table = _build_difference_table(ys)
    rows = []
    for i in range(n):
        row = {"x": xs[i], "y": round(ys[i], 6)}
        for k in range(1, n - i):
            row[f"Delta^{k}"] = round(table[i, k], 6)
        rows.append(row)
    return rows
