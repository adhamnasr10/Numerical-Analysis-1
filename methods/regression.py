"""
methods/regression.py
Least-squares regression methods.
"""

from __future__ import annotations
import numpy as np


def linear_regression(xs: list, ys: list):
    n = len(xs)
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    sx = np.sum(xs_arr)
    sy = np.sum(ys_arr)
    sxy = np.sum(xs_arr * ys_arr)
    sx2 = np.sum(xs_arr ** 2)
    b = (n * sxy - sx * sy) / (n * sx2 - sx ** 2)
    a = (sy - b * sx) / n
    y_pred = a + b * xs_arr
    ss_res = np.sum((ys_arr - y_pred) ** 2)
    ss_tot = np.sum((ys_arr - np.mean(ys_arr)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    table = _residual_table(xs_arr, ys_arr, y_pred)
    return a, b, r2, y_pred.tolist(), table


def _r2_score(ys_arr, y_pred):
    ss_res = np.sum((ys_arr - y_pred) ** 2)
    ss_tot = np.sum((ys_arr - np.mean(ys_arr)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot != 0 else 1.0


def _residual_table(xs_arr, ys_arr, y_pred):
    table = []
    for xi, yi, yp in zip(xs_arr, ys_arr, y_pred):
        table.append({"x": round(float(xi), 4), "y (observed)": round(float(yi), 4), "y_hat (predicted)": round(float(yp), 6), "Residual": round(float(yi - yp), 6), "Residual^2": round(float((yi - yp) ** 2), 8)})
    return table


def exponential_regression(xs: list, ys: list):
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    if len(xs_arr) < 2:
        raise ValueError("Exponential Fit requires at least 2 data points.")
    if np.any(ys_arr <= 0):
        raise ValueError("Exponential Fit requires all y values to be positive.")
    b, ln_a = np.polyfit(xs_arr, np.log(ys_arr), 1)
    a = float(np.exp(ln_a))
    y_pred = a * np.exp(b * xs_arr)
    r2 = _r2_score(ys_arr, y_pred)
    eq = f"y = {a:.4f}e^({b:.4f}x)"
    return eq, r2, y_pred.tolist(), _residual_table(xs_arr, ys_arr, y_pred), (a, b)


def power_regression(xs: list, ys: list):
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    if len(xs_arr) < 2:
        raise ValueError("Power Fit requires at least 2 data points.")
    if np.any(xs_arr <= 0) or np.any(ys_arr <= 0):
        raise ValueError("Power Fit requires all x and y values to be positive.")
    b, ln_a = np.polyfit(np.log(xs_arr), np.log(ys_arr), 1)
    a = float(np.exp(ln_a))
    y_pred = a * (xs_arr ** b)
    r2 = _r2_score(ys_arr, y_pred)
    eq = f"y = {a:.4f}x^{b:.4f}"
    return eq, r2, y_pred.tolist(), _residual_table(xs_arr, ys_arr, y_pred), (a, b)


def quadratic_regression(xs: list, ys: list):
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    if len(xs_arr) < 3:
        raise ValueError("Quadratic Fit requires at least 3 data points.")
    a, b, c = np.polyfit(xs_arr, ys_arr, 2)
    y_pred = a * xs_arr ** 2 + b * xs_arr + c
    r2 = _r2_score(ys_arr, y_pred)
    sign_b = "+" if b >= 0 else "-"
    sign_c = "+" if c >= 0 else "-"
    eq = f"y = {a:.4f}x^2 {sign_b} {abs(b):.4f}x {sign_c} {abs(c):.4f}"
    return eq, r2, y_pred.tolist(), _residual_table(xs_arr, ys_arr, y_pred), (a, b, c)
