"""
methods/euler.py
Euler and Modified Euler methods for solving first-order ODEs.
"""

from __future__ import annotations
import numpy as np


def euler(f, x0: float, y0: float, h: float, x_end: float):
    """Approximate y(x_end) using Euler's Method."""
    if h <= 0:
        raise ValueError("Step size h must be positive.")
    if x_end <= x0:
        raise ValueError("x_end must be greater than x0.")

    xs = [x0]
    ys = [y0]
    table_data = [{"Step": 0, "x": round(x0, 6), "y": round(y0, 8), "f(x,y)": round(f(x0, y0), 8), "y_next": "—"}]
    x, y = x0, y0
    step = 1
    while x < x_end - 1e-10:
        slope = f(x, y)
        y_next = y + h * slope
        x_next = x + h
        if x_next > x_end + 1e-10:
            break
        table_data.append({"Step": step, "x": round(x_next, 6), "y": round(y_next, 8), "f(x,y)": round(f(x_next, y_next), 8), "y_next": "—"})
        table_data[-2]["y_next"] = round(y_next, 8)
        xs.append(x_next)
        ys.append(y_next)
        x, y = x_next, y_next
        step += 1
    return np.array(xs), np.array(ys), table_data


def modified_euler(f, x0: float, y0: float, h: float, x_end: float):
    """Approximate y(x_end) using Modified Euler's Method (Heun predictor-corrector)."""
    if h <= 0:
        raise ValueError("Step size h must be positive.")
    if x_end <= x0:
        raise ValueError("x_end must be greater than x0.")

    xs = [x0]
    ys = [y0]
    table_data = [{"Step": 0, "x": round(x0, 6), "y": round(y0, 8), "k1": round(f(x0, y0), 8), "Predictor": "—", "k2": "—", "Corrected y": round(y0, 8)}]
    x, y = x0, y0
    step = 1
    while x < x_end - 1e-10:
        x_next = x + h
        if x_next > x_end + 1e-10:
            break
        k1 = f(x, y)
        predictor = y + h * k1
        k2 = f(x_next, predictor)
        y_next = y + (h / 2) * (k1 + k2)
        table_data.append({"Step": step, "x": round(x_next, 6), "y": round(y, 8), "k1": round(k1, 8), "Predictor": round(predictor, 8), "k2": round(k2, 8), "Corrected y": round(y_next, 8)})
        xs.append(x_next)
        ys.append(y_next)
        x, y = x_next, y_next
        step += 1
    return np.array(xs), np.array(ys), table_data
