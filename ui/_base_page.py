"""
ui/_base_page.py
Shared base class for all content pages.
"""

from __future__ import annotations
import customtkinter as ctk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

BG_MAIN = "#0d1117"
BG_CARD = "#161b22"
BG_INPUT = "#21262d"
ACCENT = "#00b4d8"
ACCENT2 = "#90e0ef"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
SUCCESS = "#3fb950"
ERROR = "#f85149"
BORDER = "#30363d"


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_MAIN, **kwargs)
        self._canvas_widget = None
        self._table_frame = None

    def labeled_entry(self, parent, label: str, default: str = "", width: int = 220, tooltip: str = ""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=label, text_color=TEXT_SEC, font=ctk.CTkFont(size=12), anchor="w").pack(anchor="w", padx=2)
        entry = ctk.CTkEntry(frame, width=width, fg_color=BG_INPUT, border_color=BORDER, text_color=TEXT_PRI, font=ctk.CTkFont(size=13), placeholder_text=tooltip)
        entry.insert(0, default)
        entry.pack(pady=(2, 0))
        return frame, entry

    def make_result_label(self, parent):
        lbl = ctk.CTkLabel(parent, text="", text_color=ACCENT2, font=ctk.CTkFont(size=13, weight="bold"), wraplength=700, justify="left", anchor="w")
        lbl.pack(anchor="w", pady=(4, 0), padx=4)
        return lbl

    def show_result(self, label, text: str, error: bool = False):
        label.configure(text=text, text_color=ERROR if error else ACCENT2)

    def embed_figure(self, parent, fig: Figure):
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            self._canvas_widget = None
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg="#0d1117")
        widget.pack(fill="both", expand=True, pady=(8, 0))
        self._canvas_widget = canvas

    def show_table(self, parent, data: list[dict], max_rows: int = 20):
        if self._table_frame:
            self._table_frame.destroy()
        if not data:
            return
        df = pd.DataFrame(data[:max_rows])
        cols = list(df.columns)
        outer = ctk.CTkScrollableFrame(parent, fg_color=BG_CARD, height=200, scrollbar_button_color=ACCENT)
        outer.pack(fill="x", pady=(8, 0))
        self._table_frame = outer
        hdr = ctk.CTkFrame(outer, fg_color="#0f3460")
        hdr.pack(fill="x", pady=(0, 2))
        for c in cols:
            ctk.CTkLabel(hdr, text=c, text_color=ACCENT2, font=ctk.CTkFont(size=11, weight="bold"), width=max(80, 140 // max(1, len(cols) // 4)), anchor="center").pack(side="left", padx=4, pady=4)
        for r_idx, (_, row) in enumerate(df.iterrows()):
            bg = BG_CARD if r_idx % 2 == 0 else BG_INPUT
            row_frame = ctk.CTkFrame(outer, fg_color=bg)
            row_frame.pack(fill="x", pady=1)
            for val in row.values:
                ctk.CTkLabel(row_frame, text=str(val), text_color=TEXT_PRI, font=ctk.CTkFont(size=11), width=max(80, 140 // max(1, len(cols) // 4)), anchor="center").pack(side="left", padx=4, pady=3)

    def clear_outputs(self, parent):
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            self._canvas_widget = None
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
