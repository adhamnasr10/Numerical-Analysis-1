from __future__ import annotations
import customtkinter as ctk
from ui._base_page import BasePage, BG_MAIN, BG_CARD, BG_INPUT, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.bisection import bisection
from methods.newton_raphson import newton_raphson
from methods.secant import secant
from graphs.root_graphs import plot_root_function, plot_convergence
from utils.parser import parse_function
from utils.validators import validate_float, validate_int


class RootPage(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._c1 = self._c2 = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🔍  Root Finding Methods", text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(18, 2))
        self._method = ctk.StringVar(value="Bisection")
        tab = ctk.CTkFrame(self, fg_color="transparent"); tab.pack(anchor="w", padx=20, pady=(0, 8))
        for m in ["Bisection", "Newton-Raphson", "Secant"]:
            ctk.CTkRadioButton(tab, text=m, variable=self._method, value=m, text_color=TEXT_PRI, fg_color=ACCENT, command=self._toggle_inputs).pack(side="left", padx=10)
        content = ctk.CTkFrame(self, fg_color="transparent"); content.pack(fill="both", expand=True, padx=20, pady=4); content.columnconfigure(1, weight=1); content.rowconfigure(0, weight=1)
        inp = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=260); inp.grid(row=0, column=0, sticky="ns", padx=(0, 12)); inp.grid_propagate(False)
        ctk.CTkLabel(inp, text="Parameters", text_color=ACCENT2, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))
        f, self._e_func = self.labeled_entry(inp, "f(x)", "x**3 - x - 2", width=220); f.pack(padx=14, pady=4, fill="x")
        self._guess = ctk.CTkFrame(inp, fg_color="transparent"); self._guess.pack(fill="x", padx=14, pady=4)
        self._ab = ctk.CTkFrame(self._guess, fg_color="transparent"); fa, self._e_a = self.labeled_entry(self._ab, "a", "1", 95); fa.pack(side="left", padx=(0, 6)); fb, self._e_b = self.labeled_entry(self._ab, "b", "2", 95); fb.pack(side="left")
        self._newton = ctk.CTkFrame(self._guess, fg_color="transparent"); fn, self._e_nx0 = self.labeled_entry(self._newton, "x0", "1.5", 200); fn.pack(side="left")
        self._sec = ctk.CTkFrame(self._guess, fg_color="transparent"); fx0, self._e_x0 = self.labeled_entry(self._sec, "x0", "1", 95); fx0.pack(side="left", padx=(0, 6)); fx1, self._e_x1 = self.labeled_entry(self._sec, "x1", "2", 95); fx1.pack(side="left")
        ft, self._e_tol = self.labeled_entry(inp, "Tolerance", "1e-6", width=220); ft.pack(padx=14, pady=4, fill="x")
        fm, self._e_mi = self.labeled_entry(inp, "Max Iterations", "50", width=220); fm.pack(padx=14, pady=4, fill="x")
        ctk.CTkButton(inp, text="  ▶  Solve", height=38, corner_radius=8, fg_color=ACCENT, hover_color=ACCENT2, text_color="#000000", command=self._solve).pack(padx=14, pady=(14, 6), fill="x")
        out = ctk.CTkScrollableFrame(content, fg_color=BG_MAIN); out.grid(row=0, column=1, sticky="nsew")
        self._result_lbl = self.make_result_label(out)
        self._g1 = ctk.CTkFrame(out, fg_color=BG_CARD, height=280); self._g1.pack(fill="x", pady=4)
        self._g2 = ctk.CTkFrame(out, fg_color=BG_CARD, height=240); self._g2.pack(fill="x", pady=4)
        self._tbl_card = ctk.CTkFrame(out, fg_color=BG_CARD, corner_radius=10); self._tbl_card.pack(fill="x", pady=4)
        self._toggle_inputs()

    def _toggle_inputs(self):
        for f in [self._ab, self._newton, self._sec]: f.pack_forget()
        {"Bisection": self._ab, "Newton-Raphson": self._newton}.get(self._method.get(), self._sec).pack(fill="x")

    def _embed(self, fig, frame, attr):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        old = getattr(self, attr, None)
        if old: old.get_tk_widget().destroy()
        for w in frame.winfo_children(): w.destroy()
        c = FigureCanvasTkAgg(fig, master=frame); c.draw(); c.get_tk_widget().pack(fill="both", expand=True); setattr(self, attr, c)

    def _solve(self):
        try:
            f = parse_function(self._e_func.get()); tol = validate_float(self._e_tol.get(), "Tolerance"); max_iter = validate_int(self._e_mi.get(), "Max Iterations")
            method = self._method.get()
            if method == "Bisection":
                a = validate_float(self._e_a.get(), "a"); b = validate_float(self._e_b.get(), "b"); root, rows = bisection(f, a, b, tol, max_iter); fig1 = plot_root_function(f, a, b, root)
            elif method == "Newton-Raphson":
                x0 = validate_float(self._e_nx0.get(), "x0"); root, rows, f = newton_raphson(self._e_func.get(), x0, tol, max_iter); fig1 = plot_root_function(f, x0 - 1, x0 + 1, root)
            else:
                x0 = validate_float(self._e_x0.get(), "x0"); x1 = validate_float(self._e_x1.get(), "x1"); root, rows = secant(f, x0, x1, tol, max_iter); fig1 = plot_root_function(f, min(x0, x1) - 1, max(x0, x1) + 1, root)
            self._embed(fig1, self._g1, "_c1"); self._embed(plot_convergence(rows), self._g2, "_c2"); self.show_table(self._tbl_card, rows); self.show_result(self._result_lbl, f"OK  Root ≈ {root:.8f} | Iterations: {len(rows)}")
        except Exception as ex:
            self.show_result(self._result_lbl, f"Error: {ex}", error=True)
