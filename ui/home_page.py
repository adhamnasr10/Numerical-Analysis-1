"""
ui/home_page.py
Welcome / Home page.
"""

from __future__ import annotations
import customtkinter as ctk

BG_MAIN  = "#0d1117"
BG_CARD  = "#161b22"
ACCENT   = "#00b4d8"
ACCENT2  = "#90e0ef"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
BORDER   = "#30363d"

MEMBERS = [
    ("Abdullah",    "Root Finding",              "Bisection · Secant"),
    ("Omar",        "Interpolation",             "Lagrange"),
    ("Adham",       "Interpolation",             "Newton Forward · Backward"),
    ("Abdelrahman", "Numerical Integration",     "Trapezoidal Rule"),
    ("Youssef",     "Numerical Integration",     "Simpson's Rule"),
    ("Ziad",        "Differential Equations",    "Euler Method"),
    ("Islam",       "Regression",                "Least Squares · Linear Fitting"),
    ("Mahmoud",     "Graphs & Visualization",    "Plotting · Integration"),
    ("Moataz",      "UI/UX Design",              "Sidebar · Theming · Styling"),
]


class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_MAIN, **kwargs)
        self._build()

    def _build(self):
        # ── Hero banner ──────────────────────────────────────────────────────
        hero = ctk.CTkFrame(self, fg_color="#0d2137", corner_radius=14)
        hero.pack(fill="x", padx=20, pady=(20, 14))

        ctk.CTkLabel(
            hero,
            text="Numerical Analysis Solver",
            text_color=ACCENT,
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            hero,
            text="A university project implementing core Numerical Analysis algorithms\n"
                 "with interactive graphs and iteration tables.",
            text_color=TEXT_SEC,
            font=ctk.CTkFont(size=13),
        ).pack(pady=(0, 22))

        # ── Module cards row ─────────────────────────────────────────────────
        ctk.CTkLabel(
            self, text="📦  Application Modules",
            text_color=TEXT_PRI, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=24, pady=(10, 6))

        modules = [
            ("🔍", "Root Finding",       "Bisection · Secant",     "#0f3460"),
            ("📐", "Interpolation",      "Lagrange · Newton Fwd/Bwd","#1a3a4a"),
            ("∫",  "Integration",        "Trapezoidal · Simpson's", "#0f3460"),
            ("📈", "Differential Eq.",   "Euler Method",            "#1a3a4a"),
            ("📊", "Regression",         "Least Squares · Linear",  "#0f3460"),
        ]
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=4)

        for i, (icon, title, desc, color) in enumerate(modules):
            card = ctk.CTkFrame(grid, fg_color=color, corner_radius=12, border_width=1, border_color=BORDER)
            card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")
            grid.columnconfigure(i % 3, weight=1)
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=28)).pack(pady=(14, 2))
            ctk.CTkLabel(card, text=title, text_color=ACCENT2,
                         font=ctk.CTkFont(size=13, weight="bold")).pack()
            ctk.CTkLabel(card, text=desc, text_color=TEXT_SEC,
                         font=ctk.CTkFont(size=11)).pack(pady=(2, 14))

        # ── Team members table ───────────────────────────────────────────────
        ctk.CTkLabel(
            self, text="👥  Team Members",
            text_color=TEXT_PRI, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=24, pady=(18, 6))

        table_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10)
        table_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Header
        hdr = ctk.CTkFrame(table_frame, fg_color="#0f3460")
        hdr.pack(fill="x")
        for col, w in [("Name", 120), ("Module", 200), ("Algorithms", 300)]:
            ctk.CTkLabel(hdr, text=col, text_color=ACCENT2,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         width=w, anchor="w").pack(side="left", padx=10, pady=8)

        # Rows
        for i, (name, module, algos) in enumerate(MEMBERS):
            bg = BG_CARD if i % 2 == 0 else "#1c2128"
            row = ctk.CTkFrame(table_frame, fg_color=bg)
            row.pack(fill="x")
            for text, w in [(name, 120), (module, 200), (algos, 300)]:
                ctk.CTkLabel(row, text=text, text_color=TEXT_PRI,
                             font=ctk.CTkFont(size=12), width=w, anchor="w"
                             ).pack(side="left", padx=10, pady=6)
