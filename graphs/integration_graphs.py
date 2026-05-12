"""
graphs/integration_graphs.py
Visualization for Numerical Integration.
"""

import numpy as np
from matplotlib.figure import Figure
from graphs._base import make_figure
from utils.helpers import LINE_BLUE, LINE_GREEN, TEXT_COLOR, ACCENT


def plot_integration(f, a: float, b: float, xs, method: str = "Trapezoidal") -> Figure:
    margin = abs(b - a) * 0.2
    x_fine = np.linspace(a - margin, b + margin, 600)
    try:
        y_fine = f(x_fine)
    except Exception:
        y_fine = np.array([f(xi) for xi in x_fine])
    fig, ax = make_figure()
    ax.plot(x_fine, y_fine, color=LINE_BLUE, linewidth=2, label="f(x)", zorder=3)
    x_fill = np.linspace(a, b, 400)
    try:
        y_fill = f(x_fill)
    except Exception:
        y_fill = np.array([f(xi) for xi in x_fill])
    ax.fill_between(x_fill, 0, y_fill, alpha=0.25, color=ACCENT, label="Integration Area")
    for xi in xs:
        try:
            ax.plot([xi, xi], [0, f(xi)], color=LINE_GREEN, linewidth=0.8, alpha=0.5)
        except Exception:
            pass
    ax.axhline(0, color=TEXT_COLOR, linewidth=0.8, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"{method} Rule — Integration Area")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig
