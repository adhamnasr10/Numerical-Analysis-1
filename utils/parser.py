"""
utils/parser.py
Parses mathematical expressions from strings into callable functions.
"""

import numpy as np
import sympy as sp


def parse_function(expr_str: str):
    x = sp.Symbol("x")
    try:
        expr = sp.sympify(expr_str, locals={"x": x})
        return sp.lambdify(x, expr, modules=["numpy"])
    except Exception as e:
        raise ValueError(f"Could not parse expression '{expr_str}': {e}")


def parse_ode(expr_str: str):
    x, y = sp.symbols("x y")
    try:
        expr = sp.sympify(expr_str, locals={"x": x, "y": y})
        return sp.lambdify((x, y), expr, modules=["numpy"])
    except Exception as e:
        raise ValueError(f"Could not parse ODE expression '{expr_str}': {e}")


def get_sympy_expr(expr_str: str):
    x = sp.Symbol("x")
    try:
        return sp.sympify(expr_str, locals={"x": x}), x
    except Exception as e:
        raise ValueError(f"Symbolic parse failed: {e}")
