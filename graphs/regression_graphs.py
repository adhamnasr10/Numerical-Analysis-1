"""
graphs/regression_graphs.py
Visualization for regression fitting.
"""

import numpy as np
from matplotlib.figure import Figure
from graphs._base import make_figure
from utils.helpers import LINE_BLUE, LINE_RED, LINE_GREEN, TEXT_COLOR


def plot_regression(xs, ys, a: float, b: float, r2: float) -> Figure:
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    x_line = np.linspace(xs_arr.min() - 0.5, xs_arr.max() + 0.5, 200)
    y_line = a + b * x_line
    sign = "+" if b >= 0 else ""
    label = f"y = {a:.4f} {sign}{b:.4f}x  (R2={r2:.4f})"
    fig, ax = make_figure()
    ax.scatter(xs_arr, ys_arr, color=LINE_GREEN, s=60, zorder=5, label="Data Points")
    ax.plot(x_line, y_line, color=LINE_RED, linewidth=2, label=label)
    for xi, yi in zip(xs_arr, ys_arr):
        y_hat = a + b * xi
        ax.plot([xi, xi], [yi, y_hat], color=LINE_BLUE, linewidth=0.8, linestyle="--", alpha=0.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Least Squares Linear Regression")
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig


def plot_fit(xs, ys, y_model, equation: str, r2: float, title: str = "Regression Fit") -> Figure:
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    x_min, x_max = xs_arr.min(), xs_arr.max()
    margin = (x_max - x_min) * 0.12 if x_max != x_min else 1.0
    x_line = np.linspace(x_min - margin, x_max + margin, 250)
    y_line = y_model(x_line)
    fig, ax = make_figure()
    ax.scatter(xs_arr, ys_arr, color=LINE_GREEN, s=60, zorder=5, label="Data Points")
    ax.plot(x_line, y_line, color=LINE_RED, linewidth=2, label=f"{equation}  (R2={r2:.4f})")
    y_pred = y_model(xs_arr)
    for xi, yi, yp in zip(xs_arr, ys_arr, y_pred):
        ax.plot([xi, xi], [yi, yp], color=LINE_BLUE, linewidth=0.8, linestyle="--", alpha=0.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.legend(facecolor="#0f3460", labelcolor=TEXT_COLOR)
    return fig
