"""
utils/helpers.py
Miscellaneous helper utilities.
"""

import pandas as pd


def make_dataframe(data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def format_number(val, decimals: int = 8) -> str:
    try:
        return f"{float(val):.{decimals}f}"
    except (TypeError, ValueError):
        return str(val)


DARK_BG = "#1a1a2e"
AXES_BG = "#16213e"
GRID_COLOR = "#0f3460"
LINE_BLUE = "#4fc3f7"
LINE_GREEN = "#69f0ae"
LINE_RED = "#ff5252"
LINE_ORANGE = "#ffab40"
LINE_PURPLE = "#b388ff"
TEXT_COLOR = "#e0e0e0"
ACCENT = "#00b4d8"
