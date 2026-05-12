"""
methods/secant.py
Secant root-finding method.
"""

from __future__ import annotations
import numpy as np


def secant(f, x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100):
    """Find a root of f using the Secant Method."""
    iterations = []
    if x0 == x1:
        raise ValueError("Secant Method requires two distinct initial guesses.")

    for i in range(1, max_iter + 1):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-14:
            raise ValueError("Division by near-zero in Secant method (f(x1) ≈ f(x0)).")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        error = abs(x2 - x1)
        iterations.append({"Iteration": i, "x0": round(x0, 8), "x1": round(x1, 8), "x2 (new)": round(x2, 8), "f(x2)": round(f(x2), 8), "Error": round(error, 8)})

        if error < tol:
            return x2, iterations
        x0, x1 = x1, x2

    return x1, iterations
