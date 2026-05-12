"""
graphs/root_graphs.py
Visualization for Root Finding methods.
"""

import numpy as np
from matplotlib.figure import Figure
from graphs._base import make_figure
from utils.helpers import LINE_BLUE, LINE_RED, LINE_GREEN, TEXT_COLOR


def plot_root_function(f, a: float, b: float, root: float) -> Figure:
    margin = abs(b - a) * 0.3
    x = np.linspace(a - margin, b + margin, 600)
    try:
        y = f(x)
    except Exception:
        y = np.array([f(xi) for xi in x])
    fig, ax = make_figure()
    ax.plot(x, y, color=LINE_BLUE, linewidth=2, label="f(x)")
    ax.axhline(0, color=TEXT_COLOR, linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvline(root, color=LINE_RED, linewidth=1.5, linestyle="--", label=f"Root ≈ {root:.6f}")
    ax.scatter([root], [0], color=LINE_RED, s=80, zorder=5)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Function Plot with Root")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig


def plot_convergence(iterations: list[dict], key: str = "Error") -> Figure:
    iters = [d["Iteration"] for d in iterations]
    errors = [d[key] for d in iterations]
    fig, ax = make_figure()
    ax.semilogy(iters, errors, color=LINE_GREEN, linewidth=2, marker="o", markersize=4, label=key)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error (log scale)")
    ax.set_title("Convergence Plot")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig
