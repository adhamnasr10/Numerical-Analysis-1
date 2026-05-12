"""
ui/root_page.py
Root Finding module: Bisection Method & Secant Method.
"""

from __future__ import annotations
import customtkinter as ctk
from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC, BORDER, ERROR
from methods.bisection import bisection
from methods.newton_raphson import newton_raphson
from methods.secant import secant
from graphs.root_graphs import plot_root_function, plot_convergence
from utils.parser import parse_function
from utils.validators import validate_float, validate_int


class RootPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._build()

    def _build(self):
        # Page title
        ctk.CTkLabel(
            self, text="🔍  Root Finding Methods",
            text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Find roots of f(x) using Bisection and Secant methods.",
            text_color=TEXT_SEC, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        # Method selector tabs
        tab_bar = ctk.CTkFrame(self, fg_color="transparent")
        tab_bar.pack(anchor="w", padx=20, pady=(0, 8))
        self._method = ctk.StringVar(value="Bisection")
        for m in ["Bisection", "Newton-Raphson", "Secant"]:
            ctk.CTkRadioButton(
                tab_bar, text=m, variable=self._method, value=m,
                text_color=TEXT_PRI, fg_color=ACCENT, hover_color=ACCENT2,
                command=self._toggle_inputs,
            ).pack(side="left", padx=10)

        # Main layout: inputs left, outputs right
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=4)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # ── Input card ───────────────────────────────────────────────────────
        inp_card = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=260)
        inp_card.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=4)
        inp_card.grid_propagate(False)

        ctk.CTkLabel(inp_card, text="Parameters", text_color=ACCENT2,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))

        # Function
        f_frame, self._e_func = self.labeled_entry(inp_card, "f(x)", "x**3 - x - 2",
                                                    tooltip="e.g. x**3 - x - 2", width=220)
        f_frame.pack(padx=14, pady=4, fill="x")

        # Shared container that swaps between a/b and x0/x1 inputs
        self._guess_container = ctk.CTkFrame(inp_card, fg_color="transparent")
        self._guess_container.pack(fill="x", padx=14, pady=4)

        # a, b widgets (bisection)
        self._ab_frame = ctk.CTkFrame(self._guess_container, fg_color="transparent")
        f_a, self._e_a = self.labeled_entry(self._ab_frame, "a (left)", "1", width=95)
        f_a.pack(side="left", padx=(0, 6))
        f_b, self._e_b = self.labeled_entry(self._ab_frame, "b (right)", "2", width=95)
        f_b.pack(side="left")

        # x0, x1 widgets (secant)
        self._x01_frame = ctk.CTkFrame(self._guess_container, fg_color="transparent")
        f_x0, self._e_x0 = self.labeled_entry(self._x01_frame, "x₀ (guess 1)", "1", width=95)
        f_x0.pack(side="left", padx=(0, 6))
        f_x1, self._e_x1 = self.labeled_entry(self._x01_frame, "x₁ (guess 2)", "2", width=95)
        f_x1.pack(side="left")

        # x0 widget (Newton-Raphson)
        self._newton_frame = ctk.CTkFrame(self._guess_container, fg_color="transparent")
        f_nx0, self._e_nx0 = self.labeled_entry(self._newton_frame, "x0 (initial guess)", "1.5", width=200)
        f_nx0.pack(side="left")

        # Tolerance + max iter
        f_tol, self._e_tol = self.labeled_entry(inp_card, "Tolerance", "1e-6", width=220)
        f_tol.pack(padx=14, pady=4, fill="x")
        f_mi, self._e_mi = self.labeled_entry(inp_card, "Max Iterations", "50", width=220)
        f_mi.pack(padx=14, pady=4, fill="x")

        # Solve button
        ctk.CTkButton(
            inp_card, text="  ▶  Solve", height=38, corner_radius=8,
            fg_color=ACCENT, hover_color=ACCENT2, text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._solve,
        ).pack(padx=14, pady=(14, 6), fill="x")

        # Clear button
        ctk.CTkButton(
            inp_card, text="Clear", height=32, corner_radius=8,
            fg_color=BG_INPUT, hover_color="#2d333b", text_color=TEXT_SEC,
            font=ctk.CTkFont(size=12),
            command=self._clear,
        ).pack(padx=14, pady=(0, 14), fill="x")

        # ── Output area ──────────────────────────────────────────────────────
        out_area = ctk.CTkScrollableFrame(content, fg_color=BG_MAIN)
        out_area.grid(row=0, column=1, sticky="nsew", pady=4)
        self._out_area = out_area

        self._result_lbl = self.make_result_label(out_area)

        # Graph container (function)
        g1_card = ctk.CTkFrame(out_area, fg_color=BG_CARD, corner_radius=10)
        g1_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g1_card, text="Function Graph", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._g1 = ctk.CTkFrame(g1_card, fg_color=BG_CARD, height=280)
        self._g1.pack(fill="x", padx=6, pady=(0, 8))

        # Graph container (convergence)
        g2_card = ctk.CTkFrame(out_area, fg_color=BG_CARD, corner_radius=10)
        g2_card.pack(fill="x", pady=4)
        ctk.CTkLabel(g2_card, text="Convergence Plot", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._g2 = ctk.CTkFrame(g2_card, fg_color=BG_CARD, height=240)
        self._g2.pack(fill="x", padx=6, pady=(0, 8))

        # Table card
        self._tbl_card = ctk.CTkFrame(out_area, fg_color=BG_CARD, corner_radius=10)
        self._tbl_card.pack(fill="x", pady=4)
        ctk.CTkLabel(self._tbl_card, text="Iteration Table", text_color=ACCENT2,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=6)
        self._tbl_area = self._tbl_card

        self._c1 = None
        self._c2 = None
        self._toggle_inputs()

    def _toggle_inputs(self):
        m = self._method.get()
        if m == "Bisection":
            self._x01_frame.pack_forget()
            self._newton_frame.pack_forget()
            self._ab_frame.pack(fill="x")
        elif m == "Newton-Raphson":
            self._ab_frame.pack_forget()
            self._x01_frame.pack_forget()
            self._newton_frame.pack(fill="x")
        else:
            self._ab_frame.pack_forget()
            self._newton_frame.pack_forget()
            self._x01_frame.pack(fill="x")

    def _embed(self, fig, frame, canvas_attr: str):
        """Embed figure in a frame, replacing any prior canvas."""
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        old = getattr(self, canvas_attr, None)
        if old:
            old.get_tk_widget().destroy()
        for w in frame.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().configure(bg="#0d1117")
        canvas.get_tk_widget().pack(fill="both", expand=True)
        setattr(self, canvas_attr, canvas)

    def _solve(self):
        try:
            f = parse_function(self._e_func.get())
            tol = validate_float(self._e_tol.get(), "Tolerance")
            if tol <= 0:
                raise ValueError("Tolerance must be positive.")
            max_iter = validate_int(self._e_mi.get(), "Max Iterations", min_val=1)

            method = self._method.get()

            if method == "Bisection":
                a = validate_float(self._e_a.get(), "a")
                b = validate_float(self._e_b.get(), "b")
                root, iters = bisection(f, a, b, tol, max_iter)
                fig1 = plot_root_function(f, a, b, root)
            elif method == "Newton-Raphson":
                x0 = validate_float(self._e_nx0.get(), "x0")
                root, iters, f = newton_raphson(self._e_func.get(), x0, tol, max_iter)
                span = max(1.0, abs(root - x0) * 2)
                fig1 = plot_root_function(f, min(x0, root) - span * 0.2, max(x0, root) + span * 0.2, root)
            else:
                x0 = validate_float(self._e_x0.get(), "x₀")
                x1 = validate_float(self._e_x1.get(), "x₁")
                root, iters = secant(f, x0, x1, tol, max_iter)
                span = abs(x1 - x0) * 2
                fig1 = plot_root_function(f, min(x0, x1) - span * 0.2, max(x0, x1) + span * 0.2, root)

            fig2 = plot_convergence(iters)

            self._embed(fig1, self._g1, "_c1")
            self._embed(fig2, self._g2, "_c2")
            self.show_table(self._tbl_area, iters)
            self.show_result(
                self._result_lbl,
                f"✅  Root ≈ {root:.8f}   |   Iterations: {len(iters)}   |   "
                f"f(root) ≈ {f(root):.2e}"
            )

        except Exception as ex:
            self.show_result(self._result_lbl, f"❌  {ex}", error=True)

    def _clear(self):
        self.show_result(self._result_lbl, "")
        for frame in [self._g1, self._g2]:
            for w in frame.winfo_children():
                w.destroy()
        if self._table_frame:
            self._table_frame.destroy()
            self._table_frame = None
