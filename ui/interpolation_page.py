"""
ui/interpolation_page.py
Interpolation module: Lagrange, Newton Forward, Newton Backward.
"""

from __future__ import annotations
import customtkinter as ctk
from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC, BORDER
from methods.lagrange import lagrange_interpolate
from methods.newton_interpolation import newton_forward, newton_backward, difference_table_as_dicts
from graphs.interpolation_graphs import plot_lagrange, plot_newton_interpolation
from utils.validators import validate_float, validate_points, validate_equal_spacing


class InterpolationPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._c1 = None
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="📐  Interpolation",
            text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Lagrange · Newton Forward · Newton Backward",
            text_color=TEXT_SEC, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        # Method selector
        tab_bar = ctk.CTkFrame(self, fg_color="transparent")
        tab_bar.pack(anchor="w", padx=20)
        self._method = ctk.StringVar(value="Lagrange")
        for m in ["Lagrange", "Newton Forward", "Newton Backward"]:
            ctk.CTkRadioButton(
                tab_bar, text=m, variable=self._method, value=m,
                text_color=TEXT_PRI, fg_color=ACCENT,
            ).pack(side="left", padx=10)

        # Content area
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=8)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # ── Input card ───────────────────────────────────────────────────────
        inp = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=260)
        inp.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=4)
        inp.grid_propagate(False)

        ctk.CTkLabel(inp, text="Parameters", text_color=ACCENT2,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))

        f_xs, self._e_xs = self.labeled_entry(inp, "x values (comma-separated)",
                                              "1, 2, 3, 4", tooltip="e.g. 0,1,2,3", width=220)
        f_xs.pack(padx=14, pady=4, fill="x")

        f_ys, self._e_ys = self.labeled_entry(inp, "y values (comma-separated)",
                                              "1, 4, 9, 16", tooltip="e.g. 1,4,9,16", width=220)
        f_ys.pack(padx=14, pady=4, fill="x")

        f_xt, self._e_xt = self.labeled_entry(inp, "x* (interpolation point)",
                                              "2.5", tooltip="Point to interpolate", width=220)
        f_xt.pack(padx=14, pady=4, fill="x")

        ctk.CTkButton(
            inp, text="  ▶  Interpolate", height=38, corner_radius=8,
            fg_color=ACCENT, hover_color=ACCENT2, text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._solve,
        ).pack(padx=14, pady=(16, 6), fill="x")

        ctk.CTkButton(
            inp, text="Clear", height=32, corner_radius=8,
            fg_color=BG_INPUT, hover_color="#2d333b", text_color=TEXT_SEC,
            command=self._clear,
        ).pack(padx=14, pady=(0, 14), fill="x")

        # ── Output area ──────────────────────────────────────────────────────
        out = ctk.CTkScrollableFrame(content, fg_color=BG_MAIN)
        out.grid(row=0, column=1, sticky="nsew", pady=4)
        self._out = out

        self._result_lbl = self.make_result_label(out)

        self._poly_lbl = ctk.CTkLabel(
            out, text="", text_color=TEXT_SEC, font=ctk.CTkFont(size=11),
            wraplength=700, justify="left", anchor="w"
        )
        self._poly_lbl.pack(anchor="w", padx=4, pady=(2, 4))

        # Graph
        g_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        g_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g_card, text="Interpolation Graph", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._gf = ctk.CTkFrame(g_card, fg_color=BG_CARD, height=300)
        self._gf.pack(fill="x", padx=6, pady=(0, 8))

        # Table card
        self._tbl_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        self._tbl_card.pack(fill="x", pady=4)
        ctk.CTkLabel(self._tbl_card, text="Difference / Basis Table", text_color=ACCENT2,
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
            x_target = validate_float(self._e_xt.get(), "x*")
            method = self._method.get()

            if method == "Lagrange":
                value, poly_str, table_data = lagrange_interpolate(xs, ys, x_target)
                fig = plot_lagrange(xs, ys, x_target, value)
                self._poly_lbl.configure(text=f"Polynomial: {poly_str[:200]}")
                self.show_table(self._tbl_card, table_data)

            elif method == "Newton Forward":
                validate_equal_spacing(xs)
                value, _, steps = newton_forward(xs, ys, x_target)
                fig = plot_newton_interpolation(xs, ys, x_target, value, "Forward")
                diff_rows = difference_table_as_dicts(xs, ys)
                self.show_table(self._tbl_card, diff_rows)
                self._poly_lbl.configure(text="Newton Forward Interpolation (Finite Difference Table shown below)")

            else:  # Newton Backward
                validate_equal_spacing(xs)
                value, _, steps = newton_backward(xs, ys, x_target)
                fig = plot_newton_interpolation(xs, ys, x_target, value, "Backward")
                diff_rows = difference_table_as_dicts(xs, ys)
                self.show_table(self._tbl_card, diff_rows)
                self._poly_lbl.configure(text="Newton Backward Interpolation (Finite Difference Table shown below)")

            self._embed(fig)
            self.show_result(
                self._result_lbl,
                f"✅  P({x_target}) ≈ {value:.8f}   |   Method: {method}"
            )

        except Exception as ex:
            self.show_result(self._result_lbl, f"❌  {ex}", error=True)

    def _clear(self):
        self.show_result(self._result_lbl, "")
        self._poly_lbl.configure(text="")
        for w in self._gf.winfo_children():
            w.destroy()
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
