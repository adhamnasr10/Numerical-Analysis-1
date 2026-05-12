"""
ui/integration_page.py
Numerical Integration: Trapezoidal Rule & Simpson's Rule.
"""

from __future__ import annotations
import customtkinter as ctk
import sympy as sp
from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.trapezoidal import trapezoidal
from methods.simpson import simpson_one_third, simpson_three_eighth
from graphs.integration_graphs import plot_integration
from utils.parser import parse_function, get_sympy_expr
from utils.validators import validate_float, validate_int


class IntegrationPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._c1 = None
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="∫  Numerical Integration",
            text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Trapezoidal Rule  ·  Simpson's 1/3 Rule",
            text_color=TEXT_SEC, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        tab = ctk.CTkFrame(self, fg_color="transparent")
        tab.pack(anchor="w", padx=20)
        self._method = ctk.StringVar(value="Trapezoidal")
        for m in ["Trapezoidal", "Simpson 1/3", "Simpson 3/8"]:
            ctk.CTkRadioButton(
                tab, text=m, variable=self._method, value=m,
                text_color=TEXT_PRI, fg_color=ACCENT,
            ).pack(side="left", padx=10)

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=8)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # ── Inputs ───────────────────────────────────────────────────────────
        inp = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=260)
        inp.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=4)
        inp.grid_propagate(False)

        ctk.CTkLabel(inp, text="Parameters", text_color=ACCENT2,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))

        f_fn, self._e_fn = self.labeled_entry(inp, "f(x)", "x**2", tooltip="e.g. sin(x)", width=220)
        f_fn.pack(padx=14, pady=4, fill="x")

        ab = ctk.CTkFrame(inp, fg_color="transparent")
        ab.pack(fill="x", padx=14, pady=4)
        f_a, self._e_a = self.labeled_entry(ab, "Lower limit a", "0", width=95)
        f_a.pack(side="left", padx=(0, 6))
        f_b, self._e_b = self.labeled_entry(ab, "Upper limit b", "1", width=95)
        f_b.pack(side="left")

        f_n, self._e_n = self.labeled_entry(inp, "Number of intervals n", "10",
                                             tooltip="Even number recommended", width=220)
        f_n.pack(padx=14, pady=4, fill="x")

        ctk.CTkButton(
            inp, text="  ▶  Integrate", height=38, corner_radius=8,
            fg_color=ACCENT, hover_color=ACCENT2, text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._solve,
        ).pack(padx=14, pady=(16, 6), fill="x")

        ctk.CTkButton(
            inp, text="Clear", height=32, corner_radius=8,
            fg_color=BG_INPUT, hover_color="#2d333b", text_color=TEXT_SEC,
            command=self._clear,
        ).pack(padx=14, pady=(0, 14), fill="x")

        # ── Output ───────────────────────────────────────────────────────────
        out = ctk.CTkScrollableFrame(content, fg_color=BG_MAIN)
        out.grid(row=0, column=1, sticky="nsew", pady=4)
        self._out = out

        self._result_lbl = self.make_result_label(out)
        self._exact_lbl  = ctk.CTkLabel(
            out, text="", text_color=TEXT_SEC, font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self._exact_lbl.pack(anchor="w", padx=4, pady=2)

        g_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        g_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g_card, text="Integration Graph", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._gf = ctk.CTkFrame(g_card, fg_color=BG_CARD, height=300)
        self._gf.pack(fill="x", padx=6, pady=(0, 8))

        self._tbl_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        self._tbl_card.pack(fill="x", pady=4)
        ctk.CTkLabel(self._tbl_card, text="Strip Table (first 30 rows)", text_color=ACCENT2,
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
            f = parse_function(self._e_fn.get())
            a = validate_float(self._e_a.get(), "a")
            b = validate_float(self._e_b.get(), "b")
            n = validate_int(self._e_n.get(), "n", min_val=2)
            method = self._method.get()

            if method == "Trapezoidal":
                result, xs, ys, table = trapezoidal(f, a, b, n)
            elif method == "Simpson 1/3":
                result, xs, ys, table = simpson_one_third(f, a, b, n)
            else:
                result, xs, ys, table = simpson_three_eighth(f, a, b, n)

            fig = plot_integration(f, a, b, xs, method)
            self._embed(fig)
            self.show_table(self._tbl_card, table, max_rows=30)

            # Attempt exact integration via sympy
            try:
                expr, x = get_sympy_expr(self._e_fn.get())
                exact = float(sp.integrate(expr, (x, a, b)))
                err_pct = abs(result - exact) / abs(exact) * 100 if exact != 0 else 0
                self._exact_lbl.configure(
                    text=f"Exact: {exact:.8f}   |   Approx: {result:.8f}   |   Error: {err_pct:.4f}%"
                )
            except Exception:
                self._exact_lbl.configure(text="")

            self.show_result(
                self._result_lbl,
                f"✅  ∫f(x)dx ≈ {result:.8f}   |   Method: {method}   |   n = {n}"
            )

        except Exception as ex:
            self.show_result(self._result_lbl, f"❌  {ex}", error=True)

    def _clear(self):
        self.show_result(self._result_lbl, "")
        self._exact_lbl.configure(text="")
        for w in self._gf.winfo_children():
            w.destroy()
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
