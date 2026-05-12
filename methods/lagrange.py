"""
methods/lagrange.py
Lagrange Interpolation.
"""

from __future__ import annotations
import numpy as np
import sympy as sp


def lagrange_interpolate(xs: list, ys: list, x_target: float):
    n = len(xs)
    basis_info = []
    result = 0.0
    for i in range(n):
        li = 1.0
        for j in range(n):
            if j != i:
                li *= (x_target - xs[j]) / (xs[i] - xs[j])
        term = ys[i] * li
        result += term
        basis_info.append({"i": i, "x_i": xs[i], "y_i": ys[i], "L_i(x*)": round(li, 8), "y_i * L_i(x*)": round(term, 8)})

    x = sp.Symbol("x")
    poly = sp.sympify(0)
    for i in range(n):
        li_sym = sp.sympify(1)
        for j in range(n):
            if j != i:
                li_sym *= (x - xs[j]) / (xs[i] - xs[j])
        poly += ys[i] * li_sym
    return result, str(sp.expand(poly)), basis_info


def lagrange_curve(xs: list, ys: list, x_vals):
    n = len(xs)
    y_vals = np.zeros_like(x_vals, dtype=float)
    for i in range(n):
        li = np.ones_like(x_vals, dtype=float)
        for j in range(n):
            if j != i:
                li *= (x_vals - xs[j]) / (xs[i] - xs[j])
        y_vals += ys[i] * li
    return y_vals
