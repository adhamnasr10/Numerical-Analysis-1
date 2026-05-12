"""
graphs/interpolation_graphs.py
Visualization for Interpolation methods.
"""

import numpy as np
from matplotlib.figure import Figure
from graphs._base import make_figure
from methods.lagrange import lagrange_curve
from utils.helpers import LINE_BLUE, LINE_RED, LINE_GREEN, TEXT_COLOR


def plot_lagrange(xs, ys, x_target: float, y_interp: float) -> Figure:
    margin = (max(xs) - min(xs)) * 0.2
    x_plot = np.linspace(min(xs) - margin, max(xs) + margin, 500)
    y_plot = lagrange_curve(list(xs), list(ys), x_plot)
    fig, ax = make_figure()
    ax.plot(x_plot, y_plot, color=LINE_BLUE, linewidth=2, label="Lagrange Polynomial")
    ax.scatter(xs, ys, color=LINE_GREEN, s=60, zorder=5, label="Data Points")
    ax.scatter([x_target], [y_interp], color=LINE_RED, s=80, zorder=6, marker="*", label=f"P({x_target:.4f}) ≈ {y_interp:.6f}")
    ax.axvline(x_target, color=LINE_RED, linewidth=1, linestyle="--", alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Lagrange Interpolation")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig


def plot_newton_interpolation(xs, ys, x_target: float, y_interp: float, method: str = "Forward") -> Figure:
    fig, ax = make_figure()
    ax.scatter(xs, ys, color=LINE_GREEN, s=60, zorder=5, label="Data Points")
    ax.plot(xs, ys, color=LINE_BLUE, linewidth=1.5, linestyle="--", alpha=0.6)
    ax.scatter([x_target], [y_interp], color=LINE_RED, s=100, zorder=6, marker="*", label=f"P({x_target:.4f}) ≈ {y_interp:.6f}")
    ax.axvline(x_target, color=LINE_RED, linewidth=1, linestyle=":", alpha=0.5)
    ax.plot([x_target, x_target], [0, y_interp], color=LINE_RED, linewidth=1, linestyle=":", alpha=0.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Newton {method} Interpolation")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig
