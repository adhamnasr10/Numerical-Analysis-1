"""
ui/about_page.py
About page.
"""

from __future__ import annotations
import customtkinter as ctk

BG_MAIN = "#0d1117"
BG_CARD = "#161b22"
ACCENT = "#00b4d8"
ACCENT2 = "#90e0ef"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"

STACK = [("Python", "Core language"), ("customtkinter", "Modern desktop GUI"), ("matplotlib", "Embedded scientific graphs"), ("numpy", "Numerical arrays"), ("sympy", "Expression parsing"), ("pandas", "Tables")]


class AboutPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_MAIN, **kwargs)
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="ℹ️  About This Project", text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(18, 4))
        desc = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        desc.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(desc, text="Numerical Analysis Solver is a university course project implementing root finding, interpolation, numerical integration, differential equations and curve fitting with interactive visualization.", text_color=TEXT_PRI, font=ctk.CTkFont(size=13), wraplength=740, justify="left", anchor="w").pack(padx=16, pady=14)
        ctk.CTkLabel(self, text="🛠️  Technology Stack", text_color=TEXT_PRI, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(14, 6))
        tbl = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10)
        tbl.pack(fill="x", padx=20, pady=4)
        for i, (lib, role) in enumerate(STACK):
            bg = BG_CARD if i % 2 == 0 else "#1c2128"
            row = ctk.CTkFrame(tbl, fg_color=bg)
            row.pack(fill="x")
            ctk.CTkLabel(row, text=lib, text_color=ACCENT, font=ctk.CTkFont(size=12, weight="bold"), width=180, anchor="w").pack(side="left", padx=12, pady=7)
            ctk.CTkLabel(row, text=role, text_color=TEXT_PRI, font=ctk.CTkFont(size=12), width=400, anchor="w").pack(side="left", padx=4, pady=7)
