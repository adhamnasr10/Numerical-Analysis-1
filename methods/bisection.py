"""
methods/bisection.py
Bisection root-finding method.
"""

from __future__ import annotations
import numpy as np


def bisection(f, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    """Find a root of f in [a, b] using the Bisection Method."""
    if f(a) * f(b) >= 0:
        raise ValueError("Bisection Method requires f(a) and f(b) to have opposite signs.")

    iterations = []
    for i in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)
        error = abs(b - a) / 2.0

        iterations.append({"Iteration": i, "a": round(a, 8), "b": round(b, 8), "c (midpoint)": round(c, 8), "f(c)": round(fc, 8), "Error": round(error, 8)})

        if error < tol or fc == 0:
            break

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return c, iterations
