"""
graphs/differential_graphs.py
Visualization for Euler ODE solvers.
"""

import numpy as np
from matplotlib.figure import Figure
from graphs._base import make_figure
from utils.helpers import LINE_BLUE, LINE_GREEN, LINE_ORANGE, TEXT_COLOR


def plot_euler(xs: np.ndarray, ys: np.ndarray, method: str = "Euler") -> Figure:
    fig, ax = make_figure()
    ax.plot(xs, ys, color=LINE_BLUE, linewidth=2, marker="o", markersize=5, label=f"{method} Approximation", zorder=3)
    for i in range(len(xs) - 1):
        ax.plot([xs[i], xs[i + 1]], [ys[i], ys[i]], color=LINE_ORANGE, linewidth=0.8, linestyle="--", alpha=0.5)
        ax.plot([xs[i + 1], xs[i + 1]], [ys[i], ys[i + 1]], color=LINE_ORANGE, linewidth=0.8, linestyle="--", alpha=0.5)
    ax.scatter([xs[0]], [ys[0]], color=LINE_GREEN, s=80, zorder=5, label="Initial Point")
    ax.scatter([xs[-1]], [ys[-1]], color=LINE_ORANGE, s=80, zorder=5, label=f"Final y ≈ {ys[-1]:.6f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"{method} Method — ODE Approximation")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig
