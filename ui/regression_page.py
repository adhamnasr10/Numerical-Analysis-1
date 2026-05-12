"""
ui/regression_page.py
Regression: Linear, Exponential, Power and Quadratic fitting.
"""

from __future__ import annotations

import customtkinter as ctk
import numpy as np

from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.regression import exponential_regression, linear_regression, power_regression, quadratic_regression
from graphs.regression_graphs import plot_fit, plot_regression
from utils.validators import validate_points


class RegressionPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._c1 = None
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="Regression",
            text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Linear, Exponential, Power and Quadratic least-squares fitting",
            text_color=TEXT_SEC, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=8)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        inp = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=260)
        inp.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=4)
        inp.grid_propagate(False)

        ctk.CTkLabel(inp, text="Data Points", text_color=ACCENT2,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))

        f_xs, self._e_xs = self.labeled_entry(inp, "x values (comma-separated)",
                                              "1, 2, 3, 4, 5",
                                              tooltip="e.g. 0,1,2,3,4", width=220)
        f_xs.pack(padx=14, pady=4, fill="x")

        f_ys, self._e_ys = self.labeled_entry(inp, "y values (comma-separated)",
                                              "2.1, 3.9, 6.2, 8.0, 9.8",
                                              tooltip="e.g. 2,4,6,8,10", width=220)
        f_ys.pack(padx=14, pady=4, fill="x")

        self._method = ctk.StringVar(value="Linear")
        fit_frame = ctk.CTkFrame(inp, fg_color="transparent")
        fit_frame.pack(fill="x", padx=14, pady=(6, 2))
        for m in ["Linear", "Exponential", "Power", "Quadratic"]:
            ctk.CTkRadioButton(
                fit_frame, text=m, variable=self._method, value=m,
                text_color=TEXT_PRI, fg_color=ACCENT,
            ).pack(anchor="w", pady=1)

        ctk.CTkButton(
            inp, text="  >  Fit", height=38, corner_radius=8,
            fg_color=ACCENT, hover_color=ACCENT2, text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._solve,
        ).pack(padx=14, pady=(16, 6), fill="x")

        ctk.CTkButton(
            inp, text="Clear", height=32, corner_radius=8,
            fg_color=BG_INPUT, hover_color="#2d333b", text_color=TEXT_SEC,
            command=self._clear,
        ).pack(padx=14, pady=(0, 14), fill="x")

        stats = ctk.CTkFrame(inp, fg_color="#0f3460", corner_radius=10)
        stats.pack(fill="x", padx=14, pady=4)
        ctk.CTkLabel(stats, text="Results", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self._lbl_eq = ctk.CTkLabel(stats, text="Equation: -", text_color=TEXT_PRI,
                                    font=ctk.CTkFont(size=12), anchor="w", wraplength=210)
        self._lbl_eq.pack(anchor="w", padx=10, pady=2)
        self._lbl_r2 = ctk.CTkLabel(stats, text="R2 = -", text_color=TEXT_PRI,
                                    font=ctk.CTkFont(size=12), anchor="w")
        self._lbl_r2.pack(anchor="w", padx=10, pady=(0, 10))

        out = ctk.CTkScrollableFrame(content, fg_color=BG_MAIN)
        out.grid(row=0, column=1, sticky="nsew", pady=4)
        self._out = out

        self._result_lbl = self.make_result_label(out)

        g_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        g_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g_card, text="Regression Plot", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._gf = ctk.CTkFrame(g_card, fg_color=BG_CARD, height=320)
        self._gf.pack(fill="x", padx=6, pady=(0, 8))

        self._tbl_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        self._tbl_card.pack(fill="x", pady=4)
        ctk.CTkLabel(self._tbl_card, text="Residual Table", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)

    def _embed(self, fig):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        if self._c1:
            self._c1.get_tk_widget().destroy()
        for w in self._gf.winfo_children():
            w.destroy()
        c = FigureCanvasTkAgg(fig, master=self._gf)
        c.draw()
        c.get_tk_widget().configure(bg="#0d1117")
        c.get_tk_widget().pack(fill="both", expand=True)
        self._c1 = c

    def _solve(self):
        try:
            xs, ys = validate_points(self._e_xs.get(), self._e_ys.get())
            method = self._method.get()

            if method == "Linear":
                a, b, r2, _, table = linear_regression(xs, ys)
                sign = "+" if b >= 0 else ""
                eq = f"y = {a:.4f} {sign}{b:.4f}x"
                fig = plot_regression(xs, ys, a, b, r2)
            elif method == "Exponential":
                eq, r2, _, table, (a, b) = exponential_regression(xs, ys)
                fig = plot_fit(xs, ys, lambda x: a * np.exp(b * x), eq, r2, "Exponential Fit")
            elif method == "Power":
                eq, r2, _, table, (a, b) = power_regression(xs, ys)
                fig = plot_fit(xs, ys, lambda x: a * (x ** b), eq, r2, "Power Fit")
            else:
                eq, r2, _, table, (a, b, c) = quadratic_regression(xs, ys)
                fig = plot_fit(xs, ys, lambda x: a * x ** 2 + b * x + c, eq, r2, "Quadratic Fit")

            self._embed(fig)
            self.show_table(self._tbl_card, table)

            self._lbl_eq.configure(text=f"Equation: {eq}")
            self._lbl_r2.configure(text=f"R2 = {r2:.6f}")
            self.show_result(
                self._result_lbl,
                f"OK  {eq}   |   R2 = {r2:.6f}   |   Method: {method}   |   n = {len(xs)}"
            )

        except Exception as ex:
            self.show_result(self._result_lbl, f"Error: {ex}", error=True)

    def _clear(self):
        self.show_result(self._result_lbl, "")
        self._lbl_eq.configure(text="Equation: -")
        self._lbl_r2.configure(text="R2 = -")
        for w in self._gf.winfo_children():
            w.destroy()
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
