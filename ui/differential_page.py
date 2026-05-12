"""
ui/differential_page.py
Differential Equations: Euler's Method.
"""

from __future__ import annotations
import customtkinter as ctk
from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.euler import euler, modified_euler
from graphs.differential_graphs import plot_euler
from utils.parser import parse_ode
from utils.validators import validate_float


class DifferentialPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._c1 = None
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="📈  Differential Equations",
            text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Euler's Method  —  First-Order ODE solver",
            text_color=TEXT_SEC, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        tab = ctk.CTkFrame(self, fg_color="transparent")
        tab.pack(anchor="w", padx=20)
        self._method = ctk.StringVar(value="Euler")
        for m in ["Euler", "Modified Euler"]:
            ctk.CTkRadioButton(
                tab, text=m, variable=self._method, value=m,
                text_color=TEXT_PRI, fg_color=ACCENT,
            ).pack(side="left", padx=10)

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

        # dy/dx hint
        ctk.CTkLabel(inp, text="dy/dx = f(x, y)", text_color=TEXT_SEC,
                     font=ctk.CTkFont(size=11)).pack(anchor="w", padx=14)
        f_fn, self._e_fn = self.labeled_entry(inp, "f(x, y)", "x + y",
                                               tooltip="e.g. x + y, x*y, -2*x*y", width=220)
        f_fn.pack(padx=14, pady=(2, 6), fill="x")

        row1 = ctk.CTkFrame(inp, fg_color="transparent")
        row1.pack(fill="x", padx=14, pady=4)
        f_x0, self._e_x0 = self.labeled_entry(row1, "x₀", "0", width=95)
        f_x0.pack(side="left", padx=(0, 6))
        f_y0, self._e_y0 = self.labeled_entry(row1, "y₀", "1", width=95)
        f_y0.pack(side="left")

        row2 = ctk.CTkFrame(inp, fg_color="transparent")
        row2.pack(fill="x", padx=14, pady=4)
        f_h, self._e_h = self.labeled_entry(row2, "Step size h", "0.1", width=95)
        f_h.pack(side="left", padx=(0, 6))
        f_xe, self._e_xe = self.labeled_entry(row2, "x end", "1.0", width=95)
        f_xe.pack(side="left")

        ctk.CTkButton(
            inp, text="  ▶  Solve ODE", height=38, corner_radius=8,
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

        g_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        g_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g_card, text="ODE Solution Graph", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._gf = ctk.CTkFrame(g_card, fg_color=BG_CARD, height=300)
        self._gf.pack(fill="x", padx=6, pady=(0, 8))

        self._tbl_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10)
        self._tbl_card.pack(fill="x", pady=4)
        ctk.CTkLabel(self._tbl_card, text="Step Table", text_color=ACCENT2,
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
            f   = parse_ode(self._e_fn.get())
            x0  = validate_float(self._e_x0.get(), "x₀")
            y0  = validate_float(self._e_y0.get(), "y₀")
            h   = validate_float(self._e_h.get(), "h")
            xe  = validate_float(self._e_xe.get(), "x end")

            method = self._method.get()
            if method == "Euler":
                xs, ys, table = euler(f, x0, y0, h, xe)
            else:
                xs, ys, table = modified_euler(f, x0, y0, h, xe)
            fig = plot_euler(xs, ys, method)
            self._embed(fig)
            self.show_table(self._tbl_card, table)
            self.show_result(
                self._result_lbl,
                f"✅  y({xs[-1]:.4f}) ≈ {ys[-1]:.8f}   |   Steps: {len(xs)-1}   |   h = {h}"
            )

        except Exception as ex:
            self.show_result(self._result_lbl, f"❌  {ex}", error=True)

    def _clear(self):
        self.show_result(self._result_lbl, "")
        for w in self._gf.winfo_children():
            w.destroy()
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
