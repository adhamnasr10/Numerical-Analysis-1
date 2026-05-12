"""
ui/_base_page.py
Shared base class for all content pages.
"""

from __future__ import annotations
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

# ── Colour tokens ────────────────────────────────────────────────────────────
BG_MAIN    = "#0d1117"
BG_CARD    = "#161b22"
BG_INPUT   = "#21262d"
ACCENT     = "#00b4d8"
ACCENT2    = "#90e0ef"
TEXT_PRI   = "#e6edf3"
TEXT_SEC   = "#8b949e"
SUCCESS    = "#3fb950"
ERROR      = "#f85149"
BORDER     = "#30363d"


class BasePage(ctk.CTkFrame):
    """
    Base class every module page inherits from.
    Provides helpers for:
      - build_input_card()   – labelled entry in a card frame
      - build_result_label() – result display label
      - embed_figure()       – embed a matplotlib Figure
      - show_table()         – display a pandas DataFrame as a scrollable table
      - show_error()         – display error text
      - clear_area()         – remove graph/table widgets
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_MAIN, **kwargs)
        self._canvas_widget = None
        self._table_frame   = None

    # ── Input helpers ─────────────────────────────────────────────────────────
    def labeled_entry(
        self,
        parent,
        label: str,
        default: str = "",
        width: int = 220,
        tooltip: str = "",
    ) -> ctk.CTkEntry:
        """Return a labeled entry widget pair (frame, entry)."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        lbl = ctk.CTkLabel(
            frame, text=label, text_color=TEXT_SEC,
            font=ctk.CTkFont(size=12), anchor="w"
        )
        lbl.pack(anchor="w", padx=2)
        entry = ctk.CTkEntry(
            frame,
            width=width,
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRI,
            font=ctk.CTkFont(size=13),
            placeholder_text=tooltip,
        )
        entry.insert(0, default)
        entry.pack(pady=(2, 0))
        return frame, entry

    # ── Result label ──────────────────────────────────────────────────────────
    def make_result_label(self, parent) -> ctk.CTkLabel:
        lbl = ctk.CTkLabel(
            parent,
            text="",
            text_color=ACCENT2,
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=700,
            justify="left",
            anchor="w",
        )
        lbl.pack(anchor="w", pady=(4, 0), padx=4)
        return lbl

    def show_result(self, label: ctk.CTkLabel, text: str, error: bool = False):
        label.configure(text=text, text_color=ERROR if error else ACCENT2)

    # ── Graph embedding ───────────────────────────────────────────────────────
    def embed_figure(self, parent, fig: Figure):
        """Embed a matplotlib figure in a given parent frame."""
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            self._canvas_widget = None

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg="#0d1117")
        widget.pack(fill="both", expand=True, pady=(8, 0))
        self._canvas_widget = canvas

    # ── Table display ─────────────────────────────────────────────────────────
    def show_table(self, parent, data: list[dict], max_rows: int = 20):
        """Render a list of dicts as a scrollable table inside parent."""
        if self._table_frame:
            self._table_frame.destroy()

        if not data:
            return

        df = pd.DataFrame(data[:max_rows])
        cols = list(df.columns)

        outer = ctk.CTkScrollableFrame(
            parent, fg_color=BG_CARD, height=200,
            scrollbar_button_color=ACCENT
        )
        outer.pack(fill="x", pady=(8, 0))
        self._table_frame = outer

        # Header row
        hdr = ctk.CTkFrame(outer, fg_color="#0f3460")
        hdr.pack(fill="x", pady=(0, 2))
        for c in cols:
            ctk.CTkLabel(
                hdr, text=c, text_color=ACCENT2,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=max(80, 140 // max(1, len(cols) // 4)),
                anchor="center",
            ).pack(side="left", padx=4, pady=4)

        # Data rows
        for r_idx, (_, row) in enumerate(df.iterrows()):
            bg = BG_CARD if r_idx % 2 == 0 else BG_INPUT
            row_frame = ctk.CTkFrame(outer, fg_color=bg)
            row_frame.pack(fill="x", pady=1)
            for val in row.values:
                ctk.CTkLabel(
                    row_frame, text=str(val), text_color=TEXT_PRI,
                    font=ctk.CTkFont(size=11),
                    width=max(80, 140 // max(1, len(cols) // 4)),
                    anchor="center",
                ).pack(side="left", padx=4, pady=3)

    def clear_outputs(self, parent):
        """Remove embedded graph and table."""
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            self._canvas_widget = None
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
