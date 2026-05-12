"""
graphs/_base.py
Shared figure/axes factory with dark-mode styling.
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.helpers import DARK_BG, AXES_BG, GRID_COLOR, TEXT_COLOR


def make_figure(figsize=(7, 4)) -> tuple[Figure, plt.Axes]:
    fig = Figure(figsize=figsize, facecolor=DARK_BG)
    ax = fig.add_subplot(111, facecolor=AXES_BG)
    ax.tick_params(colors=TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["top"].set_color(DARK_BG)
    ax.spines["right"].set_color(DARK_BG)
    ax.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout(pad=2.0)
    return fig, ax
